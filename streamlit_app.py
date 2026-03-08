import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🤖",
    layout="centered"
)

API_URL = "http://127.0.0.1:8000"


# Header
st.title("🤖 AI Interview Assistant")

st.markdown(
"""
Practice technical interview questions and receive **AI-powered feedback** on your answers.

This system evaluates responses using **sentence embeddings and semantic similarity scoring**.
"""
)

st.divider()


# Fetch questions from API
response = requests.get(f"{API_URL}/questions")
questions = response.json()["questions"]


# Question Section
st.subheader("📋 Interview Question")

selected_question = st.selectbox(
    "Choose a question",
    questions
)


# Answer Section
st.subheader("✍️ Your Answer")

candidate_answer = st.text_area(
    "Write your response below",
    height=200
)


# Evaluate Button
evaluate = st.button("🚀 Evaluate Answer")


if evaluate:

    if candidate_answer.strip() == "":
        st.warning("Please write an answer before evaluation.")

    else:

        payload = {
            "question": selected_question,
            "answer": candidate_answer
        }

        result = requests.post(
            f"{API_URL}/evaluate",
            json=payload
        ).json()

        st.divider()

        st.subheader("📊 Evaluation Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Score", f"{result['score']:.2f}%")

        with col2:

            if result["score"] > 85:
                st.success("Excellent Answer")

            elif result["score"] > 70:
                st.info("Good Answer")

            elif result["score"] > 50:
                st.warning("Average Answer")

            else:
                st.error("Needs Improvement")

        st.write("### 💡 Feedback")

        st.info(result["feedback"])