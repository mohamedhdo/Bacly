from django.conf import settings
from django.db import models


class PracticeExercise(models.Model):
    DIFFICULTY_CHOICES = (
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Bac level", "Bac level"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="practice_exercises",
    )
    chapter = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default="Medium")
    question = models.TextField()
    hints_json = models.JSONField(default=list)  # list of 2 strings
    solution = models.TextField()  # hidden until answered
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.chapter} ({self.difficulty}) - {self.created_at.strftime('%Y-%m-%d')}"


class PracticeResult(models.Model):
    exercise = models.ForeignKey(
        PracticeExercise,
        on_delete=models.CASCADE,
        related_name="results",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="practice_results",
    )
    chapter = models.CharField(max_length=100)
    score = models.FloatField()  # 0 to 10
    feedback = models.TextField()
    answer_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.chapter} ({self.score}/10)"
