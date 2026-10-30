import os
import json
import re
import base64
import requests
from django.conf import settings
from bacly.services import mock_ai

BASE_SYSTEM_PROMPT = (
    "You are Bacly, a patient, precise mathematics tutor for Algerian Baccalauréat students, "
    "following the Algerian national curriculum and the style of past Bac exams. "
    "Respond in English. Write all math in LaTeX between $ signs. Solve step by step and double-check calculations. "
    "Never invent facts. If the image is unreadable or not a math exercise, explain this in the 'error' field. "
    "Return ONLY valid JSON matching the schema."
)

def is_mock_mode_active():
    """
    Checks if mock mode should be used.
    Returns True only if no API key is configured. The live API is always
    attempted first on each request; failures fall back to mock per-request.
    """
    key = getattr(settings, "GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
    if not key or key.strip() == "":
        return True
    return False


def strip_json_fences(raw_text):
    """
    Strips markdown code fences (```json ... ```) from model response.
    """
    if not raw_text:
        return ""
    text = raw_text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    return text


def call_ai(system_prompt, user_text, images=None, schema=None, feature="tutor", fallback_handler=None):
    """
    Unified AI service layer with timeout, retry, json parsing, and mock mode fallback.
    Tries providers in order: Gemini, then OpenRouter, then mock fallback.
    """
    images = images or []
    gemini_key = getattr(settings, "GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
    openrouter_key = getattr(settings, "OPENROUTER_API_KEY", "") or os.getenv("OPENROUTER_API_KEY", "")

    # Build list of providers to try (in order)
    providers = []
    if gemini_key:
        providers.append(("gemini", gemini_key))
    if openrouter_key:
        providers.append(("openrouter", openrouter_key))

    # No keys configured at all -> mock
    if not providers:
        if fallback_handler:
            return fallback_handler()
        return mock_ai.get_mock_tutor_response()

    last_error = None
    for provider_name, api_key in providers:
        for attempt in range(2):
            try:
                if provider_name == "gemini":
                    result = _call_gemini(system_prompt, user_text, images, api_key)
                else:
                    result = _call_openrouter(system_prompt, user_text, images)

                cleaned = strip_json_fences(result)
                parsed = json.loads(cleaned)
                return parsed
            except Exception as e:
                last_error = e
                # On first attempt failure, retry once. On second failure, try next provider.
                if attempt == 1:
                    break

    # All providers failed -> mock fallback
    if fallback_handler:
        return fallback_handler()
    return mock_ai.get_mock_tutor_response()


def _call_gemini(system_prompt, user_text, images, api_key):
    """
    Calls Gemini API via Google GenAI SDK or direct REST with 60s timeout.
    """
    model_name = getattr(settings, "GEMINI_MODEL", "gemini-flash-latest")
    # Clean model prefix if needed
    clean_model = model_name.replace("models/", "")

    # Use REST endpoint for robust timeout control in container
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_model}:generateContent?key={api_key}"
    parts = []
    if system_prompt:
        parts.append({"text": f"System Instructions:\n{system_prompt}\n\nTask:\n"})
    if user_text:
        parts.append({"text": user_text})

    for img_path in images:
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                mime = "image/jpeg"
                if img_path.lower().endswith(".png"):
                    mime = "image/png"
                elif img_path.lower().endswith(".webp"):
                    mime = "image/webp"
                parts.append({
                    "inlineData": {
                        "mimeType": mime,
                        "data": b64
                    }
                })

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2
        }
    }

    resp = requests.post(url, json=payload, timeout=20)
    if resp.status_code != 200:
        raise ValueError(f"Gemini API returned HTTP {resp.status_code}: {resp.text[:200]}")

    data = resp.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise ValueError("No candidates returned from Gemini")

    return candidates[0]["content"]["parts"][0]["text"]


def _call_openrouter(system_prompt, user_text, images):
    """
    Calls OpenRouter OpenAI-compatible endpoint.
    """
    api_key = getattr(settings, "OPENROUTER_API_KEY", "") or os.getenv("OPENROUTER_API_KEY", "")
    model = getattr(settings, "OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
    if not api_key:
        raise ValueError("OpenRouter API key is empty")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://bacly.app",
        "X-Title": "Bacly Math Tutor",
    }

    content_list = []
    if user_text:
        content_list.append({"type": "text", "text": user_text})

    for img_path in images:
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                mime = "image/jpeg"
                if img_path.lower().endswith(".png"):
                    mime = "image/png"
                elif img_path.lower().endswith(".webp"):
                    mime = "image/webp"
                content_list.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime};base64,{b64}"}
                })

    messages = [
        {"role": "system", "content": system_prompt + "\nReturn ONLY raw JSON, with no markdown code blocks."},
        {"role": "user", "content": content_list}
    ]

    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json={"model": model, "messages": messages, "response_format": {"type": "json_object"}},
        timeout=30,
    )

    if resp.status_code != 200:
        raise ValueError(f"OpenRouter returned {resp.status_code}: {resp.text[:200]}")

    return resp.json()["choices"][0]["message"]["content"]


# Prompt Builders
def build_tutor_prompt(chapter, exercise_text, attempt_text=""):
    """
    Prompt builder for tutor explanation and mistake detection.
    """
    prompt = (
        f"{BASE_SYSTEM_PROMPT}\n\n"
        f"Topic Chapter: {chapter or 'Bac Mathematics'}\n"
        f"Exercise Statement: {exercise_text}\n"
    )
    if attempt_text:
        prompt += (
            f"\nStudent's Attempt:\n{attempt_text}\n"
            f"Analyze the student's attempt carefully. If there is a mistake, populate the 'mistake' object "
            f"with: 'step', 'explanation' (why it is wrong), and 'correction' (how to fix it). "
            f"If the attempt is completely correct or no attempt was provided, set 'mistake': null.\n"
        )
    else:
        prompt += "\nNo student attempt provided. Set 'mistake': null.\n"

    prompt += (
        "\nProvide 3 practice questions with concise answers in 'practice'. "
        "Include a helpful Bacly 'tip' for the Algerian Bac exam.\n"
        "Return a JSON object conforming strictly to:\n"
        "{\n"
        '  "chapter": "string",\n'
        '  "exercise_summary": "string",\n'
        '  "solution_steps": ["step 1 with LaTeX $...$", "step 2 with LaTeX $...$"],\n'
        '  "mistake": { "step": "string", "explanation": "string", "correction": "string" } or null,\n'
        '  "practice": [ { "question": "string with LaTeX", "answer": "string with LaTeX" }, ... (3 items) ],\n'
        '  "tip": "string",\n'
        '  "error": null\n'
        "}\n"
    )
    return prompt
