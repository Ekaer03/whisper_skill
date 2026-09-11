# Whisper Skill - Audio Transcription

A Python skill for automatic speech recognition and audio transcription using OpenAI's Whisper model.

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

## 🎯 Quick Start

```python
from whisper_skill import WhisperSkill

# Initialize the skill
skill = WhisperSkill()

# Transcribe audio
result = skill.transcribe("path/to/audio.mp3")
print(result['text'])
```

## 📦 Installation

### From GitHub
```bash
git clone https://github.com/Ekaer03/whisper_skill.git
cd whisper_skill
pip install -r requirements.txt
```

### Requirements
- Python 3.8 or higher
- ffmpeg
- openai-whisper

## 🚀 Features

- **Multi-format Support**: MP3, WAV, FLAC, OGG, M4A, WEBM
- **Multi-language**: Automatic language detection or specify language
- **Batch Processing**: Transcribe multiple files efficiently
- **Flexible Models**: Tiny, Base, Small, Medium, Large
- **Translation**: Translate audio to English
- **Segment Information**: Get timestamps and confidence scores
- **GPU Support**: CUDA acceleration for faster processing
- **Error Handling**: Comprehensive error management

## 📚 Usage Examples

### Basic Transcription
```python
from whisper_skill import WhisperSkill

skill = WhisperSkill(model="base")
result = skill.transcribe("meeting.mp3")
print(result['text'])
```

### Translate to English
```python
result = skill.transcribe("spanish_audio.mp3", task="translate")
print(result['text'])  # English translation
```

### Specify Language
```python
result = skill.transcribe("french_audio.mp3", language="fr")
```

### Batch Processing
```python
audio_files = ["audio1.mp3", "audio2.mp3", "audio3.mp3"]
results = skill.transcribe_batch(audio_files)

for filename, result in results.items():
    print(f"{filename}: {result['text']}")
```

## ⚙️ Configuration

Set environment variables or create `.env`:

```env
WHISPER_MODEL=base
WHISPER_DEVICE=cuda
LOG_LEVEL=INFO
```

## 🔧 API Reference

### WhisperSkill Class

#### `transcribe(audio_file, language=None, task='transcribe')`
Transcribe audio file.

**Parameters:**
- `audio_file` (str): Path to audio file
- `language` (str): ISO-639-1 language code (optional)
- `task` (str): 'transcribe' or 'translate'

**Returns:** Dictionary with text, language, duration, and segments

#### `transcribe_batch(audio_files, language=None)`
Transcribe multiple audio files.

#### `save_to_file(result, output_path)`
Save transcription to text file.

#### `save_to_json(result, output_path)`
Save transcription to JSON file.

## 📝 Examples

See `example_usage.py` for detailed usage examples including:
- Basic transcription
- Language-specific transcription
- Translation
- Batch processing
- Output formatting
- Error handling

## 🤝 Contributing

Contributions welcome! Please submit pull requests or open issues.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Support

- **Documentation**: See [skill.md](skill.md)
- **Issues**: [GitHub Issues](https://github.com/Ekaer03/whisper_skill/issues)

---

**Made with ❤️ by Ekaer03**