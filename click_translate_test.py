import base64
import streamlit as st
from chatbot import chat_with_bot
from speak_text import generate_tts_audio_bytes

# Initialize dictionary for translation popup
if "clicked_word" not in st.session_state:
    st.session_state.clicked_word = None
if "word_translation" not in st.session_state:
    st.session_state.word_translation = {"fr": None, "en": None}

def show_chat_tab():
    st.subheader("\ud83d\udcac Chat with LuneBot")
    st.markdown("Type your message in English or French. LuneBot replies in French with helpful tips!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "chat_input" not in st.session_state:
        st.session_state.chat_input = ""

    for idx, entry in enumerate(st.session_state.chat_history):
        sender, msg = entry.get("sender"), entry.get("message")

        if sender == "user":
            st.markdown(f"""
                <div style='text-align: right; padding: 8px;'>
                    <div style='display: inline-block; background-color: #2D3748; color: #E2E8F0; 
                                padding: 10px 15px; border-radius: 12px;'>
                        {msg}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
                <div style='text-align: left; padding: 8px;'>
                    <div style='display: inline-block; background-color: #1A202C; color: #63B3ED; 
                                padding: 10px 15px; border-radius: 12px;'>
                        {' '.join([f"<button style='border:none;background:none;color:#63B3ED;cursor:pointer' "
                            f"onClick=\"fetch('/?word_clicked={word}');\">{word}</button>" for word in msg.split()])}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if st.button("\ud83d\udd0a Play", key=f"play_{idx}"):
                try:
                    audio_bytes = generate_tts_audio_bytes(msg)
                    audio_bytes.seek(0)
                    if audio_bytes.getbuffer().nbytes > 0:
                        b64 = base64.b64encode(audio_bytes.read()).decode()
                        st.markdown(f"""
                            <audio controls>
                                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                                Your browser does not support the audio element.
                            </audio>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("\u26a0\ufe0f Audio generation failed: No audio data returned.")
                except Exception as e:
                    st.error("\u274c Exception during audio playback:")
                    st.exception(e)

    if st.session_state.clicked_word:
        word = st.session_state.clicked_word
        prompt = f"""
        Give a short French and English description of the French word: '{word}'.
        Respond in this format:
        French: [brief description in French]
        English: [brief translation or explanation in English]
        """
        response = chat_with_bot(prompt)
        try:
            lines = response.strip().splitlines()
            st.session_state.word_translation = {
                "fr": lines[0].replace("French:", "").strip(),
                "en": lines[1].replace("English:", "").strip()
            }
        except Exception:
            st.session_state.word_translation = {"fr": "N/A", "en": response}

        st.markdown(f"""
            <div style='margin-top: 20px; padding: 18px 22px; background: rgba(255, 255, 255, 0.95); border: 1px solid #E2E8F0;
                        border-radius: 16px; max-width: 520px; box-shadow: 0 8px 24px rgba(0,0,0,0.08); font-family: "Segoe UI", sans-serif;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <strong style='font-size: 20px;'>\ud83d\udd0d {word}</strong>
                    <form action="" method="post">
                        <button style='background: none; border: none; font-size: 18px; cursor: pointer; color: #999;' name='close_popup'>\u274c</button>
                    </form>
                </div>
                <div style='margin-top: 16px; font-size: 16px; color: #333;'>
                    <p><strong>\ud83c\uddeb\ud83c\uddf7 French:</strong> {st.session_state.word_translation['fr']}</p>
                    <p><strong>\ud83c\uddec\ud83c\udde7 English:</strong> {st.session_state.word_translation['en']}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("\u274c Close Translation"):
            st.session_state.clicked_word = None
            st.session_state.word_translation = {"fr": None, "en": None}

    st.divider()

    user_input = st.text_input("Type your message", value=st.session_state.chat_input, key="chat_input")

    col1, col2 = st.columns([1, 12])
    with col1:
        send_clicked = st.button("Send")
    with col2:
        reset_clicked = st.button("Reset")

    if send_clicked:
        cleaned_input = user_input.strip()
        if cleaned_input:
            st.session_state.chat_history.append({"sender": "user", "message": cleaned_input})
            try:
                bot_reply = chat_with_bot(cleaned_input)
            except Exception as e:
                bot_reply = "\u26a0\ufe0f Sorry, there was an error getting a response. Please try again."
            st.session_state.chat_history.append({"sender": "bot", "message": bot_reply})
            if "chat_input" in st.session_state:
                del st.session_state["chat_input"]
            st.query_params["refresh"] = str(len(st.session_state.chat_history))
            st.rerun()

    if reset_clicked:
        st.session_state.chat_history = []
        if "chat_input" in st.session_state:
            del st.session_state["chat_input"]
        st.query_params["refresh"] = "reset"
        st.rerun()
