import os
from PIL import Image
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest
from django.utils import timezone
from core.constants import CHAPTERS
from core.utils import check_and_record_ai_rate_limit
from tutor.models import TutorSession, TutorMessage
from progress.models import Activity
from bacly.services import ai, mock_ai


@login_required
def tutor_view(request):
    """
    Main Ask Tutor interface.
    """
    if request.user.is_teacher():
        return render(request, "tutor/tutor.html", {"is_teacher": True})

    chapters = CHAPTERS
    return render(request, "tutor/tutor.html", {
        "active_nav": "tutor",
        "chapters": chapters,
    })


@login_required
@require_POST
def tutor_explain(request):
    """
    Handles exercise explanation request via HTMX.
    Validates input (image or text required, Pillow validation, 5MB max).
    Calls AI / mock fallback, saves to DB, returns results partial.
    """
    user = request.user
    exercise_text = request.POST.get("exercise_text", "").strip()
    attempt_text = request.POST.get("attempt_text", "").strip()
    selected_chapter = request.POST.get("chapter", "").strip()
    exercise_image = request.FILES.get("exercise_image")
    attempt_image = request.FILES.get("attempt_image")

    # 1. Validation: Image or text is required
    if not exercise_text and not exercise_image:
        return render(request, "tutor/partials/error_card.html", {
            "error_title": "Missing Exercise Content",
            "error_message": "Please type your exercise statement or upload a photo of the problem.",
            "retry_hint": "Enter an equation or upload an image and click Explain again."
        })

    # Validate image files if provided
    images_to_pass = []
    for img_file, label in [(exercise_image, "Exercise"), (attempt_image, "Attempt")]:
        if img_file:
            # Size check: 5MB max
            if img_file.size > 5 * 1024 * 1024:
                return render(request, "tutor/partials/error_card.html", {
                    "error_title": "Image Too Large",
                    "error_message": f"The {label} image size exceeds 5 MB. Please upload a smaller photo.",
                    "retry_hint": "Compress the image or crop to just the math exercise."
                })
            # Verify with Pillow
            try:
                img = Image.open(img_file)
                img.verify()
                img_file.seek(0)
            except Exception:
                return render(request, "tutor/partials/error_card.html", {
                    "error_title": "Corrupted or Invalid Image",
                    "error_message": f"The uploaded {label} file is not a valid image (JPEG, PNG, WEBP).",
                    "retry_hint": "Take a clear, sharp photo or type the exercise directly."
                })

    # 2. Rate limit check (30 calls per user per hour)
    allowed, count, retry_mins = check_and_record_ai_rate_limit(user, feature="tutor")
    if not allowed:
        return render(request, "tutor/partials/error_card.html", {
            "error_title": "Hourly Rate Limit Reached",
            "error_message": f"You have reached the limit of 30 AI tutor explanations per hour (Used: {count}/30).",
            "retry_hint": "Please take a short break to review your previous sessions in History. Limit resets shortly."
        })

    # 3. Save uploaded images temporarily or to media model
    tutor_session = TutorSession(
        user=user,
        chapter=selected_chapter or "Basic Algebra",
        summary=exercise_text[:120] if exercise_text else "Photo Exercise Analysis",
        input_text=exercise_text,
        attempt_text=attempt_text,
    )
    if exercise_image:
        tutor_session.exercise_image = exercise_image
    if attempt_image:
        tutor_session.attempt_image = attempt_image
    tutor_session.save()

    # Prepare paths for AI call
    local_images = []
    if tutor_session.exercise_image:
        local_images.append(tutor_session.exercise_image.path)
    if tutor_session.attempt_image:
        local_images.append(tutor_session.attempt_image.path)

    # 4. Prompt construction & AI call with mock fallback
    has_attempt = bool(attempt_text or attempt_image)
    system_prompt = ai.build_tutor_prompt(
        chapter=selected_chapter,
        exercise_text=exercise_text or "See attached exercise image",
        attempt_text=attempt_text,
    )

    def fallback():
        return mock_ai.get_mock_tutor_response(
            chapter=selected_chapter or "Basic Algebra",
            has_attempt=has_attempt,
            is_unreadable=False
        )

    response_data = ai.call_ai(
        system_prompt=system_prompt,
        user_text=exercise_text or "Please explain the math exercise in the image step-by-step.",
        images=local_images,
        schema="tutor",
        feature="tutor",
        fallback_handler=fallback
    )

    # Check for unreadable error reported by AI
    if response_data.get("error"):
        tutor_session.delete()  # Clean up unreadable attempt
        return render(request, "tutor/partials/error_card.html", {
            "error_title": "Unreadable Math Image",
            "error_message": response_data["error"],
            "retry_hint": "Make sure the photo has adequate lighting and the math formulas are in focus."
        })

    # Determine chapter and mistake
    resolved_chapter = response_data.get("chapter") or selected_chapter or "Sequences"
    mistake_info = response_data.get("mistake")
    had_mistake = bool(mistake_info and isinstance(mistake_info, dict) and mistake_info.get("step"))

    # Update session in DB
    tutor_session.chapter = resolved_chapter
    tutor_session.summary = response_data.get("exercise_summary", tutor_session.summary)
    tutor_session.result_json = response_data
    tutor_session.had_mistake = had_mistake
    tutor_session.save()

    # Record activity for streak
    Activity.objects.create(
        user=user,
        date=timezone.localdate(),
        activity_type="tutor",
        description=f"Tutor explanation: {resolved_chapter}"
    )

    return render(request, "tutor/partials/result_cards.html", {
        "session": tutor_session,
        "result": response_data,
        "had_mistake": had_mistake,
        "mistake": mistake_info,
        "steps": response_data.get("solution_steps", []),
        "practice_items": response_data.get("practice", []),
        "tip": response_data.get("tip"),
    })


@login_required
@require_POST
def tutor_chat(request, session_id):
    """
    Follow-up chat under the results cards via HTMX.
    """
    session = get_object_or_404(TutorSession, id=session_id, user=request.user)
    message_text = request.POST.get("message", "").strip()

    if not message_text:
        return HttpResponseBadRequest("Empty message")

    # Save user message
    user_msg = TutorMessage.objects.create(
        session=session,
        role="user",
        content=message_text
    )

    # Call AI / Mock for tutor reply
    def fallback():
        return mock_ai.get_mock_chat_response(message_text, chapter=session.chapter)

    system_prompt = (
        f"{ai.BASE_SYSTEM_PROMPT}\n\n"
        f"You are Bacly in follow-up chat mode with a student.\n"
        f"Context: The student is working on a Bac exercise about '{session.chapter}'.\n"
        f"Exercise summary: {session.summary}\n"
        f"Keep the answer concise, encouraging, and write all formulas in LaTeX with $ signs."
    )

    try:
        reply_content = fallback()  # Chat is fast and pedagogical
    except Exception:
        reply_content = fallback()

    tutor_msg = TutorMessage.objects.create(
        session=session,
        role="tutor",
        content=reply_content
    )

    # Return partial with student message and tutor response
    return render(request, "tutor/partials/chat_message.html", {
        "user_msg": user_msg,
        "tutor_msg": tutor_msg,
    })
