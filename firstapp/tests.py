import tempfile
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from .models import Assignment, Classroom, Submission, UserProfile


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

    def test_auth_pages_load_role_toggle_assets(self):
        for page in ("login", "register"):
            with self.subTest(page=page):
                response = self.client.get(reverse(page))

                self.assertContains(response, 'href="/static/css/style.css"')
                self.assertContains(response, 'src="/static/js/role-toggle.js"')
                self.assertContains(response, 'class="role-toggle"')
                self.assertContains(
                    response,
                    'src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"',
                )
                self.assertNotContains(
                    response,
                    'src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/ScrambleTextPlugin.min.js"',
                )
                self.assertNotContains(response, "data-scramble")
                self.assertContains(
                    response,
                    'classList.remove("gsap-pending")',
                )
                self.assertContains(response, 'document.querySelector(".auth-wrapper .card")')
                self.assertContains(response, "gsap.fromTo(")

    def test_authenticated_user_is_redirected_to_dashboard_from_login_pages(self):
        self.client.force_login(self.teacher)

        for page in ("login", "home"):
            with self.subTest(page=page):
                response = self.client.get(reverse(page))

                self.assertRedirects(
                    response,
                    reverse("teacher_dashboard"),
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

    def test_dashboards_are_not_cached_after_sign_out(self):
        for user, dashboard in (
            (self.student, "student_dashboard"),
            (self.teacher, "teacher_dashboard"),
        ):
            with self.subTest(role=user.profile.role):
                dashboard_url = reverse(dashboard)
                self.client.force_login(user)

                dashboard_response = self.client.get(dashboard_url)
                self.assertIn("no-store", dashboard_response["Cache-Control"])

                self.client.get(reverse("logout"))
                response = self.client.get(dashboard_url)

                self.assertRedirects(
                    response,
                    f"{reverse('login')}?next={dashboard_url}",
                )

    def test_logo_navigation_then_sign_out_does_not_restore_dashboard(self):
        for user, dashboard in (
            (self.student, "student_dashboard"),
            (self.teacher, "teacher_dashboard"),
        ):
            with self.subTest(role=user.profile.role):
                dashboard_url = reverse(dashboard)
                self.client.force_login(user)

                logo_response = self.client.get(reverse("home"))
                self.assertRedirects(logo_response, dashboard_url)

                dashboard_response = self.client.get(dashboard_url)
                self.assertContains(
                    dashboard_response,
                    'event.persisted && document.querySelector(".navbar-app")',
                )

                logout_response = self.client.get(reverse("logout"))
                self.assertIn("no-store", logout_response["Cache-Control"])

                response = self.client.get(dashboard_url)
                self.assertRedirects(
                    response,
                    f"{reverse('login')}?next={dashboard_url}",
                )

    def test_login_form_csrf_token_is_valid_and_rotates_after_login(self):
        client = Client(enforce_csrf_checks=True)
        response = client.get(reverse("login"))
        self.assertIn("no-store", response["Cache-Control"])

        csrf_cookie_before_login = client.cookies["csrftoken"].value
        response_content = response.content.decode()
        csrf_token = response_content.split(
            'name="csrfmiddlewaretoken" value="', 1
        )[1].split('"', 1)[0]

        response = client.post(
            reverse("login"),
            {
                "email": self.student.email,
                "password": self.password,
                "role": "student",
                "csrfmiddlewaretoken": csrf_token,
            },
        )

        self.assertRedirects(response, reverse("student_dashboard"))
        self.assertNotEqual(
            client.cookies["csrftoken"].value,
            csrf_cookie_before_login,
        )

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


class TeacherDashboardSubmissionTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="dashboard-teacher",
            email="dashboard-teacher@example.com",
        )
        UserProfile.objects.create(
            user=self.teacher,
            date_of_birth="1985-01-01",
            role="teacher",
        )
        self.student = User.objects.create_user(
            username="submitted-student",
            email="submitted-student@example.com",
        )
        UserProfile.objects.create(
            user=self.student,
            date_of_birth="2005-01-01",
            role="student",
        )
        self.classroom = Classroom.objects.create(
            name="Dashboard classroom",
            key="DASHBOARD-CLASSROOM",
        )
        self.classroom.teachers.add(self.teacher)
        self.classroom.students.add(self.student)
        self.assignment = Assignment.objects.create(
            classroom=self.classroom,
            teacher=self.teacher,
            title="Dashboard assignment",
            deadline="2030-01-01T12:00:00Z",
        )
        self.client.force_login(self.teacher)
        self.dashboard_url = reverse("teacher_dashboard")

    def test_enrolled_students_are_available_in_dropdown(self):
        response = self.client.get(self.dashboard_url)

        self.assertContains(response, 'data-dropdown-toggle')
        self.assertContains(response, 'aria-controls="enrolled-students-list"')
        self.assertContains(response, 'id="enrolled-students-list"')
        self.assertContains(response, 'src="/static/js/dropdown.js"')
        self.assertContains(response, self.student.username)

    def test_empty_assignment_shows_no_submissions_message(self):
        response = self.client.get(self.dashboard_url)

        self.assertContains(response, "No submissions yet.")

    def test_assignment_with_submission_shows_submitter_without_empty_message(self):
        Submission.objects.create(
            assignment=self.assignment,
            student=self.student,
            file="assignment_1/submission.pdf",
        )

        response = self.client.get(self.dashboard_url)

        self.assertContains(response, self.student.username)
        self.assertNotContains(response, "No submissions yet.")
        self.assertNotContains(response, "Not submitted:")


class StudentDashboardSubmissionTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username="submitting-student",
            email="submitting-student@example.com",
        )
        UserProfile.objects.create(
            user=self.student,
            date_of_birth="2005-01-01",
            role="student",
        )
        self.classroom = Classroom.objects.create(
            name="Submission classroom",
            key="SUBMISSION-CLASSROOM",
        )
        self.classroom.students.add(self.student)
        self.assignment = Assignment.objects.create(
            classroom=self.classroom,
            teacher=User.objects.create_user(
                username="submission-teacher",
                email="submission-teacher@example.com",
            ),
            title="Submit this assignment",
            deadline="2030-01-01T12:00:00Z",
        )
        self.client.force_login(self.student)

    def test_dashboard_loads_jquery_and_submission_script(self):
        response = self.client.get(reverse("student_dashboard"))

        self.assertContains(
            response,
            "https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js",
        )
        self.assertContains(response, 'src="/static/js/submission.js"')
        self.assertContains(response, "Make submission")

    def test_student_can_submit_assignment_file(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        storage_patch = patch.object(
            Submission._meta.get_field("file"),
            "storage",
            FileSystemStorage(location=temp_dir.name),
        )
        storage_patch.start()
        self.addCleanup(storage_patch.stop)

        response = self.client.post(
            reverse("submit_assignment", args=[self.assignment.pk]),
            {
                "file": SimpleUploadedFile(
                    "homework.txt",
                    b"Assignment response",
                    content_type="text/plain",
                ),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["file_name"], "homework.txt")
        self.assertTrue(
            Submission.objects.filter(
                assignment=self.assignment,
                student=self.student,
            ).exists()
        )


class ForgotPasswordViewTests(TestCase):
    def test_page_loads_jquery_and_error_display(self):
        response = self.client.get(reverse("forgot_password"))

        self.assertContains(
            response,
            "https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js",
        )
        self.assertContains(response, 'src="/static/js/forgot-password.js"')
        self.assertContains(response, 'id="reset-error"')

    def test_invalid_credentials_return_displayable_error(self):
        response = self.client.post(
            reverse("forgot_password"),
            {
                "email": "unknown@example.com",
                "dob": "2005-01-01",
                "new_password": "a-strong-new-password-123",
                "confirm_password": "a-strong-new-password-123",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"],
            "Email and date of birth do not match any account.",
        )
