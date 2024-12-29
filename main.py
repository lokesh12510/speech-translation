import asyncio

import edge_tts
import soundfile as sf
from transformers import pipeline

OUTPUT_FILE = 'output_tts.wav'

def initialize_stt_pipeline(model_name="facebook/wav2vec2-base-960h"):
    """
    Initializes the speech-to-text pipeline using a Hugging Face model.

    Args:
        model_name (str): The name of the Hugging Face model from the model hub.
                          Default is "facebook/wav2vec2-base-960h".

    Returns:
        pipeline: A Hugging Face pipeline for speech recognition.
    """
    return pipeline(task="automatic-speech-recognition", model=model_name)



def initialize_translation_pipeline(model_name="Helsinki-NLP/opus-mt-en-hi"):
    """
    Initializes the translation pipeline using a Hugging Face model.

    Args:
        model_name (str): The name of the Hugging Face model from the model hub.
                          Default is "Helsinki-NLP/opus-mt-ta-en".

    Returns:
        pipeline: A Hugging Face pipeline for translation.
    """
    return pipeline(task="translation", model=model_name)


async def get_voice_for_language(language_code):
    """
    Retrieves a suitable voice for the given language code.

    Args:
        language_code (str): The language code (e.g., 'en', 'de', 'fr').

    Returns:
        str: The name of the voice.
    """
    voices = await edge_tts.VoicesManager.create()
    for voice in voices.voices:
        if voice["Locale"].startswith(language_code):
            return voice["Name"]
    raise ValueError(f"No voice found for language code: {language_code}")

async def text_to_speech(text, language_code, output_audio_path):
    """
    Converts text to speech and saves the output as an audio file.

    Args:
        text (str): The text to be converted to speech.
        language_code (str): The language code for the desired voice.
        output_audio_path (str): Path to save the output audio file.
    """
    try:
        voice = await get_voice_for_language(language_code)
        tts = edge_tts.Communicate(text, voice)
        await tts.save(output_audio_path)
        print(f"Audio saved to {output_audio_path}")
    except Exception as e:
        print(f"Error during text-to-speech conversion: {e}")

def speech_to_text(stt_pipeline, audio_path):
    """
    Converts speech in an audio file to text using the specified pipeline.

    Args:
        stt_pipeline: The speech-to-text pipeline initialized with a Hugging Face model.
        audio_path (str): Path to the audio file to be transcribed.

    Returns:
        str: The transcribed text from the audio file.
    """
    try:
        result = stt_pipeline(audio_path)
        return result["text"]
    except Exception as e:
        print(f"Error during speech-to-text conversion: {e}")
        return None


def translate_text(translation_pipeline, text):
    """
    Translates text using the specified pipeline.

    Args:
        translation_pipeline: The translation pipeline initialized with a Hugging Face model.
        text (str): The text to be translated.

    Returns:
        str: The translated text.
    """
    try:
        result = translation_pipeline(text)
        return result[0]["translation_text"]
    except Exception as e:
        print(f"Error during text translation: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Initialize the pipelines
    stt_pipeline = initialize_stt_pipeline()
    translation_pipeline = initialize_translation_pipeline()

    # Path to the audio file
    audio_file_path = "./input_tts.mp3"  # Replace with your audio file path

    # Perform speech-to-text
    transcription = speech_to_text(stt_pipeline, audio_file_path)

    if transcription:
        print("Transcription:", transcription)
        
        # Translate the transcribed text
        translated_text = translate_text(translation_pipeline, transcription)
        if translated_text:
            print("Translated Text:", translated_text)
            
            # Define the language code for TTS
            language_code = "hi"  # Replace with the desired language code (e.g., 'de' for German)

            try:
                asyncio.run(text_to_speech(translated_text, language_code, OUTPUT_FILE))
            except Exception as e:
                print(f"Error during text-to-speech conversion: {e}")
        else:
            print("Translation failed.")
    else:
        print("Transcription failed.")