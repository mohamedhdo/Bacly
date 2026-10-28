from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from accounts.forms import SignUpForm, UserSettingsForm, JoinClassForm
from classes.models import SchoolClass


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_teacher():
            return redirect("teacher_overview")
        return redirect("dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_teacher():
                return redirect("teacher_overview")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Bacly, {user.first_name}!")
            if user.is_teacher():
                return redirect("teacher_overview")
            return redirect("dashboard")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


def demo_login_student(request):
    """
    Instantly logs in the seeded demo student (Yasmine Benali).
    """
    user = User.objects.filter(username="demo_student").first()
    if not user:
        from django.core.management import call_command
        call_command("seed_demo")
        user = User.objects.filter(username="demo_student").first()

    if user:
        login(request, user)
        messages.success(request, f"Logged in as Demo Student: {user.get_full_name() or user.username}")
        return redirect("dashboard")
    messages.error(request, "Could not load demo student account.")
    return redirect("login")


def demo_login_teacher(request):
    """
    Instantly logs in the seeded demo teacher (Mr. Karim Mansouri).
    """
    user = User.objects.filter(username="demo_teacher").first()
    if not user:
        from django.core.management import call_command
        call_command("seed_demo")
        user = User.objects.filter(username="demo_teacher").first()

    if user:
        login(request, user)
        messages.success(request, f"Logged in as Demo Teacher: {user.get_full_name() or user.username}")
        return redirect("teacher_overview")
    messages.error(request, "Could not load demo teacher account.")
    return redirect("login")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


@login_required
def settings_view(request):
    user = request.user
    user_form = UserSettingsForm(instance=user)
    password_form = PasswordChangeForm(user=user)
    join_form = JoinClassForm()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "update_profile":
            user_form = UserSettingsForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect("settings")
        elif action == "change_password":
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your password was changed successfully.")
                return redirect("settings")
            else:
                messages.error(request, "Please correct the password errors below.")
        elif action == "join_class":
            join_form = JoinClassForm(request.POST)
            if join_form.is_valid():
                code = join_form.cleaned_data["join_code"].strip().upper()
                s_class = SchoolClass.objects.filter(join_code=code).first()
                if s_class:
                    user.school_class = s_class
                    user.save()
                    messages.success(request, f"Successfully joined class '{s_class.name}'!")
                    return redirect("settings")
                else:
                    messages.error(request, f"No class found with join code '{code}'. Check with your teacher.")

    return render(request, "accounts/settings.html", {
        "user_form": user_form,
        "password_form": password_form,
        "join_form": join_form,
        "active_nav": "settings",
    })
