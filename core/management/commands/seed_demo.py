import os
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User
from classes.models import SchoolClass
from tutor.models import TutorSession, TutorMessage
from practice.models import PracticeExercise, PracticeResult
from exams.models import Exam
from progress.models import StudyPlan, Activity
from core.constants import CHAPTERS
from bacly.services import mock_ai


class Command(BaseCommand):
    help = "Seeds idempotent demo data for Bacly (Demo Student Yasmine Benali and Demo Teacher Mr. Karim)"

    def handle(self, *args, **options):
        self.stdout.write("Seeding Bacly demo data...")

        # 1. Teacher: Mr. Karim
        teacher, created = User.objects.get_or_create(
            username="demo_teacher",
            defaults={
                "first_name": "Karim",
                "last_name": "Mansouri",
                "email": "karim.mansouri@lycee-alger.dz",
                "role": "teacher",
                "stream": "Mathematics",
            }
        )
        teacher.set_password("demo1234")
        teacher.role = "teacher"
        teacher.save()

        # Teacher's Class
        school_class, _ = SchoolClass.objects.get_or_create(
            teacher=teacher,
            name="Terminale Maths A (Lycée Frantz Fanon)",
            defaults={"join_code": "BAC26M"}
        )

        # 2. Demo Student: Yasmine Benali
        today = timezone.localdate()
        bac_date = today + timedelta(days=70)

        student, created = User.objects.get_or_create(
            username="demo_student",
            defaults={
                "first_name": "Yasmine",
                "last_name": "Benali",
                "email": "yasmine.benali@student.bacly.dz",
                "role": "student",
                "stream": "Mathematics",
                "bac_date": bac_date,
                "school_class": school_class,
            }
        )
        student.set_password("demo1234")
        student.role = "student"
        student.stream = "Mathematics"
        student.bac_date = bac_date
        student.school_class = school_class
        student.save()

        # Clear previous data for idempotent re-seed
        TutorSession.objects.filter(user=student).delete()
        PracticeExercise.objects.filter(user=student).delete()
        PracticeResult.objects.filter(user=student).delete()
        Exam.objects.filter(user=student).delete()
        StudyPlan.objects.filter(user=student).delete()
        Activity.objects.filter(user=student).delete()

        # 3. 5-day streak for Yasmine
        for day_offset in range(5):
            act_date = today - timedelta(days=day_offset)
            Activity.objects.create(
                user=student,
                date=act_date,
                activity_type="practice",
                description="Completed 3 Bac practice exercises"
            )

        # 4. History items (40+ items across all chapters)
        # We will create ~25 tutor sessions and ~25 practice results
        sample_questions = {
            "Sequences": [
                ("Study the convergence of $u_{n+1} = \\frac{1}{3}u_n + 2$ with $u_0 = 1$.", False),
                ("Prove by induction that $u_n > 0$ for all $n \\in \\mathbb{N}$.", False),
                ("Calculate the sum $S_n = \\sum_{k=0}^n v_k$ for a geometric sequence.", True),
            ],
            "Probability": [
                ("Two balls drawn without replacement from 3 red and 5 white balls.", True),
                ("Calculate the conditional probability $P(A|B)$ in a tree diagram.", True),
                ("Find the expectation and variance of binomial distribution $B(10, 0.4)$.", True),
            ],
            "Complex Numbers": [
                ("Solve in $\\mathbb{C}$ the quadratic equation $z^2 - 2\\sqrt{3}z + 4 = 0$.", False),
                ("Find the exponential form of $z = -1 + i\\sqrt{3}$.", False),
                ("Determine the nature of triangle with vertices $A(1+i), B(3-i)$.", False),
            ],
            "Derivatives": [
                ("Compute the derivative of $f(x) = (2-x)e^x - 1$ and establish variations.", False),
                ("Find the equation of the tangent line at $x_0 = 1$.", False),
            ],
            "Logarithmic Functions": [
                ("Study the variations and limits of $g(x) = x - 1 + \\ln(x)$ on $]0, +\\infty[$.", False),
                ("Solve the inequality $\\ln(2x - 3) \\le \\ln(x + 5)$.", False),
            ],
            "Exponential Functions": [
                ("Determine the horizontal asymptote of $f(x) = \\frac{e^x}{e^x + 1}$ at $\\pm\\infty$.", False),
                ("Prove that the curve intersects the line $y = x$ at a unique point $\\alpha$.", False),
            ],
            "Integrals": [
                ("Calculate using integration by parts $\\int_1^e x \\ln(x) dx$.", True),
                ("Determine the area between the curves $C_f$ and $C_g$ on $[0, 2]$.", False),
            ],
            "Limits and Continuity": [
                ("Remove the indeterminate form for $\\lim_{x \\to 0} \\frac{\\sqrt{x+1}-1}{x}$.", False),
                ("Apply the Intermediate Value Theorem to show $f(x) = 0$ has a unique root.", False),
            ],
            "Geometry in Space": [
                ("Find the Cartesian equation of the plane passing through $A(1,2,0)$ with normal $\\vec{n}(2,-1,3)$.", False),
                ("Calculate the distance from point $M(3, -1, 2)$ to plane $(P)$.", True),
            ]
        }

        created_at_base = timezone.now() - timedelta(days=25)
        step_idx = 0

        # Seed Tutor Sessions
        for ch in CHAPTERS:
            q_list = sample_questions.get(ch, [("General Bac practice question", False)])
            for q_text, had_mistake in q_list:
                # Probability has lower mastery (around 25%) so more mistakes and lower scores
                if ch == "Probability":
                    had_mistake = True
                step_idx += 1
                session_time = created_at_base + timedelta(hours=step_idx * 14)
                
                res_data = mock_ai.get_mock_tutor_response(chapter=ch, has_attempt=had_mistake)
                
                t_session = TutorSession.objects.create(
                    user=student,
                    chapter=ch,
                    summary=f"Analysis of {ch} Bac question",
                    input_text=q_text,
                    attempt_text="My initial working steps written during revision..." if had_mistake else "",
                    result_json=res_data,
                    had_mistake=had_mistake,
                )
                TutorSession.objects.filter(pk=t_session.pk).update(created_at=session_time)

                # Seed sample message
                TutorMessage.objects.create(
                    session=t_session,
                    role="user",
                    content="Can you clarify why we used this theorem?",
                    created_at=session_time + timedelta(minutes=2)
                )
                TutorMessage.objects.create(
                    session=t_session,
                    role="tutor",
                    content="In Algerian Bac marking schemes, applying the theorem requires verifying continuity and strict monotonicity.",
                    created_at=session_time + timedelta(minutes=3)
                )

        # Seed Practice Exercises & Results (total 40+ history items combined)
        for ch in CHAPTERS:
            # 2 to 3 practice exercises per chapter
            for i in range(3):
                step_idx += 1
                ex_time = created_at_base + timedelta(hours=step_idx * 11)
                
                ex = PracticeExercise.objects.create(
                    user=student,
                    chapter=ch,
                    difficulty="Bac level" if i == 0 else "Medium",
                    question=f"Bac Question on {ch} - Part {i+1}: Study the function and calculate key limits.",
                    hints_json=["Review standard limits in the course summary.", "Use auxiliary relations."],
                    solution="Detailed step-by-step solution according to the national syllabus.",
                )
                PracticeExercise.objects.filter(pk=ex.pk).update(created_at=ex_time)

                # Score varies by chapter to ensure Probability is ~25% and Sequences is high ~85%
                if ch == "Probability":
                    score = random.choice([2.5, 3.0, 3.5])
                elif ch in ("Sequences", "Exponential Functions", "Complex Numbers"):
                    score = random.choice([8.0, 8.5, 9.0, 9.5])
                else:
                    score = random.choice([6.0, 7.0, 7.5])

                res = PracticeResult.objects.create(
                    exercise=ex,
                    user=student,
                    chapter=ch,
                    score=score,
                    feedback=f"Good effort on {ch}. Pay attention to final units and asymptotic behavior.",
                    answer_text="Calculated the derivative, found variations and deduced the sign.",
                )
                PracticeResult.objects.filter(pk=res.pk).update(created_at=ex_time)

        # 5. 4 Past Mock Exams with grades: 9.5, 11, 12.5, 13.5
        past_grades = [9.5, 11.0, 12.5, 13.5]
        for idx, grade in enumerate(past_grades):
            exam_time = today - timedelta(days=(24 - idx * 7))
            exam_data = mock_ai.get_mock_exam()
            exam_grading = mock_ai.get_mock_exam_grading(exam_data, {"1": "answered", "2": "answered"})
            exam_grading["total_grade"] = grade
            
            ex_obj = Exam.objects.create(
                user=student,
                duration_minutes=180,
                exercises_json=exam_data,
                status="submitted",
                total_grade=grade,
                result_json=exam_grading,
            )
            Exam.objects.filter(pk=ex_obj.pk).update(
                started_at=timezone.make_aware(timezone.datetime.combine(exam_time, timezone.datetime.min.time())),
                submitted_at=timezone.make_aware(timezone.datetime.combine(exam_time, timezone.datetime.min.time()) + timedelta(hours=3))
            )

        # 6. Saved Study Plan for Yasmine
        week_start = today - timedelta(days=today.weekday())
        tasks = mock_ai.get_mock_study_plan(["Probability", "Sequences"])
        StudyPlan.objects.create(
            user=student,
            week_start=week_start,
            tasks_json=tasks
        )

        # 7. Other Class Students for Mr. Karim's Class (8 students total)
        other_students_data = [
            ("Amine", "Cherif", "amine.cherif@student.bacly.dz", "Experimental Sciences", 14.5, "Probability"),
            ("Sara", "Boudiaf", "sara.boudiaf@student.bacly.dz", "Mathematics", 16.0, "Geometry in Space"),
            ("Mohamed", "Zitouni", "m.zitouni@student.bacly.dz", "Technical Mathematics", 8.5, "Probability"),
            ("Lina", "Khelifi", "lina.k@student.bacly.dz", "Mathematics", 12.0, "Sequences"),
            ("Bilal", "Meziane", "bilal.m@student.bacly.dz", "Mathematics", 9.0, "Sequences"),
            ("Rania", "Saadi", "rania.s@student.bacly.dz", "Experimental Sciences", 15.5, "Integrals"),
            ("Walid", "Bouzid", "walid.b@student.bacly.dz", "Technical Mathematics", 7.5, "Derivatives"),
        ]

        for first, last, email, stream, avg_score, weakest in other_students_data:
            uname = f"student_{first.lower()}"
            st_obj, _ = User.objects.get_or_create(
                username=uname,
                defaults={
                    "first_name": first,
                    "last_name": last,
                    "email": email,
                    "role": "student",
                    "stream": stream,
                    "bac_date": bac_date,
                    "school_class": school_class,
                }
            )
            st_obj.set_password("demo1234")
            st_obj.save()

            # Seed simple activity and practice to support class stats
            Activity.objects.create(
                user=st_obj,
                date=today - timedelta(days=random.choice([0, 1, 2, 8 if avg_score < 10 else 1])),
                activity_type="practice",
                description="Class revision"
            )

            # Sample practice results for class averages
            p_ex = PracticeExercise.objects.create(
                user=st_obj,
                chapter=weakest,
                difficulty="Medium",
                question=f"Class revision on {weakest}",
                hints_json=["Check lecture notes"],
                solution="Reference solution",
            )
            PracticeResult.objects.create(
                exercise=p_ex,
                user=st_obj,
                chapter=weakest,
                score=avg_score / 2.0,  # convert /20 to /10
                feedback="Good work.",
                answer_text="Student answers."
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Bacly demo accounts & content!"))
        self.stdout.write("Student: demo_student / demo1234")
        self.stdout.write("Teacher: demo_teacher / demo1234")
