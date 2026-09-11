# Whisper Transcription Skill

## Overview
This skill enables audio transcription using OpenAI's Whisper model. It supports multiple audio formats and languages, providing accurate speech-to-text conversion.

## Features
- 🎙️ Audio transcription in multiple languages
- 📁 Support for various audio formats (MP3, WAV, M4A, FLAC, etc.)
- 🚀 Fast and accurate transcription
- 🔄 Batch processing capability
- 📊 Confidence scoring
- 🌍 Automatic language detection

## Audio Formats Supported
- MP3
- WAV
- FLAC
- OGG
- M4A
- WEBM
- and more via ffmpeg

## Installation

### Prerequisites
- Python 3.8+
- pip package manager
- ffmpeg (for audio processing)

### Setup
```bash
pip install -r requirements.txt
```

## Usage

### Basic Transcription
```python
from whisper_skill import WhisperSkill

skill = WhisperSkill()
result = skill.transcribe("audio.mp3")
print(result['text'])
```

### With Language Specification
```python
result = skill.transcribe("audio.mp3", language="es")
print(result['text'])
```

### Batch Processing
```python
files = ["audio1.mp3", "audio2.mp3", "audio3.mp3"]
results = skill.transcribe_batch(files)

for file, result in results.items():
    print(f"{file}: {result['text']}")
```

### Advanced Options
```python
result = skill.transcribe(
    "audio.mp3",
    language="en",
    temperature=0.0,
    verbose=False
)
```

## API Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| audio_file | str | Required | Path to audio file |
| language | str | None | ISO-639-1 language code |
| temperature | float | 0.0 | Temperature for decoding (0-1) |
| verbose | bool | False | Print verbose output |
| task | str | "transcribe" | "transcribe" or "translate" |

## Response Format

```json
{
  "text": "Full transcribed text",
  "language": "en",
  "duration": 45.5,
  "segments": [
    {
      "id": 0,
      "seek": 0,
      "start": 0.0,
      "end": 5.2,
      "text": "Segment text",
      "confidence": 0.95
    }
  ]
}
```

## Error Handling

```python
from whisper_skill import WhisperSkill, TranscriptionError

skill = WhisperSkill()
try:
    result = skill.transcribe("audio.mp3")
except TranscriptionError as e:
    print(f"Transcription failed: {e}")
except FileNotFoundError:
    print("Audio file not found")
```

## Configuration

Create a `.env` file:
```
WHISPER_MODEL=base
WHISPER_DEVICE=cuda
LOG_LEVEL=INFO
```

## Performance Tips

1. **Model Selection**: Use smaller models (`tiny`, `base`) for speed, larger models (`medium`, `large`) for accuracy
2. **Language Hints**: Specify language to improve accuracy and speed
3. **Batch Processing**: Process multiple files efficiently
4. **GPU Acceleration**: Ensure CUDA is properly configured for faster processing

## Limitations

- Maximum file size: ~25MB (API limit)
- Processing time depends on audio duration and model size
- Accuracy varies based on audio quality and background noise

## Troubleshooting

### Issue: Model download fails
**Solution**: Manually set the model path or check internet connection

### Issue: GPU memory error
**Solution**: Use smaller model or ensure sufficient VRAM

### Issue: Poor transcription quality
**Solution**: Specify correct language or use larger model

## Contributing

Contributions are welcome! Please follow PEP 8 style guide and include tests.

## License

MIT License - see LICENSE file for details

## Support

For issues and feature requests, please visit the [GitHub Issues](https://github.com/Ekaer03/whisper_skill/issues) page.
