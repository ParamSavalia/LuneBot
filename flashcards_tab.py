import streamlit as st
from vocab_data import vocab_by_topic

def show_flashcards_tab():
    st.subheader("🧠 Vocabulary Flashcards")
    st.markdown("Practice French words by topic. Click to flip the card!")

    # Select topic
    topic = st.selectbox("Choose a topic:", list(vocab_by_topic.keys()))

    # Initialize session state
    if "flashcard_index" not in st.session_state:
        st.session_state.flashcard_index = 0

    words = vocab_by_topic[topic]
    current = words[st.session_state.flashcard_index]

    # Flip logic
    if "flip" not in st.session_state:
        st.session_state.flip = False

    if st.button("🔄 Flip Card"):
        st.session_state.flip = not st.session_state.flip

    # Flashcard display
    st.markdown("---")
    st.markdown("### 🃏 Flashcard:")

    if isinstance(current, dict) and "fr" in current and "en" in current:
        if st.session_state.flip:
            st.markdown(f"**🇬🇧 English:** {current['en']}")
        else:
            st.markdown(f"**🇫🇷 French:** {current['fr']}")
    else:
        st.warning("⚠️ Invalid flashcard format. Please check your vocab data.")

    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Previous") and st.session_state.flashcard_index > 0:
            st.session_state.flashcard_index -= 1
            st.session_state.flip = False

    with col3:
        if st.button("➡️ Next") and st.session_state.flashcard_index < len(words) - 1:
            st.session_state.flashcard_index += 1
            st.session_state.flip = False
