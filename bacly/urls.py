from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import core.views as core_views
import accounts.views as account_views
import tutor.views as tutor_views
import practice.views as practice_views
import exams.views as exam_views
import progress.views as progress_views
import classes.views as class_views

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Root
    path("", core_views.home_redirect, name="home"),

    # Authentication & Profile
    path("login/", account_views.login_view, name="login"),
    path("signup/", account_views.signup_view, name="signup"),
    path("logout/", account_views.logout_view, name="logout"),
    path("demo-login/student/", account_views.demo_login_student, name="demo_login_student"),
    path("demo-login/teacher/", account_views.demo_login_teacher, name="demo_login_teacher"),
    path("settings/", account_views.settings_view, name="settings"),

    # Student Dashboard & History
    path("dashboard/", core_views.dashboard_view, name="dashboard"),
    path("history/", core_views.history_view, name="history"),
    path("history/tutor/<int:session_id>/", core_views.history_detail_tutor, name="history_detail_tutor"),
    path("history/practice/<int:result_id>/", core_views.history_detail_practice, name="history_detail_practice"),

    # Ask Tutor
    path("tutor/", tutor_views.tutor_view, name="tutor"),
    path("tutor/explain/", tutor_views.tutor_explain, name="tutor_explain"),
    path("tutor/chat/<int:session_id>/", tutor_views.tutor_chat, name="tutor_chat"),

    # Practice
    path("practice/", practice_views.practice_view, name="practice"),
    path("practice/generate/", practice_views.practice_generate, name="practice_generate"),
    path("practice/check/<int:exercise_id>/", practice_views.practice_check, name="practice_check"),

    # Mock Exam
    path("exam/", exam_views.exam_intro_view, name="exam_intro"),
    path("exam/start/", exam_views.exam_start, name="exam_start"),
    path("exam/<int:exam_id>/", exam_views.exam_taking_view, name="exam_taking"),
    path("exam/<int:exam_id>/submit/", exam_views.exam_submit, name="exam_submit"),
    path("exam/<int:exam_id>/result/", exam_views.exam_result_view, name="exam_result"),

    # Progress & Study Plan
    path("progress/", progress_views.progress_view, name="progress"),
    path("progress/task/<int:task_id>/toggle/", progress_views.toggle_task, name="toggle_task"),
    path("progress/plan/regenerate/", progress_views.regenerate_plan, name="regenerate_plan"),

    # Teacher
    path("teacher/", class_views.teacher_overview, name="teacher_overview"),
    path("teacher/students/", class_views.teacher_students_view, name="teacher_students"),
    path("teacher/student/<int:student_id>/detail/", class_views.student_detail_modal, name="student_detail_modal"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
