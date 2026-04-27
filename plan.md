# Chinese Cuisine Menu Decoder — Development Plan

**Project:** Convert the Google Slides prototype into a working Flask web app
**Stack:** Flask · Jinja2 · HTML · Bootstrap 5 · jQuery · JSON
**Deadline:** Monday Apr 20, 2026 · 11:59 PM (no grace period)

---

## What We're Building

The app teaches users two things — regional cooking styles and cooking methods — then immediately tests their knowledge with a quiz. The learning section presents vocabulary in a table paired with images. The quiz progresses from "pick the description" to "match the image" to "apply it in a real restaurant scenario." At the end the user sees their score and can review every answer.

The full user journey looks like this:

```
/ (Home)
  → /learn/1  (Cooking Methods = Texture)
  → /learn/2  (Flavor & Style Words = Taste Preview)
  → /quiz/1   (Round 1 · Step 1 · Describe Hunan Beef)
  → /quiz/2   (Round 1 · Step 2 · Identify Hunan Beef image)
  → /quiz/3   (Round 2 · Step 1 · Describe Cantonese Fish)
  → /quiz/4   (Round 2 · Step 2 · Identify Cantonese Fish image)
  → /quiz/5   (Scenario · Spicy-food avoidance)
  → /result   (Score + full review)
```

---

## Where We Stand Right Now

### What is fully working
- All four Flask routes exist (`/`, `/learn/<n>`, `/quiz/<n>`, `/result`)
- The entire quiz flow is functional end-to-end: question rendering, POST submission, per-answer feedback page, final result page with score and review
- `quiz_data.json` holds all 5 questions with options, correct answers, explanations, and placeholder images
- `logQuiz.js` handles option-card highlighting and submission guard
- `quiz_feedback.html` shows correct/incorrect badge, the right image, and the full explanation (or per-option tag breakdown for the scenario question)
- `quiz_result.html` shows `score / total` and a row-by-row review
- Real images exist in `static/images/` for both learning slides (stir_fried, braised, steamed, qing_chao, hunan, cantonese, mala, yuxiang)

### What is not yet working
Three things block a clean click-through:

1. **Home page is a stub.** `/` returns a raw string, not a rendered template. There is no `home.html` and no Start button.

2. **Learning route is a stub.** `/learn/<n>` logs a visit but renders another raw string. The `learning.html` template exists and `logLearning.js` knows how to populate it, but the route never renders the template — so the learning pages are unreachable from the browser.

3. **Learningdata.json is actually a JS file.** `static/Learningdata.json` contains `const lesson1Contents = {...}` JavaScript syntax, not valid JSON. The server cannot `json.load()` it, and `logLearning.js` expects a `learningContents` variable to already exist in the page's scope — which nothing currently provides.

### Smaller gaps
- The Prev / Next buttons in `layout.html` have no `onclick` or `href` logic attached.
- `quiz_data.json` still uses `placehold.co` placeholder URLs for quiz option images. These should be swapped for real food photos before the demo.
- `main.css` has almost no styling beyond container widths. The quiz pages look functional but bare.

---

## Page-by-Page Breakdown

Each section below describes what the finished page should contain, maps it to the prototype slides, and lists the concrete work needed.

---

### Page 1 — Home  (`/`)

**Slide reference:** Slides 1–3 (Cover, "What is this app?", "How it works")

The home page introduces the problem — you are standing in front of a Chinese restaurant menu and have no idea what anything means — and offers a single clear entry point. It should feel welcoming and low-pressure.

**What the page needs:**
- A headline: *"Chinese Cuisine Menu Decoder"*
- A one-sentence value proposition: *"Learn to read a Chinese menu in 2 minutes — then test yourself."*
- A brief flow preview (2 learning slides → 5 quiz questions → your score)
- A prominent **Start Learning** button that POSTs to `/start` or simply links to `/learn/1`

**Backend work (Ray):**
- Replace the stub string in the `home()` route with `return render_template('home.html')`
- Log a `{"event": "start", "timestamp": ...}` entry to `user_state["learning_log"]` when the user clicks Start (either via a POST route or by recording it at the top of `/learn/1`)

**Frontend work (Zhonghao):**
- Create `templates/home.html` extending `layout.html`
- Hide the Prev/Next nav bar on this page (add `{% block nav %}{% endblock %}` or a CSS class)
- The Start button should be a Bootstrap primary button linking to `/learn/1`

---

### Page 2 — Learning Slide 1  (`/learn/1`)

**Slide reference:** Slides 4–7 ("Cooking Methods = Texture")

This page teaches the six core cooking methods. The left half is a two-column table (method name + Chinese character + texture outcome). The right half is a 2×2 image grid showing stir-fry, braised, steamed, and qing-chao dishes. Users read this page at their own pace, then click Next.

**What the page needs:**
- Page title: *"Cooking Methods = Texture"*
- Introductory sentence: *"The cooking method tells you exactly what texture to expect before the food arrives."*
- A Bootstrap table with columns: Cooking Method · Chinese · Texture Outcome
- A 2×2 image grid using `static/images/stir_fried.jpg`, `braised.jpg`, `steamed.png`, `qing_chao.png`
- Next button → `/learn/2`; Prev button → `/` (or hidden)

**Backend work (Ray):**
- Convert `static/Learningdata.json` from JS syntax to a real JSON file:

```json
{
  "lessons": [
    {
      "id": 1,
      "title": "Cooking Methods = Texture",
      "intro": "The cooking method tells you exactly what texture to expect before the food arrives.",
      "table": [
        {"method": "Stir-fried",      "chinese": "爆炒", "outcome": "Savory, quick wok toss, lightly charred"},
        {"method": "Braised",         "chinese": "炖",   "outcome": "Fall-apart tender, rich in liquid"},
        {"method": "Smoked",          "chinese": "熏",   "outcome": "Deep, earthy, smoky complexity"},
        {"method": "Steamed",         "chinese": "蒸",   "outcome": "Light, tender, clean natural taste"},
        {"method": "Qing-chao",       "chinese": "清炒", "outcome": "Fresh, bright, crisp — minimal seasoning"},
        {"method": "Deep-fried",      "chinese": "炸",   "outcome": "Crispy golden outside, tender inside"}
      ],
      "images": [
        "/static/images/stir_fried.jpg",
        "/static/images/braised.jpg",
        "/static/images/steamed.png",
        "/static/images/qing_chao.png"
      ]
    },
    {
      "id": 2,
      "title": "Flavor & Style Words = Taste Preview",
      "intro": "These words in a dish name preview what your taste buds will experience.",
      "table": [
        {"method": "Hunan-style",        "chinese": "湘",  "outcome": "Intensely spicy, smoky, garlicky. Dry and fragrant."},
        {"method": "Cantonese-style",    "chinese": "粤",  "outcome": "Light, fresh, ingredient-forward. Clean and elegant."},
        {"method": "Mala / Numbing-Spicy","chinese": "麻辣","outcome": "Numbing peppercorn + chili burn. Layered and electric."},
        {"method": "Yu-xiang / Fish-Fragrant","chinese": "鱼香","outcome": "No fish. Sweet-sour-savory-spicy sauce with garlic and pickled chili."}
      ],
      "images": [
        "/static/images/hunan.jpg",
        "/static/images/cantonese.jpg",
        "/static/images/mala.png",
        "/static/images/yuxiang.png"
      ]
    }
  ]
}
```

- Update `/learn/<n>` route to load this JSON, find the matching lesson by `id`, and pass it to the template:

```python
@app.route('/learn/<int:n>')
def learn(n):
    user_state["learning_log"].append({
        "timestamp": datetime.now().isoformat(),
        "lesson": n, "action": "visit"
    })
    with open(os.path.join(app.static_folder, 'learning_data.json'), encoding='utf-8') as f:
        all_lessons = json.load(f)['lessons']
    total = len(all_lessons)
    lesson = next((l for l in all_lessons if l['id'] == n), None)
    if lesson is None:
        return redirect(url_for('quiz', n=1))
    next_url = url_for('learn', n=n+1) if n < total else url_for('quiz', n=1)
    prev_url = url_for('learn', n=n-1) if n > 1 else url_for('home')
    return render_template('learning.html', lesson=lesson, next_url=next_url, prev_url=prev_url)
```

**Frontend work (Zhonghao):**
- Rewrite `templates/learning.html` to use Jinja2 variables instead of relying on a JS global:

```html
{% extends "layout.html" %}
{% block content %}
<div class="main_container">
  <h1>{{ lesson.title }}</h1>
  <p>{{ lesson.intro }}</p>
  <div class="row">
    <div class="col-6">
      <table class="table">
        <thead><tr><th>Method</th><th>Chinese</th><th>Texture / Taste</th></tr></thead>
        <tbody>
          {% for row in lesson.table %}
          <tr><td>{{ row.method }}</td><td>{{ row.chinese }}</td><td>{{ row.outcome }}</td></tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
    <div class="col-6">
      <div class="row">
        {% for img in lesson.images %}
        <div class="col-6 mb-2"><img src="{{ img }}" class="img-fluid rounded"></div>
        {% endfor %}
      </div>
    </div>
  </div>
  <div class="d-flex justify-content-between mt-3">
    <a href="{{ prev_url }}" class="btn btn-outline-secondary">← Back</a>
    <a href="{{ next_url }}" class="btn btn-primary">Next →</a>
  </div>
</div>
{% endblock %}
```

- Remove the `logLearning.js` script block from this template (it is no longer needed once Jinja2 handles rendering)

---

### Page 3 — Learning Slide 2  (`/learn/2`)

**Slide reference:** Slides 8–11 ("Flavor & Style Words = Taste Preview")

Same layout as `/learn/1` but with the second lesson's data (four regional style words). Images are `hunan.jpg`, `cantonese.jpg`, `mala.png`, `yuxiang.png`. Next button goes to `/quiz/1`.

No additional backend or frontend work beyond what is described for `/learn/1` — the same route and template handle both lessons automatically once the JSON and route are fixed.

---

### Pages 4–8 — Quiz Questions  (`/quiz/1` through `/quiz/5`)

**Slide reference:** Slides 12–14 (Quiz walkthrough)

The quiz is already the most complete part of the app. The remaining work is refinement, not new building.

**What still needs to happen:**

- **Replace placeholder images in `quiz_data.json`.**
  Questions 2 and 4 (the image-matching steps) show four `placehold.co` option images. These should be real food photos. The `static/images/` folder already has `hunan.jpg` and `cantonese.jpg` which can be used for the correct answers. Additional distractor images (e.g., a braised pork belly shot and a mapo tofu shot) need to be found or photographed.

  Update the `"image"` fields in `quiz_data.json` for questions 2 and 4 to point to real files, e.g.:
  ```json
  {"key": "C", "text": "Dry-tossed chili beef ...", "image": "/static/images/hunan.jpg"}
  ```

- **Scenario question (Q5) image support.**
  Q5 currently has no `"image"` field per option, only a `"correct_image"`. The scenario format shows menu-style option cards — these look better as text cards, which is already how they render, so no image swap is needed here.

- **Quiz option card click feedback.**
  `logQuiz.js` already adds a `selected` class on click, but `main.css` has no `.selected` rule. Add a visible highlight (border + background tint) so users can clearly see their pick before submitting.

---

### Quiz Feedback Pages  (`quiz_feedback.html`)

These pages show after each answer is submitted. They are fully implemented. The only improvement needed is making the **Next Question** link more prominent — currently it is a plain `<a>` tag at the bottom. Wrapping it in a `btn btn-primary` Bootstrap class is a one-line change.

---

### Page 9 — Results  (`/result`)

**Slide reference:** Slide 15 ("Your Score")

The results page is fully implemented. It shows `score / total` and a per-question review table. Two small improvements before the demo:

1. Add a **motivational message** based on score range (e.g., 5/5 = "Menu Master!", 3–4 = "Menu Confident", below 3 = "Keep practicing!"). This can be computed in the `quiz_result()` route and passed as a `message` variable.

2. The **Back to Home** link should also reset `user_state` so a second run-through works. Add a `/reset` route or simply re-initialize the dict inside `home()`.

---

## Data Architecture Summary

| File | Owner | Format | Purpose |
|---|---|---|---|
| `static/learning_data.json` | Ray | JSON array | Lesson content — titles, tables, image paths |
| `static/quiz_data.json` | Yu Qiu / Alice | JSON array | All 5 quiz questions with options, correct answers, explanations |
| `user_state` dict in `server.py` | Ray | Python dict in memory | Per-session log of learning visits, quiz answers, score |

No database is needed. HW10 spec explicitly allows single-user in-memory state.

---

## Team Roles & Task Assignments

### Part 1 — Learning + Home  (Ray Tang & Zhonghao Liu)

| Task | Owner | Status |
|---|---|---|
| Rewrite `Learningdata.json` → `learning_data.json` (valid JSON) | Ray | To do |
| Update `/learn/<n>` route to load JSON + render template | Ray | To do |
| Create `templates/home.html` with Start button | Zhonghao | To do |
| Fix `/` route stub → `render_template('home.html')` | Ray | To do |
| Rewrite `templates/learning.html` to use Jinja2 (drop logLearning.js) | Zhonghao | To do |
| Wire Prev/Next nav into learning pages | Zhonghao | To do |
| Log Start event to `user_state` | Ray | To do |

### Part 2 — Quiz  (Yu Qiu & Alice / Shurong Zhang)

| Task | Owner | Status |
|---|---|---|
| Replace placehold.co URLs in `quiz_data.json` with real image paths | Yu Qiu | To do |
| Add `.selected` CSS rule to `main.css` for option card highlight | Alice | To do |
| Wrap "Next Question" link in `quiz_feedback.html` as btn-primary | Alice | To do |
| Add score-based message to `quiz_result()` + pass to template | Yu Qiu | To do |
| Add `/reset` route or reset logic in `home()` for repeat sessions | Yu Qiu | To do |

### Shared / Integration

| Task | Who | Status |
|---|---|---|
| Verify full click-through: `/` → `/learn/1` → `/learn/2` → all quiz questions → result | All | To do |
| Check `/debug/state` logs learning visits AND quiz answers correctly | Ray | To do |
| Each member pushes at least one commit to GitHub | Everyone | To do |

---

## Acceptance Checklist (HW10 Requirements)

Before recording the demo video, confirm every item below:

- [ ] `/` renders a real home page with a visible Start button
- [ ] Clicking Start navigates to `/learn/1`
- [ ] `/learn/1` shows the Cooking Methods table and 4 images
- [ ] `/learn/2` shows the Flavor & Style table and 4 images
- [ ] Prev/Next navigation works on both learning pages
- [ ] `/quiz/1` through `/quiz/5` each render a question with selectable options
- [ ] Clicking an option highlights it; submitting without selecting shows an alert
- [ ] Each quiz answer renders a feedback page with correct/incorrect badge and explanation
- [ ] `/result` shows the correct score out of 5 and a per-question review
- [ ] `/debug/state` shows learning page visits and all quiz answers stored
- [ ] At least one real commit per team member in the GitHub repo
- [ ] Every team member can run the app on their own laptop (`python server.py`)

---

## What to Skip for HW10

HW10 is explicitly about **basic functionality**. Polish and graphic design are HW11's job. For now:

- Don't spend time on custom fonts, color palettes, or hover animations
- Don't add user authentication or multi-user support (the spec says single-user is fine)
- Don't add extra quiz questions — the 5 in `quiz_data.json` are the right scope
- Don't worry about mobile responsiveness — Bootstrap's default grid is enough

The goal this week is a complete click-through, logged backend state, and every team member with a GitHub commit.
