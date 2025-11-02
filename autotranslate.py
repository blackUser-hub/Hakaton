#!/usr/bin/env python3
"""
Video Translation Tool
Translates videos by extracting audio, transcribing, translating, and generating new audio.
"""

import os
import sys
import argparse
from pathlib import Path
import whisper
from deep_translator import GoogleTranslator
import edge_tts
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip
import tempfile
import ssl
import urllib.request


class VideoTranslator:
    """Main class for translating videos"""
    
    def __init__(self):
        self.model = None
        self.temp_dir = None
        
    def load_model(self):
        """Load Whisper model for transcription"""
        print("Loading Whisper model...")
        
        # Handle SSL certificate verification issues
        # This is needed when there are self-signed certificates or corporate firewalls
        original_ssl_context = ssl._create_default_https_context
        ssl._create_default_https_context = ssl._create_unverified_context
        
        try:
            self.model = whisper.load_model("base")
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
        finally:
            # Restore original SSL context
            ssl._create_default_https_context = original_ssl_context
        
    def extract_audio(self, video_path):
        """Extract audio from video file"""
        print(f"Extracting audio from {video_path}...")
        video = VideoFileClip(video_path)
        audio_path = os.path.join(self.temp_dir, "original_audio.wav")
        video.audio.write_audiofile(audio_path, logger=None)
        video.close()
        print("Audio extracted successfully!")
        return audio_path
    
    def transcribe_audio(self, audio_path):
        """Transcribe audio to text using Whisper"""
        print("Transcribing audio...")
        result = self.model.transcribe(audio_path)
        text = result["text"]
        segments = result["segments"]
        print(f"Transcription completed: {len(segments)} segments found")
        return text, segments
    
    def translate_text(self, text, target_language):
        """Translate text to target language"""
        print(f"Translating to {target_language}...")
        try:
            translator = GoogleTranslator(source="auto", target=target_language)
            translated_text = translator.translate(text)
            print("Translation completed!")
            return translated_text
        except Exception as e:
            print(f"Translation error: {e}")
            sys.exit(1)
    
    async def generate_audio(self, text, target_language, output_path):
        """Generate audio from translated text using Edge TTS"""
        print(f"Generating audio in {target_language}...")
        
        # Map language codes to Edge TTS voice names
        voice_map = {
            "en": "en-US-AriaNeural",
            "es": "es-ES-ElviraNeural",
            "fr": "fr-FR-DeniseNeural",
            "de": "de-DE-KatjaNeural",
            "it": "it-IT-ElsaNeural",
            "pt": "pt-BR-FranciscaNeural",
            "ru": "ru-RU-SvetlanaNeural",
            "ja": "ja-JP-NanamiNeural",
            "ko": "ko-KR-SunHiNeural",
            "zh": "zh-CN-XiaoxiaoNeural",
            "ar": "ar-SA-ZariyahNeural",
            "hi": "hi-IN-SwaraNeural",
            "nl": "nl-NL-ColetteNeural",
            "pl": "pl-PL-AgnieszkaNeural",
            "tr": "tr-TR-EmelNeural",
        }
        
        # Get language code (first 2 characters)
        lang_code = target_language[:2].lower() if len(target_language) >= 2 else target_language.lower()
        
        # Default voice or get from map
        voice = voice_map.get(lang_code, "en-US-AriaNeural")
        
        # If exact match not found, try to find similar
        if voice == "en-US-AriaNeural" and lang_code not in voice_map:
            # Try to find a voice that starts with the language code
            communicate = edge_tts.Communicate(text, voice)
            # Get available voices and find one matching the language
            voices = await edge_tts.list_voices()
            matching_voices = [v for v in voices if v["Locale"].startswith(lang_code)]
            if matching_voices:
                voice = matching_voices[0]["ShortName"]
            else:
                print(f"Warning: Using default English voice for {target_language}")
        
        print(f"Using voice: {voice}")
        
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        print("Audio generated successfully!")
    
    def create_translated_video(self, original_video_path, new_audio_path, output_path):
        """Combine original video with new translated audio"""
        print("Creating translated video...")
        video = VideoFileClip(original_video_path)
        new_audio = AudioFileClip(new_audio_path)
        
        # Replace audio
        final_video = video.set_audio(new_audio)
        
        # Write output video
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=os.path.join(self.temp_dir, "temp_audio.m4a"),
            remove_temp=True,
            logger=None
        )
        
        video.close()
        new_audio.close()
        final_video.close()
        print("Translated video created successfully!")
    
    def translate_video(self, video_path, target_language, output_path):
        """Main method to translate video"""
        try:
            # Create temp directory
            self.temp_dir = tempfile.mkdtemp()
            print(f"Using temporary directory: {self.temp_dir}")
            
            # Step 1: Load model
            if not self.model:
                self.load_model()
            
            # Step 2: Extract audio
            audio_path = self.extract_audio(video_path)
            
            # Step 3: Transcribe
            text, segments = self.transcribe_audio(audio_path)
            print(f"Original text: {text[:100]}..." if len(text) > 100 else f"Original text: {text}")
            
            # Step 4: Translate
            translated_text = self.translate_text(text, target_language)
            print(f"Translated text: {translated_text[:100]}..." if len(translated_text) > 100 else f"Translated text: {translated_text}")
            
            # Step 5: Generate new audio
            new_audio_path = os.path.join(self.temp_dir, "translated_audio.mp3")
            asyncio.run(self.generate_audio(translated_text, target_language, new_audio_path))
            
            # Step 6: Create final video
            self.create_translated_video(video_path, new_audio_path, output_path)
            
            # Cleanup
            print(f"Cleaning up temporary files...")
            import shutil
            shutil.rmtree(self.temp_dir)
            
            print(f"\n✅ Success! Translated video saved to: {output_path}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Translate videos to different languages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python autotranslate.py input.mp4 -l es -o output_spanish.mp4
  python autotranslate.py video.mov -l fr -o video_french.mov
  python autotranslate.py clip.avi -l ja
        """
    )
    
    parser.add_argument(
        "input",
        help="Path to input video file"
    )
    
    parser.add_argument(
        "-l", "--language",
        required=True,
        help="Target language code (e.g., 'es' for Spanish, 'fr' for French, 'de' for German)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Path to output video file (default: input_filename_translated_language.ext)"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input):
        print(f"❌ Error: Input file '{args.input}' not found!")
        sys.exit(1)
    
    # Generate output filename if not provided
    if not args.output:
        input_path = Path(args.input)
        output_path = input_path.parent / f"{input_path.stem}_translated_{args.language}{input_path.suffix}"
    else:
        output_path = Path(args.output)
    
    # Create translator and process video
    translator = VideoTranslator()
    translator.translate_video(
        str(args.input),
        args.language,
        str(output_path)
    )


if __name__ == "__main__":
    main()

