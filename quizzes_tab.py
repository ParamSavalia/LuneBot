import streamlit as st
from vocab_data import quizzes_by_level

def show_quizzes_tab():
    st.subheader("📝 French Quizzes")
    st.markdown("Test your knowledge by answering questions based on your level!")

    # --- Select Level ---
    level = st.selectbox("Choose your level:", list(quizzes_by_level.keys()))

    questions = quizzes_by_level[level]

    # --- Session State Initialization ---
    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "quiz_feedback" not in st.session_state:
        st.session_state.quiz_feedback = ""

    if "selected_option" not in st.session_state:
        st.session_state.selected_option = ""

    quiz_index = st.session_state.quiz_index

    # --- Validate Index ---
    if quiz_index >= len(questions):
        st.success(f"🏁 Quiz complete! Your score: {st.session_state.score} / {len(questions)}")
        if st.button("🔁 Restart Quiz"):
            st.session_state.quiz_index = 0
            st.session_state.score = 0
            st.session_state.quiz_feedback = ""
            st.session_state.selected_option = ""
        return  # Exit early if quiz is over

    current = questions[quiz_index]

    # --- Question Display ---
    st.markdown(f"**Question {quiz_index + 1}/{len(questions)}:**")
    st.markdown(f"**{current['question']}**")

    # --- Options ---
    st.session_state.selected_option = st.radio(
        "Choose an answer:",
        options=current["options"],
        index=0,
        key=f"option_{quiz_index}"
    )

    # --- Submit Button ---
    if st.button("Submit Answer"):
        if st.session_state.selected_option == current["answer"]:
            st.session_state.score += 1
            st.session_state.quiz_feedback = "✅ Correct!"
        else:
            st.session_state.quiz_feedback = f"❌ Incorrect. The correct answer was: **{current['answer']}**"

    # --- Feedback ---
    if st.session_state.quiz_feedback:
        st.info(st.session_state.quiz_feedback)

        if st.button("Next Question"):
            st.session_state.quiz_index += 1
            st.session_state.quiz_feedback = ""
            st.session_state.selected_option = ""
            st.rerun()  # Force rerun to load next question properly
