"""
Realistic Baccalauréat Mathematics Mock AI Service for Bacly.
Provides authentic, curriculum-aligned Algerian Bac math responses
in the exact schemas required when real API calls are unavailable.
"""

MOCK_TUTOR_DATABASE = {
    "Sequences": {
        "chapter": "Sequences",
        "exercise_summary": "Study the convergence of the sequence $(u_n)$ defined by $u_0 = 1$ and $u_{n+1} = \\frac{1}{3}u_n + 2$ for all $n \\in \\mathbb{N}$.",
        "solution_steps": [
            "Step 1: Identify the fixed point $\\alpha$ by solving $\\alpha = \\frac{1}{3}\\alpha + 2 \\implies \\frac{2}{3}\\alpha = 2 \\implies \\alpha = 3$. Define the auxiliary sequence $v_n = u_n - 3$.",
            "Step 2: Prove that $(v_n)$ is geometric: $v_{n+1} = u_{n+1} - 3 = \\left(\\frac{1}{3}u_n + 2\\right) - 3 = \\frac{1}{3}u_n - 1 = \\frac{1}{3}(u_n - 3) = \\frac{1}{3}v_n$. Thus, $(v_n)$ is a geometric sequence with common ratio $q = \\frac{1}{3}$.",
            "Step 3: Calculate the first term: $v_0 = u_0 - 3 = 1 - 3 = -2$.",
            "Step 4: Express $v_n$ and $u_n$ in terms of $n$: $v_n = v_0 \\cdot q^n = -2 \\left(\\frac{1}{3}\\right)^n$. Therefore, $u_n = v_n + 3 = 3 - 2\\left(\\frac{1}{3}\\right)^n$.",
            "Step 5: Determine the limit: Since $-1 < \\frac{1}{3} < 1$, we have $\\lim_{n \\to +\\infty} \\left(\\frac{1}{3}\\right)^n = 0$. Hence, $\\lim_{n \\to +\\infty} u_n = 3 - 0 = 3$. The sequence converges to $3$."
        ],
        "mistake": {
            "step": "Calculation of the initial term $v_0$",
            "explanation": "You calculated $v_0 = u_0 + 3 = 4$, which inverts the sign in the auxiliary relation $v_n = u_n - 3$.",
            "correction": "Substitute carefully: with $v_n = u_n - 3$ and $u_0 = 1$, we have $v_0 = 1 - 3 = -2$."
        },
        "practice": [
            {
                "question": "Given $w_0 = 5$ and $w_{n+1} = \\frac{1}{2}w_n + 3$. Find the fixed point and express $w_n$ in terms of $n$.",
                "answer": "Fixed point is $\\alpha = 6$. Let $t_n = w_n - 6$, then $t_0 = -1$ and $q = \\frac{1}{2}$. $w_n = 6 - \\left(\\frac{1}{2}\\right)^n$, limit is $6$."
            },
            {
                "question": "Prove that the geometric sequence $z_n = 4 \\cdot (0.75)^n$ is strictly decreasing for $n \\ge 0$.",
                "answer": "Since $0 < 0.75 < 1$ and $z_0 = 4 > 0$, $\\frac{z_{n+1}}{z_n} = 0.75 < 1$, so $(z_n)$ is strictly decreasing."
            },
            {
                "question": "Calculate the sum $S_n = v_0 + v_1 + \\dots + v_n$ where $v_n = -2 \\left(\\frac{1}{3}\\right)^n$.",
                "answer": "$S_n = -2 \\cdot \\frac{1 - (1/3)^{n+1}}{1 - 1/3} = -3 \\left(1 - \\left(\\frac{1}{3}\\right)^{n+1}\\right)$."
            }
        ],
        "tip": "In Algerian Bac exam problems with recurrence relations $u_{n+1} = au_n + b$, the auxiliary geometric sequence always allows you to find an explicit closed-form formula in under 4 minutes.",
        "error": None
    },
    "Probability": {
        "chapter": "Probability",
        "exercise_summary": "An urn contains 3 red balls and 5 white balls. Two balls are drawn at random without replacement. Calculate the probability of drawing at least one red ball.",
        "solution_steps": [
            "Step 1: Total number of balls is $N = 3 + 5 = 8$. The total number of outcomes when drawing 2 balls without replacement is $\\binom{8}{2} = \\frac{8 \\times 7}{2} = 28$.",
            "Step 2: Let $E$ be the event 'drawing at least one red ball'. Consider the complementary event $\\bar{E}$: 'drawing zero red balls' (i.e. both are white).",
            "Step 3: The number of favorable outcomes for $\\bar{E}$ is $\\binom{5}{2} = \\frac{5 \\times 4}{2} = 10$.",
            "Step 4: Compute $P(\\bar{E}) = \\frac{10}{28} = \\frac{5}{14}$.",
            "Step 5: Apply the complement rule: $P(E) = 1 - P(\\bar{E}) = 1 - \\frac{5}{14} = \\frac{9}{14} \\approx 0.643$."
        ],
        "mistake": {
            "step": "Counting combinations for the complement",
            "explanation": "You calculated with replacement using $8^2 = 64$ outcomes instead of without replacement $\\binom{8}{2} = 28$.",
            "correction": "The problem states 'without replacement', so use combinations $\\binom{n}{k}$ or conditional product $\\frac{5}{8} \\times \\frac{4}{7} = \\frac{5}{14}$."
        },
        "practice": [
            {
                "question": "If the draw is with replacement, find the probability that both balls are red.",
                "answer": "$P(\\text{both red}) = \\frac{3}{8} \\times \\frac{3}{8} = \\frac{9}{64}$."
            },
            {
                "question": "Calculate the expected value $E(X)$ where $X$ is the random variable counting the number of red balls drawn.",
                "answer": "$E(X) = 2 \\times \\frac{3}{8} = \\frac{3}{4} = 0.75$."
            },
            {
                "question": "Calculate the variance $V(X)$ of the hyper-geometric variable $X$.",
                "answer": "$V(X) = 2 \\times \\frac{3}{8} \\times \\frac{5}{8} \\times \\frac{8-2}{8-1} = \\frac{15}{32} \\times \\frac{6}{7} = \\frac{45}{112} \\approx 0.402$."
            }
        ],
        "tip": "Whenever you see 'at least one' in a Bac probability problem, immediately check whether using the complementary event $1 - P(\\bar{A})$ simplifies the calculations.",
        "error": None
    },
    "Complex Numbers": {
        "chapter": "Complex Numbers",
        "exercise_summary": "Solve in $\\mathbb{C}$ the equation $z^2 - 2\\sqrt{3}z + 4 = 0$ and write the solutions in trigonometric form.",
        "solution_steps": [
            "Step 1: Compute the discriminant: $\\Delta = (-2\\sqrt{3})^2 - 4(1)(4) = 12 - 16 = -4 = (2i)^2$.",
            "Step 2: Since $\\Delta < 0$, there are two conjugate complex solutions: $z_1 = \\frac{2\\sqrt{3} - 2i}{2} = \\sqrt{3} - i$ and $z_2 = \\frac{2\\sqrt{3} + 2i}{2} = \\sqrt{3} + i$.",
            "Step 3: Modulus of $z_1$: $|z_1| = \\sqrt{(\\sqrt{3})^2 + (-1)^2} = \\sqrt{3+1} = 2$.",
            "Step 4: Argument of $z_1$: $\\cos(\\theta) = \\frac{\\sqrt{3}}{2}$ and $\\sin(\\theta) = -\\frac{1}{2}$, so $\\arg(z_1) \\equiv -\\frac{\\pi}{6} \\pmod{2\\pi}$.",
            "Step 5: Trigonometric forms: $z_1 = 2\\left(\\cos\\left(-\\frac{\\pi}{6}\\right) + i\\sin\\left(-\\frac{\\pi}{6}\\right)\\right) = 2e^{-i\\frac{\\pi}{6}}$ and $z_2 = 2e^{i\\frac{\\pi}{6}}$."
        ],
        "mistake": {
            "step": "Determining the argument $\\theta$",
            "explanation": "You wrote $\\arg(z_1) = \\frac{\\pi}{6}$ instead of $-\\frac{\\pi}{6}$, ignoring the negative sign in the imaginary part.",
            "correction": "Because $\\sin(\\theta) = -1/2 < 0$ and $\\cos(\\theta) = \\sqrt{3}/2 > 0$, the angle lies in the fourth quadrant, so $\\theta = -\\pi/6$."
        },
        "practice": [
            {
                "question": "Calculate $(z_2)^{2026}$ and write it in algebraic form.",
                "answer": "$z_2^{2026} = 2^{2026} e^{i \\frac{2026\\pi}{6}} = 2^{2026} e^{i \\frac{1013\\pi}{3}} = 2^{2026} e^{-i \\frac{\\pi}{3}} = 2^{2025}(1 - i\\sqrt{3})$."
            },
            {
                "question": "Identify the nature of the triangle $OAB$ where $A$ has affix $z_1$ and $B$ has affix $z_2$.",
                "answer": "$OA = |z_1| = 2$, $OB = |z_2| = 2$, and $\\angle(\\vec{OA}, \\vec{OB}) = \\frac{\\pi}{3}$. Hence $OAB$ is an equilateral triangle."
            },
            {
                "question": "Find the affix of point $C$ such that $OACB$ is a rhombus.",
                "answer": "$z_C = z_A + z_B = (\\sqrt{3} - i) + (\\sqrt{3} + i) = 2\\sqrt{3}$."
            }
        ],
        "tip": "Remember that if $P(z)$ is a polynomial with real coefficients, non-real roots always appear in conjugate pairs: $z_2 = \\bar{z}_1$.",
        "error": None
    },
    "Basic Algebra": {
        "chapter": "Basic Algebra",
        "exercise_summary": "Solve the linear equation $x + 1 = 0$.",
        "solution_steps": [
            "Step 1: Write the equation: $x + 1 = 0$.",
            "Step 2: Subtract 1 from both sides: $x = -1$.",
            "Step 3: The solution is $x = -1$."
        ],
        "mistake": None,
        "practice": [
            {
                "question": "Solve $x - 5 = 0$.",
                "answer": "$x = 5$."
            },
            {
                "question": "Solve $x + 7 = 0$.",
                "answer": "$x = -7$."
            },
            {
                "question": "Solve $2x = 10$.",
                "answer": "Divide both sides by 2: $x = 5$."
            }
        ],
        "tip": "To solve a linear equation, isolate $x$ by doing the same operation on both sides.",
        "error": None
    }
}


def get_mock_tutor_response(chapter=None, has_attempt=False, is_unreadable=False):
    """Returns a realistic mock tutor response matching the Tutor schema."""
    if is_unreadable:
        return {
            "chapter": "Unknown",
            "exercise_summary": "Unreadable image",
            "solution_steps": [],
            "mistake": None,
            "practice": [],
            "tip": "Ensure good lighting and frame the math equation clearly.",
            "error": "The uploaded image is unreadable or does not contain a clear Baccalauréat mathematics problem. Please retake the photo with good lighting or type the exercise text."
        }

    key = chapter if chapter in MOCK_TUTOR_DATABASE else "Basic Algebra"
    data = dict(MOCK_TUTOR_DATABASE[key])
    # If the user did not provide an attempt, remove the mistake card
    if not has_attempt:
        data["mistake"] = None
    return data


def get_mock_chat_response(message, chapter="Sequences"):
    """Returns a contextual tutor response to follow-up questions."""
    msg_lower = message.lower()
    if "another method" in msg_lower or "alternative" in msg_lower:
        return (
            "Certainly! Another standard method frequently accepted in the Algerian Bac is **Mathematical Induction** (le raisonnement par récurrence):\n\n"
            "1. **Base Case**: For $n = 0$, verify the conjecture $u_0 < 3$ ($1 < 3$, true).\n"
            "2. **Inductive Hypothesis**: Assume $u_k < 3$ for some $k \\ge 0$.\n"
            "3. **Inductive Step**: Show $u_{k+1} < 3$. Since $u_{k+1} = \\frac{1}{3}u_k + 2$, multiplying by $\\frac{1}{3}$ yields $\\frac{1}{3}u_k < 1$, then adding $2$ gives $u_{k+1} < 3$.\n\n"
            "By induction, $u_n < 3$ for all $n \\in \\mathbb{N}$. Combined with monotonicity, this proves convergence by the Monotone Convergence Theorem."
        )
    if "theorem" in msg_lower or "why" in msg_lower:
        return (
            "We applied the **Monotone Convergence Theorem**: Every sequence that is increasing and bounded from above (or decreasing and bounded from below) is convergent in $\\mathbb{R}$.\n\n"
            "In Bac marking criteria, stating both conditions explicitly:\n"
            "- $(u_n)$ is strictly increasing\n"
            "- $(u_n)$ is bounded above by $3$\n"
            "guarantees you full points for the convergence justification."
        )
    return (
        f"Great question! In Algerian Bac problems on **{chapter}**, always make sure to justify each algebraic step and write all intermediate limits clearly.\n\n"
        "Recall that $\\lim_{n \\to +\\infty} q^n = 0$ is valid if and only if $-1 < q < 1$. Do you want to try a similar exercise to test your understanding?"
    )


def get_mock_practice_exercise(chapter="Sequences", difficulty="Bac level"):
    """Returns a generated exercise with hints and solution."""
    if chapter == "Probability":
        return {
            "chapter": chapter,
            "difficulty": difficulty,
            "question": (
                "An urn contains 4 red balls and 6 green balls. Two balls are drawn at random without replacement.\n\n"
                "1. Calculate the probability of drawing two balls of the same color.\n"
                "2. Calculate the probability of drawing two balls of different colors.\n"
                "3. Let X be the number of red balls drawn. Determine the probability law of X."
            ),
            "hints": [
                "Hint 1: Use combinations. Total ways to draw 2 balls from 10 is $\\binom{10}{2} = 45$.",
                "Hint 2: For different colors, use $\\binom{4}{1} \\times \\binom{6}{1}$ for red then green, and $\\binom{6}{1} \\times \\binom{4}{1}$ for green then red."
            ],
            "solution": (
                "**Detailed Solution:**\n\n"
                "1. **Same color:**\n"
                "- Both red: $\\frac{\\binom{4}{2}}{\\binom{10}{2}} = \\frac{6}{45} = \\frac{2}{15}$.\n"
                "- Both green: $\\frac{\\binom{6}{2}}{\\binom{10}{2}} = \\frac{15}{45} = \\frac{1}{3}$.\n"
                "- Total: $\\frac{2}{15} + \\frac{1}{3} = \\frac{2}{15} + \\frac{5}{15} = \\frac{7}{15}$.\n\n"
                "2. **Different colors:**\n"
                "- Red then green: $\\frac{4}{10} \\times \\frac{6}{9} = \\frac{24}{90}$.\n"
                "- Green then red: $\\frac{6}{10} \\times \\frac{4}{9} = \\frac{24}{90}$.\n"
                "- Total: $\\frac{48}{90} = \\frac{8}{15}$.\n\n"
                "3. **Probability law of X:**\n"
                "- $P(X=0) = \\frac{\\binom{6}{2}}{\\binom{10}{2}} = \\frac{15}{45} = \\frac{1}{3}$.\n"
                "- $P(X=1) = \\frac{\\binom{4}{1}\\binom{6}{1}}{\\binom{10}{2}} = \\frac{24}{45} = \\frac{8}{15}$.\n"
                "- $P(X=2) = \\frac{\\binom{4}{2}}{\\binom{10}{2}} = \\frac{6}{45} = \\frac{2}{15}$."
            )
        }

    return {
        "chapter": chapter,
        "difficulty": difficulty,
        "question": (
            f"Consider the function $f$ defined on $\\mathbb{{R}}$ by $f(x) = (2 - x)e^x - 1$.\n\n"
            f"1. Compute $\\lim_{{x \\to -\\infty}} f(x)$ and $\\lim_{{x \\to +\\infty}} f(x)$.\n"
            f"2. Show that for all $x \\in \\mathbb{{R}}$, $f'(x) = (1 - x)e^x$.\n"
            f"3. Set up the table of variations of $f$ on $\\mathbb{{R}}$."
        ),
        "hints": [
            "Hint 1: Expand $(2-x)e^x = 2e^x - xe^x$ and use the standard Bac growth limit $\\lim_{x \\to -\\infty} xe^x = 0$.",
            "Hint 2: Apply the product rule $(uv)' = u'v + uv'$ with $u(x) = 2 - x$ and $v(x) = e^x$."
        ],
        "solution": (
            "**Detailed Solution:**\n\n"
            "1. **Limits:**\n"
            "- At $-\\infty$: $f(x) = 2e^x - xe^x - 1$. Since $\\lim_{x \\to -\\infty} e^x = 0$ and $\\lim_{x \\to -\\infty} xe^x = 0$, we have $\\lim_{x \\to -\\infty} f(x) = -1$.\n"
            "- At $+\\infty$: $\\lim_{x \\to +\\infty} (2-x) = -\\infty$ and $\\lim_{x \\to +\\infty} e^x = +\\infty$. By product, $\\lim_{x \\to +\\infty} f(x) = -\\infty$.\n\n"
            "2. **Derivative:**\n"
            "$f'(x) = (-1)(e^x) + (2 - x)(e^x) = (-1 + 2 - x)e^x = (1 - x)e^x$.\n\n"
            "3. **Variations:**\n"
            "Since $e^x > 0$ for all $x$, the sign of $f'(x)$ is that of $1 - x$. Thus $f'(x) > 0$ for $x < 1$ (strictly increasing) and $f'(x) < 0$ for $x > 1$ (strictly decreasing). Maximum value at $x = 1$ is $f(1) = e - 1 \\approx 1.718$."
        )
    }


def get_mock_practice_grade(answer_text):
    """Grades student practice answer out of 10."""
    length = len(answer_text.strip()) if answer_text else 0
    if length > 50:
        score = 8.5
        feedback = (
            "**Excellent work!** (Score: 8.5/10)\n\n"
            "- Limits at $-\\infty$ correctly used $\\lim xe^x = 0$.\n"
            "- Product differentiation was executed properly without sign mistakes.\n"
            "- *Minor note for Bac criteria:* Remember to explicitly state the horizontal asymptote $y = -1$ at $-\\infty$ when asked in Bac exams."
        )
    elif length > 15:
        score = 6.0
        feedback = (
            "**Good attempt!** (Score: 6.0/10)\n\n"
            "- You identified the correct form of the derivative $(1-x)e^x$.\n"
            "- *Needs improvement:* The justification of the limit at $-\\infty$ was incomplete. Make sure to detail the indeterminate form removal using standard growth comparison theorems."
        )
    else:
        score = 4.0
        feedback = (
            "**Partial solution.** (Score: 4.0/10)\n\n"
            "- You started in the right direction, but key justification steps are missing.\n"
            "- Review the full solution below to see how to structure your answers for the Bac corrector."
        )
    return {"score": score, "feedback": feedback}


def get_mock_exam(duration_minutes=180):
    """Returns a full 4-exercise Baccalauréat Mathematics mock exam."""
    return [
        {
            "id": 1,
            "chapter": "Sequences",
            "points": 4.5,
            "title": "Exercise 1: Numerical Sequences & Auxiliary Relations",
            "question": (
                "Let $(u_n)$ be defined by $u_0 = 1$ and $u_{n+1} = \\frac{2u_n + 3}{u_n + 4}$ for all $n \\in \\mathbb{N}$.\n\n"
                "1. Prove by induction that for all $n \\in \\mathbb{N}$, $0 < u_n < 1$.\n"
                "2. Show that the auxiliary sequence $v_n = \\frac{u_n - 1}{u_n + 3}$ is geometric with common ratio $q = \\frac{1}{5}$.\n"
                "3. Express $v_n$ then $u_n$ in terms of $n$, and calculate $\\lim_{n \\to +\\infty} u_n$."
            ),
            "solution": "1. Induction proof: base case $0 < 1 < 1$ true. Inductive step: $u_{n+1} - 1 = \\frac{u_n-1}{u_n+4} < 0$. 2. $v_{n+1} = \\frac{1}{5}v_n$. 3. $v_n = -\\frac{1}{2}(1/5)^n$, $u_n = \\frac{1 + 3v_n}{1 - v_n} \\to 1$."
        },
        {
            "id": 2,
            "chapter": "Complex Numbers",
            "points": 5.0,
            "title": "Exercise 2: Complex Plane & Similitudes",
            "question": (
                "In the complex plane referred to an orthonormal direct frame $(O; \\vec{u}, \\vec{v})$:\n\n"
                "1. Solve in $\\mathbb{C}$ the equation: $z^2 - 4z + 8 = 0$.\n"
                "2. Let $A$ and $B$ have affixes $z_A = 2 + 2i$ and $z_B = 2 - 2i$.\n"
                "   a) Write $z_A$ and $z_B$ in exponential form.\n"
                "   b) Determine the nature of the triangle $OAB$."
            ),
            "solution": "1. $\\Delta = -16 = (4i)^2$, roots $z = 2 \\pm 2i$. 2. a) $z_A = 2\\sqrt{2}e^{i\\pi/4}$, $z_B = 2\\sqrt{2}e^{-i\\pi/4}$. b) Isosceles right-angled triangle at $O$."
        },
        {
            "id": 3,
            "chapter": "Probability",
            "points": 4.0,
            "title": "Exercise 3: Discrete Random Variables & Trees",
            "question": (
                "A box contains 4 red balls and 6 green balls. Two draws are performed without replacement.\n\n"
                "1. Represent the situation with a weighted probability tree.\n"
                "2. Calculate the probability of obtaining two balls of different colors.\n"
                "3. Let $X$ be the number of red balls obtained. Determine the probability law of $X$ and compute $E(X)$."
            ),
            "solution": "1. Weighted tree. 2. $P(\\text{different}) = \\frac{4}{10} \\times \\frac{6}{9} + \\frac{6}{10} \\times \\frac{4}{9} = \\frac{48}{90} = \\frac{8}{15}$. 3. $P(X=0)=1/3, P(X=1)=8/15, P(X=2)=2/15, E(X)=0.8$."
        },
        {
            "id": 4,
            "chapter": "Exponential Functions",
            "points": 6.5,
            "title": "Exercise 4: Analysis of an Exponential Function",
            "question": (
                "Let $g(x) = (x - 1)e^{-x} + 1$ defined on $\\mathbb{R}$.\n\n"
                "1. Determine the limits of $g$ at $-\\infty$ and $+\\infty$.\n"
                "2. Calculate $g'(x)$ and construct the table of variations.\n"
                "3. Deduce the sign of $g(x)$ for all $x \\in \\mathbb{R}$.\n"
                "4. Let $f(x) = x + 1 - (x + 2)e^{-x}$. Show that $f'(x) = g(x)$ and conclude the variations of $f$."
            ),
            "solution": "1. $\\lim_{-\\infty} g = -\\infty$, $\\lim_{+\\infty} g = 1$. 2. $g'(x) = (2-x)e^{-x}$, maximum at $x=2$ with $g(2) = e^{-2}+1 > 0$. 3. $g(x) > 0$ for $x > \\alpha \\approx 0.3$. 4. $f'(x) = 1 - (e^{-x} - (x+2)e^{-x}) = 1 + (x+1)e^{-x} = g(x)$."
        }
    ]


def get_mock_exam_grading(exercises, answers):
    """Grades submitted mock exam exercises out of 20."""
    total_grade = 0.0
    grades = []
    for ex in exercises:
        ex_id = str(ex["id"])
        ans = answers.get(ex_id, "").strip()
        max_pts = ex["points"]
        if len(ans) > 40:
            obtained = round(max_pts * 0.85, 2)
            comment = "Clear argumentation, correct mathematical formulation."
        elif len(ans) > 10:
            obtained = round(max_pts * 0.60, 2)
            comment = "Partially answered; some justifications omitted."
        else:
            obtained = round(max_pts * 0.25, 2)
            comment = "Incomplete response. Key formulas missing."
        total_grade += obtained
        grades.append({
            "id": ex["id"],
            "title": ex["title"],
            "chapter": ex["chapter"],
            "max_points": max_pts,
            "obtained_points": obtained,
            "comment": comment
        })

    total_grade = round(min(20.0, max(0.0, total_grade)), 2)

    return {
        "total_grade": total_grade,
        "grades": grades,
        "strengths": [
            "Strong grasp of complex number equations and exponential forms.",
            "Accurate derivation steps in exponential function analysis.",
            "Solid induction proof structure in Sequences."
        ],
        "weaknesses": [
            "Remember to write the full asymptote justification ($y = ax + b$).",
            "Be cautious when computing probabilities without replacement vs with replacement."
        ]
    }


def get_mock_study_plan(weakest_chapters):
    """Generates a 7-day study plan tailored to student's weakest chapters."""
    primary = weakest_chapters[0] if weakest_chapters else "Probability"
    secondary = weakest_chapters[1] if len(weakest_chapters) > 1 else "Sequences"

    return [
        {"id": 1, "day": "Monday", "chapter": primary, "text": f"Review core theory & definitions of {primary} (30 mins)", "done": True},
        {"id": 2, "day": "Tuesday", "chapter": primary, "text": f"Solve 3 practice exercises on {primary} without looking at hints", "done": True},
        {"id": 3, "day": "Wednesday", "chapter": secondary, "text": f"Re-solve missed problems from past Bac exams on {secondary}", "done": False},
        {"id": 4, "day": "Thursday", "chapter": secondary, "text": f"Ask Bacly Tutor for step-by-step breakdown of 1 complex {secondary} exercise", "done": False},
        {"id": 5, "day": "Friday", "chapter": "Derivatives", "text": "Quick 15-minute speed drill on function variation tables", "done": False},
        {"id": 6, "day": "Saturday", "chapter": "Full Exam", "text": "Take a 2-hour timed Mock Exam on Bacly under realistic conditions", "done": False},
        {"id": 7, "day": "Sunday", "chapter": "Review", "text": "Analyze exam corrections, strengths, and update your focus chapters", "done": False},
    ]
