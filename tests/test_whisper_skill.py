"""Unit tests for WhisperSkill class"""

import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
from pathlib import Path

try:
    from whisper_skill import WhisperSkill, TranscriptionError
except ImportError:
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from whisper_skill import WhisperSkill, TranscriptionError


class TestWhisperSkillInit(unittest.TestCase):
    """Test WhisperSkill initialization"""
    
    @patch('whisper_skill.whisper.load_model')
    def test_init_with_valid_model(self, mock_load):
        """Test initialization with valid model"""
        mock_load.return_value = MagicMock()
        skill = WhisperSkill(model='base')
        self.assertEqual(skill.model_name, 'base')
        mock_load.assert_called_once()
    
    def test_init_with_invalid_model(self):
        """Test initialization with invalid model raises ValueError"""
        with self.assertRaises(ValueError):
            WhisperSkill(model='invalid_model')
    
    @patch('whisper_skill.whisper.load_model')
    def test_device_detection(self, mock_load):
        """Test automatic device detection"""
        mock_load.return_value = MagicMock()
        skill = WhisperSkill()
        self.assertIn(skill.device, ['cuda', 'cpu'])


class TestAudioValidation(unittest.TestCase):
    """Test audio file validation"""
    
    @patch('whisper_skill.whisper.load_model')
    def setUp(self, mock_load):
        """Set up test fixtures"""
        mock_load.return_value = MagicMock()
        self.skill = WhisperSkill()
    
    def test_validate_nonexistent_file(self):
        """Test validation of non-existent file"""
        with self.assertRaises(FileNotFoundError):
            self.skill._validate_audio_file('nonexistent_file.mp3')
    
    def test_validate_existing_file(self):
        """Test validation of existing file"""
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            temp_path = f.name
        
        try:
            result = self.skill._validate_audio_file(temp_path)
            self.assertIsInstance(result, Path)
        finally:
            os.unlink(temp_path)


class TestInputValidation(unittest.TestCase):
    """Test input parameter validation"""
    
    @patch('whisper_skill.whisper.load_model')
    def setUp(self, mock_load):
        """Set up test fixtures"""
        mock_load.return_value = MagicMock()
        self.skill = WhisperSkill()
    
    def test_invalid_task(self):
        """Test invalid task parameter"""
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            temp_path = f.name
        
        try:
            with self.assertRaises(ValueError):
                self.skill.transcribe(temp_path, task='invalid')
        finally:
            os.unlink(temp_path)
    
    def test_invalid_temperature(self):
        """Test invalid temperature parameter"""
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            temp_path = f.name
        
        try:
            with self.assertRaises(ValueError):
                self.skill.transcribe(temp_path, temperature=1.5)
        finally:
            os.unlink(temp_path)


class TestOutputFormatting(unittest.TestCase):
    """Test output formatting methods"""
    
    @patch('whisper_skill.whisper.load_model')
    def setUp(self, mock_load):
        """Set up test fixtures"""
        mock_load.return_value = MagicMock()
        self.skill = WhisperSkill()
        self.sample_result = {
            'text': 'Hello world',
            'language': 'en',
            'duration': 5.0,
            'segments': [
                {'start': 0.0, 'end': 2.5, 'text': 'Hello'},
                {'start': 2.5, 'end': 5.0, 'text': 'world'}
            ]
        }
    
    def test_save_to_file(self):
        """Test saving to text file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_path = f.name
        
        try:
            self.skill.save_to_file(self.sample_result, temp_path)
            with open(temp_path, 'r') as f:
                content = f.read()
            self.assertIn('Hello world', content)
        finally:
            os.unlink(temp_path)
    
    def test_seconds_to_timestamp(self):
        """Test timestamp conversion"""
        timestamp = self.skill._seconds_to_timestamp(65.5)
        self.assertEqual(timestamp, '00:01:05.500')


if __name__ == '__main__':
    unittest.main()
