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
    TTS.speek("Всі системи активні, я готова до роботи")

    while True:
        speech_text = listen_to_user()

        text_lower = speech_text.lower()

        if speech_text is None:
            continue

        if "відключись" in text_lower or "вихід" in text_lower:
            TTS.speek("Перехожу в режим сну, до зустрічі")
            break
        elif "відкрий браузер" in text_lower or "відкрий google" in text_lower or "відкрий гугл" in text_lower:
            response = Action.open_browser()
            TTS.speek(response)
            continue
        elif "вимкни компа" in text_lower or "заверши роботу" in text_lower:
            response = Action.shutdown()
            TTS.speek(response)
        elif "скасуй вимкнення" in text_lower or "скасуй завершення" in text_lower or "скасуй завершення роботи" in text_lower:
            response = Action.cancel_shutdown()
            TTS.speek(response)
        elif "зменши звук" in text_lower or "зменши гучність" in text_lower:
            response = Action.volume_down
            TTS.speek(response)
        elif "збільши звук" in text_lower or "збільши гучність" in text_lower:
            response = Action.volume_up
            TTS.speek(response)
        elif "вимкни звук" in text_lower or "вимкни гучність" in text_lower:
            response = Action.volume_mute
            TTS.speek(response)
        elif "на ютубі" in text_lower or "в ютубі" in text_lower:
            response = Action.search_youtube
            TTS.speek(response)
        else:
            reply = LLM.ask_emma(speech_text)
            TTS.speek(reply)

if __name__ == "__main__":
    main()