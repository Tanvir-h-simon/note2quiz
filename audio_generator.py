from gtts import gTTS # Google Text-To-Speech
from io import BytesIO
import re

def generate_audio(notes):

    # Removing Markdown symbols so they are not read aloud
    text = re.sub(r"[#*_`>]", "", notes)
    text = re.sub(r"^\s*[-+]\s+", "", text, flags=re.MULTILINE)

    audio = BytesIO()
    gTTS(text=text, lang='en').write_to_fp(audio)

    return audio.getvalue()