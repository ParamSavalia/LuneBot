import streamlit as st
from chat_tab import show_chat_tab
from grammar_tab import show_grammar_tab
from flashcards_tab import show_flashcards_tab
from quizzes_tab import show_quizzes_tab
# from progress_tab import show_progress_tab  # placeholder for later

st.set_page_config(page_title="LuneBot", layout="wide")
st.markdown("""
    <style>
    .main {
        background-color: #1E1E1E;
        color: #E2E8F0;
    }
    .main > div {
        padding-top: 20px;
        max-width: 800px;
        margin: auto;
    }
    #MainMenu, footer, header {
        visibility: hidden;
    
    </style>
""", unsafe_allow_html=True)

st.title("🇫🇷 LuneBot – Your French Learning Buddy")
st.markdown("Choose a tab to begin practicing:")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 Chat",
    "✏️ Grammar",
    "🧠 Flashcards",
    "📝 Quizzes",
    "📊 Progress"
])

with tab1:
    show_chat_tab()

with tab2:
    show_grammar_tab()

with tab3:
    show_flashcards_tab()

with tab4:
    show_quizzes_tab()

with tab5:
    st.subheader("📊 Progress Tracking Coming Soon!")
