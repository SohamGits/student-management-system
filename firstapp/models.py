import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone


def private_storage():
    return FileSystemStorage(location=settings.BASE_DIR / "private_media")


def submission_upload_path(instance, filename):
    return f"assignment_{instance.assignment_id}/{filename}"


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
    attachment = models.FileField(
        upload_to="assignment_attachments/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["deadline"]

    def __str__(self):
        return self.title

    def attachment_name(self):
        return os.path.basename(self.attachment.name)

    def is_overdue(self):
        return timezone.now() > self.deadline


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    file = models.FileField(
        upload_to=submission_upload_path,
        storage=private_storage
    )

    submitted_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-submitted_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "student"],
                name="one_submission_per_student"
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

    def file_name(self):
        return os.path.basename(self.file.name)

    def is_late(self):
        return self.submitted_at > self.assignment.deadline