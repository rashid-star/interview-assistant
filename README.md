# 🤖 AI Interview Assistant

AI Interview Assistant is an intelligent web application that evaluates technical interview answers using **Natural Language Processing (NLP)** and **semantic similarity** techniques.

The system compares a candidate's response with an ideal answer using **sentence embeddings** and calculates a similarity score to determine how closely the answer matches the expected explanation.

This project demonstrates a **real-world AI application architecture**, integrating **NLP models, APIs, and a frontend interface**.

---

# 🚀 Features

* Practice technical interview questions
* AI-powered answer evaluation
* Semantic similarity scoring using sentence embeddings
* Automatic feedback generation
* Interactive user interface using Streamlit
* FastAPI backend for evaluation services
* Abbreviation normalization (ML → Machine Learning, AI → Artificial Intelligence)
* Scalable question bank for multiple interview topics

---

# 🧠 How It Works

The system evaluates candidate answers using **semantic similarity between sentences**.

### Evaluation Pipeline

User selects a question and writes an answer.

```
User Answer
      │
      ▼
Streamlit UI
      │
      ▼
FastAPI API Request
      │
      ▼
Text Normalization
(abbreviation expansion)
      │
      ▼
Sentence Transformer Model
      │
      ▼
Sentence Embeddings
      │
      ▼
Cosine Similarity Calculation
      │
      ▼
Score Generation
      │
      ▼
AI Feedback Generation
      │
      ▼
Result Returned to UI
```

---

# 📊 Example Output

```
Question:
What is Machine Learning?

Candidate Answer:
Machine learning is a subset of artificial intelligence.

Score:
84.76%

Feedback:
Good answer. You covered most important concepts but could add more details.
```

---

# 🧱 Project Architecture

```
ai-interview-assistant
│
├── src
│   ├── questions.py       # Question bank and abbreviation handling
│   ├── evaluator.py       # AI evaluation logic and scoring
│   └── embeddings.py      # Sentence transformer embedding model
│
├── app.py                 # FastAPI backend API
├── streamlit_app.py       # Streamlit frontend interface
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
└── .gitignore
```

---

# 🧰 Tech Stack

### Programming Language

* Python

### Backend Framework

* FastAPI

### Frontend Framework

* Streamlit

### NLP / AI Libraries

* Sentence Transformers
* Scikit-learn

### Machine Learning Techniques

* Sentence Embeddings
* Cosine Similarity
* Semantic Text Matching

### Other Libraries

* Requests
* Pydantic

---

# 🧠 AI Model Used

This project uses the **Sentence Transformer model**:

```
all-MiniLM-L6-v2
```

Features of this model:

* 384-dimensional sentence embeddings
* Fast and lightweight
* Good semantic similarity performance
* Suitable for real-time applications

---

# 📏 Scoring Method

The similarity score between candidate and ideal answers is calculated using **Cosine Similarity**.

```
Similarity = cosine_similarity(candidate_embedding, ideal_embedding)
```

The similarity value is converted into a percentage:

```
Score = Similarity × 100
```

Feedback is generated based on score ranges:

| Score Range | Feedback          |
| ----------- | ----------------- |
| 85 – 100    | Excellent answer  |
| 70 – 85     | Good answer       |
| 50 – 70     | Average answer    |
| 0 – 50      | Needs improvement |

---

# 🔤 Abbreviation Handling

The system normalizes common AI abbreviations to improve evaluation accuracy.

Example mappings:

```
ML → Machine Learning
AI → Artificial Intelligence
DL → Deep Learning
NLP → Natural Language Processing
```

Example:

```
User Input:
"ML is a subset of AI"

Normalized Input:
"Machine learning is a subset of artificial intelligence"
```

This ensures the AI model understands abbreviated answers correctly.

---

# ⚙️ Installation

### Clone the repository

```
git clone https://github.com/YOUR_USERNAME/ai-interview-assistant.git
```

### Navigate to the project folder

```
cd ai-interview-assistant
```

### Create virtual environment (optional)

```
python -m venv venv
```

Activate environment:

Windows:

```
venv\Scripts\activate
```

Mac/Linux:

```
source venv/bin/activate
```

---

# 📦 Install Dependencies

```
pip install -r requirements.txt
```

---

# ▶️ Run the Backend

Start the FastAPI server:

```
uvicorn app:app --reload
```

API documentation will be available at:

```
http://127.0.0.1:8000/docs
```

---

# 💻 Run the Frontend

Start the Streamlit interface:

```
streamlit run streamlit_app.py
```

The application will open automatically in your browser.

---

# 🎯 Example Questions Included

The system currently includes multiple machine learning interview questions such as:

* What is Machine Learning?
* What is the difference between supervised and unsupervised learning?
* What is overfitting?
* What is underfitting?
* What is the bias-variance tradeoff?
* What is cross validation?
* What is gradient descent?
* What is a confusion matrix?
* What is precision and recall?
* What is Natural Language Processing?

The question bank can easily be expanded.

---

# 🔮 Future Improvements

Planned upgrades for the project:

* Voice-based interview system (Speech-to-Text)
* AI-generated interview questions using LLMs
* Multi-question interview sessions
* Candidate performance analytics
* Admin dashboard for recruiters
* Cloud deployment (AWS / Docker)

---

# 👨‍💻 Author

**Khan Hammad Abdul Wahab**

AI / Machine Learning Enthusiast
Focused on building real-world AI applications using Python and modern ML frameworks.
