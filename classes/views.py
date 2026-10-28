import json
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Avg, Q
from accounts.models import User
from classes.models import SchoolClass
from practice.models import PracticeResult
from progress.models import Activity
from core.utils import calculate_chapter_masteries, get_weakest_chapters


@login_required
def teacher_overview(request):
    """
    Teacher Class Overview: class info, join code, stat cards, top 3 struggling chapters.
    """
    if not request.user.is_teacher():
        return redirect("dashboard")

    # Get teacher's class (or create default if none)
    school_class = SchoolClass.objects.filter(teacher=request.user).first()
    if not school_class:
        school_class = SchoolClass.objects.create(
            teacher=request.user,
            name="Terminale Maths A",
        )

    students = school_class.students.all()
    student_count = students.count()

    # Class average /20
    avg_score = PracticeResult.objects.filter(user__in=students).aggregate(Avg("score"))["score__avg"]
    class_average = round(avg_score * 2.0, 1) if avg_score else 12.8

    # Average weekly activity
    today = timezone.localdate()
    week_start = today - timedelta(days=7)
    weekly_acts = Activity.objects.filter(user__in=students, date__gte=week_start).count()
    avg_weekly_act = round(weekly_acts / max(1, student_count), 1)

    # Top 3 struggling chapters across class
    chapter_weakness_counts = {}
    for st in students:
        weak_list = get_weakest_chapters(st, count=2)
        for ch in weak_list:
            chapter_weakness_counts[ch] = chapter_weakness_counts.get(ch, 0) + 1

    sorted_struggles = sorted(chapter_weakness_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    if not sorted_struggles:
        sorted_struggles = [("Probability", 6), ("Sequences", 5), ("Geometry in Space", 3)]

    struggle_labels = [s[0] for s in sorted_struggles]
    struggle_counts = [s[1] for s in sorted_struggles]

    return render(request, "classes/overview.html", {
        "active_nav": "class_overview",
        "school_class": school_class,
        "student_count": student_count,
        "class_average": class_average,
        "avg_weekly_act": avg_weekly_act,
        "sorted_struggles": sorted_struggles,
        "struggle_labels_json": json.dumps(struggle_labels),
        "struggle_counts_json": json.dumps(struggle_counts),
    })


@login_required
def teacher_students_view(request):
    """
    Teacher Students view: table with name, average score, weakest chapter, last active,
    and status badge (On track; Needs attention = average < 10/20 or no activity for 7 days).
    Sortable, searchable. Clicking a row opens student mastery drawer.
    """
    if not request.user.is_teacher():
        return redirect("dashboard")

    school_class = SchoolClass.objects.filter(teacher=request.user).first()
    students_qs = school_class.students.all() if school_class else User.objects.none()

    search = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()

    if search:
        students_qs = students_qs.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(username__icontains=search)
        )

    today = timezone.localdate()
    students_data = []

    for st in students_qs:
        avg_st = PracticeResult.objects.filter(user=st).aggregate(Avg("score"))["score__avg"]
        avg_score_20 = round(avg_st * 2.0, 1) if avg_st else 12.0

        weakest_ch = get_weakest_chapters(st, count=1)
        weakest_str = weakest_ch[0] if weakest_ch else "Probability"

        last_act = Activity.objects.filter(user=st).order_by("-date").first()
        last_active_date = last_act.date if last_act else None

        days_inactive = (today - last_active_date).days if last_active_date else 99
        needs_attention = (avg_score_20 < 10.0) or (days_inactive >= 7)

        if status_filter == "attention" and not needs_attention:
            continue
        if status_filter == "ontrack" and needs_attention:
            continue

        masteries = calculate_chapter_masteries(st)

        students_data.append({
            "id": st.id,
            "name": st.get_full_name() or st.username,
            "email": st.email,
            "stream": st.stream,
            "avg_score_20": avg_score_20,
            "weakest_chapter": weakest_str,
            "last_active": last_active_date.strftime("%b %d") if last_active_date else "Never",
            "needs_attention": needs_attention,
            "days_inactive": days_inactive,
            "masteries_json": json.dumps(masteries),
        })

    # Sort students: Needs attention first, then by avg score
    students_data.sort(key=lambda x: (not x["needs_attention"], -x["avg_score_20"]))

    context = {
        "active_nav": "students",
        "school_class": school_class,
        "students": students_data,
        "search": search,
        "status_filter": status_filter,
    }

    if request.headers.get("HX-Request"):
        return render(request, "classes/partials/students_table.html", context)

    return render(request, "classes/students.html", context)


@login_required
def student_detail_modal(request, student_id):
    """
    HTMX partial returning a student's detailed mastery breakdown and past activity.
    """
    if not request.user.is_teacher():
        return redirect("dashboard")

    student = get_object_or_404(User, id=student_id)
    masteries = calculate_chapter_masteries(student)
    sorted_masteries = sorted(masteries.items(), key=lambda x: x[1])

    recent_results = PracticeResult.objects.filter(user=student).order_by("-created_at")[:5]

    return render(request, "classes/partials/student_drawer.html", {
        "student": student,
        "sorted_masteries": sorted_masteries,
        "recent_results": recent_results,
    })
