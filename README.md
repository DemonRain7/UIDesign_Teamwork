# Chinese Cuisine Menu Decoder
### How to Order Classic Chinese Dishes from an Unfamiliar Menu

An interactive web-based learning module that teaches non-Chinese diners how to
decode English-translated Chinese menu names. Users learn the building blocks
(cooking methods, flavor words, regional styles) in short lessons, then apply
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
| Shurong Zhang (Alice) | @alice20030504 | Quiz Part II — Final Scenario · Full UI/UX redesign: home progress tracker, sticky nav, viewport-fit layout system · CSS design system (main.css) — all visual styles, animations, micro-interactions · App flow restructuring · Interaction-state visual polish (selected / correct / incorrect / locked states) · Retake flow signaling (gold ribbon + eyebrow) · Clickable stepper navigation · Decode page two-column layout · Cross-page spacing audit |

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
| `/learn/<n>` | GET | Lesson page (lessons 1, 2); accepts `?mode=learn_only` |
| `/transition/<n>` | GET | Between-lesson transition card |
| `/quiz/<n>` | GET / POST | Quiz question `n`; POST submits and returns feedback; accepts `?mode=quiz_only` |
| `/quiz/decode` | GET | Mid-quiz reveal page that decodes 鱼香肉丝 |
| `/quiz/result` | GET | Final score and per-question review |
| `/quiz/retake/<n>` | GET / POST | Retake a single question without resetting the whole quiz |
| `/quiz/retake-all` | GET | Reset all quiz answers and restart from question 1 |
| `/reset` | GET | Full reset of all user state (answers + learning log) |
| `/debug/state` | GET | Development-only JSON dump of in-memory user state |

All state lives in an in-memory `user_state` dict in `server.py` — the app supports one user at a time.

---

## Entry Modes

| Mode | Query param | Stepper nodes |
|------|-------------|---------------|
| **Full journey** (default) | — | Hook → Lesson 1 → Quiz 1 → Lesson 2 → Quiz 2 → Decode → Final |
| **Learn-only** | `?mode=learn_only` | Home → Lesson 1 → Lesson 2 |
| **Quiz-only** | `?mode=quiz_only` | Hook → Quiz 1 → Quiz 2 → Final → Results |

Completed stepper nodes are clickable — they link back to that stage without clearing progress.

---

## User Flow

1. **Home** — choose "Start Learning →" (learn-only), "Go to Quiz →" (quiz-only),
   or click any unlocked stage tile to follow the full journey.
2. **Learning** — short lessons on cooking methods and flavor / regional words.
   Arrow keys browse table rows; ↵ Enter advances to the next page.
3. **Quiz** —
   - **The Hook** (Q1): guess what 鱼香肉丝 actually is.
   - **Part 1 — Progressive Decoding** (Q2, Q3): match a Hunan-style stir-fry and a Cantonese steamed fish.
   - **Decode interlude**: the full breakdown of 鱼香肉丝 is revealed.
   - **Part 2 — Final Scenario** (Q4): multi-select — pick all dishes a spice-averse friend must avoid.
4. **Result** — final score with per-question review; tap ↻ Retry on any row to redo just that question, or "↺ Retake Quiz" to reset everything.

---

## Visual Design System

All styles live in `static/main.css`. Key design tokens:

| Token | Value | Usage |
|-------|-------|-------|
| Accent gold | `#C8932B` | Primary CTAs, selected state, borders |
| Dark navy | `#1F2A3D` | Secondary buttons, table header, vibe block |
| Warm cream | `#F0EAD6` | Page background |
| Card white | `#FAFAF8` / `#fff` | Card surfaces |

### Option-card interaction states

| Class | Visual treatment |
|-------|-----------------|
| *(default)* | Neutral border `#E8E2D0`, cream background |
| `.selected` | Double gold ring (2px solid + 5px rgba halo + inset warmth) |
| `.correct` | Gold border ring, warm tint, gold ✓ chip (top-right corner) |
| `.incorrect` | Red border ring, red tint, red ✗ chip (top-right corner) |
| `.neutral` | 42% opacity + 35% grayscale (unselected options on feedback page) |

Feedback page renders all 4 options with their states so the user can see every choice in context.

### Locked stage cards (Home)

Upcoming stages use `grayscale(70%) saturate(0.4)` + `pointer-events: none` to signal they are not yet reachable.

### Retake mode

When a user retakes a single question from the result page:
- A full-width **gold gradient ribbon** bleeds across the top of the quiz card.
- A small **"↻ Retake" eyebrow pill** appears above the question title.
- Both the question page and the feedback page show a direct "← Back to Results" link in the ribbon.

---

## Project Structure

```
server.py                # Flask backend — routes, user_state, nav_ctx()
learningData.json        # Lesson content (cooking methods, flavor words)
static/
  quiz_data.json         # Quiz questions, options, answers, explanations
  main.css               # All shared styles
  logQuiz.js             # Quiz interaction (radio, multi-select, keyboard shortcuts)
  logLearning.js         # Learning page (table render, image card, arrow-key nav)
  images/                # Dish photos used by quiz and learning module
templates/
  layout.html            # Base layout — Bootstrap 5 + jQuery; clickable stepper nav
  home.html              # Landing page — entry shortcuts + progress timeline
  learning.html          # Lesson page (lesson-N class for per-lesson CSS targeting)
  transition.html        # Between-lesson transition card
  quiz_question.html     # Quiz question (radio or checkbox); retake ribbon support
  quiz_feedback.html     # Per-question feedback + all-options state review
  quiz_decode.html       # Mid-quiz 鱼香肉丝 decode page (two-column + footer row)
  quiz_result.html       # Final score page
```

---

## Data Files

Content is never hardcoded in HTML.

- **`static/quiz_data.json`** — list of questions with `id`, `part`, `step`, `dish`,
  `title`, `prompt`, `options[]`, `correct`, `explanation`. Multi-select questions
  set `multi_select: true` and use a list for `correct`.
- **`learningData.json`** — keyed by lesson number; each lesson holds a title,
  intro copy, table rows (Chinese term + meaning + image), and captions.

To edit quiz content, modify `static/quiz_data.json`.  
To edit lessons, modify `learningData.json`.  
Restart the Flask dev server to pick up changes.
