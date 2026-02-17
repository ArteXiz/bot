import tkinter as tk
import pyautogui
import keyboard
import pyperclip
import threading
import time
import winsound

# ============ НАСТРОЙКИ ============
COPY_KEY = 'f7'        # Скопировать координаты
EXIT_KEY = 'f8'        # Выйти
OFFSET_X = 20          # Смещение подсказки от курсора
OFFSET_Y = 20
UPDATE_RATE = 30       # Обновлений в секунду
# ====================================


class MouseTracker:
    def __init__(self):
        self.saved_points = []
        self.running = True

        # Создаём прозрачное окно-оверлей
        self.root = tk.Tk()
        self.root.title("Tracker")
        self.root.attributes('-topmost', True)       # Всегда поверх
        self.root.attributes('-alpha', 0.85)         # Полупрозрачность
        self.root.overrideredirect(True)             # Без рамки
        self.root.configure(bg='black')

        # Лейбл с координатами
        self.label = tk.Label(
            self.root,
            text="X: 0  Y: 0",
            font=("Consolas", 14, "bold"),
            fg="#00ff00",
            bg="black",
            padx=8,
            pady=4
        )
        self.label.pack()

        # Лейбл с подсказками
        self.hint = tk.Label(
            self.root,
            text=f"{COPY_KEY.upper()} — скопировать | {EXIT_KEY.upper()} — выход",
            font=("Consolas", 9),
            fg="#888888",
            bg="black",
            padx=8,
            pady=2
        )
        self.hint.pack()

        # Лейбл для последнего сохранения
        self.saved_label = tk.Label(
            self.root,
            text="",
            font=("Consolas", 10),
            fg="#ffcc00",
            bg="black",
            padx=8,
            pady=2
        )
        self.saved_label.pack()

        # Делаем окно "прозрачным" для кликов мыши
        self.make_click_through()

        # Горячие клавиши
        keyboard.on_press_key(COPY_KEY, lambda _: self.copy_position())
        keyboard.on_press_key(EXIT_KEY, lambda _: self.stop())

        # Запускаем обновление
        self.update_position()

        print(f"\n{'='*45}")
        print(f"  Трекер мыши запущен")
        print(f"  {COPY_KEY.upper()} — скопировать координаты")
        print(f"  {EXIT_KEY.upper()} — выйти")
        print(f"{'='*45}\n")

        self.root.mainloop()

    def make_click_through(self):
        """Окно не перехватывает клики мыши (Windows)"""
        try:
            import ctypes
            hwnd = ctypes.windll.user32.FindWindowW(None, "Tracker")
            # Находим окно по handle tkinter
            hwnd = self.root.winfo_id()

            import ctypes.wintypes
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x80000
            WS_EX_TRANSPARENT = 0x20

            # Получаем handle родительского окна
            parent = ctypes.windll.user32.GetParent(hwnd)
            if parent:
                hwnd = parent

            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        except Exception:
            pass  # Не критично если не сработает

    def update_position(self):
        """Обновляет позицию и текст оверлея"""
        if not self.running:
            return

        try:
            x, y = pyautogui.position()

            # Получаем цвет пикселя
            try:
                r, g, b = pyautogui.pixel(x, y)
                color_text = f"RGB({r},{g},{b})"
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                color_display = f"{color_text} {hex_color}"
            except Exception:
                color_display = ""

            # Обновляем текст
            self.label.config(
                text=f"X: {x}   Y: {y}\n{color_display}"
            )

            # Позиция окна рядом с курсором
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()
            win_w = self.root.winfo_width()
            win_h = self.root.winfo_height()

            # Если окно уходит за правый край — показываем слева от курсора
            new_x = x + OFFSET_X
            new_y = y + OFFSET_Y

            if new_x + win_w > screen_w:
                new_x = x - win_w - OFFSET_X
            if new_y + win_h > screen_h:
                new_y = y - win_h - OFFSET_Y

            self.root.geometry(f"+{new_x}+{new_y}")

        except Exception:
            pass

        # Повторяем
        self.root.after(1000 // UPDATE_RATE, self.update_position)

    def copy_position(self):
        """Копирует координаты в буфер обмена"""
        x, y = pyautogui.position()

        # Формат для вставки в код
        text = f"X = {x}, Y = {y}"
        pyperclip.copy(text)

        # Сохраняем
        self.saved_points.append((x, y))
        index = len(self.saved_points)

        # Обновляем лейбл
        self.saved_label.config(
            text=f"✓ Сохранено #{index}: X={x} Y={y}"
        )

        # Звук подтверждения
        try:
            winsound.Beep(800, 150)
        except Exception:
            pass

        # Выводим в консоль
        print(f"  [{index}] Скопировано: X = {x}, Y = {y}")

        # Если набрали достаточно точек — показываем итог
        if len(self.saved_points) >= 1:
            self.print_summary()

    def print_summary(self):
        """Выводит все сохранённые точки"""
        print(f"\n  --- Сохранённые координаты ---")
        labels = [
            "INPUT_FIELD (поле ввода)",
            "SUBMIT_BUTTON (кнопка)",
            "ERROR_TEXT (ошибка)",
            "Точка 4",
            "Точка 5"
        ]
        for i, (x, y) in enumerate(self.saved_points):
            name = labels[i] if i < len(labels) else f"Точка {i+1}"
            print(f"  {name}: X = {x}, Y = {y}")
        print()

    def stop(self):
        self.running = False
        print(f"\n{'='*45}")
        print("  Итоговые координаты для скрипта:")
        print(f"{'='*45}")

        if len(self.saved_points) >= 1:
            p = self.saved_points[0]
            print(f"  INPUT_FIELD_X = {p[0]}")
            print(f"  INPUT_FIELD_Y = {p[1]}")

        if len(self.saved_points) >= 2:
            p = self.saved_points[1]
            print(f"  SUBMIT_BUTTON_X = {p[0]}")
            print(f"  SUBMIT_BUTTON_Y = {p[1]}")

        if len(self.saved_points) >= 3:
            p = self.saved_points[2]
            print(f"  # Позиция ошибки: X = {p[0]}, Y = {p[1]}")

        print(f"{'='*45}\n")

        try:
            self.root.destroy()
        except:
            pass


if __name__ == "__main__":
    tracker = MouseTracker()