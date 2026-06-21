import os
import time
import threading
import tempfile
import pygame
import asyncio
import edge_tts
import logging

logger = logging.getLogger("EMMA.TTS")

VOICE = "uk-UA-PolinaNeural"

pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
pygame.mixer.init()

_tts_lock = threading.Lock()


async def _generate_audio(text: str, output_file: str) -> None:
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)


def speak(text: str) -> None:
    if not text or not text.strip():
        return

    print(f"E.M.M.A: {text}")

    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp_path = tmp.name
    tmp.close()

    with _tts_lock:
        try:
            asyncio.run(_generate_audio(text, tmp_path))

            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()

            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.05)

        except Exception as e:
            logger.error(f"Помилка голосу: {e}")

        finally:
            try:
                pygame.mixer.music.unload()
            except Exception:
                pass

            time.sleep(0.05)
            try:
                os.remove(tmp_path)
            except OSError:
                pass


if __name__ == "__main__":
    speak("Тест системи пройдено успішно, сер.")