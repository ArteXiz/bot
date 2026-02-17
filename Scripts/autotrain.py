import ctypes
import ctypes.wintypes
import time
import threading
import keyboard
import win32gui
import win32con
import win32api
import win32process
import os

# ======================== НАСТРОЙКИ ========================
TOGGLE_KEY = "F6"        # Клавиша вкл/выкл
EXIT_KEY = "F7"          # Клавиша выхода из скрипта
HOLD_KEY = 0x57          # Virtual key code для W (0x57)
HOLD_KEY_NAME = "W"
# ===========================================================

# Коды сканирования
W_SCANCODE = 0x11  # Scan code для W

class RobloxAutoW:
    def __init__(self):
        self.active = False
        self.running = True
        self.roblox_hwnd = None
        self.lock = threading.Lock()

    def find_roblox_window(self):
        """Ищет окно Roblox"""
        result = []

        def enum_callback(hwnd, _):
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd):
                title = win32gui.GetWindowText(hwnd)
                # Roblox окно обычно называется "Roblox"
                if "Roblox" in title:
                    # Проверяем что это именно игровое окно, а не браузер
                    try:
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        import psutil
                        proc = psutil.Process(pid)
                        proc_name = proc.name().lower()
                        if "robloxplayer" in proc_name or "roblox" in proc_name:
                            result.append(hwnd)
                    except Exception:
                        # Если psutil не установлен, просто добавляем по имени
                        result.append(hwnd)
            return True

        win32gui.EnumWindows(enum_callback, None)
        return result[0] if result else None

    def send_key_down(self, hwnd):
        """Отправляет WM_KEYDOWN для W в конкретное окно"""
        lparam_down = (1) | (W_SCANCODE << 16) | (0 << 24) | (0 << 29) | (0 << 30) | (0 << 31)
        try:
            win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, HOLD_KEY, lparam_down)
        except Exception as e:
            print(f"[!] Ошибка отправки KEYDOWN: {e}")

    def send_key_up(self, hwnd):
        """Отправляет WM_KEYUP для W в конкретное окно"""
        lparam_up = (1) | (W_SCANCODE << 16) | (0 << 24) | (0 << 29) | (1 << 30) | (1 << 31)
        try:
            win32api.PostMessage(hwnd, win32con.WM_KEYUP, HOLD_KEY, lparam_up)
        except Exception as e:
            print(f"[!] Ошибка отправки KEYUP: {e}")

    def worker(self):
        """Основной рабочий поток"""
        key_is_held = False

        while self.running:
            with self.lock:
                is_active = self.active

            if is_active:
                # Ищем окно Roblox если ещё не нашли
                if self.roblox_hwnd is None or not win32gui.IsWindow(self.roblox_hwnd):
                    self.roblox_hwnd = self.find_roblox_window()
                    if self.roblox_hwnd:
                        title = win32gui.GetWindowText(self.roblox_hwnd)
                        print(f"[+] Найдено окно Roblox: '{title}' (hwnd={self.roblox_hwnd})")
                    else:
                        print("[!] Окно Roblox не найдено, повтор через 2 сек...")
                        time.sleep(2)
                        continue

                # Зажимаем W — периодически шлём KEYDOWN
                if not key_is_held:
                    self.send_key_down(self.roblox_hwnd)
                    key_is_held = True
                    print(f"[>] {HOLD_KEY_NAME} зажата")
                else:
                    # Повторная отправка KEYDOWN для имитации удержания
                    self.send_key_down(self.roblox_hwnd)

            else:
                # Отпускаем клавишу если была зажата
                if key_is_held and self.roblox_hwnd and win32gui.IsWindow(self.roblox_hwnd):
                    self.send_key_up(self.roblox_hwnd)
                    key_is_held = False
                    print(f"[□] {HOLD_KEY_NAME} отпущена")

            time.sleep(0.05)  # 50мс между повторами

        # При выходе отпускаем
        if key_is_held and self.roblox_hwnd and win32gui.IsWindow(self.roblox_hwnd):
            self.send_key_up(self.roblox_hwnd)
            print(f"[□] {HOLD_KEY_NAME} отпущена (выход)")

    def toggle(self):
        """Переключение вкл/выкл"""
        with self.lock:
            self.active = not self.active
            state = self.active
        status = "ВКЛЮЧЕНО ✅" if state else "ВЫКЛЮЧЕНО ❌"
        print(f"[*] Авто-{HOLD_KEY_NAME}: {status}")

    def stop(self):
        """Полная остановка"""
        with self.lock:
            self.active = False
        self.running = False
        print("\n[X] Скрипт остановлен.")

    def run(self):
        """Запуск"""
        self.print_banner()

        # Запуск рабочего потока
        worker_thread = threading.Thread(target=self.worker, daemon=True)
        worker_thread.start()

        # Регистрация горячих клавиш
        keyboard.on_press_key(TOGGLE_KEY, lambda _: self.toggle(), suppress=False)
        keyboard.on_press_key(EXIT_KEY, lambda _: self.stop(), suppress=False)

        print("[~] Ожидание команд...\n")

        # Главный цикл
        while self.running:
            time.sleep(0.1)

        worker_thread.join(timeout=2)

    def print_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 50)
        print("   ROBLOX AUTO-W HOLDER")
        print("=" * 50)
        print(f"   [{TOGGLE_KEY}]  — Вкл/Выкл удержание {HOLD_KEY_NAME}")
        print(f"   [{EXIT_KEY}]  — Выход из скрипта")
        print(f"   Клавиша: {HOLD_KEY_NAME}")
        print("=" * 50)
        print(f"   Работает даже при свёрнутом окне!")
        print("=" * 50)
        print()


if __name__ == "__main__":
    # Проверка прав администратора (рекомендуется)
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        is_admin = False

    if not is_admin:
        print("[⚠] Рекомендуется запуск от имени администратора!")
        print("    Без этого может не работать с некоторыми окнами.")
        print()

    app = RobloxAutoW()
    try:
        app.run()
    except KeyboardInterrupt:
        app.stop()