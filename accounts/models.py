from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
    )
    STREAM_CHOICES = (
        ("Mathematics", "Mathematics"),
        ("Experimental Sciences", "Experimental Sciences"),
        ("Technical Mathematics", "Technical Mathematics"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    stream = models.CharField(max_length=50, choices=STREAM_CHOICES, default="Mathematics")
    bac_date = models.DateField(null=True, blank=True)
    school_class = models.ForeignKey(
        "classes.SchoolClass",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="students",
    )

    def is_student(self):
        return self.role == "student"

    def is_teacher(self):
        return self.role == "teacher"

    def get_initials(self):
        first = self.first_name[:1] if self.first_name else ""
        last = self.last_name[:1] if self.last_name else ""
        if first or last:
            return f"{first}{last}".upper()
        return self.username[:2].upper()
