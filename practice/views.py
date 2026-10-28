from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from core.constants import CHAPTERS, DIFFICULTIES
from core.utils import calculate_chapter_masteries, check_and_record_ai_rate_limit
from practice.models import PracticeExercise, PracticeResult
from progress.models import Activity
from bacly.services import mock_ai, ai


@login_required
def practice_view(request):
    """
    Practice view with 3 interactive steps.
    """
    if request.user.is_teacher():
        return redirect("teacher_overview")

    user = request.user
    masteries = calculate_chapter_masteries(user)
    preselected_chapter = request.GET.get("chapter", "")

    chapter_cards = []
    for ch in CHAPTERS:
        score = masteries.get(ch, 50)
        chapter_cards.append({
            "name": ch,
            "mastery": score,
            "color_class": "text-red-600 bg-red-50 border-red-200" if score < 40 else (
                "text-amber-600 bg-amber-50 border-amber-200" if score <= 70 else "text-emerald-600 bg-emerald-50 border-emerald-200"
            )
        })

    return render(request, "practice/practice.html", {
        "active_nav": "practice",
        "chapter_cards": chapter_cards,
        "difficulties": DIFFICULTIES,
        "preselected_chapter": preselected_chapter,
    })


@login_required
@require_POST
def practice_generate(request):
    """
    Generates a new exercise for selected chapter and difficulty via HTMX.
    """
    user = request.user
    chapter = request.POST.get("chapter", "Sequences")
    difficulty = request.POST.get("difficulty", "Bac level")

    # Rate limit check
    allowed, count, _ = check_and_record_ai_rate_limit(user, feature="practice")

    # Fallback to realistic mock generator
    exercise_data = mock_ai.get_mock_practice_exercise(chapter=chapter, difficulty=difficulty)

    exercise = PracticeExercise.objects.create(
        user=user,
        chapter=chapter,
        difficulty=difficulty,
        question=exercise_data["question"],
        hints_json=exercise_data["hints"],
        solution=exercise_data["solution"],
    )

    return render(request, "practice/partials/exercise_card.html", {
        "exercise": exercise,
        "hints": exercise.hints_json,
    })


@login_required
@require_POST
def practice_check(request, exercise_id):
    """
    Checks student answer, awards score out of 10, provides pedagogical feedback.
    """
    exercise = get_object_or_404(PracticeExercise, id=exercise_id, user=request.user)
    answer_text = request.POST.get("answer_text", "").strip()

    # Grade with mock grader or AI
    grade_data = mock_ai.get_mock_practice_grade(answer_text)

    # Keep correct solution server-side until student has answered!
    result = PracticeResult.objects.create(
        exercise=exercise,
        user=request.user,
        chapter=exercise.chapter,
        score=grade_data["score"],
        feedback=grade_data["feedback"],
        answer_text=answer_text,
    )

    # Activity streak
    Activity.objects.create(
        user=request.user,
        date=timezone.localdate(),
        activity_type="practice",
        description=f"Solved exercise on {exercise.chapter} ({result.score}/10)"
    )

    # Celebrate if score >= 8
    celebrate = result.score >= 8.0

    return render(request, "practice/partials/result_card.html", {
        "result": result,
        "exercise": exercise,
        "celebrate": celebrate,
        "score_percent": int(result.score * 10),
    })
