import os
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from accounts.models import User
from classes.models import SchoolClass
from tutor.models import TutorSession
from practice.models import PracticeExercise, PracticeResult
from exams.models import Exam
from progress.models import StudyPlan, Activity


class BaclyCoreTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Seed teacher
        self.teacher = User.objects.create_user(
            username="test_teacher",
            password="password123",
            role="teacher",
            first_name="Karim",
            last_name="Mansouri"
        )
        self.school_class = SchoolClass.objects.create(
            teacher=self.teacher,
            name="Terminale Maths A",
            join_code="BAC99M"
        )

        # Seed student
        self.student = User.objects.create_user(
            username="test_student",
            password="password123",
            role="student",
            stream="Mathematics",
            first_name="Yasmine",
            last_name="Benali",
            school_class=self.school_class
        )

        # Seed activity
        Activity.objects.create(
            user=self.student,
            date=timezone.localdate(),
            activity_type="practice"
        )

    def test_demo_login_student(self):
        response = self.client.get(reverse("demo_login_student"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")

    def test_demo_login_teacher(self):
        response = self.client.get(reverse("demo_login_teacher"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Class Overview")

    def test_student_dashboard(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Good day, Yasmine")
        self.assertContains(response, "Day Streak")

    def test_tutor_explain_with_attempt(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse("tutor_explain"), {
            "exercise_text": "Study the convergence of the sequence u(n+1) = (1/3)u(n) + 2 with u(0) = 1.",
            "attempt_text": "I set v(n) = u(n) - 3, then v(0) = 1 + 3 = 4...",
            "chapter": "Sequences",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Step-by-Step Solution")
        self.assertContains(response, "Where You Went Wrong")
        self.assertContains(response, "Similar Practice Exercises")

    def test_tutor_explain_empty_validation(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse("tutor_explain"), {
            "exercise_text": "",
            "attempt_text": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Missing Exercise Content")

    def test_practice_generate_and_check(self):
        self.client.force_login(self.student)
        gen_resp = self.client.post(reverse("practice_generate"), {
            "chapter": "Sequences",
            "difficulty": "Bac level",
        })
        self.assertEqual(gen_resp.status_code, 200)
        self.assertContains(gen_resp, "Step-by-step Hints")

        ex = PracticeExercise.objects.filter(user=self.student).first()
        self.assertIsNotNone(ex)

        check_resp = self.client.post(reverse("practice_check", kwargs={"exercise_id": ex.id}), {
            "answer_text": "I used mathematical induction to show u(n) is bounded by 3, then calculated the derivative.",
        })
        self.assertEqual(check_resp.status_code, 200)
        self.assertContains(check_resp, "Evaluation & Feedback")
        self.assertContains(check_resp, "/ 10 pts")

    def test_mock_exam_lifecycle(self):
        self.client.force_login(self.student)
        start_resp = self.client.post(reverse("exam_start"), {"duration": 180}, follow=True)
        self.assertEqual(start_resp.status_code, 200)
        self.assertContains(start_resp, "Exercise 1")

        exam = Exam.objects.filter(user=self.student, status="in_progress").first()
        self.assertIsNotNone(exam)

        submit_resp = self.client.post(reverse("exam_submit", kwargs={"exam_id": exam.id}), {
            "answer_1": "Complete derivation for sequence exercise 1 with induction hypothesis.",
            "answer_2": "Complex plane rotation proof.",
        }, follow=True)
        self.assertEqual(submit_resp.status_code, 200)
        self.assertContains(submit_resp, "Mock Exam Report")
        self.assertContains(submit_resp, "/ 20 Points")

    def test_progress_view_and_toggle(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse("progress"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Curriculum Chapter Mastery")
        self.assertContains(response, "7-Day Adaptive Study Plan")

        plan = StudyPlan.objects.filter(user=self.student).first()
        self.assertIsNotNone(plan)
        first_task_id = plan.tasks_json[0]["id"]

        toggle_resp = self.client.post(reverse("toggle_task", kwargs={"task_id": first_task_id}))
        self.assertEqual(toggle_resp.status_code, 200)
        self.assertContains(toggle_resp, "Weekly Goal Progress")

    def test_teacher_overview_and_students(self):
        self.client.force_login(self.teacher)
        overview_resp = self.client.get(reverse("teacher_overview"))
        self.assertEqual(overview_resp.status_code, 200)
        self.assertContains(overview_resp, "Class Overview")
        self.assertContains(overview_resp, "BAC99M")

        students_resp = self.client.get(reverse("teacher_students"))
        self.assertEqual(students_resp.status_code, 200)
        self.assertContains(students_resp, "Yasmine Benali")
