from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("teacher/assignments/create/", views.create_assignment, name="create_assignment"),
    path(
        "teacher/assignments/<int:assignment_id>/edit/",
        views.edit_assignment,
        name="edit_assignment",
    ),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("student/assignments/<int:assignment_id>/submit/", views.submit_assignment, name="submit_assignment"),
    path("submissions/<int:submission_id>/download/", views.download_submission, name="download_submission"),
]
