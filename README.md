# Note2Quiz

Turn photos of your handwritten or printed notes into a short summary, an audio version you can listen to, and a quiz to test yourself.

Built with [Streamlit](https://streamlit.io) and Google's [Gemini API](https://ai.google.dev).

## Features

- **Note summary**: upload up to 3 images or PDFs of your notes and get a clear summary in under 100 words, organized with headings and bullet points.
- **Audio transcription**: listen to the summary in the browser, or download it as an MP3.
- **Quiz generator**: get 5 multiple-choice questions at the difficulty you choose (Easy, Medium or Hard). Check your answers to see your score, the correct answers and a short explanation for each question.

## How it works

1. Your uploaded files are sent to Gemini, which reads them and writes the summary.
2. The summary is converted to speech with [gTTS](https://pypi.org/project/gTTS/) (Google Text-to-Speech).
3. Gemini creates a quiz from the summary and returns it as structured data, which the app shows as an interactive form.

## Project structure

```
note2quiz/
├── app.py               # Streamlit interface
├── gemini_client.py     # Loads the API key and sets up the Gemini client
├── note_generator.py    # Summarizes the uploaded notes
├── audio_generator.py   # Turns the summary into audio
├── quiz_generator.py    # Creates the quiz
└── requirements.txt     # Python dependencies
```

## Getting started

### Prerequisites

- Python 3.10 or newer
- A Gemini API key. You can get one for free from [Google AI Studio](https://aistudio.google.com/apikey).

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Tanvir-h-simon/note2quiz.git
   cd note2quiz
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

   On macOS or Linux:

   ```bash
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a file named `.env` in the project folder and add your API key:

   ```
   GEMINI_API_KEY=your_api_key_here
   ```

   `.env` is listed in `.gitignore`, so your key will not be committed.

### Run the app

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

## Usage

1. Upload 1 to 3 photos or PDFs of your notes from the sidebar.
2. Choose a quiz difficulty.
3. Press **Submit**.
4. Read your summary, play the audio, then answer the quiz and press **Check answers** to see your score.

## Configuration

The Gemini model is set in `gemini_client.py`:

```python
MODEL = 'gemini-3.8-flash'
```

Change it to any Gemini model that supports image input.
