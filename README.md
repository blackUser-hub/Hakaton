<div align="center">

# Video Translation Tool

An AI-powered application that automatically translates videos to over 100 languages, making your content accessible to global audiences with just a few clicks.

[Installation](#installation) •
[How To Use](#how-to-use) •
[How It Works](#how-it-works) •
[Demo](#demo)

</div>

## About This Project

Video Translation Tool addresses a critical challenge in content creation: making videos accessible to international audiences. Traditional video translation methods are time-consuming, expensive, and require manual editing. Using cutting-edge AI technology, we automatically extract speech, transcribe it, translate the content, and generate natural-sounding voice in any target language - all while preserving your original video.

## Installation

To get Video Translation Tool running on your machine, follow these steps:

1. **Prerequisites:**
   - Python 3.8+ installed
   - FFmpeg installed (required for video processing)
     - **macOS**: `brew install ffmpeg`
     - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
     - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

2. **Clone the Repository:**
   ```bash
   git clone YOUR_GITHUB_REPO_URL
   cd autotranslate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

5. **Verification:**
   - Navigate to http://localhost:8501 in your web browser
   - You should see the Video Translation Tool interface ready to use
   - Note: The first time you load the Whisper model, it will download automatically (~150MB)

## How To Use

Translate your videos in four simple steps:

1. **Load the AI Model:**
   - Click "🔄 Load Whisper Model" in the sidebar
   - Wait for the model to load (first-time download may take a few minutes)

2. **Upload Your Video:**
   - Drag and drop or select a video file (MP4, AVI, MOV, MKV, WEBM, FLV)
   - Preview your video to ensure it uploaded correctly

3. **Select Target Language:**
   - Choose from 100+ languages using the dropdown menu
   - Options include Spanish, French, German, Japanese, Chinese, Arabic, Hindi, and many more

4. **Translate and Download:**
   - Click "🚀 Translate Video"
   - Watch real-time progress through six processing steps
   - Preview your translated video
   - Download the final result with one click

Alternatively, use the command-line interface:

```bash
python autotranslate.py input_video.mp4 -l es -o output_spanish.mp4
```

## How It Works

Video Translation Tool combines multiple AI technologies in a seamless pipeline:

```
Video File → Audio Extraction → Speech Transcription → Translation → Voice Generation → Final Video
```

**Technical Approach:**
- **Audio Extraction**: Extracts audio track from video files using MoviePy
- **Speech Transcription**: Leverages OpenAI Whisper AI to convert speech to text with high accuracy
- **Translation**: Uses Google Translate API to convert text to target language
- **Text-to-Speech**: Generates natural-sounding voice using Microsoft Edge TTS
- **Video Assembly**: Combines translated audio with original video using MoviePy

**Key Technologies:**
- `openai-whisper` - AI-powered speech recognition
- `deep-translator` - Multi-language translation
- `edge-tts` - Natural voice synthesis
- `moviepy` - Video processing and editing
- `streamlit` - Interactive web interface

## Demo

See Video Translation Tool in action:

[Watch Demo Video](screencast.mp4)

## Features

✨ **AI-Powered Translation** - Automatically translates speech to 100+ languages
🌐 **Easy Web Interface** - User-friendly Streamlit panel with drag-and-drop upload
📊 **Real-time Progress** - Track translation progress through six processing steps
🎤 **High-Quality Transcription** - Powered by OpenAI Whisper for accurate speech recognition
🔊 **Natural Voices** - Microsoft Edge TTS generates human-like speech
👁️ **Video Preview** - Preview both original and translated videos before downloading
⚡️ **Fast Processing** - Optimized pipeline for quick turnaround
📥 **One-Click Download** - Simple download interface for completed translations
💻 **Command-Line Support** - Use via CLI for automated workflows

## Supported Languages

The tool supports all languages available in Google Translate and Microsoft Edge TTS, including:

- English (en), Spanish (es), French (fr), German (de)
- Italian (it), Portuguese (pt), Russian (ru)
- Japanese (ja), Korean (ko), Chinese (zh)
- Arabic (ar), Hindi (hi), Dutch (nl)
- Polish (pl), Turkish (tr), Swedish (sv)
- And 80+ more languages...

Use standard two-letter language codes (ISO 639-1).

## Use Cases

- **Content Creators**: Reach international audiences by translating YouTube videos, tutorials, and educational content
- **Educators**: Make courses accessible to students worldwide with multilingual lecture translations
- **Businesses**: Translate corporate presentations, training materials, and marketing videos for global markets
- **Non-Profits**: Break down language barriers and make information accessible across cultures
- **Personal Projects**: Translate family videos, personal recordings, or any content for friends and family abroad

## Troubleshooting

**FFmpeg not found:**
- Ensure FFmpeg is installed and in your system PATH
- Verify installation: `ffmpeg -version`

**Model download issues:**
- Whisper models download automatically on first use
- Ensure stable internet connection and sufficient disk space (~150MB for base model)
- If SSL certificate errors occur, the tool handles them automatically

**Memory issues with large videos:**
- Process videos in shorter segments
- Use a smaller Whisper model (modify code: change `"base"` to `"tiny"` or `"small"`)

**Processing time:**
- Processing time depends on video length and system capabilities
- Expect 2-5 minutes for a 1-minute video on average hardware
- Large videos (10+ minutes) may take significantly longer

## License

See LICENSE file for details.

## Contact

For questions about this project, please open an issue in this repository.

---
