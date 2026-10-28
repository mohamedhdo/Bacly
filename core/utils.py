from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from core.models import AiCallLog
from core.constants import CHAPTERS
from tutor.models import TutorSession
from practice.models import PracticeResult
from progress.models import Activity


def check_and_record_ai_rate_limit(user, feature="tutor"):
    """
    Checks if user exceeded rate limit (30 calls per hour).
    Returns (allowed: bool, current_count: int, retry_after_minutes: int)
    """
    limit = getattr(settings, "AI_RATE_LIMIT_PER_HOUR", 30)
    one_hour_ago = timezone.now() - timedelta(hours=1)
    recent_calls = AiCallLog.objects.filter(user=user, created_at__gte=one_hour_ago).count()

    if recent_calls >= limit:
        return False, recent_calls, 60

    AiCallLog.objects.create(user=user, feature=feature)
    return True, recent_calls + 1, 0


def calculate_streak(user):
    """
    Calculates consecutive days of activity ending today or yesterday.
    """
    activities = Activity.objects.filter(user=user).values_list("date", flat=True).distinct().order_by("-date")
    if not activities:
        return 0

    today = timezone.localdate()
    yesterday = today - timedelta(days=1)

    act_dates = set(activities)
    current = today if today in act_dates else yesterday
    if current not in act_dates:
        return 0

    streak = 0
    check_day = current
    while check_day in act_dates:
        streak += 1
        check_day -= timedelta(days=1)

    return streak


def calculate_chapter_masteries(user):
    """
    Mastery logic: weighted average of practice scores (x10) and tutor sessions
    (no mistake = 100, mistake = 40), recent items weigh more, default 50 when no data.
    Returns a dict {chapter: mastery_percentage (int 0-100)}.
    """
    masteries = {}
    now = timezone.now()

    for ch in CHAPTERS:
        points = []
        weights = []

        # Tutor sessions
        sessions = TutorSession.objects.filter(user=user, chapter=ch).order_by("-created_at")[:10]
        for s in sessions:
            score = 40 if s.had_mistake else 95
            days_ago = max(1, (now - s.created_at).days)
            recency_weight = 1.0 / (1.0 + (days_ago * 0.1))
            points.append(score)
            weights.append(recency_weight)

        # Practice results
        p_results = PracticeResult.objects.filter(user=user, chapter=ch).order_by("-created_at")[:10]
        for p in p_results:
            score = p.score * 10  # convert 0-10 to 0-100
            days_ago = max(1, (now - p.created_at).days)
            recency_weight = 1.0 / (1.0 + (days_ago * 0.1))
            points.append(score)
            weights.append(recency_weight * 1.2)  # slightly higher weight for solved exercises

        if points:
            weighted_avg = sum(p * w for p, w in zip(points, weights)) / sum(weights)
            masteries[ch] = int(round(min(100, max(15, weighted_avg))))
        else:
            masteries[ch] = 50  # default 50 when no data

    return masteries


def get_weakest_chapters(user, count=2):
    """
    Returns list of the weakest chapters sorted ascending by mastery.
    """
    masteries = calculate_chapter_masteries(user)
    sorted_chs = sorted(masteries.items(), key=lambda x: x[1])
    return [ch for ch, _ in sorted_chs[:count]]
