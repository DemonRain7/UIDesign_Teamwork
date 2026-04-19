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
            'with a Start button.</p>'
            '<p><a href="/quiz/1">Jump to Quiz (owned by Yu Qiu / Alice)</a></p>')

@app.route('/learn/<int:n>')
def learn(n):
    user_state["learning_log"].append({
        "timestamp": datetime.now().isoformat(),
        "lesson": n,
        "action": "visit"
    })
    return render_template('learning.html', lesson_number=n)
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
