import logging
import speech_recognition as sr
import LLM
import TTS
import Action

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("EMMA.Main")


def _handle_youtube(text: str) -> str:
    return Action.search_youtube(text)


def _handle_google(text: str) -> str:
    for kw in ("загугли", "знайди в гуглі", "пошукай в гуглі"):
        if kw in text:
            query = text.replace(kw, "").strip()
            return Action.open_google(query)
    return Action.open_browser()


COMMAND_TABLE: list[tuple[tuple[str, ...], callable]] = [
    (("на ютубі", "в ютубі", "ютуб"), _handle_youtube),
    (("загугли", "знайди в гуглі", "пошукай в гуглі"), _handle_google),
    (("відкрий браузер", "відкрий гугл", "гугл"), lambda _: Action.open_browser()),
    (("збільши звук", "збільши гучність", "гучніше"), lambda _: Action.volume_up()),
    (("зменши звук", "зменши гучність", "тихіше"), lambda _: Action.volume_down()),
    (("вимкни звук", "режим тиші", "без звуку"), lambda _: Action.volume_mute()),
    (("скасуй вимкнення", "скасуй завершення"), lambda _: Action.cancel_shutdown()),
    (("вимкни комп", "заверши роботу", "вимкни систему"), lambda _: Action.shutdown()),
    (("перезавантаж", "перезапусти"), lambda _: Action.restart()),
    (("очисти пам'ять", "скинь контекст", "нова розмова"),
        lambda _: (LLM.clear_history(), "Контекст розмови очищено, сер.")[1]),
]


def _route(text: str) -> str | None:
    for keywords, handler in COMMAND_TABLE:
        if any(kw in text for kw in keywords):
            return handler(text)
    return None


def listen(recognizer: sr.Recognizer, microphone: sr.Microphone) -> str | None:
    with microphone as source:
        recognizer.pause_threshold = 0.6
        print("\n🎤 Слухаю...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language="uk-UA")
            print(f"👤 Ви: {text}")
            return text.lower().strip()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            logger.error(f"Google STT недоступний: {e}")
            return None


def main() -> None:
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("⏳ Налаштування мікрофона...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1.0)

    TTS.speak("Всі системи активні, я готова до роботи, сер.")

    while True:
        text = listen(recognizer, microphone)

        if not text:
            continue

        if any(kw in text for kw in ("відключись", "вихід", "стоп emma", "стоп емма")):
            TTS.speak("Переходжу в режим сну. До зустрічі, сер.")
            break

        response = _route(text)

        if response is not None:
            TTS.speak(response)
            if any(kw in text for kw in ("вимкни комп", "заверши роботу", "вимкни систему")):
                break
        else:
            try:
                reply = LLM.ask_emma(text)
                TTS.speak(reply)
            except Exception as e:
                logger.error(f"LLM помилка: {e}")
                TTS.speak("Сталася помилка зв'язку з модулем ШІ, сер.")


if __name__ == "__main__":
    main()