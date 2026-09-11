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

### Get Detailed Segments
```python
result = skill.transcribe("podcast.mp3")

for segment in result['segments']:
    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")
```

### Save Transcription
```python
result = skill.transcribe("audio.mp3")
skill.save_to_file(result, "transcription.txt")
skill.save_to_json(result, "transcription.json")
```

## ⚙️ Configuration

Set environment variables or create `.env`:

```env
# Model size: tiny, base, small, medium, large
WHISPER_MODEL=base

# Device: cuda, cpu
WHISPER_DEVICE=cuda

# Logging level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO

# Download directory for models
WHISPER_MODEL_DIR=~/.cache/whisper
```

## 📊 Model Comparison

| Model | English-only | Multilingual | Size | Speed | Accuracy |
|-------|--------------|--------------|------|-------|----------|
| tiny | ✓ | ✓ | 39M | Very Fast | Low |
| base | ✓ | ✓ | 74M | Fast | Medium |
| small | ✓ | ✓ | 244M | Medium | Good |
| medium | ✓ | ✓ | 769M | Slow | Very Good |
| large | - | ✓ | 1.5G | Very Slow | Best |

## 🔧 API Reference

### WhisperSkill Class

#### `__init__(model='base', device='auto')`
Initialize the Whisper skill.

**Parameters:**
- `model` (str): Model size (tiny, base, small, medium, large)
- `device` (str): 'cuda', 'cpu', or 'auto'

#### `transcribe(audio_file, language=None, task='transcribe', temperature=0.0)`
Transcribe audio file.

**Parameters:**
- `audio_file` (str): Path to audio file
- `language` (str): ISO-639-1 language code (optional)
- `task` (str): 'transcribe' or 'translate'
- `temperature` (float): Sampling temperature (0-1)

**Returns:** Dictionary with text, language, duration, and segments

#### `transcribe_batch(audio_files, language=None)`
Transcribe multiple audio files.

**Parameters:**
- `audio_files` (list): List of file paths
- `language` (str): ISO-639-1 language code (optional)

**Returns:** Dictionary mapping filenames to results

#### `save_to_file(result, output_path)`
Save transcription to text file.

#### `save_to_json(result, output_path)`
Save transcription to JSON file.

## 🐛 Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'whisper'"**
```bash
pip install openai-whisper
```

**Issue: "ffmpeg not found"**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

**Issue: CUDA out of memory**
```python
skill = WhisperSkill(model="base", device="cpu")
```

**Issue: Slow transcription**
- Use smaller model (tiny, base)
- Enable GPU acceleration
- Check audio duration (longer = slower)

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=whisper_skill tests/
```

## 📝 Examples

Check the `examples/` directory for:
- Basic transcription
- Batch processing
- Language detection
- Translation
- Output formatting
- Error handling

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - The underlying transcription model
- [ffmpeg](https://ffmpeg.org/) - Audio processing

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Ekaer03/whisper_skill/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Ekaer03/whisper_skill/discussions)
- **Documentation**: See [skill.md](skill.md)

## 📈 Roadmap

- [ ] Real-time transcription streaming
- [ ] Speaker diarization
- [ ] Custom vocabulary support
- [ ] API server implementation
- [ ] Web UI
- [ ] Docker support

---

**Made with ❤️ by Ekaer03**
