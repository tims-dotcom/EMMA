import speech_recognition as sr
import LLM
import TTS
import Action


def listen_to_user():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Слухаю вас, сер")

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            text = recognizer.recognize_google(audio, language="uk-UA")
            return text
        except:
            return None
        
def main():
    TTS.speek("Всі системі активовані, сер, я готовий до роботи")

    while True:
        speech_text = listen_to_user()

        if speech_text is None:
            continue

        if 'відключись' in speech_text.lower():
            break

        if speech_text is not None:
            text_lower = speech_text.lower()

            if "відкрий гугл" in text_lower or "відкрий google":
                response = Action.open_browser()
                TTS.speek(response)
                continue
        
        reply = LLM.ask_emma(speech_text)
        TTS.speek(reply)

if __name__ == "__main__":
    main()