from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    date_of_birth = models.DateField()

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Classroom(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=50, unique=True)

    teachers = models.ManyToManyField(
        User,
        related_name="teaching_classrooms",
        blank=True
    )

    students = models.ManyToManyField(
        User,
        related_name="student_classrooms",
        blank=True
    )

    def __str__(self):
        return self.name


class Assignment(models.Model):
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_assignments"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["deadline"]

    def __str__(self):
        return self.title