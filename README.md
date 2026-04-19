# Chinese Cuisine Menu Decoder
### How to Order Classic Chinese Dishes from an Unfamiliar Menu

An interactive web-based learning module that teaches non-Chinese diners how to
decode English-translated Chinese menu names. Users learn the building blocks
(cooking methods, flavor words, regional styles) in a short lesson, then apply
them in a guided quiz that ends with a real-world ordering scenario.

---

## Course

**UI Design** — Final Project (HW10 Technical Prototypes)

## Team Members

| Name | GitHub | Role |
|------|--------|------|
| Yu Qiu | @DemonRain7 | Quiz Part I — Progressive Decoding (rounds 1 & 2) + shared quiz infrastructure |
| Ray Tang | @LisiruiTang | Learning module — backend |
| Zhonghao Liu | — | Learning module — frontend |
| Shurong Zhang (Alice) | @alice20030504 | Quiz Part II — Final Scenario |

**TA:** Max-Zhang63

---

## Getting Started

**Requirements:** Python 3, Flask

```bash
pip install flask
python server.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home — links to the learning module and the quiz |
| `/learn/<n>` | GET | Lesson page (lessons 1, 2 …) |
| `/quiz/<n>` | GET / POST | Quiz question `n`; POST submits an answer and returns feedback |
| `/quiz/decode` | GET | Mid-quiz reveal page that decodes 鱼香肉丝 (Fish-Fragrant Shredded Pork) |
| `/quiz/result` | GET | Final score and per-question review |
| `/debug/state` | GET | Development-only JSON dump of the in-memory user state |

The app is built for a single user at a time (per HW10 spec) — all state lives
in an in-memory `user_state` dict in `server.py`.

---

## User Flow

1. **Home** — pick a starting point (most users go through learning first).
2. **Learning** — short lessons on cooking methods and flavor / regional words.
3. **Quiz** —
    - **The Hook** (Q1): guess what 鱼香肉丝 actually is.
    - **Part 1 — Progressive Decoding** (Q2, Q3): match a Hunan-style stir-fry
      and a Cantonese steamed fish.
    - **Decode interlude**: the rules behind 鱼香 are revealed.
    - **Part 2 — Final Scenario** (Q4): pick all dishes a spice-averse friend
      should avoid (multi-select).
4. **Result** — final score with a per-question review.

---

## Project Structure

```
server.py                # Flask backend (single file, ~6 routes)
learningData.json        # Lesson content (cooking methods, flavor words)
static/
  quiz_data.json         # All quiz questions, options, answers, explanations
  main.css               # Shared styles (home, learning, quiz, feedback, result)
  logQuiz.js             # Quiz interaction logic (radio + multi-select)
  logLearning.js         # Learning page interaction logic
  images/                # Dish photos used by the quiz and learning module
templates/
  layout.html            # Base layout (Bootstrap 5 + jQuery via CDN)
  home.html              # Landing page linking to learning and quiz
  learning.html          # Lesson page
  quiz_question.html     # Quiz question page (radio or checkbox)
  quiz_feedback.html     # Per-question feedback
  quiz_decode.html       # Mid-quiz 鱼香 decode page
  quiz_result.html       # Final score page
```

---

## Data Files

Question and lesson content is **never** hardcoded in HTML (HW10 spec #5).

- `static/quiz_data.json` — list of questions with `id`, `part`, `step`, `dish`,
  `title`, `prompt`, `options[]`, `correct`, `explanation`. Multi-select
  questions set `multi_select: true` and use a list for `correct`.
- `learningData.json` — keyed by lesson number; each lesson holds a title,
  intro copy, table rows (term + meaning), and image references.

To edit quiz content, modify `static/quiz_data.json`. To edit lessons, modify
`learningData.json`. Restart the Flask dev server to pick up changes.
