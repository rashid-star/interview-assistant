import streamlit as st
import requests

API_URL = "https://interview-assistant-production-0ce6.up.railway.app"

st.set_page_config(
    page_title="AI Interview Assistant Hub",
    page_icon="🤖",
    layout="centered",
)

# ===== Header & global spacing =====
st.markdown(
    """
    <style>
    /* Reduce but don't cut top gap between navbar and content */
    .block-container {
        padding-top: 1.5rem;
    }
    /* Slightly enlarge radio label text for mode selector */
    div[data-baseweb="radio"] > label > div:nth-child(2) {
        font-size: 0.95rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align: center; margin-bottom: 0.1rem; font-size: 2.3rem;'>🤖 AI Interview Assistant Hub</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #BBBBBB; font-size: 0.95rem;'>Choose a domain, learn core ideas, and practice real interview answers with AI feedback.</p>",
    unsafe_allow_html=True,
)

st.markdown("---")

# ===== Helper functions to talk to backend =====
@st.cache_data(show_spinner=False)
def fetch_domains():
    resp = requests.get(f"{API_URL}/domains")
    resp.raise_for_status()
    return resp.json().get("domains", [])


@st.cache_data(show_spinner=False)
def fetch_questions(domain: str):
    if not domain:
        return []
    resp = requests.get(f"{API_URL}/questions", params={"domain": domain})
    resp.raise_for_status()
    return resp.json().get("questions", [])


def call_evaluate(domain: str, question: str, answer: str):
    payload = {
        "domain": domain,
        "question": question,
        "answer": answer,
    }
    resp = requests.post(f"{API_URL}/evaluate", json=payload)
    resp.raise_for_status()
    return resp.json()


def call_chat(domain: str, message: str):
    payload = {
        "domain": domain,
        "message": message,
    }
    resp = requests.post(f"{API_URL}/chat", json=payload)
    resp.raise_for_status()
    return resp.json()


def call_generate_question(domain: str, difficulty: str):
    payload = {"domain": domain, "difficulty": difficulty}
    resp = requests.post(f"{API_URL}/generate-question", json=payload)
    resp.raise_for_status()
    return resp.json()


# ===== Step 1 – Select mode =====
st.markdown("### 1️⃣ Choose how you want to practice")

col_mode_left, col_mode_right = st.columns(2)
with col_mode_left:
    st.markdown("### 🧠 Learn concepts")
    st.markdown(
        "- Ask any theory question.\n"
        "- Get a clear, short explanation.",
    )
with col_mode_right:
    st.markdown("### ✍️ Practice answers")
    st.markdown(
        "- Get an interview question.\n"
        "- Write an answer and get a score.",
    )

mode = st.radio(
    "Mode",
    options=["Learn concepts (Q&A Chat)", "Practice answers (Evaluation)"],
    index=1,
    horizontal=True,
)

st.markdown("---")

# ===== Step 2 – Select domain =====
st.markdown("### 2️⃣ Choose your interview domain")

domains = fetch_domains()
if not domains:
    st.error("No domains available from the backend. Is the FastAPI server running?")
    st.stop()

domain_labels = {
    "machine_learning": "Machine Learning",
    "deep_learning": "Deep Learning",
    "nlp": "NLP",
    "ai": "AI (General)",
    "data_science": "Data Science",
    "data_analytics": "Data Analytics",
    "web_development": "Web Development",
}

display_domains = [domain_labels.get(d, d) for d in domains]
selected_display_domain = st.selectbox("Select your track", display_domains)

# Map back to internal key
inverse_domain_labels = {v: k for k, v in domain_labels.items()}
selected_domain = inverse_domain_labels.get(selected_display_domain, domains[0])

st.markdown("---")

# ===== Content area – depends on mode =====

# --- Learn Mode: Chat Q&A ---
if mode == "Learn concepts (Q&A Chat)":
    st.subheader("3️⃣ Learn Mode – Ask Anything")

    st.markdown(
        f"Ask questions about **{selected_display_domain}**. "
        "For example: *“What is overfitting?”* or *“How should I prepare for this interview?”*"
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Show chat history
    for entry in st.session_state.chat_history:
        role = entry["role"]
        content = entry["content"]
        if role == "user":
            st.markdown(f"**You:** {content}")
        else:
            st.markdown(f"**Assistant:** {content}")

    user_message = st.text_input("Type your question here")

    col1, col2 = st.columns([1, 3])
    with col1:
        ask_btn = st.button("💬 Ask")

    if ask_btn and user_message.strip():
        # Add user message
        st.session_state.chat_history.append(
            {"role": "user", "content": user_message.strip()}
        )

        try:
            response = call_chat(selected_domain, user_message.strip())
            answer = response.get("answer", "No answer received from backend.")
        except Exception as e:
            answer = f"Error calling backend: {e}"

        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )
        st.rerun()

# --- Practice Mode: Evaluation ---
else:
    st.subheader("3️⃣ Practice Mode – Answer & Get Feedback")

    if "extra_questions" not in st.session_state:
        st.session_state.extra_questions = {}

    if selected_domain not in st.session_state.extra_questions:
        st.session_state.extra_questions[selected_domain] = []

    base_questions = fetch_questions(selected_domain)
    questions = base_questions + st.session_state.extra_questions[selected_domain]

    if not questions:
        st.warning("No questions available for this domain yet.")
    else:
        # Track current question index separately from the widget key
        if "question_index" not in st.session_state:
            st.session_state.question_index = 0

        if st.session_state.question_index >= len(questions):
            st.session_state.question_index = 0

        col_q1, col_q2 = st.columns([3, 2])
        with col_q1:
            selected_question = st.selectbox(
                "📋 Interview Question",
                questions,
                index=st.session_state.question_index,
                key="question_select",
            )
        with col_q2:
            difficulty = st.selectbox(
                "Difficulty",
                ["easy", "medium", "hard"],
                index=1,
                key="difficulty",
            )
            gen_clicked = st.button("➕ Generate new question")

        if gen_clicked:
            try:
                resp = call_generate_question(selected_domain, difficulty)
                new_q = resp.get("question")
                if new_q:
                    if new_q not in st.session_state.extra_questions[selected_domain]:
                        st.session_state.extra_questions[selected_domain].append(new_q)
                    # update index to newly added question
                    questions = base_questions + st.session_state.extra_questions[selected_domain]
                    st.session_state.question_index = questions.index(new_q)
                    st.rerun()
            except Exception as e:
                st.error(f"Error generating question: {e}")

        st.subheader("✍️ Your Answer")
        candidate_answer = st.text_area(
            "Write your response below",
            height=220,
        )

        evaluate_clicked = st.button("🚀 Evaluate Answer")

        if evaluate_clicked:
            if candidate_answer.strip() == "":
                st.warning("Please write an answer before evaluation.")
            else:
                try:
                    result = call_evaluate(
                        selected_domain, selected_question, candidate_answer
                    )
                except Exception as e:
                    st.error(f"Error calling backend: {e}")
                else:
                    st.divider()
                    st.subheader("📊 Evaluation Result")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Score", f"{result['score']:.2f}%")
                    with col2:
                        st.write(f"**Rating:** {result['label']}")

                    st.write("### 💡 Feedback")
                    st.info(result.get("basic_feedback", "No feedback provided yet."))

                    st.write("### 🧭 Next steps")
                    score = float(result.get("score", 0))

                    if score >= 85:
                        st.success("You’re doing great. Try a harder follow‑up or move to the next question.")
                    elif score >= 70:
                        st.info("Good answer. Improve it and then move forward.")
                    else:
                        st.warning("Low score. Review the ideal answer, then try again.")

                    coach_feedback = result.get("coach_feedback")
                    improved_answer = result.get("improved_answer")
                    follow_up_question = result.get("follow_up_question")
                    ideal_answer = result.get("ideal_answer")

                    if coach_feedback:
                        with st.expander("Coach feedback (Groq)", expanded=True):
                            st.markdown(coach_feedback)

                    cols_actions = st.columns(3)
                    with cols_actions[0]:
                        if st.button("🔁 Try again (keep question)"):
                            st.rerun()
                    with cols_actions[1]:
                        if follow_up_question and st.button("➡️ Use follow‑up question"):
                            # Add follow-up into list and select it
                            if follow_up_question not in st.session_state.extra_questions[selected_domain]:
                                st.session_state.extra_questions[selected_domain].append(follow_up_question)
                            questions = base_questions + st.session_state.extra_questions[selected_domain]
                            st.session_state.question_index = questions.index(follow_up_question)
                            st.rerun()
                    with cols_actions[2]:
                        if st.button("⏭️ Next random question"):
                            # Rotate to a different question from the existing list
                            if len(questions) > 1:
                                idx = questions.index(selected_question) if selected_question in questions else 0
                                st.session_state.question_index = (idx + 1) % len(questions)
                                st.rerun()

                    if improved_answer:
                        with st.expander("Improved answer (example)", expanded=False):
                            st.markdown(improved_answer)

                    if ideal_answer:
                        with st.expander("Ideal / reference answer", expanded=False):
                            st.markdown(ideal_answer)