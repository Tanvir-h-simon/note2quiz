import streamlit as st
from note_generator import generate_note
from audio_generator import generate_audio
from quiz_generator import generate_quiz

st.set_page_config(page_title="Note2Quiz", page_icon=":material/quiz:")

# --- Session state ---
# Results are saved here so they stay on screen when the quiz is answered
if "quiz_id" not in st.session_state:
    st.session_state.quiz_id = 0

st.title("Note summarizer and quiz generator")
st.markdown("Upload photos of your notes to get a short summary, an audio version of it, and a quiz to test yourself.")
st.divider()

with st.sidebar:
    st.header("Instructions")

    # --- Files ---
    files = st.file_uploader(
        "Upload the photos of your note",
        type = ['jpg', 'jpeg', 'png', 'pdf'],
        accept_multiple_files = True
    )

    too_many_files = len(files) > 3

    if files:
        if too_many_files:
            st.error("Upload at max 3 files")
        else:
            st.subheader("Uploaded files")
            col = st.columns(len(files))

            for i, file in enumerate(files):
                with col[i]:
                    if file.type == "application/pdf":
                        st.caption(f":material/picture_as_pdf: {file.name}")
                    else:
                        st.image(file, alt=f"Uploaded note {i + 1}")

    # --- Quiz Difficulty ---
    difficulty_level = st.segmented_control(
        "Select the difficulty of the quiz",
        ['Easy', 'Medium', 'Hard']
    )

    pressed = st.button("Submit", type='primary', icon=":material/auto_awesome:", width="stretch")

if pressed:
    if not files:
        st.error("You must upload at least 1 file")
    if not difficulty_level:
        st.error("You must select the difficulty level")

    if files and difficulty_level and not too_many_files:
        try:
            with st.spinner("Reading your notes..."):
                st.session_state.notes = generate_note(files)

            with st.spinner("Creating the audio..."):
                st.session_state.audio = generate_audio(st.session_state.notes)

            with st.spinner("Writing your quiz..."):
                st.session_state.quiz = generate_quiz(st.session_state.notes, difficulty_level)

            st.session_state.difficulty = difficulty_level
            # A new id gives the quiz fresh radio buttons, so old answers don't carry over
            st.session_state.quiz_id += 1
        except Exception as e:
            st.error(f"Something went wrong while talking to Gemini: {e}", title="Generation failed")

if "quiz" not in st.session_state:
    st.info("Upload your notes and choose a difficulty from the sidebar, then press **Submit**.", icon=":material/arrow_back:")
else:
    # --- Note ---
    with st.container(border=True):
        st.subheader(":material/description: Your note")
        st.markdown(st.session_state.notes)

    # --- Audio transcript ---
    with st.container(border=True):
        st.subheader(":material/headphones: Audio transcription")
        st.audio(st.session_state.audio, format="audio/mp3", alt="Audio reading of your note")
        st.download_button(
            "Download audio",
            data=st.session_state.audio,
            file_name="note.mp3",
            mime="audio/mp3",
            icon=":material/download:"
        )

    # --- Quiz ---
    with st.container(border=True):
        st.subheader(f":material/quiz: Quiz level: {st.session_state.difficulty}")
        quiz = st.session_state.quiz
        quiz_id = st.session_state.quiz_id

        with st.form(f"quiz_form_{quiz_id}"):
            for i, q in enumerate(quiz):
                st.radio(f"**{i + 1}. {q.question}**", q.options, index=None, key=f"q_{quiz_id}_{i}")

            checked = st.form_submit_button("Check answers", type="primary")

        if checked:
            score = 0

            for i, q in enumerate(quiz):
                chosen = st.session_state[f"q_{quiz_id}_{i}"]

                if chosen == q.answer:
                    score += 1
                    st.success(q.explanation, title=f"{i + 1}. Correct")
                elif chosen is None:
                    st.warning(f"Answer: **{q.answer}**. {q.explanation}", title=f"{i + 1}. Not answered")
                else:
                    st.error(f"Answer: **{q.answer}**. {q.explanation}", title=f"{i + 1}. Wrong")

            st.metric("Your score", f"{score} / {len(quiz)}")

            if score == len(quiz):
                st.balloons()
