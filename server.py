from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)


# ---------------------------------------------------------------------------
# In-memory user state (HW10 spec: app only needs to support one user at a time)
# ---------------------------------------------------------------------------
user_state = {
    "learning_log": [],      # [{timestamp, lesson, action}]
    "quiz_visits": [],       # [{timestamp, question_id}]
    "quiz_answers": {},      # {question_id: {chosen, correct, timestamp}}
    "quiz_score": 0,
    "quiz_total": 0
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
    return render_template('transition.html', t=t)


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
        total_lessons=TOTAL_LESSONS
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

        return render_template(
            'quiz_feedback.html',
            question=question,
            chosen=chosen,
            is_correct=is_correct,
            next_url=next_url,
            question_number=n,
            total_questions=TOTAL_QUESTIONS
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
        echoed_description=echoed_description
    )


@app.route('/quiz/decode')
def quiz_decode():
    return render_template('quiz_decode.html', total_questions=TOTAL_QUESTIONS)


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
        review=review
    )


# Development-only endpoint to inspect what's being recorded on the backend.
@app.route('/debug/state')
def debug_state():
    return jsonify(user_state)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

 
 
