import speech_recognition as sr
import librosa
import numpy as np
import tempfile
from typing import Dict, Optional
import aiofiles

from app.services.sentiment_service import SentimentService

class VoiceService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    async def speech_to_text(self, audio_path: str, language: str = "en-US") -> str:
        """Convert speech to text using speech recognition"""
        try:
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
                
                # Recognize speech
                text = self.recognizer.recognize_google(audio, language=language)
                return text
                
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Speech recognition service error: {e}"
    
    async def analyze_sentiment_from_audio(self, audio_path: str, language: str = "auto") -> Dict:
        """Extract text from audio and analyze sentiment"""
        # Convert speech to text
        transcribed_text = await self.speech_to_text(audio_path, language)
        
        if not transcribed_text or transcribed_text.startswith("Could not"):
            return {
                "error": "Failed to transcribe audio",
                "transcribed_text": transcribed_text
            }
        
        # Analyze sentiment of transcribed text
        sentiment = await SentimentService.analyze(transcribed_text)
        
        return {
            "transcribed_text": transcribed_text,
            "sentiment": sentiment["sentiment"],
            "confidence": sentiment["confidence"],
            "probabilities": sentiment["probabilities"]
        }
    
    async def analyze_voice_tone(self, audio_path: str) -> Dict:
        """Analyze voice tone features (pitch, energy, speaking rate)"""
        # Load audio file
        y, sr = librosa.load(audio_path, sr=None)
        
        # Extract features
        # Pitch (fundamental frequency)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[pitches > 0]
        avg_pitch = np.mean(pitch_values) if len(pitch_values) > 0 else 0
        
        # Energy (RMS)
        rms = librosa.feature.rms(y=y)
        avg_energy = np.mean(rms)
        
        # Speaking rate (estimated)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        # Zero crossing rate (for noise/emotion detection)
        zcr = librosa.feature.zero_crossing_rate(y)
        avg_zcr = np.mean(zcr)
        
        # Determine emotional state based on features
        tone_emotion = self._classify_tone(avg_pitch, avg_energy, avg_zcr)
        
        return {
            "average_pitch_hz": float(avg_pitch),
            "average_energy": float(avg_energy),
            "estimated_tempo_bpm": float(tempo),
            "zero_crossing_rate": float(avg_zcr),
            "dominant_tone": tone_emotion["emotion"],
            "tone_confidence": tone_emotion["confidence"],
            "tone_description": tone_emotion["description"]
        }
    
    def _classify_tone(self, pitch: float, energy: float, zcr: float) -> Dict:
        """Classify tone emotion based on audio features"""
        # Heuristic rules for tone classification
        if pitch > 200 and energy > 0.1:
            return {
                "emotion": "excited",
                "confidence": min(0.9, (pitch / 500) * 0.5 + energy),
                "description": "High-energy, enthusiastic tone"
            }
        elif pitch < 120 and energy < 0.05:
            return {
                "emotion": "calm",
                "confidence": min(0.8, 1 - (pitch / 200) + (1 - energy)),
                "description": "Relaxed, peaceful tone"
            }
        elif energy > 0.15 and zcr > 0.1:
            return {
                "emotion": "angry",
                "confidence": min(0.85, energy + zcr),
                "description": "Intense, aggressive tone"
            }
        elif pitch < 100 and zcr < 0.05:
            return {
                "emotion": "sad",
                "confidence": min(0.7, 1 - (pitch / 150)),
                "description": "Low-energy, melancholic tone"
            }
        else:
            return {
                "emotion": "neutral",
                "confidence": 0.6,
                "description": "Balanced, neutral tone"
            }
    
    async def record_audio(self, duration: int = 5) -> Optional[str]:
        """Record audio from microphone"""
        try:
            import pyaudio
            import wave
            
            # Audio recording parameters
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            CHUNK = 1024
            
            audio = pyaudio.PyAudio()
            
            # Start recording
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                               rate=RATE, input=True,
                               frames_per_buffer=CHUNK)
            
            frames = []
            
            for _ in range(0, int(RATE / CHUNK * duration)):
                data = stream.read(CHUNK)
                frames.append(data)
            
            # Stop recording
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            with wave.open(temp_file.name, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
            
            return temp_file.name
            
        except Exception as e:
            print(f"Recording error: {e}")
            return None