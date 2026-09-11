"""
Example usage of the Whisper Skill for audio transcription.
"""

from whisper_skill import WhisperSkill, TranscriptionError
import json


def example_basic_transcription():
    """Example 1: Basic transcription"""
    print("=" * 60)
    print("Example 1: Basic Transcription")
    print("=" * 60)
    
    skill = WhisperSkill(model='base')
    
    try:
        result = skill.transcribe("audio_sample.mp3")
        print(f"\nTranscribed Text:")
        print(result['text'])
        print(f"\nDetected Language: {result['language']}")
        print(f"Duration: {result.get('duration', 'N/A')} seconds")
    except FileNotFoundError:
        print("Note: Audio file not found. Please provide a valid audio file.")
    except TranscriptionError as e:
        print(f"Transcription error: {e}")


def example_language_specific():
    """Example 2: Transcription with language specification"""
    print("\n" + "=" * 60)
    print("Example 2: Language-Specific Transcription")
    print("=" * 60)
    
    skill = WhisperSkill(model='base')
    
    try:
        result = skill.transcribe("spanish_audio.mp3", language="es")
        print(f"\nTranscribed Spanish Text:")
        print(result['text'])
    except FileNotFoundError:
        print("Note: Audio file not found.")
    except TranscriptionError as e:
        print(f"Error: {e}")


def example_translation():
    """Example 3: Translate audio to English"""
    print("\n" + "=" * 60)
    print("Example 3: Audio Translation")
    print("=" * 60)
    
    skill = WhisperSkill(model='base')
    
    try:
        result = skill.transcribe(
            "foreign_audio.mp3",
            task='translate'
        )
        print(f"\nTranslated to English:")
        print(result['text'])
        print(f"Original Language: {result['language']}")
    except FileNotFoundError:
        print("Note: Audio file not found.")
    except TranscriptionError as e:
        print(f"Error: {e}")


def example_batch_processing():
    """Example 4: Batch transcription"""
    print("\n" + "=" * 60)
    print("Example 4: Batch Processing")
    print("=" * 60)
    
    skill = WhisperSkill(model='base')
    
    audio_files = [
        "meeting_part1.mp3",
        "meeting_part2.mp3",
        "meeting_part3.mp3"
    ]
    
    try:
        results = skill.transcribe_batch(audio_files)
        
        for filename, result in results.items():
            if 'error' not in result:
                print(f"\n{filename}:")
                print(f"  Text: {result['text'][:100]}...")
            else:
                print(f"\n{filename}: {result['error']}")
    except Exception as e:
        print(f"Batch processing error: {e}")


def example_save_outputs():
    """Example 5: Save transcription in various formats"""
    print("\n" + "=" * 60)
    print("Example 5: Save Outputs")
    print("=" * 60)
    
    skill = WhisperSkill(model='base')
    
    try:
        result = skill.transcribe("podcast.mp3")
        
        # Save as text
        skill.save_to_file(result, "transcription.txt")
        
        # Save as JSON
        skill.save_to_json(result, "transcription.json", pretty=True)
        
        # Save as WebVTT subtitle
        skill.save_to_vtt(result, "subtitles.vtt")
        
        print("Files saved successfully:")
        print("  - transcription.txt")
        print("  - transcription.json")
        print("  - subtitles.vtt")
    except FileNotFoundError:
        print("Note: Audio file not found.")
    except TranscriptionError as e:
        print(f"Error: {e}")


def example_segments_with_timestamps():
    """Example 6: Get segments with timestamps"""
    print("\n" + "=" * 60)
    print("Example 6: Segments with Timestamps")
    print("=" * 60)
    
    skill = WhisperSkill(model='base')
    
    try:
        result = skill.transcribe("interview.mp3")
        
        print("\nTranscription Segments:")
        if 'segments' in result:
            for segment in result['segments'][:5]:  # Show first 5 segments
                start = segment['start']
                end = segment['end']
                text = segment['text'].strip()
                print(f"[{start:.2f}s - {end:.2f}s] {text}")
        else:
            print(result['text'])
    except FileNotFoundError:
        print("Note: Audio file not found.")
    except TranscriptionError as e:
        print(f"Error: {e}")


def example_skill_info():
    """Example 7: Get skill information"""
    print("\n" + "=" * 60)
    print("Example 7: Skill Information")
    print("=" * 60)
    
    skill = WhisperSkill(model='medium')
    
    info = skill.get_info()
    print("\nSkill Configuration:")
    print(json.dumps(info, indent=2))


def example_error_handling():
    """Example 8: Error handling"""
    print("\n" + "=" * 60)
    print("Example 8: Error Handling")
    print("=" * 60)
    
    skill = WhisperSkill(model='base')
    
    # Try with non-existent file
    try:
        result = skill.transcribe("non_existent_file.mp3")
    except FileNotFoundError as e:
        print(f"✓ Caught FileNotFoundError: {e}")
    
    # Try with invalid task
    try:
        result = skill.transcribe("audio.mp3", task="invalid_task")
    except ValueError as e:
        print(f"✓ Caught ValueError: {e}")
    
    # Try with invalid temperature
    try:
        result = skill.transcribe("audio.mp3", temperature=1.5)
    except ValueError as e:
        print(f"✓ Caught ValueError: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("WHISPER SKILL - USAGE EXAMPLES")
    print("=" * 60 + "\n")
    
    # Run examples
    example_basic_transcription()
    example_language_specific()
    example_translation()
    example_batch_processing()
    example_save_outputs()
    example_segments_with_timestamps()
    example_skill_info()
    example_error_handling()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60 + "\n")
