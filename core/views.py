from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Avg, Q
from core.utils import calculate_streak, calculate_chapter_masteries, get_weakest_chapters
from core.constants import CHAPTERS
from tutor.models import TutorSession
from practice.models import PracticeResult, PracticeExercise
from exams.models import Exam
from progress.models import Activity


def home_redirect(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.is_teacher():
        return redirect("teacher_overview")
    return redirect("dashboard")


@login_required
def dashboard_view(request):
    user = request.user
    if user.is_teacher():
        return redirect("teacher_overview")

    today = timezone.localdate()
    streak = calculate_streak(user)

    # Exercises solved this week
    week_start = today - timedelta(days=today.weekday())
    solved_this_week = PracticeResult.objects.filter(
        user=user,
        created_at__date__gte=week_start
    ).count() + TutorSession.objects.filter(
        user=user,
        created_at__date__gte=week_start
    ).count()

    # Average score (/20)
    avg_practice = PracticeResult.objects.filter(user=user).aggregate(Avg("score"))["score__avg"]
    avg_score_20 = round(avg_practice * 2, 1) if avg_practice else 12.0

    # Bac countdown
    bac_date = user.bac_date or (today + timedelta(days=70))
    days_left = max(0, (bac_date - today).days)
    total_prep_days = 270  # roughly 9-month school year
    prep_progress = min(100, max(0, int(((total_prep_days - days_left) / total_prep_days) * 100)))

    # Focus this week (weakest chapter)
    masteries = calculate_chapter_masteries(user)
    sorted_masteries = sorted(masteries.items(), key=lambda x: x[1])
    weakest_chapter, weakest_score = sorted_masteries[0] if sorted_masteries else ("Sequences", 45)

    # Recent activity list (last 5 items)
    recent_tutor = list(TutorSession.objects.filter(user=user).order_by("-created_at")[:5])
    recent_practice = list(PracticeResult.objects.filter(user=user).order_by("-created_at")[:5])

    # Merge and sort
    all_activities = []
    for t in recent_tutor:
        all_activities.append({
            "type": "tutor",
            "title": f"Tutor Session: {t.chapter}",
            "subtitle": t.summary[:65] + ("..." if len(t.summary) > 65 else ""),
            "chapter": t.chapter,
            "created_at": t.created_at,
            "had_mistake": t.had_mistake,
            "url": f"/history/tutor/{t.id}/",
        })
    for p in recent_practice:
        all_activities.append({
            "type": "practice",
            "title": f"Practice Drill: {p.chapter}",
            "subtitle": f"Score: {p.score}/10 - {p.feedback[:50]}...",
            "chapter": p.chapter,
            "created_at": p.created_at,
            "score": p.score,
            "url": f"/history/practice/{p.id}/",
        })

    all_activities.sort(key=lambda x: x["created_at"], reverse=True)
    recent_activities = all_activities[:5]

    return render(request, "core/dashboard.html", {
        "active_nav": "dashboard",
        "today_str": today.strftime("%A, %B %d, %Y"),
        "streak": streak,
        "solved_this_week": solved_this_week,
        "avg_score_20": avg_score_20,
        "days_left": days_left,
        "prep_progress": prep_progress,
        "weakest_chapter": weakest_chapter,
        "weakest_score": weakest_score,
        "recent_activities": recent_activities,
    })


@login_required
def history_view(request):
    user = request.user
    selected_chapter = request.GET.get("chapter", "").strip()
    search_query = request.GET.get("q", "").strip()

    tutor_qs = TutorSession.objects.filter(user=user)
    practice_qs = PracticeResult.objects.filter(user=user)

    if selected_chapter:
        tutor_qs = tutor_qs.filter(chapter=selected_chapter)
        practice_qs = practice_qs.filter(chapter=selected_chapter)

    if search_query:
        tutor_qs = tutor_qs.filter(Q(summary__icontains=search_query) | Q(input_text__icontains=search_query))
        practice_qs = practice_qs.filter(Q(chapter__icontains=search_query) | Q(feedback__icontains=search_query))

    items = []
    for t in tutor_qs[:30]:
        items.append({
            "type": "tutor",
            "id": t.id,
            "title": f"Tutor Session: {t.chapter}",
            "description": t.summary,
            "chapter": t.chapter,
            "had_mistake": t.had_mistake,
            "score": None,
            "created_at": t.created_at,
            "url": f"/history/tutor/{t.id}/",
        })

    for p in practice_qs[:30]:
        items.append({
            "type": "practice",
            "id": p.id,
            "title": f"Practice: {p.chapter}",
            "description": p.feedback,
            "chapter": p.chapter,
            "had_mistake": False,
            "score": p.score,
            "created_at": p.created_at,
            "url": f"/history/practice/{p.id}/",
        })

    items.sort(key=lambda x: x["created_at"], reverse=True)

    context = {
        "active_nav": "history",
        "items": items,
        "chapters": CHAPTERS,
        "selected_chapter": selected_chapter,
        "search_query": search_query,
    }

    if request.headers.get("HX-Request"):
        return render(request, "core/partials/history_list.html", context)

    return render(request, "core/history.html", context)


@login_required
def history_detail_tutor(request, session_id):
    session = get_object_or_404(TutorSession, id=session_id, user=request.user)
    return render(request, "core/history_detail_tutor.html", {
        "active_nav": "history",
        "session": session,
        "result": session.result_json,
    })


@login_required
def history_detail_practice(request, result_id):
    result = get_object_or_404(PracticeResult, id=result_id, user=request.user)
    return render(request, "core/history_detail_practice.html", {
        "active_nav": "history",
        "result": result,
        "exercise": result.exercise,
    })
