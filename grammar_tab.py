import streamlit as st
from grammar import correct_grammar  # Your backend logic for grammar correction

def show_grammar_tab():
    st.subheader("✏️ Grammar Correction")
    st.markdown("Paste your sentence and get a corrected version instantly.")

    if "grammar_input" not in st.session_state:
        st.session_state.grammar_input = ""

    # Input box
    user_text = st.text_area("Enter a sentence in French or English:",
                             value=st.session_state.grammar_input,
                             key="grammar_input")

    # Language selector (optional)
    language = st.selectbox("Select language to correct:", ["French", "English"], index=0)

    # Correct button
    if st.button("✅ Correct My Grammar"):
        if user_text.strip():
            try:
                corrected = correct_grammar(user_text.strip(), language.lower())
                st.markdown("### ✨ Corrected Sentence:")
                st.success(corrected)
            except Exception as e:
                st.error(f"Error correcting grammar: {e}")
        else:
            st.warning("Please enter some text to correct.")
