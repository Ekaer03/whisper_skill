"""
Whisper Skill - Audio Transcription using OpenAI's Whisper Model

This module provides a skill for automatic speech recognition and audio transcription.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import warnings

try:
    import whisper
except ImportError:
    raise ImportError(
        "Please install openai-whisper: pip install openai-whisper"
    )

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TranscriptionError(Exception):
    """Custom exception for transcription errors"""
    pass


class WhisperSkill:
    """
    A skill for audio transcription using OpenAI's Whisper model.
    
    Attributes:
        model_name (str): Name of the Whisper model to use
        device (str): Device to use for inference ('cuda' or 'cpu')
        model: Loaded Whisper model
    """
    
    SUPPORTED_FORMATS = {
        '.mp3', '.wav', '.flac', '.ogg', '.m4a', 
        '.webm', '.aac', '.opus', '.vorbis'
    }
    
    AVAILABLE_MODELS = ['tiny', 'base', 'small', 'medium', 'large']
    
    def __init__(
        self, 
        model: str = 'base',
        device: Optional[str] = None
    ):
        """
        Initialize the Whisper Skill.
        
        Args:
            model (str): Model size - 'tiny', 'base', 'small', 'medium', or 'large'
            device (str): Device to use - 'cuda', 'cpu', or None for auto-detection
            
        Raises:
            ValueError: If model name is invalid
        """
        if model not in self.AVAILABLE_MODELS:
            raise ValueError(
                f"Model must be one of {self.AVAILABLE_MODELS}, got {model}"
            )
        
        self.model_name = model
        self.device = device or self._detect_device()
        
        logger.info(f"Loading Whisper model: {model}")
        logger.info(f"Using device: {self.device}")
        
        try:
            self.model = whisper.load_model(
                model, 
                device=self.device,
                download_root=os.getenv('WHISPER_MODEL_DIR')
            )
            logger.info(f"Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise TranscriptionError(f"Failed to load Whisper model: {e}")
    
    @staticmethod
    def _detect_device() -> str:
        """
        Auto-detect the best device to use.
        
        Returns:
            str: 'cuda' if available, otherwise 'cpu'
        """
        try:
            import torch
            if torch.cuda.is_available():
                logger.info("CUDA detected, using GPU")
                return 'cuda'
        except ImportError:
            pass
        
        logger.info("Using CPU for inference")
        return 'cpu'
    
    def _validate_audio_file(self, audio_file: str) -> Path:
        """
        Validate that the audio file exists and has a supported format.
        
        Args:
            audio_file (str): Path to audio file
            
        Returns:
            Path: Path object of the audio file
            
        Raises:
            FileNotFoundError: If file doesn't exist
            TranscriptionError: If file format is not supported
        """
        path = Path(audio_file)
        
        if not path.exists():
            logger.error(f"Audio file not found: {audio_file}")
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            logger.warning(
                f"Unsupported format {path.suffix}. "
                f"Supported formats: {self.SUPPORTED_FORMATS}"
            )
            # Allow attempt anyway, ffmpeg might handle it
        
        return path
    
    def transcribe(
        self,
        audio_file: str,
        language: Optional[str] = None,
        task: str = 'transcribe',
        temperature: float = 0.0,
        verbose: bool = False
    ) -> Dict[str, Any]:
        """
        Transcribe an audio file.
        
        Args:
            audio_file (str): Path to audio file
            language (str): ISO-639-1 language code (e.g., 'en', 'es', 'fr')
            task (str): 'transcribe' for transcription or 'translate' for translation
            temperature (float): Sampling temperature between 0 and 1
            verbose (bool): Whether to print processing messages
            
        Returns:
            dict: Dictionary containing:
                - text: Full transcribed text
                - language: Detected or specified language
                - duration: Audio duration in seconds
                - segments: List of segments with timestamps and text
                
        Raises:
            FileNotFoundError: If audio file doesn't exist
            TranscriptionError: If transcription fails
        """
        # Validate inputs
        self._validate_audio_file(audio_file)
        
        if task not in ['transcribe', 'translate']:
            raise ValueError(f"Task must be 'transcribe' or 'translate', got {task}")
        
        if not 0 <= temperature <= 1:
            raise ValueError(f"Temperature must be between 0 and 1, got {temperature}")
        
        logger.info(f"Starting transcription of {audio_file}")
        logger.info(f"Task: {task}, Language: {language or 'auto-detect'}")
        
        try:
            # Transcribe with Whisper
            result = self.model.transcribe(
                audio_file,
                language=language,
                task=task,
                temperature=temperature,
                verbose=verbose
            )
            
            logger.info(
                f"Transcription completed. "
                f"Duration: {result.get('duration', 'unknown')}s, "
                f"Language: {result.get('language', 'unknown')}"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise TranscriptionError(f"Transcription failed: {e}")
    
    def transcribe_batch(
        self,
        audio_files: List[str],
        language: Optional[str] = None,
        task: str = 'transcribe'
    ) -> Dict[str, Dict[str, Any]]:
        """
        Transcribe multiple audio files.
        
        Args:
            audio_files (list): List of paths to audio files
            language (str): ISO-639-1 language code
            task (str): 'transcribe' or 'translate'
            
        Returns:
            dict: Dictionary mapping filenames to transcription results
        """
        results = {}
        
        logger.info(f"Starting batch transcription of {len(audio_files)} files")
        
        for i, audio_file in enumerate(audio_files, 1):
            try:
                logger.info(f"Processing {i}/{len(audio_files)}: {audio_file}")
                result = self.transcribe(
                    audio_file,
                    language=language,
                    task=task
                )
                results[audio_file] = result
                
            except (FileNotFoundError, TranscriptionError) as e:
                logger.warning(f"Skipped {audio_file}: {e}")
                results[audio_file] = {'error': str(e)}
        
        logger.info(f"Batch transcription completed")
        return results
    
    def save_to_file(
        self,
        result: Dict[str, Any],
        output_path: str,
        include_segments: bool = False
    ) -> None:
        """
        Save transcription result to a text file.
        
        Args:
            result (dict): Transcription result from transcribe()
            output_path (str): Path to save the text file
            include_segments (bool): Whether to include segment timestamps
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                if include_segments and 'segments' in result:
                    for segment in result['segments']:
                        start = segment['start']
                        end = segment['end']
                        text = segment['text'].strip()
                        f.write(f"[{start:.2f}s - {end:.2f}s] {text}\n")
                else:
                    f.write(result.get('text', ''))
            
            logger.info(f"Transcription saved to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to save to file: {e}")
            raise TranscriptionError(f"Failed to save to file: {e}")
    
    def save_to_json(
        self,
        result: Dict[str, Any],
        output_path: str,
        pretty: bool = True
    ) -> None:
        """
        Save transcription result to a JSON file.
        
        Args:
            result (dict): Transcription result from transcribe()
            output_path (str): Path to save the JSON file
            pretty (bool): Whether to format JSON with indentation
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(
                    result,
                    f,
                    indent=2 if pretty else None,
                    ensure_ascii=False
                )
            
            logger.info(f"Transcription saved to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to save to JSON: {e}")
            raise TranscriptionError(f"Failed to save to JSON: {e}")
    
    def get_segments_as_vtt(self, result: Dict[str, Any]) -> str:
        """
        Convert transcription segments to WebVTT format.
        
        Args:
            result (dict): Transcription result from transcribe()
            
        Returns:
            str: WebVTT format string
        """
        vtt_lines = ['WEBVTT\n']
        
        if 'segments' not in result:
            return ''.join(vtt_lines)
        
        for segment in result['segments']:
            start = self._seconds_to_timestamp(segment['start'])
            end = self._seconds_to_timestamp(segment['end'])
            text = segment['text'].strip()
            
            vtt_lines.append(f"{start} --> {end}\n")
            vtt_lines.append(f"{text}\n\n")
        
        return ''.join(vtt_lines)
    
    def save_to_vtt(self, result: Dict[str, Any], output_path: str) -> None:
        """
        Save transcription as WebVTT subtitle file.
        
        Args:
            result (dict): Transcription result from transcribe()
            output_path (str): Path to save the VTT file
        """
        try:
            vtt_content = self.get_segments_as_vtt(result)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(vtt_content)
            
            logger.info(f"WebVTT file saved to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to save VTT file: {e}")
            raise TranscriptionError(f"Failed to save VTT file: {e}")
    
    @staticmethod
    def _seconds_to_timestamp(seconds: float) -> str:
        """
        Convert seconds to HH:MM:SS.mmm format.
        
        Args:
            seconds (float): Time in seconds
            
        Returns:
            str: Timestamp in HH:MM:SS.mmm format
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the current skill configuration.
        
        Returns:
            dict: Configuration information
        """
        return {
            'model': self.model_name,
            'device': self.device,
            'supported_formats': list(self.SUPPORTED_FORMATS),
            'available_models': self.AVAILABLE_MODELS
        }


if __name__ == "__main__":
    # Example usage
    print("Whisper Skill - Audio Transcription\n")
    
    # Initialize
    skill = WhisperSkill(model='base')
    
    print("Skill Info:")
    print(json.dumps(skill.get_info(), indent=2))
