# Chinese Cuisine Menu Decoder
### How to Order Classic Chinese Dishes from an Unfamiliar Menu

An interactive web-based learning module that teaches non-Chinese diners how to
decode English-translated Chinese menu names. Users learn the building blocks
(cooking methods, flavor words, regional styles) in a short lesson, then apply
them in a guided quiz that ends with a real-world ordering scenario.

---

## Course

**UI Design** — Final Project (HW11)

## Team Members

| Name | GitHub | Role |
|------|--------|------|
| Yu Qiu | @DemonRain7 | Quiz Part I — Progressive Decoding (rounds 1 & 2) + shared quiz infrastructure |
| Ray Tang | @LisiruiTang | Learning module — backend |
| Zhonghao Liu | @zeeliu7 | Learning module — frontend |
| Shurong Zhang (Alice) | @alice20030504 | Quiz Part II — Final Scenario · Full UI/UX redesign: home progress tracker, sticky nav, viewport-fit layout system · CSS design system (main.css) — all visual styles, animations, micro-interactions (streak, shake/glow, hook reveal, scenario scene) · App flow restructuring (Home → Hook → Lesson → Quiz → Decode → Scenario → Results) · Decode page two-column layout · Image curation |

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
| `/` | GET | Home — entry shortcuts (Learn-only / Quiz-only) and progress timeline |
| `/learn/<n>` | GET | Lesson page (lessons 1, 2 …); accepts `?mode=learn_only` |
| `/transition/<n>` | GET | Between-lesson transition card with keyboard shortcut (↵ Enter) |
| `/quiz/<n>` | GET / POST | Quiz question `n`; POST submits an answer and returns feedback; accepts `?mode=quiz_only` |
| `/quiz/decode` | GET | Mid-quiz reveal page that decodes 鱼香肉丝 (Fish-Fragrant Shredded Pork) |
| `/quiz/result` | GET | Final score and per-question review; includes "Retake Quiz" button |
| `/quiz/retake/<n>` | GET / POST | Retake a single question without resetting the whole quiz |
| `/quiz/retake-all` | GET | Reset all quiz answers and restart from question 1 |
| `/reset` | GET | Full reset of all user state (answers + learning log) |
| `/debug/state` | GET | Development-only JSON dump of the in-memory user state |

The app is built for a single user at a time — all state lives in an in-memory
`user_state` dict in `server.py`.

---

## Entry Modes

The home page offers three paths, each with its own stepper variant in the nav:

| Mode | Query param | Stepper nodes |
|------|------------|---------------|
| **Full journey** (default) | — | Hook → Lesson 1 → Quiz 1 → Lesson 2 → Quiz 2 → Decode → Final (7 nodes) |
| **Learn-only** | `?mode=learn_only` | Home → Lesson 1 → Lesson 2 (3 nodes) |
| **Quiz-only** | `?mode=quiz_only` | Hook → Quiz 1 → Quiz 2 → Final → Results (5 nodes) |

---

## User Flow

1. **Home** — choose "Start Learning →" (learn-only), "Go to Quiz →" (quiz-only),
   or click any unlocked stage tile to follow the full journey.
2. **Learning** — short lessons on cooking methods and flavor / regional words.
   Press ↵ Enter on transition cards to advance.
3. **Quiz** —
    - **The Hook** (Q1): guess what 鱼香肉丝 actually is.
    - **Part 1 — Progressive Decoding** (Q2, Q3): match a Hunan-style stir-fry
      and a Cantonese steamed fish.
    - **Decode interlude**: the rules behind 鱼香 are revealed.
    - **Part 2 — Final Scenario** (Q4): pick all dishes a spice-averse friend
      should avoid (multi-select).
4. **Result** — final score with a per-question review; tap ↻ Retry on any row
   to redo just that question, or "↺ Retake Quiz" to reset the whole quiz.

---

## Project Structure

```
server.py                # Flask backend (~10 routes, three entry-mode variants)
learningData.json        # Lesson content (cooking methods, flavor words)
static/
  quiz_data.json         # All quiz questions, options, answers, explanations
  main.css               # Shared styles (home, learning, quiz, feedback, result)
  logQuiz.js             # Quiz interaction logic (radio + multi-select)
  logLearning.js         # Learning page interaction logic
  images/                # Dish photos used by the quiz and learning module
templates/
  layout.html            # Base layout (Bootstrap 5 + jQuery via CDN); node stepper nav
  home.html              # Landing page — entry shortcuts + progress timeline
  learning.html          # Lesson page
  transition.html        # Between-lesson transition card (↵ Enter shortcut)
  quiz_question.html     # Quiz question page (radio or checkbox)
  quiz_feedback.html     # Per-question feedback
  quiz_decode.html       # Mid-quiz 鱼香 decode page
  quiz_result.html       # Final score page with full-retake button
```

---

## Data Files

Question and lesson content is **never** hardcoded in HTML.

- `static/quiz_data.json` — list of questions with `id`, `part`, `step`, `dish`,
  `title`, `prompt`, `options[]`, `correct`, `explanation`. Multi-select
  questions set `multi_select: true` and use a list for `correct`.
- `learningData.json` — keyed by lesson number; each lesson holds a title,
  intro copy, table rows (term + meaning), and image references.

To edit quiz content, modify `static/quiz_data.json`. To edit lessons, modify
`learningData.json`. Restart the Flask dev server to pick up changes.
