from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, Classroom, Assignment

from .models import UserProfile, Classroom

TEACHER_CLASSROOM_KEY = "TYITF2"

def home(request):
    return render(request, "firstapp/login.html")


def login_view(request):
    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        password = request.POST.get("password")
        role = request.POST.get("role")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            authenticated_user = authenticate(
                request,
                username=user.username,
                password=password
            )

            if authenticated_user is not None:

                if authenticated_user.profile.role != role:
                    return render(
                        request,
                        "firstapp/login.html",
                        {"error": "Incorrect role selected for this account."}
                    )

                login(request, authenticated_user)

                if role == "teacher":
                    return redirect("teacher_dashboard")

                return redirect("student_dashboard")

        return render(
            request,
            "firstapp/login.html",
            {"error": "Invalid email or password."}
        )

    return render(request, "firstapp/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def register(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        dob = request.POST.get("dob")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")
        teacher_key = request.POST.get("teacher_key", "").strip()

        if password != confirm_password:
            return render(
                request,
                "firstapp/register.html",
                {"error": "Passwords do not match."}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "firstapp/register.html",
                {"error": "Username already exists."}
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "firstapp/register.html",
                {"error": "An account with this email already exists."}
            )

        if role == "teacher" and teacher_key != TEACHER_CLASSROOM_KEY:
            return render(
                request,
                "firstapp/register.html",
                {"error": "Invalid classroom key."}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            date_of_birth=dob,
            role=role
        )

        if role == "teacher":
            classroom, created = Classroom.objects.get_or_create(
                key=TEACHER_CLASSROOM_KEY,
                defaults={"name": "TYITF2 Classroom"}
            )

            classroom.teachers.add(user)

        return redirect("login")

    return render(request, "firstapp/register.html")


@login_required
def student_dashboard(request):
    if request.user.profile.role != "student":
        return redirect("teacher_dashboard")

    classroom = request.user.student_classrooms.first()

    return render(
        request,
        "firstapp/student_dashboard.html",
        {"classroom": classroom}
    )


@login_required
def teacher_dashboard(request):
    if request.user.profile.role != "teacher":
        return redirect("student_dashboard")

    classroom = request.user.teaching_classrooms.first()

    if request.method == "POST":
        email = request.POST.get("student_email", "").strip()

        student_profile = UserProfile.objects.filter(
            user__email__iexact=email,
            role="student"
        ).select_related("user").first()

        if student_profile is None:
            messages.error(request, "No student account found with that email.")
        elif classroom.students.filter(pk=student_profile.user.pk).exists():
            messages.info(request, "That student is already in the classroom.")
        else:
            classroom.students.add(student_profile.user)
            messages.success(
                request,
                f"{student_profile.user.username} was added to {classroom.name}."
            )

        return redirect("teacher_dashboard")

    return render(
        request,
        "firstapp/teacher_dashboard.html",
        {
            "classroom": classroom,
            "students": classroom.students.all() if classroom else [],
            "assignments": classroom.assignments.all() if classroom else [],
        }
    )

@login_required
def create_assignment(request):
    if request.user.profile.role != "teacher":
        return redirect("student_dashboard")

    classroom = request.user.teaching_classrooms.first()

    if request.method == "POST" and classroom:
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        deadline = request.POST.get("deadline")
        attachment = request.FILES.get("attachment")

        if not title or not deadline:
            messages.error(request, "Title and deadline are required.")
        elif attachment and attachment.size > 10 * 1024 * 1024:
            messages.error(request, "Attachment must be 10 MB or smaller.")
        else:
            Assignment.objects.create(
                classroom=classroom,
                teacher=request.user,
                title=title,
                description=description,
                deadline=deadline,
                attachment=attachment
            )
            messages.success(request, f'Assignment "{title}" created.')

    return redirect("teacher_dashboard")