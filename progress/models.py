from django.conf import settings
from django.db import models


class StudyPlan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="study_plans",
    )
    week_start = models.DateField()
    tasks_json = models.JSONField(default=list)  # 7 tasks with id, day, text, done
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Study Plan for {self.user.username} (Week {self.week_start})"


class Activity(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    date = models.DateField(db_index=True)
    activity_type = models.CharField(max_length=50, default="practice")
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"
