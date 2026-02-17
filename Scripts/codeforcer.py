import pyautogui
import pydirectinput
import pyperclip
import keyboard
import random
import string
import time
import ctypes
import os
from datetime import datetime

pyautogui.PAUSE = 0
pydirectinput.PAUSE = 0

# ============== НАСТРОЙКИ ==============
CHARSET = string.ascii_letters + string.digits
CODE_LENGTH = 6

# === КООРДИНАТЫ ===
JOIN_MENU_X = 40
JOIN_MENU_Y = 520

INPUT_FIELD_X = 967
INPUT_FIELD_Y = 608

SUBMIT_BUTTON_X = 944
SUBMIT_BUTTON_Y = 750

# === ЗАДЕРЖКИ ===
DELAY_OPEN_MENU = 0.1
DELAY_CLICK_FIELD = 0.05
DELAY_CLEAR = 0.05
DELAY_PASTE = 0.15
DELAY_SUBMIT = 0.1
DELAY_BETWEEN = 0.1

# === УПРАВЛЕНИЕ ===
START_KEY = 'f5'
STOP_KEY = 'f6'
LOG_FILE = "../bruteforce_log.txt"
# ====================================


def bring_roblox_focus():
    try:
        hwnd = ctypes.windll.user32.FindWindowW(None, "Roblox")
        if hwnd:
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            return True
    except:
        pass
    return False


class DeadRailsBruteforcer:
    def __init__(self):
        self.running = False
        self.attempts = 0
        self.start_time = None
        self.tried_codes = set()

    def generate_code(self) -> str:
        while True:
            code = ''.join(random.choices(CHARSET, k=CODE_LENGTH))
            if code not in self.tried_codes:
                self.tried_codes.add(code)
                return code

    def log(self, msg: str):
        t = datetime.now().strftime("%H:%M:%S")
        line = f"[{t}] {msg}"
        print(line)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def do_attempt(self, code: str):
        # 1) Join — открыть меню
        pyautogui.moveTo(JOIN_MENU_X, JOIN_MENU_Y)
        time.sleep(0.05)
        pydirectinput.click(JOIN_MENU_X, JOIN_MENU_Y)
        time.sleep(DELAY_OPEN_MENU)

        # 2) Клик по полю ввода — двойной для надёжности
        pyautogui.moveTo(INPUT_FIELD_X, INPUT_FIELD_Y)
        time.sleep(0.05)
        pydirectinput.click(INPUT_FIELD_X, INPUT_FIELD_Y)
        time.sleep(0.05)
        pydirectinput.click(INPUT_FIELD_X, INPUT_FIELD_Y)
        time.sleep(DELAY_CLICK_FIELD)

        # 3) Выделить всё и удалить
        pydirectinput.keyDown('ctrl')
        time.sleep(0.03)
        pydirectinput.press('a')
        time.sleep(0.03)
        pydirectinput.keyUp('ctrl')
        time.sleep(0.03)
        pydirectinput.press('backspace')
        time.sleep(DELAY_CLEAR)

        # 4) Вставить код — посимвольно (надёжнее в Roblox)
        for char in code:
            if char.isupper():
                pydirectinput.keyDown('shift')
                time.sleep(0.02)
                pydirectinput.press(char.lower())
                time.sleep(0.02)
                pydirectinput.keyUp('shift')
            else:
                pydirectinput.press(char)
            time.sleep(0.03)
        time.sleep(DELAY_PASTE)

        # 5) Submit
        pyautogui.moveTo(SUBMIT_BUTTON_X, SUBMIT_BUTTON_Y)
        time.sleep(0.05)
        pydirectinput.click(SUBMIT_BUTTON_X, SUBMIT_BUTTON_Y)
        time.sleep(DELAY_SUBMIT)

    def stats(self) -> str:
        elapsed = time.time() - self.start_time
        rate = self.attempts / elapsed if elapsed > 0 else 0
        return f"#{self.attempts} | {rate:.1f}/сек | {elapsed:.0f}с | ~{rate * 3600:.0f}/час"

    def run(self):
        total = len(CHARSET) ** CODE_LENGTH
        self.log("=" * 50)
        self.log("  Dead Rails Bruteforcer v6")
        self.log(f"  Комбинаций: {total:,}")
        self.log(f"  {START_KEY.upper()} старт | {STOP_KEY.upper()} стоп")
        self.log("=" * 50)

        keyboard.wait(START_KEY)
        for i in range(3, 0, -1):
            self.log(f"  Старт через {i}...")
            time.sleep(1)

        bring_roblox_focus()
        self.running = True
        self.start_time = time.time()
        keyboard.on_press_key(STOP_KEY, lambda _: self.stop())

        try:
            while self.running:
                code = self.generate_code()
                self.attempts += 1
                self.do_attempt(code)

                if self.attempts % 10 == 0:
                    self.log(f"  Код: {code} | {self.stats()}")

                time.sleep(DELAY_BETWEEN)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def stop(self):
        if self.running:
            self.running = False
            elapsed = time.time() - self.start_time if self.start_time else 0
            rate = self.attempts / elapsed if elapsed > 0 else 0
            self.log("=" * 50)
            self.log("  ОСТАНОВЛЕНО")
            self.log(f"  Попыток: {self.attempts}")
            self.log(f"  Время: {elapsed:.0f}с")
            self.log(f"  Скорость: {rate:.1f}/сек ({rate * 3600:.0f}/час)")
            self.log("=" * 50)


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Dead Rails Bruteforcer v6")
    print("-" * 30)
    print("1 — Брутфорс")
    print("2 — Тест")
    print()
    choice = input("Выбор: ").strip()

    if choice == "2":
        print("\nЧерез 3 сек — переключись на Roblox!\n")
        time.sleep(3)
        bring_roblox_focus()

        print("1. Join...")
        pyautogui.moveTo(JOIN_MENU_X, JOIN_MENU_Y)
        time.sleep(0.05)
        pydirectinput.click(JOIN_MENU_X, JOIN_MENU_Y)
        time.sleep(0.5)

        print("2. Поле ввода (двойной клик)...")
        pyautogui.moveTo(INPUT_FIELD_X, INPUT_FIELD_Y)
        time.sleep(0.05)
        pydirectinput.click(INPUT_FIELD_X, INPUT_FIELD_Y)
        time.sleep(0.05)
        pydirectinput.click(INPUT_FIELD_X, INPUT_FIELD_Y)
        time.sleep(0.3)

        print("3. Посимвольный ввод 'AbCd12'...")
        test = "AbCd12"
        for char in test:
            if char.isupper():
                pydirectinput.keyDown('shift')
                time.sleep(0.02)
                pydirectinput.press(char.lower())
                time.sleep(0.02)
                pydirectinput.keyUp('shift')
            else:
                pydirectinput.press(char)
            time.sleep(0.05)
        time.sleep(0.3)

        print("4. Submit (944, 750)...")
        pyautogui.moveTo(SUBMIT_BUTTON_X, SUBMIT_BUTTON_Y)
        time.sleep(0.05)
        pydirectinput.click(SUBMIT_BUTTON_X, SUBMIT_BUTTON_Y)

        print("\n✅ Готово!")
    else:
        bf = DeadRailsBruteforcer()
        bf.run()