# Chinese Cuisine Menu Decoder
### How to Order Classic Chinese Dishes from an Unfamiliar Menu

An interactive web-based learning module that teaches users how to decode Chinese menu names — understanding flavor words, cooking methods, and regional styles — through a guided quiz experience.

---

## Course

**UI Design**

## Team Members

| Name | GitHub |
|------|--------|
| Yu Qiu | — |
| Ray Tang | @LisiruiTang |
| Zhonghao Liu | — |
| Shurong Zhang | @alice20030504 |

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

## Structure

```
server.py              # Flask backend
static/
  quiz_data.json       # All quiz questions and answers
  main.css             # Shared styles
  logQuiz.js           # Quiz interaction logic
  images/              # Food photos
templates/
  layout.html          # Base layout
  quiz_question.html   # Quiz question page
  quiz_feedback.html   # Answer feedback page
  quiz_decode.html     # 鱼香肉丝 decode info page
  quiz_result.html     # Final score page
```
