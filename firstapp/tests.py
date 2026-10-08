from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Assignment, Classroom, UserProfile


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


class AssignmentEditViewTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="assignment-teacher",
            email="assignment-teacher@example.com",
            password="StrongPass!123",
        )
        UserProfile.objects.create(
            user=self.teacher,
            date_of_birth="1985-01-01",
            role="teacher",
        )
        self.classroom = Classroom.objects.create(
            name="Test classroom",
            key="TEST-CLASSROOM",
        )
        self.classroom.teachers.add(self.teacher)
        self.assignment = Assignment.objects.create(
            classroom=self.classroom,
            teacher=self.teacher,
            title="Original title",
            description="Original description",
            deadline="2030-01-01T12:00:00Z",
        )
        self.client.force_login(self.teacher)
        self.edit_url = reverse(
            "edit_assignment",
            args=[self.assignment.pk],
        )

    def test_teacher_can_edit_assignment_details(self):
        response = self.client.post(
            self.edit_url,
            {
                "title": "Updated title",
                "description": "Updated description",
                "deadline": "2030-02-03T14:30",
            },
        )

        self.assertRedirects(response, reverse("teacher_dashboard"))
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.title, "Updated title")
        self.assertEqual(self.assignment.description, "Updated description")
        self.assertEqual(
            self.assignment.deadline.isoformat(),
            "2030-02-03T09:00:00+00:00",
        )

    def test_invalid_deadline_does_not_update_assignment(self):
        response = self.client.post(
            self.edit_url,
            {
                "title": "Updated title",
                "description": "Updated description",
                "deadline": "not-a-deadline",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid date/time.")
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.title, "Original title")

    def test_teacher_can_open_assignment_edit_form(self):
        response = self.client.get(self.edit_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit assignment")
        self.assertContains(response, "Original title")
        self.assertContains(response, "Original description")

    def test_teacher_cannot_edit_another_teachers_assignment(self):
        other_teacher = User.objects.create_user(
            username="another-teacher",
            email="another-teacher@example.com",
            password="StrongPass!123",
        )
        UserProfile.objects.create(
            user=other_teacher,
            date_of_birth="1985-01-01",
            role="teacher",
        )
        self.client.force_login(other_teacher)

        response = self.client.get(self.edit_url)

        self.assertEqual(response.status_code, 404)
