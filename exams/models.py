from django.conf import settings
from django.db import models


class Exam(models.Model):
    STATUS_CHOICES = (
        ("in_progress", "In Progress"),
        ("submitted", "Submitted"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="exams",
    )
    duration_minutes = models.IntegerField(default=180)  # 60, 120, 180
    exercises_json = models.JSONField(default=list)  # 3-4 exercises with points and questions
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="in_progress")
    total_grade = models.FloatField(null=True, blank=True)  # out of 20
    result_json = models.JSONField(default=dict)  # per-exercise breakdown, strengths, weaknesses, solutions
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        grade = f"{self.total_grade}/20" if self.total_grade is not None else "In Progress"
        return f"{self.user.username} Exam ({grade}) - {self.started_at.strftime('%Y-%m-%d')}"
