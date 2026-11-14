from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, FileResponse, Http404
from django.urls import reverse
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.db import transaction

from .forms import AssignmentEditForm
from .models import UserProfile, Classroom, Assignment, Submission
from .upload_validation import has_allowed_file_type

MAX_RESET_ATTEMPTS = 5
RESET_LOCKOUT_SECONDS = 15 * 60
TEACHER_CLASSROOM_KEY = "TYITF2"
MAX_UPLOAD_BYTES = settings.MAX_UPLOAD_BYTES


@never_cache
def home(request):
    if request.user.is_authenticated:
        dashboard = (
            "teacher_dashboard"
            if request.user.profile.role == "teacher"
            else "student_dashboard"
        )
        return redirect(dashboard)

    return render(request, "firstapp/login.html")


@never_cache
def login_view(request):
    if request.method == "GET" and request.user.is_authenticated:
        dashboard = (
            "teacher_dashboard"
            if request.user.profile.role == "teacher"
            else "student_dashboard"
        )
        return redirect(dashboard)

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
                password=password,
            )

            if authenticated_user is not None:
                if getattr(authenticated_user.profile, "role", None) != role:
                    return render(
                        request,
                        "firstapp/login.html",
                        {"error": "Incorrect role selected for this account."},
                    )

                login(request, authenticated_user)
                if role == "teacher":
                    return redirect("teacher_dashboard")
                return redirect("student_dashboard")

        return render(
            request,
            "firstapp/login.html",
            {"error": "Invalid email or password."},
        )

    return render(request, "firstapp/login.html")


@never_cache
@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")


@never_cache
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
                {"error": "Passwords do not match.", "form": request.POST},
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "firstapp/register.html",
                {"error": "Username already exists.", "form": request.POST},
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "firstapp/register.html",
                {
                    "error": "An account with this email already exists.",
                    "form": request.POST,
                },
            )

        if role == "teacher" and teacher_key != TEACHER_CLASSROOM_KEY:
            return render(
                request,
                "firstapp/register.html",
                {"error": "Invalid classroom key.", "form": request.POST},
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        UserProfile.objects.create(
            user=user,
            date_of_birth=dob,
            role=role,
        )

        if role == "teacher":
            classroom, _ = Classroom.objects.get_or_create(
                key=TEACHER_CLASSROOM_KEY,
                defaults={"name": "TYITF2 Classroom"},
            )
            classroom.teachers.add(user)

        return redirect("login")

    return render(request, "firstapp/register.html")


@never_cache
@login_required
def student_dashboard(request):
    if request.user.profile.role != "student":
        return redirect("teacher_dashboard")

    classroom = request.user.student_classrooms.first()
    assignments = []

    if classroom:
        assignments = list(
            classroom.assignments.select_related("teacher")
        )
        now = timezone.now()
        assignments.sort(
            key=lambda a: (
                a.deadline < now,
                abs((a.deadline - now).total_seconds()),
            )
        )
        my_submissions = {
            submission.assignment_id: submission
            for submission in Submission.objects.filter(
                student=request.user,
                assignment__in=assignments
            ).select_related("assignment")
        }
        for assignment in assignments:
            assignment.my_submission = my_submissions.get(assignment.id)

    return render(
        request,
        "firstapp/student_dashboard.html",
        {"classroom": classroom, "assignments": assignments}
    )


@never_cache
@login_required
def teacher_dashboard(request):
    if request.user.profile.role != "teacher":
        return redirect("student_dashboard")

    classroom = request.user.teaching_classrooms.first()

    if request.method == "POST" and classroom:
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

    students = []
    assignments = []

    if classroom:
        students = list(classroom.students.all())
        assignments = list(
            classroom.assignments
            .select_related("teacher")
            .prefetch_related("submissions__student")
        )
        now = timezone.now()
        assignments.sort(
            key=lambda a: (
                a.deadline < now,
                abs((a.deadline - now).total_seconds()),
            )
        )

    return render(
        request,
        "firstapp/teacher_dashboard.html",
        {
            "classroom": classroom,
            "students": students,
            "assignments": assignments,
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

        if getattr(request, "upload_too_large", False):
            messages.error(request, "Attachment must be 10 MB or smaller.")
        elif not title or not deadline:
            messages.error(request, "Title and deadline are required.")
        elif attachment and attachment.size > MAX_UPLOAD_BYTES:
            messages.error(request, "Attachment must be 10 MB or smaller.")
        elif attachment and not has_allowed_file_type(attachment):
            messages.error(
                request,
                "Attachment must be a valid PDF, DOCX, image, or ZIP file.",
            )
        else:
            Assignment.objects.create(
                classroom=classroom,
                teacher=request.user,
                title=title,
                description=description,
                deadline=deadline,
                attachment=attachment,
            )
            messages.success(request, f'Assignment "{title}" created.')

    return redirect("teacher_dashboard")


@never_cache
@login_required
def edit_assignment(request, assignment_id):
    if request.user.profile.role != "teacher":
        return redirect("student_dashboard")

    assignment = get_object_or_404(
        Assignment,
        pk=assignment_id,
        teacher=request.user,
        classroom__teachers=request.user,
    )

    if request.method == "POST":
        form = AssignmentEditForm(request.POST, instance=assignment)
        if form.is_valid():
            updated_assignment = form.save()
            messages.success(
                request,
                f'Assignment "{updated_assignment.title}" updated.',
            )
            return redirect("teacher_dashboard")

        messages.error(
            request,
            form.errors.get("deadline", ["Please correct the errors below."])[0],
        )
        deadline_value = request.POST.get("deadline", "")
        return render(
            request,
            "firstapp/edit_assignment.html",
            {"form": form, "assignment": assignment, "deadline_value": deadline_value},
        )

    form = AssignmentEditForm(instance=assignment)
    deadline_value = timezone.localtime(assignment.deadline).strftime("%Y-%m-%dT%H:%M")
    return render(
        request,
        "firstapp/edit_assignment.html",
        {"form": form, "assignment": assignment, "deadline_value": deadline_value},
    )

@login_required
@require_POST
def delete_assignment(request, assignment_id):
    if request.user.profile.role != "teacher":
        return redirect("student_dashboard")

    # Only the teacher who created the assignment can delete it.
    assignment = get_object_or_404(
        Assignment,
        pk=assignment_id,
        teacher=request.user,
        classroom__teachers=request.user,
    )

    title = assignment.title
    stored_files = [s.file for s in assignment.submissions.all() if s.file]
    if assignment.attachment:
        stored_files.append(assignment.attachment)

    with transaction.atomic():
        assignment.delete()  # submissions are removed by the cascade

    # Remove the uploaded files from disk once the rows are gone.
    for stored_file in stored_files:
        stored_file.delete(save=False)

    messages.success(request, f'Assignment "{title}" deleted.')
    return redirect("teacher_dashboard")


@never_cache
def forgot_password(request):
    if request.method != "POST":
        return render(request, "firstapp/forgot_password.html")

    email = request.POST.get("email", "").strip().lower()
    dob = parse_date(request.POST.get("dob", ""))
    new_password = request.POST.get("new_password", "")
    confirm_password = request.POST.get("confirm_password", "")

    attempts_key = f"reset_attempts:{email}"
    cache.add(attempts_key, 0, RESET_LOCKOUT_SECONDS)
    try:
        attempts = cache.incr(attempts_key)
    except ValueError:
        cache.add(attempts_key, 0, RESET_LOCKOUT_SECONDS)
        attempts = cache.incr(attempts_key)

    if attempts > MAX_RESET_ATTEMPTS:
        return JsonResponse(
            {"ok": False, "error": "Too many attempts. Please try again in 15 minutes."},
            status=429,
        )

    if new_password != confirm_password:
        return JsonResponse({"ok": False, "error": "Passwords do not match."}, status=400)

    profile = None
    if dob is not None:
        profile = UserProfile.objects.filter(
            user__email__iexact=email,
            date_of_birth=dob,
        ).select_related("user").first()

    if profile is None:
        return JsonResponse(
            {"ok": False, "error": "Email and date of birth do not match any account."},
            status=400,
        )

    try:
        validate_password(new_password, user=profile.user)
    except ValidationError as error:
        return JsonResponse({"ok": False, "error": " ".join(error.messages)}, status=400)

    profile.user.set_password(new_password)
    profile.user.save()
    cache.delete(attempts_key)

    messages.success(request, "Password reset successful. Please log in.")
    return JsonResponse({"ok": True, "redirect": reverse("login")})


@login_required
def submit_assignment(request, assignment_id):
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "Invalid request."}, status=405)

    if request.user.profile.role != "student":
        return JsonResponse(
            {"ok": False, "error": "Only students can submit."}, status=403
        )

    assignment = get_object_or_404(
        Assignment,
        pk=assignment_id,
        classroom__students=request.user
    )

    upload = request.FILES.get("file")

    if getattr(request, "upload_too_large", False):
        return JsonResponse(
            {"ok": False, "error": "File must be 10 MB or smaller."}, status=413
        )

    if upload is None:
        return JsonResponse(
            {"ok": False, "error": "Please choose a file."}, status=400
        )

    if upload.size > MAX_UPLOAD_BYTES:
        return JsonResponse(
            {"ok": False, "error": "File must be 10 MB or smaller."}, status=413
        )

    if not has_allowed_file_type(upload):
        return JsonResponse(
            {
                "ok": False,
                "error": "File must be a valid PDF, DOCX, image, or ZIP file.",
            },
            status=400,
        )

    submission, created = Submission.objects.get_or_create(
        assignment=assignment,
        student=request.user,
        defaults={"file": upload}
    )

    if not created:
        submission.file.delete(save=False)
        submission.file = upload
        submission.save()

    return JsonResponse({
        "ok": True,
        "file_name": submission.file_name(),
        "submitted_at": timezone.localtime(
            submission.submitted_at
        ).strftime("%d %b %Y, %H:%M"),
        "late": submission.is_late(),
        "download_url": reverse("download_submission", args=[submission.id]),
    })


@login_required
def download_submission(request, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related("assignment"),
        pk=submission_id
    )

    is_owner = submission.student_id == request.user.id
    is_posting_teacher = submission.assignment.teacher_id == request.user.id

    if not (is_owner or is_posting_teacher):
        raise Http404("Submission not found.")

    return _attachment_response(submission.file, submission.file_name())


@login_required
def download_assignment_attachment(request, assignment_id):
    assignment = get_object_or_404(
        Assignment.objects.select_related("classroom"),
        pk=assignment_id,
    )
    has_access = (
        assignment.classroom.students.filter(pk=request.user.pk).exists()
        or assignment.classroom.teachers.filter(pk=request.user.pk).exists()
    )
    if not has_access:
        raise Http404("Assignment not found.")
    if not assignment.attachment:
        raise Http404("Attachment not found.")

    return _attachment_response(
        assignment.attachment,
        assignment.attachment_name(),
    )


def _attachment_response(stored_file, filename):
    try:
        file_handle = stored_file.open("rb")
    except FileNotFoundError:
        raise Http404("The file is no longer available.")

    response = FileResponse(
        file_handle,
        as_attachment=True,
        filename=filename,
        content_type="application/octet-stream",
    )
    response["Cache-Control"] = "private, no-store"
    response["X-Content-Type-Options"] = "nosniff"
    return response