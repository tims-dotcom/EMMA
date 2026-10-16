import os
import time
import logging
from groq import Groq

logger = logging.getLogger("EMMA.LLM")

_api_key = os.getenv("GROQ_API_KEY", "")
if not _api_key:
    _api_key = ""
    logger.warning("GROQ_API_KEY не знайдено в змінних середовища, використовую вбудований ключ.")

client = Groq(api_key=_api_key)

_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Ти E.M.M.A — штучний інтелект-асистент, натхненний J.A.R.V.I.S. з фільму «Залізна людина». "
        "Відповідай коротко, чітко і впевнено. Звертайся до користувача «сер». "
        "Не розписуй зайвого — лише суть."
    )
}

_MAX_HISTORY = 20
_MODEL = "llama-3.3-70b-versatile"

chat_history: list[dict] = []


def _trim_history() -> None:
    if len(chat_history) > _MAX_HISTORY:
        chat_history[:] = chat_history[-_MAX_HISTORY:]


def ask_emma(user_text: str, retries: int = 2) -> str:
    if not user_text.strip():
        return ""

    chat_history.append({"role": "user", "content": user_text})
    _trim_history()

    messages = [_SYSTEM_PROMPT] + chat_history

    for attempt in range(retries + 1):
        try:
            completion = client.chat.completions.create(
                model=_MODEL,
                messages=messages,
                temperature=0.5,
                max_tokens=400,
            )
            response = completion.choices[0].message.content.strip()
            chat_history.append({"role": "assistant", "content": response})
            return response

        except Exception as e:
            logger.error(f"Groq API помилка (спроба {attempt + 1}/{retries + 1}): {e}")
            if attempt < retries:
                time.sleep(1.5 * (attempt + 1))

    if chat_history and chat_history[-1]["role"] == "user":
        chat_history.pop()

    return "У мене виникли проблеми зі зв'язком, сер."


def clear_history() -> None:
    chat_history.clear()
    logger.info("Історія чату очищена.")


if __name__ == "__main__":
    print("E.M.M.A активована (введіть 'вихід' для завершення)")
    while True:
        user_input = input("\nТи: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "вихід":
            print("E.M.M.A: Відключаю живлення, до побачення.")
            break
        print(f"E.M.M.A: {ask_emma(user_input)}")
