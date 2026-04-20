
# Design TODO — PPT-to-Web Remaining Items

Based on the PPT → Web design review. Items already implemented are excluded.

---

## 1. Learning Table — Information Layering

**What:** The table on Lesson pages is currently flat — all information is shown at the same visual weight. Add a second layer of depth so users can choose how deep to go.

**Options (pick one):**
- Hover over a row → full row highlights + a small tooltip card pops up beside it with an example dish or extra context
- Add a `▶` expand toggle per row → click to reveal a deeper explanation below the row

**Files to change:** `static/logLearning.js`, `static/main.css`

---

## 2. Scenario Page — Menu-style Option Cards

**What:** The four dish options on the Final Scenario question look like standard quiz cards. Since the premise is "you're at a restaurant", the cards should feel more like a real menu.

**Suggestions:**
- Use a serif font (e.g. Georgia) for the dish name line inside each option card
- Add a finer, more elegant border style (thinner lines, slightly warmer color)
- Optionally: add a subtle price tag or menu-section label as a decorative detail

**Files to change:** `static/main.css`, possibly `templates/quiz_question.html`

---

## 3. Scenario Page — Atmospheric Background

**What:** The scenario page currently uses the same warm cream background as all other pages. Adding a subtle restaurant atmosphere would make the "you're at the restaurant" premise feel real.

**Suggestions:**
- Use a low-opacity blurred restaurant image as the page background (CSS `background-image` with `filter: blur`)
- Or: apply a slightly darker/richer warm tone to the body background only on the scenario question

**Files to change:** `static/main.css`, `templates/quiz_question.html`

---

## 4. Post-Quiz Achievement Summary (after Quiz 1 and Quiz 2)

**What:** After completing Quiz 1 and Quiz 2, the feedback page currently shows the answer explanation and a "Next →" button. There's no moment where the user feels they've *earned* something. Add an emotional achievement line that names the specific skill they just demonstrated.

**Suggested copy:**
- After Quiz 1 (Q2, Hunan stir-fry): *"You can now tell a stir-fried dish from a braised one just by reading the name."*
- After Quiz 2 (Q3, Cantonese fish): *"You decoded both a cooking method AND a regional style — most people can't do that."*

**Implementation:** In `templates/quiz_feedback.html`, detect `question.id == 2` and `question.id == 3` and render a styled achievement block above the Next button.

**Files to change:** `templates/quiz_feedback.html`, `static/main.css`

---

## 5. Hook Question Page — Large Chinese Characters as Visual Hook

**What:** The hook question currently shows the dish name `鱼香肉丝` only in the prompt text (small size). Since this is the very first interaction and the entire point is "this name is surprising", the characters should be the first thing the user sees — large, prominent, before the question options.

**Suggestion:** At the top of the hook question page (detected by `question.part == "hook"`), render `鱼香肉丝` at ~64px with its pinyin below, then the question prompt beneath it. This sets up the "what IS this?" mystery before they choose.

**Files to change:** `templates/quiz_question.html`, `static/main.css`

---

## Notes

- Items 2 and 3 (scenario atmosphere) can be done together in one pass
- Item 4 is purely copy + a small styled block — low effort, high emotional impact
- Item 1 (table hover) is the most technically involved but also the most reusable
