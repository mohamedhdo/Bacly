from django.conf import settings
from django.db import models


class TutorSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tutor_sessions",
    )
    chapter = models.CharField(max_length=100)
    summary = models.TextField()
    input_text = models.TextField(blank=True)
    exercise_image = models.ImageField(upload_to="tutor_exercises/", blank=True, null=True)
    attempt_text = models.TextField(blank=True)
    attempt_image = models.ImageField(upload_to="tutor_attempts/", blank=True, null=True)
    result_json = models.JSONField(default=dict)
    had_mistake = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.chapter} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class TutorMessage(models.Model):
    ROLE_CHOICES = (
        ("user", "Student"),
        ("tutor", "Bacly Tutor"),
    )
    session = models.ForeignKey(
        TutorSession,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role}: {self.content[:40]}"
