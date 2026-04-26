from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)


def nav_ctx(jump=None):
    """Return top-nav context vars for non-home pages.

    `jump` is an optional ('source', n) tuple that drives the persistent
    Learning ↔ Quiz cross-section button the TA asked us to add. The button
    appears on every page except the main menu.
    """
    total = 6
    done = sum([
        1 in user_state['quiz_answers'],           # Hook
        any(l['lesson'] == 1 for l in user_state['learning_log']),  # Lesson 1
        2 in user_state['quiz_answers'],           # Quiz 1
        any(l['lesson'] == 2 for l in user_state['learning_log']),  # Lesson 2
        3 in user_state['quiz_answers'],           # Quiz 2
        4 in user_state['quiz_answers'],           # Final
    ])
    ctx = {
        "show_home_nav": True,
        "nav_progress": round(done / total * 100),
        "nav_label": f"{done} / {total} stages",
        "jump_url": None,
        "jump_label": None,
    }
    if jump is not None:
        source, n = jump
        if source == 'quiz':
            # The hook (n=1) runs BEFORE any lesson, so "Review" is the wrong
            # verb — it's a forward jump, not a review. Quiz 2+ has a relevant
            # lesson to review.
            if n == 1:
                ctx["jump_url"] = url_for('learn', n=1)
                ctx["jump_label"] = "→ Skip to Lesson 1"
            elif n == 2:
                ctx["jump_url"] = url_for('learn', n=1)
                ctx["jump_label"] = "↔ Review Lesson 1"
            else:
                ctx["jump_url"] = url_for('learn', n=2)
                ctx["jump_label"] = "↔ Review Lesson 2"
        elif source == 'learn':
            target = 2 if n == 1 else 3   # learn/1 → Quiz 1 (q2); learn/2 → Quiz 2 (q3)
            ctx["jump_url"] = url_for('quiz', n=target)
            ctx["jump_label"] = f"↔ Skip to Quiz {n}"
        elif source == 'decode':
            ctx["jump_url"] = url_for('learn', n=2)
            ctx["jump_label"] = "↔ Review Lesson 2"
        elif source == 'transition':
            ctx["jump_url"] = url_for('learn', n=n)
            ctx["jump_label"] = f"↔ Review Lesson {n}"
        elif source == 'result':
            ctx["jump_url"] = url_for('learn', n=1)
            ctx["jump_label"] = "↔ Back to Learning"
    return ctx


# ---------------------------------------------------------------------------
# In-memory user state (HW10 spec: app only needs to support one user at a time)
# ---------------------------------------------------------------------------
user_state = {
    "learning_log": [],      # [{timestamp, lesson, action}]
    "quiz_visits": [],       # [{timestamp, question_id}]
    "quiz_answers": {},      # {question_id: {chosen, correct, timestamp}}
    "quiz_score": 0,
    "quiz_total": 0,
    "streak": 0,
    "retake_target": None,   # set when the user is retaking a single question;
                             # after they re-submit it we send them back to results.
}

# Each quiz question now declares its own `rules[]` directly inside
# static/quiz_data.json — see the "rules" arrays. The feedback page renders
# one Review-this-rule pill per entry. Hook (id=1) has rules=[] on purpose:
# the user hasn't seen a lesson yet, so there's no rule to review.

# After answering question N, where does the "Continue" button send the user?
# Each tuple is (button_label, hint_subtitle). Phrased as the destination so
# users aren't surprised when "Next →" actually goes to a Lesson page.
NEXT_LABELS = {
    1: ("Continue to Lesson 1 →", "Cooking Methods = Texture"),
    2: ("Continue to Lesson 2 →", "Flavor Words = Taste Preview"),
    3: ("Continue to Decode Reveal →", "鱼香肉丝 — Full Breakdown"),
    4: ("See My Results →", "Your Final Score"),
}


def load_quiz_data():
    path = os.path.join(app.static_folder, 'quiz_data.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_quiz_data():
    return load_quiz_data()

QUIZ_DATA = get_quiz_data()
TOTAL_QUESTIONS = len(QUIZ_DATA['questions'])


def load_learning_data():
    path = os.path.join(app.root_path, 'learningData.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


LEARNING_DATA = load_learning_data()
TOTAL_LESSONS = len(LEARNING_DATA)


def get_question(n):
    for q in QUIZ_DATA['questions']:
        if q['id'] == n:
            return q
    return None

# ===========================================================================
# HOME + LEARNING ROUTES
# Owner: Ray Tang (backend) and Zhonghao Liu (frontend)
# These stubs exist so the app runs end-to-end while the learning team builds
# their pages. Replace the stub bodies, not the route signatures.
# ===========================================================================
TRANSITIONS = {
    1: {
        "badge": "Lesson 1 Complete",
        "title": "You can now read texture from a menu.",
        "body": "Stir-fried, braised, steamed — each cooking word is a texture promise before the food arrives. You've unlocked the first decoding layer.",
        "recap": [
            ("爆炒 Stir-fried", "Quick wok-toss → charred edges, high heat"),
            ("炖 Braised", "Slow-cooked → fall-apart tender, rich liquid"),
            ("蒸 Steamed", "Gentle moist heat → light, clean natural taste"),
        ],
        "bridge": "But knowing the cooking method is only half the story. What does 'Hunan-style' actually mean for your taste buds?",
        "tease": "Quiz 1: Can you identify a Hunan-style stir-fried dish from a lineup of four beef preparations?",
        "cta": "Take Quiz 1 →",
        "next_url": "/quiz/2"
    },
    2: {
        "badge": "Lesson 2 Complete",
        "title": "You decoded 'stir-fried' in Quiz 1 — now for the tricky part.",
        "body": "You aced the cooking method. Lesson 2 gave you the flavor layer — regional styles and taste words that preview what you'll experience.",
        "recap": [
            ("湘 Hunan-style", "Chili heat, smoky, garlicky — dry and direct"),
            ("粤 Cantonese", "Light, fresh, ingredient-forward — minimal seasoning"),
            ("鱼香 Yu-xiang", "No fish! Sweet-sour-savory sauce with pickled chili"),
        ],
        "bridge": "You decoded 'stir-fried' from Lesson 1 — but how did you know '鱼香' means no fish? That's what Lesson 2 just gave you.",
        "tease": "Quiz 2: Does '鱼香肉丝' (Fish-Fragrant Shredded Pork) actually contain fish? Only one way to find out.",
        "cta": "Take Quiz 2 →",
        "next_url": "/quiz/1"
    }
}


@app.route('/transition/<int:n>')
def transition(n):
    t = TRANSITIONS.get(n)
    if not t:
        return redirect(url_for('home'))
    return render_template('transition.html', t=t, **nav_ctx(jump=('transition', n)))


@app.route('/')
def home():
    def lesson_visited(n):
        return any(l['lesson'] == n for l in user_state['learning_log'])

    stages = [
        {
            "number": 1, "label": "Hook",
            "title": "Can You Guess This Dish?",
            "desc": "A mystery dish name to spark your curiosity before the learning begins.",
            "url": "/quiz/1",
            "done": 1 in user_state['quiz_answers']
        },
        {
            "number": 2, "label": "Lesson 1",
            "title": "Cooking Methods = Texture",
            "desc": "Learn how technique words predict texture before the food arrives.",
            "url": url_for('learn', n=1),
            "done": lesson_visited(1)
        },
        {
            "number": 3, "label": "Quiz 1",
            "title": "Spot the Hunan Stir-fry",
            "desc": "Apply your texture knowledge: identify a dish from its cooking clues.",
            "url": "/quiz/2",
            "done": 2 in user_state['quiz_answers']
        },
        {
            "number": 4, "label": "Lesson 2",
            "title": "Flavor Words = Taste Preview",
            "desc": "Regional styles and flavor words that tell you exactly what you'll taste.",
            "url": url_for('learn', n=2),
            "done": lesson_visited(2)
        },
        {
            "number": 5, "label": "Quiz 2",
            "title": "Decode Cantonese Steamed Fish",
            "desc": "Combine cooking method + regional style to identify the right dish.",
            "url": "/quiz/3",
            "done": 3 in user_state['quiz_answers']
        },
        {
            "number": 6, "label": "Final Challenge",
            "title": "Decode & Order for a Friend",
            "desc": "Full decode reveal, then protect your spice-averse friend with what you've learned.",
            "url": "/quiz/decode",
            "done": 4 in user_state['quiz_answers']
        },
    ]
    found_active = False
    for s in stages:
        if s['done']:
            s['status'] = 'done'
        elif not found_active:
            s['status'] = 'active'
            found_active = True
        else:
            s['status'] = 'upcoming'

    next_stage = next((s for s in stages if not s['done']), None)
    all_done = next_stage is None
    return render_template('home.html', stages=stages, next_stage=next_stage, all_done=all_done)

@app.route('/learn/<int:n>')
def learn(n):
    lesson = LEARNING_DATA.get(str(n))
    if lesson is None:
        return redirect(url_for('home'))
    user_state["learning_log"].append({
        "timestamp": datetime.now().isoformat(),
        "lesson": n,
        "action": "visit"
    })
    return render_template(
        'learning.html',
        lesson=lesson,
        lesson_number=n,
        total_lessons=TOTAL_LESSONS,
        **nav_ctx(jump=('learn', n))
    )
# ===========================================================================
# QUIZ ROUTES
# Part 1 (Progressive Decoding, rounds 1 & 2) — Yu Qiu
# Part 2 (Scenario Question)                  — Alice (Shurong Zhang)
# Shared quiz infrastructure (routes, JSON schema, scoring, feedback page,
# final result page) is scaffolded by Yu Qiu so Alice can refine Part 2's
# copy, styling, and additional scenarios on top of it.
# ===========================================================================
@app.route('/quiz/<int:n>', methods=['GET', 'POST'])
def quiz(n):
    question = get_question(n)
    if question is None:
        return redirect(url_for('quiz_result'))

    if request.method == 'POST':
        if question.get('multi_select'):
            chosen = sorted(request.form.getlist('answer'))
            correct = sorted(question['correct']) if isinstance(question['correct'], list) else [question['correct']]
            is_correct = (chosen == correct)
        else:
            chosen = request.form.get('answer')
            is_correct = (chosen == question['correct'])

        user_state['quiz_answers'][n] = {
            'chosen': chosen,
            'correct': is_correct,
            'timestamp': datetime.now().isoformat()
        }
        user_state['quiz_score'] = sum(
            1 for a in user_state['quiz_answers'].values() if a['correct']
        )
        user_state['quiz_total'] = TOTAL_QUESTIONS
        if is_correct:
            user_state['streak'] += 1
        else:
            user_state['streak'] = 0
        current_streak = user_state['streak']

        if n == 1:
            # Hook done → go to Lesson 1
            next_url = url_for('learn', n=1)
        elif n == 2:
            # Quiz 1 done → go to Lesson 2
            next_url = url_for('learn', n=2)
        elif n == 3:
            # Quiz 2b done → decode reveal
            next_url = url_for('quiz_decode')
        else:
            next_n = n + 1
            next_url = url_for('quiz', n=next_n) if next_n <= TOTAL_QUESTIONS else url_for('quiz_result')

        # If the user came in via "Retry this question" from the result page,
        # short-circuit the normal forward flow and send them back to results.
        is_retake = (user_state.get('retake_target') == n)
        if is_retake:
            user_state['retake_target'] = None
            next_url = url_for('quiz_result')
            next_label = ("← Back to Results", "Return to your score breakdown")
        else:
            next_label = NEXT_LABELS.get(n, ("Continue →", ""))

        # Wrong-answer "Review this rule" pills. Each rule entry on the
        # question (declared in quiz_data.json) becomes a deep-link of the
        # form /learn/<lesson>?highlight=<rule_key>, so the lesson page
        # auto-scrolls to the exact row. Hook (id=1) has rules=[] so nothing
        # renders for it.
        review_pills = [
            {
                "lesson": r["lesson"],
                "rule_label": r["rule_label"],
                "url": url_for('learn', n=r["lesson"]),
            }
            for r in question.get("rules", [])
        ]
        return render_template(
            'quiz_feedback.html',
            question=question,
            chosen=chosen,
            is_correct=is_correct,
            next_url=next_url,
            question_number=n,
            total_questions=TOTAL_QUESTIONS,
            streak=current_streak,
            next_label=next_label,
            review_pills=review_pills,
            is_retake=is_retake,
            **nav_ctx(jump=('quiz', n))
        )

    # GET — record a visit and render the question.
    user_state['quiz_visits'].append({
        "timestamp": datetime.now().isoformat(),
        "question_id": n
    })

    # On image-matching steps, echo back the description the user chose in
    # the previous step. This is the concrete fix from HW9 user testing.
    echoed_description = None
    if question.get('echo_previous_description'):
        prev_id = question['echo_previous_description']
        prev = user_state['quiz_answers'].get(prev_id)
        if prev is not None:
            prev_q = get_question(prev_id)
            for opt in prev_q['options']:
                if opt['key'] == prev['chosen']:
                    echoed_description = opt['text']
                    break

    return render_template(
        'quiz_question.html',
        question=question,
        question_number=n,
        total_questions=TOTAL_QUESTIONS,
        echoed_description=echoed_description,
        **nav_ctx(jump=('quiz', n))
    )


@app.route('/quiz/decode')
def quiz_decode():
    return render_template('quiz_decode.html', total_questions=TOTAL_QUESTIONS, **nav_ctx(jump=('decode', None)))


@app.route('/quiz/result')
def quiz_result():
    review = []
    for q in QUIZ_DATA['questions']:
        ans = user_state['quiz_answers'].get(q['id'])
        review.append({
            'question': q,
            'chosen': ans['chosen'] if ans else None,
            'correct': ans['correct'] if ans else False
        })
    return render_template(
        'quiz_result.html',
        score=user_state['quiz_score'],
        total=TOTAL_QUESTIONS,
        review=review,
        **nav_ctx(jump=('result', None))
    )


@app.route('/quiz/retake/<int:n>', methods=['GET', 'POST'])
def quiz_retake(n):
    """Per-question retake: clear just question n's recorded answer, recompute
    the score, mark `retake_target` so the next POST on /quiz/n bounces back
    to the result page (instead of advancing to question n+1), then redirect
    to the question itself.
    """
    if n not in user_state['quiz_answers'] and get_question(n) is None:
        return redirect(url_for('quiz_result'))
    user_state['quiz_answers'].pop(n, None)
    user_state['quiz_score'] = sum(
        1 for a in user_state['quiz_answers'].values() if a['correct']
    )
    user_state['streak'] = 0
    user_state['retake_target'] = n
    return redirect(url_for('quiz', n=n))


# Development-only endpoint to inspect what's being recorded on the backend.
@app.route('/debug/state')
def debug_state():
    return jsonify(user_state)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

 
 
