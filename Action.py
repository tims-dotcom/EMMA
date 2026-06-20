import subprocess
import os

def open_browser():
    print("Відкриваєця браузер ...")
    os.system("start https://google.com")
    return "Відкрито ..."