# 🤖 AI Interview Assistant Hub

An AI‑powered web app to **learn concepts** and **practice interview answers** across multiple domains like Machine Learning, Deep Learning, NLP, Data Science, Data Analytics, and Web Development.

Built with **FastAPI**, **Streamlit**, **scikit‑learn**, and **Groq** LLMs.

---

## ✨ Features

- **Two modes of practice**
  - **Learn concepts (Q&A Chat)**  
    - Ask any theory or preparation question.  
    - Groq LLM explains concepts in simple language plus quick interview tips.
  - **Practice answers (Evaluation)**  
    - Pick or generate interview questions.  
    - Write your own answer and get:
      - Similarity‑based **score (0–100)** using TF‑IDF + cosine similarity.  
      - Local **rating + basic feedback**.  
      - Groq‑powered **coach feedback**, improved answer, and follow‑up question.

- **Multiple domains / tracks**
  - `machine_learning`, `deep_learning`, `nlp`, `ai`, `data_science`, `data_analytics`, `web_development`.
  - Each domain has a curated question bank with ideal reference answers.

- **Smart practice flow**
  - Generate new questions by **difficulty** (easy / medium / hard).
  - Groq suggests **follow‑up questions** depending on your score.
  - View **ideal answer** and a **model improved answer** in expandable sections.

---

## 🧱 Architecture

- **Frontend:** `Streamlit` (`app.py`)
  - Mode selection (Learn / Practice).
  - Domain selection.
  - Learn‑mode chat UI.
  - Practice‑mode question picker, answer box, and results dashboard.

- **Backend:** `FastAPI` (`main.py`)
  - `GET /domains` – list available domains.
  - `GET /questions?domain=...` – questions for a domain.
  - `POST /chat` – Groq LLM for concept Q&A.
  - `POST /evaluate` – TF‑IDF + cosine similarity + Groq coaching.
  - `POST /generate-question` – Groq LLM generates new interview questions.

- **Core logic (`src/`)**
  - `questions.py` – domain‑wise question bank + ideal answers.
  - `evaluator.py` – TF‑IDF cosine similarity scoring, labels, and base feedback.
  - `llm_groq.py` – Groq client for chat answers, coaching, and question generation.

---

## 🚀 Getting started

### 1. Clone and install dependencies

```bash
git clone https://github.com/rashid-star/interview-assistant.git
cd interview-assistant

python -m venv venv
# Windows PowerShell
.\venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt