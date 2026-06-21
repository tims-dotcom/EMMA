import os
import webbrowser
import urllib.parse
import logging

logger = logging.getLogger("EMMA.Action")

try:
    import pyautogui
    _HAS_GUI = True
except Exception:
    _HAS_GUI = False
    logger.warning("pyautogui недоступний — команди гучності не працюватимуть.")


def open_browser(url: str = "https://google.com") -> str:
    webbrowser.open(url)
    return "Відкрито браузер, сер."


def open_google(query: str = "") -> str:
    if query:
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return f"Шукаю «{query}» у Google, сер."
    return open_browser()


def shutdown(delay: int = 10) -> str:
    os.system(f"shutdown /s /t {delay}")
    return f"Запускаю протоколи вимкнення. Система вимкнеться через {delay} секунд."


def cancel_shutdown() -> str:
    os.system("shutdown /a")
    return "Протокол вимкнення скасовано."


def restart(delay: int = 10) -> str:
    os.system(f"shutdown /r /t {delay}")
    return f"Перезавантаження через {delay} секунд, сер."


def _press_volume(key: str, times: int = 5) -> None:
    if _HAS_GUI:
        for _ in range(times):
            pyautogui.press(key)


def volume_up(steps: int = 5) -> str:
    _press_volume("volumeup", steps)
    return f"Збільшила гучність на {steps} пунктів, сер."


def volume_down(steps: int = 5) -> str:
    _press_volume("volumedown", steps)
    return f"Зменшила гучність на {steps} пунктів, сер."


def volume_mute() -> str:
    _press_volume("volumemute", 1)
    return "Режим тиші увімкнено, сер."


_YT_STRIP_WORDS = (
    "знайди в ютубі", "увімкни на ютубі", "знайди на ютубі",
    "покажи на ютубі", "ютуб", "youtube",
    "на ютубі", "в ютубі",
)


def _extract_query(text: str, strip_words: tuple[str, ...]) -> str:
    result = text.lower()
    for word in sorted(strip_words, key=len, reverse=True):
        result = result.replace(word, "")
    return result.strip(" ,.")


def search_youtube(user_text: str) -> str:
    query = _extract_query(user_text, _YT_STRIP_WORDS)
    if not query:
        return "А що саме знайти на YouTube, сер?"
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return f"Шукаю «{query}» на YouTube, сер."