#!/usr/bin/env python3
"""
Web Panel for Video Translation Tool
Streamlit web interface for translating videos
"""

import streamlit as st
import os
import tempfile
import shutil
from pathlib import Path
from autotranslate import VideoTranslator
import time

# Page configuration
st.set_page_config(
    page_title="Video Translation Tool",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'translator' not in st.session_state:
    st.session_state.translator = None
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Header
st.markdown('<p class="main-header">🌍 Video Translation Tool</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Translate videos to different languages using AI</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model loading
    if st.button("🔄 Load Whisper Model", disabled=st.session_state.model_loaded):
        with st.spinner("Loading Whisper model (this may take a minute on first run)..."):
            if st.session_state.translator is None:
                st.session_state.translator = VideoTranslator()
            st.session_state.translator.load_model()
            st.session_state.model_loaded = True
            st.success("Model loaded!")
            st.rerun()
    
    if st.session_state.model_loaded:
        st.success("✅ Model is loaded and ready!")
    
    st.markdown("---")
    
    # Supported languages info
    st.subheader("📚 Supported Languages")
    st.markdown("""
    The tool supports all languages available in Google Translate, including:
    - English (en)
    - Spanish (es)
    - French (fr)
    - German (de)
    - Italian (it)
    - Portuguese (pt)
    - Russian (ru)
    - Japanese (ja)
    - Korean (ko)
    - Chinese (zh)
    - Arabic (ar)
    - Hindi (hi)
    - And many more...
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    1. Load the model first before uploading
    2. Processing time depends on video length
    3. The first run downloads the model (~150MB)
    4. Large videos may take several minutes
    """)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload Video")
    uploaded_file = st.file_uploader(
        "Choose a video file",
        type=['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv'],
        help="Supported formats: MP4, AVI, MOV, MKV, WEBM, FLV"
    )
    
    if uploaded_file is not None:
        # Display video info
        file_details = {
            "Filename": uploaded_file.name,
            "FileType": uploaded_file.type,
            "FileSize": f"{uploaded_file.size / (1024*1024):.2f} MB"
        }
        st.write("**Video Details:**")
        st.json(file_details)
        
        # Preview video
        st.video(uploaded_file)

with col2:
    st.header("⚙️ Translation Settings")
    
    # Language selection
    target_language = st.selectbox(
        "Select Target Language",
        options=[
            "es", "fr", "de", "it", "pt", "ru", "ja", "ko", 
            "zh", "ar", "hi", "nl", "pl", "tr", "en", "sv", 
            "no", "da", "fi", "cs", "hu", "ro", "el", "he"
        ],
        format_func=lambda x: {
            "es": "🇪🇸 Spanish",
            "fr": "🇫🇷 French",
            "de": "🇩🇪 German",
            "it": "🇮🇹 Italian",
            "pt": "🇵🇹 Portuguese",
            "ru": "🇷🇺 Russian",
            "ja": "🇯🇵 Japanese",
            "ko": "🇰🇷 Korean",
            "zh": "🇨🇳 Chinese",
            "ar": "🇸🇦 Arabic",
            "hi": "🇮🇳 Hindi",
            "nl": "🇳🇱 Dutch",
            "pl": "🇵🇱 Polish",
            "tr": "🇹🇷 Turkish",
            "en": "🇬🇧 English",
            "sv": "🇸🇪 Swedish",
            "no": "🇳🇴 Norwegian",
            "da": "🇩🇰 Danish",
            "fi": "🇫🇮 Finnish",
            "cs": "🇨🇿 Czech",
            "hu": "🇭🇺 Hungarian",
            "ro": "🇷🇴 Romanian",
            "el": "🇬🇷 Greek",
            "he": "🇮🇱 Hebrew"
        }.get(x, x)
    )
    
    st.markdown(f"**Selected:** {target_language.upper()}")

# Translation button and processing
st.markdown("---")

if uploaded_file is not None and target_language:
    if st.button("🚀 Translate Video", type="primary", disabled=st.session_state.processing or not st.session_state.model_loaded):
        if not st.session_state.model_loaded:
            st.error("⚠️ Please load the Whisper model first using the sidebar button!")
        else:
            st.session_state.processing = True
            
            # Create temporary file for uploaded video
            temp_dir = tempfile.mkdtemp()
            temp_video_path = os.path.join(temp_dir, uploaded_file.name)
            
            # Save uploaded file
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Prepare output path
            input_path = Path(uploaded_file.name)
            output_filename = f"{input_path.stem}_translated_{target_language}{input_path.suffix}"
            temp_output_path = os.path.join(temp_dir, output_filename)
            
            try:
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Initialize translator if needed
                if st.session_state.translator is None:
                    st.session_state.translator = VideoTranslator()
                    if not st.session_state.model_loaded:
                        st.session_state.translator.load_model()
                        st.session_state.model_loaded = True
                
                translator = st.session_state.translator
                
                # Process video with progress updates
                status_text.text("Step 1/6: Extracting audio from video...")
                progress_bar.progress(10)
                translator.temp_dir = temp_dir
                audio_path = translator.extract_audio(temp_video_path)
                
                status_text.text("Step 2/6: Transcribing audio to text...")
                progress_bar.progress(30)
                text, segments = translator.transcribe_audio(audio_path)
                
                # Show transcription
                with st.expander("📝 View Transcription", expanded=False):
                    st.write("**Original Text:**")
                    st.write(text[:500] + "..." if len(text) > 500 else text)
                    st.write(f"\n**Total segments:** {len(segments)}")
                
                status_text.text("Step 3/6: Translating text...")
                progress_bar.progress(50)
                translated_text = translator.translate_text(text, target_language)
                
                # Show translation
                with st.expander("🌍 View Translation", expanded=False):
                    st.write("**Translated Text:**")
                    st.write(translated_text[:500] + "..." if len(translated_text) > 500 else translated_text)
                
                status_text.text("Step 4/6: Generating translated audio...")
                progress_bar.progress(70)
                import asyncio
                new_audio_path = os.path.join(temp_dir, "translated_audio.mp3")
                asyncio.run(translator.generate_audio(translated_text, target_language, new_audio_path))
                
                status_text.text("Step 5/6: Creating translated video...")
                progress_bar.progress(85)
                translator.create_translated_video(temp_video_path, new_audio_path, temp_output_path)
                
                status_text.text("Step 6/6: Finalizing...")
                progress_bar.progress(100)
                
                # Read output video
                if os.path.exists(temp_output_path):
                    with open(temp_output_path, "rb") as f:
                        video_bytes = f.read()
                    
                    # Success message
                    st.success("✅ Translation completed successfully!")
                    
                    # Display translated video
                    st.header("📹 Translated Video")
                    st.video(video_bytes)
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Translated Video",
                        data=video_bytes,
                        file_name=output_filename,
                        mime="video/mp4",
                        type="primary"
                    )
                    
                    # Cleanup
                    shutil.rmtree(temp_dir)
                else:
                    st.error("❌ Output file not found. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ Error during translation: {str(e)}")
                import traceback
                with st.expander("🔍 Error Details"):
                    st.code(traceback.format_exc())
                # Cleanup on error
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            finally:
                st.session_state.processing = False
                progress_bar.empty()
                status_text.empty()

elif uploaded_file is None:
    st.info("👆 Please upload a video file to get started!")
elif not target_language:
    st.info("👆 Please select a target language!")
elif not st.session_state.model_loaded:
    st.warning("⚠️ Please load the Whisper model first using the button in the sidebar!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Video Translation Tool - Powered by OpenAI Whisper, Google Translate, and Microsoft Edge TTS</p>
    </div>
    """,
    unsafe_allow_html=True
)


