import random
import string
from django.conf import settings
from django.db import models


def generate_join_code():
    chars = string.ascii_uppercase + string.digits
    # Exclude ambiguous characters like O, 0, I, 1
    clean_chars = [c for c in chars if c not in ("O", "0", "I", "1")]
    return "".join(random.choices(clean_chars, k=6))


class SchoolClass(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="classes",
    )
    name = models.CharField(max_length=100)
    join_code = models.CharField(max_length=6, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.join_code:
            code = generate_join_code()
            while SchoolClass.objects.filter(join_code=code).exists():
                code = generate_join_code()
            self.join_code = code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.join_code})"
