from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import UserProfile


class LoginViewTests(TestCase):
    def setUp(self):
        self.password = "correct-horse-battery-staple"
        self.student = User.objects.create_user(
            username="student",
            email="student@example.com",
            password=self.password,
        )
        UserProfile.objects.create(
            user=self.student,
            date_of_birth="2005-01-01",
            role="student",
        )
        self.teacher = User.objects.create_user(
            username="teacher",
            email="teacher@example.com",
            password=self.password,
        )
        UserProfile.objects.create(
            user=self.teacher,
            date_of_birth="1985-01-01",
            role="teacher",
        )

    def test_student_login_redirects_to_student_dashboard(self):
        response = self.client.post(
            reverse("login"),
            {
                "email": self.student.email,
                "password": self.password,
                "role": "student",
            },
        )

        self.assertRedirects(response, reverse("student_dashboard"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.student.pk)

    def test_teacher_login_redirects_to_teacher_dashboard(self):
        response = self.client.post(
            reverse("login"),
            {
                "email": self.teacher.email,
                "password": self.password,
                "role": "teacher",
            },
        )

        self.assertRedirects(response, reverse("teacher_dashboard"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.teacher.pk)

    def test_invalid_password_shows_login_error(self):
        response = self.client.post(
            reverse("login"),
            {
                "email": self.student.email,
                "password": "wrong-password",
                "role": "student",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email or password.")
