from django.conf import settings
from django.db import models


class AiCallLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_calls",
    )
    feature = models.CharField(max_length=50)  # tutor, practice, exam, chat, plan
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.feature} at {self.created_at}"
