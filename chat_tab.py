import base64

import streamlit as st
from chatbot import chat_with_bot
from speak_text import generate_tts_audio_bytes  # from your working TTS test

def show_chat_tab():
    st.subheader("💬 Chat with LuneBot")
    st.markdown("Type your message in English or French. LuneBot replies in French with helpful tips!")

    # --- Initialize session state ---
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "chat_input" not in st.session_state:
        st.session_state.chat_input = ""

    # --- Display chat history ---
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
        else:  # Bot response with Play button
            st.markdown(f"""
                <div style='text-align: left; padding: 8px;'>
                    <div style='display: inline-block; background-color: #1A202C; color: #63B3ED; 
                                padding: 10px 15px; border-radius: 12px;'>
                        {msg}
                    </div>
                </div>
            """, unsafe_allow_html=True)
#play button section
            if st.button("🔊 Play", key=f"play_{idx}"):
                try:
                    #st.write("🛠️ Generating audio...")
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
                        st.success("✅ Audio ready. Click play to listen.")
                    else:
                        st.error("⚠️ Audio generation failed: No audio data returned.")
                except Exception as e:
                    st.error("❌ Exception during audio playback:")
                    st.exception(e)

    st.divider()

    # --- Input field ---
    user_input = st.text_input("Type your message", value=st.session_state.chat_input, key="chat_input")

    # --- Button row ---
    col1, col2 = st.columns([1, 12])
    with col1:
        send_clicked = st.button("Send")

    with col2:
        reset_clicked = st.button("Reset")

    # --- Send Logic ---
    if send_clicked:
        cleaned_input = user_input.strip()
        if cleaned_input:
            st.session_state.chat_history.append({"sender": "user", "message": cleaned_input})
            try:
                bot_reply = chat_with_bot(cleaned_input)
            except Exception as e:
                bot_reply = "⚠️ Sorry, there was an error getting a response. Please try again."
            st.session_state.chat_history.append({"sender": "bot", "message": bot_reply})
            if "chat_input" in st.session_state:
                del st.session_state["chat_input"]
            st.query_params["refresh"] = str(len(st.session_state.chat_history))
            st.rerun()

    # --- Reset Logic ---
    if reset_clicked:
        st.session_state.chat_history = []
        if "chat_input" in st.session_state:
            del st.session_state["chat_input"]
        st.query_params["refresh"] = "reset"
        st.rerun()