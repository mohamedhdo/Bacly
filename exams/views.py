import json
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from exams.models import Exam
from progress.models import Activity
from bacly.services import mock_ai


@login_required
def exam_intro_view(request):
    """
    Exam intro: format description, duration picker (1h, 2h, 3h), start exam button.
    """
    if request.user.is_teacher():
        return redirect("teacher_overview")

    # Check if there is an in-progress exam
    active_exam = Exam.objects.filter(user=request.user, status="in_progress").first()
    if active_exam:
        # Check if expired
        elapsed_seconds = (timezone.now() - active_exam.started_at).total_seconds()
        total_seconds = active_exam.duration_minutes * 60
        if elapsed_seconds < total_seconds:
            return redirect("exam_taking", exam_id=active_exam.id)
        else:
            # Auto-submit expired exam
            _finalize_exam(active_exam, {})
            return redirect("exam_result", exam_id=active_exam.id)

    # Past exams
    past_exams = Exam.objects.filter(user=request.user, status="submitted").order_by("-submitted_at")[:5]

    return render(request, "exams/intro.html", {
        "active_nav": "exam",
        "past_exams": past_exams,
    })


@login_required
@require_POST
def exam_start(request):
    """
    Starts a new timed mock exam.
    """
    duration = int(request.POST.get("duration", 180))
    if duration not in (60, 120, 180):
        duration = 180

    # Auto-submit any previous active exam
    previous_active = Exam.objects.filter(user=request.user, status="in_progress")
    for ex in previous_active:
        _finalize_exam(ex, {})

    exercises_data = mock_ai.get_mock_exam(duration_minutes=duration)

    new_exam = Exam.objects.create(
        user=request.user,
        duration_minutes=duration,
        exercises_json=exercises_data,
        status="in_progress",
    )

    return redirect("exam_taking", exam_id=new_exam.id)


@login_required
def exam_taking_view(request, exam_id):
    """
    Exam taking screen with sticky countdown timer and exercise tabs.
    """
    exam = get_object_or_404(Exam, id=exam_id, user=request.user)

    if exam.status == "submitted":
        return redirect("exam_result", exam_id=exam.id)

    # Remaining time calculated from started_at on the server
    now = timezone.now()
    elapsed_seconds = (now - exam.started_at).total_seconds()
    total_seconds = exam.duration_minutes * 60
    remaining_seconds = max(0, int(total_seconds - elapsed_seconds))

    if remaining_seconds <= 0:
        # Time has expired
        _finalize_exam(exam, {})
        messages.info(request, "Time expired! Your mock exam has been automatically submitted.")
        return redirect("exam_result", exam_id=exam.id)

    return render(request, "exams/taking.html", {
        "active_nav": "exam",
        "exam": exam,
        "exercises": exam.exercises_json,
        "remaining_seconds": remaining_seconds,
        "total_seconds": total_seconds,
    })


@login_required
@require_POST
def exam_submit(request, exam_id):
    """
    Submits exam, grades exercises, and redirects to results. Rejects double submission.
    """
    exam = get_object_or_404(Exam, id=exam_id, user=request.user)
    if exam.status == "submitted":
        return redirect("exam_result", exam_id=exam.id)

    # Collect answers from POST
    answers = {}
    for ex in exam.exercises_json:
        ex_id = str(ex["id"])
        ans_key = f"answer_{ex_id}"
        answers[ex_id] = request.POST.get(ans_key, "").strip()

    _finalize_exam(exam, answers)

    # Activity streak
    Activity.objects.create(
        user=request.user,
        date=timezone.localdate(),
        activity_type="exam",
        description=f"Completed {exam.duration_minutes}m Mock Exam ({exam.total_grade}/20)"
    )

    messages.success(request, f"Exam submitted! Grade: {exam.total_grade}/20")
    return redirect("exam_result", exam_id=exam.id)


@login_required
def exam_result_view(request, exam_id):
    """
    Results screen with total grade, breakdown table, strengths, weaknesses, and solutions.
    """
    exam = get_object_or_404(Exam, id=exam_id, user=request.user)
    if exam.status != "submitted":
        return redirect("exam_taking", exam_id=exam.id)

    result_data = exam.result_json or {}

    return render(request, "exams/result.html", {
        "active_nav": "exam",
        "exam": exam,
        "result": result_data,
        "grades": result_data.get("grades", []),
        "strengths": result_data.get("strengths", []),
        "weaknesses": result_data.get("weaknesses", []),
        "exercises": exam.exercises_json,
    })


def _finalize_exam(exam, answers):
    """
    Internal helper to grade and mark exam as submitted.
    """
    grading = mock_ai.get_mock_exam_grading(exam.exercises_json, answers)
    exam.status = "submitted"
    exam.total_grade = grading["total_grade"]
    exam.result_json = grading
    exam.submitted_at = timezone.now()
    exam.save()
