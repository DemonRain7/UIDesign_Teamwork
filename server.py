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


QUIZ_DATA = load_quiz_data()
TOTAL_QUESTIONS = len(QUIZ_DATA['questions'])


def get_question(n):
    for q in QUIZ_DATA['questions']:
        if q['id'] == n:
            return q
    return None

# ---------------------------------------------------------------------------
# Learning content data (lives on the server, not in static)
# ---------------------------------------------------------------------------
LEARNING_CONTENTS = {
    1: {
        "title": "Cooking Methods = Texture",
        "beginning": "The cooking method tells you exactly what texture to expect before the food arrives.",
        "table": json.dumps([
            {"Cooking Method": "Stir-fried", "Chinese": "爆炒", "Texture Outcome": "Savory, quick wok toss, lightly charred"},
            {"Cooking Method": "Braised", "Chinese": "炖", "Texture Outcome": "Fall-apart tender, rich in liquid"},
            {"Cooking Method": "Smoked", "Chinese": "熏", "Texture Outcome": "Deep, earthy, smoky complexity"},
            {"Cooking Method": "Steamed", "Chinese": "蒸", "Texture Outcome": "Light, tender, clean natural taste"},
            {"Cooking Method": "Qing-chao (Light)", "Chinese": "清炒", "Texture Outcome": "Fresh, bright, crisp — minimal seasoning"},
            {"Cooking Method": "Deep-fried", "Chinese": "炸", "Texture Outcome": "Crispy golden outside, tender inside"}
        ]),
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/5/52/Ginger_chicken_%283168342551%29.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Red_braised_pork_%2820141106191221%29.JPG/1920px-Red_braised_pork_%2820141106191221%29.JPG",
            "https://upload.wikimedia.org/wikipedia/commons/d/d0/Ipomoea_stir_fry.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/9/95/CantoneseSteamedfish.jpg"
        ]
    },
    2: {
        "title": "Flavor & Style Words = Taste Preview",
        "beginning": "These words in a dish name are a preview of what your taste buds will experience.",
        "table": json.dumps([
            {"Flavor/Style Word": "Hunan-style", "Chinese": "湘", "Taste Outcome": "Intensely spicy, smoky, garlicky. Direct chili heat — no numbing. Dry and fragrant."},
            {"Flavor/Style Word": "Cantonese-style", "Chinese": "粤", "Taste Outcome": "Light, fresh, ingredient-forward. Minimal seasoning; clean and elegant."},
            {"Flavor/Style Word": "Mala / Numbing-Spicy", "Chinese": "麻辣", "Taste Outcome": "Ma (麻) = numbing from peppercorn + La (辣) = chili burn. Layered and electric."},
            {"Flavor/Style Word": "Yu-xiang / \"Fish-Fragrant\"", "Chinese": "鱼香", "Taste Outcome": "Contains NO fish. Sweet-sour-savory-spicy sauce (garlic, pickled chili, vinegar)."}
        ]),
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Saut%C3%A9ed_pork_with_chili_pepper_at_Yinxiang_Restaurant_%2820210522180012%29.jpg/1920px-Saut%C3%A9ed_pork_with_chili_pepper_at_Yinxiang_Restaurant_%2820210522180012%29.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Har_gow_served_at_a_Chinese_restaurant_in_the_Sunset_District_of_SF.jpg/1920px-Har_gow_served_at_a_Chinese_restaurant_in_the_Sunset_District_of_SF.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Homemade_Hotpot.jpg/960px-Homemade_Hotpot.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Qiezi.jpg/1920px-Qiezi.jpg"
        ]
    }
}

# ---------------------------------------------------------------------------
# API endpoint — frontend fetches learning data via AJAX
# ---------------------------------------------------------------------------
@app.route('/api/learn/<int:n>')
def api_learn(n):
    contents = LEARNING_CONTENTS.get(n)
    if contents is None:
        return jsonify({"error": "Lesson not found"}), 404
    return jsonify(contents)


# ===========================================================================
# HOME + LEARNING ROUTES
# Owner: Ray Tang (backend) and Zhonghao Liu (frontend)
# These stubs exist so the app runs end-to-end while the learning team builds
# their pages. Replace the stub bodies, not the route signatures.
# ===========================================================================
@app.route('/')
def home():
    return ('<h2>Home (stub)</h2>'
            '<p>Placeholder until the learning team implements the home page '
            'home.html'
            'with a Start button.</p>'
            '<p><a href="/quiz/1">Jump to Quiz (owned by Yu Qiu / Alice)</a></p>')


@app.route('/learn/<int:n>')
def learn(n):
    user_state["learning_log"].append({
        "timestamp": datetime.now().isoformat(),
        "lesson": n,
        "action": "visit"
    })
    return f'<h2>Learning Page {n} (stub)</h2><p>Owned by the learning team.</p>'


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

        next_n = n + 1
        next_url = (url_for('quiz', n=next_n)
                    if next_n <= TOTAL_QUESTIONS
                    else url_for('quiz_result'))

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
