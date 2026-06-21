import subprocess
import os
import TTS
import webbrowser
import pyautogui
import urllib.parse

def open_browser():
    TTS.speek("Відкриваю браузер")
    os.system("start https://google.com")
    return "Відкрито ..."



def shutdown():
    TTS.speek("Запускаю протоколи вимкнення")
    os.system("shutdown /s /t 10")
    TTS.speek("Система вимкнеця через 10 секунд")

def cancel_shutdown():
    os.system("shutdown /a")
    TTS.speek("Протокол вимкненя скасовано")



def volume_up():
    for _ in range(5):
        pyautogui.press('volumeup')
    return TTS.speek("Збільшила гучність на 5")

def volume_down():
    for _ in range(5):
        pyautogui.press('volumedown')
    return TTS.speek("Зменшила гучність на 5")

def volume_mute():
    pyautogui.press('volumemute')
    print("Ввімкнула режим тиші")
    return TTS.speek("Ввімкнула режим тиші")



def search_youtube(user_text):
    querty = user_text.replace("знайди в ютубі", "").replace("увімкни на ютубі", "").strip()

    if not querty:
        return
    
    encoded_querty = urllib.parse.quote(querty)
    url = f"https:/www.youtube.com/results?search_query={encoded_querty}"

    webbrowser.open(url)
    return TTS.speek(f"Шукаю {querty} в Ютубі")