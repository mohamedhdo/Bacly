import json
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from core.utils import calculate_chapter_masteries, get_weakest_chapters
from core.constants import CHAPTERS
from exams.models import Exam
from progress.models import StudyPlan
from bacly.services import mock_ai


@login_required
def progress_view(request):
    """
    My Progress dashboard: mastery bar chart, exam progression line chart, 7-day plan checklist.
    """
    if request.user.is_teacher():
        return redirect("teacher_overview")

    user = request.user
    today = timezone.localdate()

    # 1. Masteries sorted weakest first
    masteries_dict = calculate_chapter_masteries(user)
    # Sort ascending (weakest first)
    sorted_masteries = sorted(masteries_dict.items(), key=lambda x: x[1])

    mastery_labels = [item[0] for item in sorted_masteries]
    mastery_values = [item[1] for item in sorted_masteries]
    # Color logic: red under 40%, orange 40-70%, green above 70%
    mastery_colors = []
    for val in mastery_values:
        if val < 40:
            mastery_colors.append("#EF4444")  # red
        elif val <= 70:
            mastery_colors.append("#F97316")  # orange
        else:
            mastery_colors.append("#10B981")  # green

    # 2. Mock exam grades over time
    past_exams = Exam.objects.filter(user=user, status="submitted").order_by("started_at")
    exam_dates = []
    exam_grades = []
    for ex in past_exams:
        exam_dates.append(ex.started_at.strftime("%b %d"))
        exam_grades.append(ex.total_grade or 10.0)

    # If no exams yet, provide a baseline
    if not exam_dates:
        exam_dates = ["Start"]
        exam_grades = [10.0]

    # 3. 7-Day Study Plan
    week_start = today - timedelta(days=today.weekday())
    study_plan = StudyPlan.objects.filter(user=user, week_start=week_start).first()
    if not study_plan:
        weakest = get_weakest_chapters(user, count=2)
        tasks = mock_ai.get_mock_study_plan(weakest)
        study_plan = StudyPlan.objects.create(
            user=user,
            week_start=week_start,
            tasks_json=tasks
        )

    tasks = study_plan.tasks_json or []
    done_count = sum(1 for t in tasks if t.get("done"))
    total_tasks = len(tasks)
    plan_progress_percent = int((done_count / total_tasks * 100)) if total_tasks else 0

    # Summary sentence: "You improved 12% this month. Focus on: Probability and Sequences."
    weakest_names = [item[0] for item in sorted_masteries[:2]]
    focus_str = " and ".join(weakest_names) if weakest_names else "Sequences"
    summary_sentence = f"You improved 12% this month. Focus on: {focus_str}."

    return render(request, "progress/progress.html", {
        "active_nav": "progress",
        "summary_sentence": summary_sentence,
        "mastery_labels_json": json.dumps(mastery_labels),
        "mastery_values_json": json.dumps(mastery_values),
        "mastery_colors_json": json.dumps(mastery_colors),
        "exam_dates_json": json.dumps(exam_dates),
        "exam_grades_json": json.dumps(exam_grades),
        "study_plan": study_plan,
        "tasks": tasks,
        "done_count": done_count,
        "total_tasks": total_tasks,
        "plan_progress_percent": plan_progress_percent,
        "sorted_masteries": sorted_masteries,
    })


@login_required
@require_POST
def toggle_task(request, task_id):
    """
    Toggles completion state of a study plan task via HTMX.
    """
    user = request.user
    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())
    plan = StudyPlan.objects.filter(user=user).order_by("-week_start").first()

    if not plan:
        return redirect("progress")

    tasks = list(plan.tasks_json)
    for t in tasks:
        if str(t.get("id")) == str(task_id):
            t["done"] = not t.get("done", False)
            break

    plan.tasks_json = tasks
    plan.save()

    done_count = sum(1 for t in tasks if t.get("done"))
    total_tasks = len(tasks)
    plan_progress_percent = int((done_count / total_tasks * 100)) if total_tasks else 0

    return render(request, "progress/partials/study_plan_checklist.html", {
        "tasks": tasks,
        "done_count": done_count,
        "total_tasks": total_tasks,
        "plan_progress_percent": plan_progress_percent,
    })


@login_required
@require_POST
def regenerate_plan(request):
    """
    Regenerates study plan tailored to current weakest chapters via HTMX.
    """
    user = request.user
    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())
    weakest = get_weakest_chapters(user, count=2)

    new_tasks = mock_ai.get_mock_study_plan(weakest)

    plan, _ = StudyPlan.objects.get_or_create(user=user, week_start=week_start)
    plan.tasks_json = new_tasks
    plan.save()

    done_count = sum(1 for t in new_tasks if t.get("done"))
    total_tasks = len(new_tasks)
    plan_progress_percent = int((done_count / total_tasks * 100)) if total_tasks else 0

    return render(request, "progress/partials/study_plan_checklist.html", {
        "tasks": new_tasks,
        "done_count": done_count,
        "total_tasks": total_tasks,
        "plan_progress_percent": plan_progress_percent,
    })
