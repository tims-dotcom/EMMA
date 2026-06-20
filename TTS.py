import os 
import time
import pygame
import asyncio
import edge_tts

voice = "uk-UA-PolinaNeural"

async def generate_audio(text, output_file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def speek(text):
    print("E.M.M.A:", text)

    filename = "reply.mp3"

    asyncio.run(generate_audio(text, filename))

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.05)

    pygame.mixer.music.unload()
    pygame.mixer.quit()

    if os.path.exists(filename):
        os.remove(filename)

if __name__ == "__main__":
    speek("Привіт це EMMA 1.2, я готова до твоїх завдань")