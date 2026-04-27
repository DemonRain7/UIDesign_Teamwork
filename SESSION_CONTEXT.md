# Session Context — Chinese Cuisine Menu Decoder

> Hand this file to a new Claude session at the start. It captures everything needed to continue without re-deriving state from the codebase.

---

## Project in One Line

Flask web app (Python 3) that teaches non-Chinese diners to decode English-translated Chinese menu names through two lessons and a four-question quiz. UI/UX by Alice (Shurong Zhang), backend by Ray Tang, learning frontend by Zhonghao Liu, quiz infrastructure by Yu Qiu.

**Run it:** `pip install flask && python server.py` → `http://127.0.0.1:5000`

---

The app is **fully functional end-to-end**. All routes work, all content is real (no placeholders). The codebase is past the "make it work" phase and is in a UI/UX polish phase.

**Latest commit:** `82b620f` — "UI polish: wider layouts, image updates, decode page redesign"

### User Flow
```
/ (Home — progress tracker)
  → /quiz/1   (Hook: guess what 鱼香肉丝 is)
  → /learn/1  (Lesson 1: Cooking Methods = Texture)
  → /quiz/2   (Quiz 1: Spot the Hunan Stir-fry)
  → /learn/2  (Lesson 2: Flavor & Style Words)
  → /quiz/3   (Quiz 2: Decode Cantonese Steamed Fish)
  → /quiz/decode  (Decode interlude: 鱼香 revealed)
  → /quiz/4   (Final Challenge: multi-select, protect spice-averse friend)
  → /quiz/result  (Score + per-question review)
```

---

## Key Files

| File | Purpose |
|------|---------|
| `server.py` | Flask backend — all routes, in-memory `user_state` |
| `static/main.css` | **Single CSS file for entire app** — Alice owns this |
| `static/quiz_data.json` | All quiz questions, options, answers, explanations |
| `learningData.json` | Lesson content (title, table rows, image paths) |
| `templates/layout.html` | Base layout — Bootstrap 5 + jQuery via CDN |
| `templates/home.html` | Home page with 6-stage progress tracker |
| `templates/learning.html` | Lesson page (JS-rendered from `learningData.json`) |
| `templates/quiz_question.html` | Quiz question (radio or checkbox) |
| `templates/quiz_feedback.html` | Per-question feedback page |
| `templates/quiz_decode.html` | Mid-quiz 鱼香肉丝 decode — two-column layout |
| `templates/quiz_result.html` | Final score + review |
| `static/logQuiz.js` | Quiz interaction (radio + multi-select, submit guard) |
| `static/logLearning.js` | Learning page rendering from JSON |
| `static/images/` | All dish photos |

---

## CSS Design System (`static/main.css`) — Key Patterns

Alice built the entire CSS. Key conventions to know before editing:

- **Layout:** `body { display: flex; flex-direction: column }` + `.main_container { margin: auto }` for vertical centering on every page
- **Card width:** `.main_container.quiz_wide { width: min(1340px, calc(100vw - 40px)) }` — used on quiz, decode, learning pages
- **Two-column layouts:** CSS Grid — `quiz_split`, `result_split`, `feedback_grid`, `decode_split`
- **Color palette:**
  - Dark navy: `#1F2A3D` (headings, active states)
  - Gold: `#C8932B` (accents, CTAs, correct answer)
  - Cream bg: `#F5F0E8`
  - Card bg: `#FAFAF8`
  - Muted text: `#5a6375`, `#9a8a6e`
- **Progress bar:** `.progress_header` + `.progress_track` + `.progress_fill` — used on quiz/decode/learn pages
- **Animations:** shake (wrong answer), glow pulse (correct), streak counter, hook reveal

---

## What Was Done in This Session

### TA Feedback Received
TA said: too much text → cognitive overload, users won't engage. Suggested LLM integration for addictive feedback loops (like 百词斩). User asked for quick UI fix first, LLM integration deferred.

### Changes Made This Session
**`templates/home.html`:**
- Removed `<p class="home_stage_desc">` from all 6 stage cards (was ~2 lines of description text per card)
- Removed `<div class="home_stage_locked_hint">` from locked cards
- Shortened `home_subtitle` from 3-line paragraph → `"Decode Chinese menu names — one stage at a time."`
- Active card CTA changed from plain text `"Start →"` → `"▶ Start"`
- Done card badge: `"✓ Completed"` → `"✓ Done"` (shorter)

**`static/main.css`:**
- `.home_stage_title`: `margin-bottom` 4px → 10px (breathing room without desc)
- `.home_stage_cta`: now `display: inline-block`, muted color for done cards
- `.home_stage_card.active .home_stage_cta`: styled as dark pill button (`background: #1F2A3D; color: #fff; padding: 6px 16px; border-radius: 20px`)
- `.home_stage_card.active:hover .home_stage_cta`: pill turns gold (`#C8932B`) on hover
- Removed `.home_stage_locked_hint` CSS rule (element removed from HTML)

---

## Pending Work (from TODO.md)

These are designed but not yet implemented. Pick up from here:

| # | Task | Files | Effort |
|---|------|-------|--------|
| 1 | Learning table hover — tooltip or expand toggle per row | `logLearning.js`, `main.css` | Medium |
| 2 | Scenario page (Q4) — menu-style option cards (serif font, elegant border) | `main.css`, `quiz_question.html` | Low |
| 3 | Scenario page — atmospheric background (blurred restaurant image or darker bg) | `main.css`, `quiz_question.html` | Low |
| 4 | Post-quiz achievement summary after Q2 and Q3 feedback pages | `quiz_feedback.html`, `main.css` | Low |
| 5 | Hook question (Q1) — large 鱼香肉丝 at ~64px above the options | `quiz_question.html`, `main.css` | Low |

**Recommended next:** Items 4 and 5 are pure HTML/CSS, high emotional impact, low effort. Do those first.

---

## LLM Integration (Deferred)

TA suggested connecting to an LLM to generate dish facts after each answer (like 百词斩 addiction loop). User is interested but hasn't started. Would require:
- Anthropic API key in environment
- New Flask route (e.g. `/api/dish-fact`) calling Claude API
- JS fetch on feedback page to show a "Did you know?" card
- Use `claude-sonnet-4-6` model (current default)

---

## Team

| Name | GitHub | Role |
|------|--------|------|
| Yu Qiu | @DemonRain7 | Quiz Part I (Q2, Q3) + shared quiz infrastructure |
| Ray Tang | @LisiruiTang | Learning module backend |
| Zhonghao Liu | @zeeliu7 | Learning module frontend |
| Shurong Zhang (Alice) | @alice20030504 | Quiz Part II (Q4) · Full UI/UX redesign · CSS design system · App flow · Decode page · Image curation |

**TA:** Max-Zhang63  
**Repo:** `https://github.com/DemonRain7/UIDesign_Teamwork.git`  
**Branch:** `main`
