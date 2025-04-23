from gtts import gTTS
import io


def generate_tts_audio_bytes(text: str):
    if not text.strip():
        raise ValueError("Text is empty. Cannot generate speech.")
    tts = gTTS(text=text, lang='fr')
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

