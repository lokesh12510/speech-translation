import asyncio

import edge_tts

OUTPUT_FILE = 'input_tts.mp3'

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

# Example usage
if __name__ == "__main__":
    text = "Hi, How are you!. How can I help you?. I am here to help you. Please let me know your questions."
    language_code = "en"  # Replace with the desired language code (e.g., 'de' for German)

    try:
        asyncio.run(text_to_speech(text, language_code, OUTPUT_FILE))
    except Exception as e:
        print(f"Error during text-to-speech conversion: {e}")