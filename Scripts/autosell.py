import keyboard
import mouse
from time import sleep
sleep(3)
while True:
    sleep(0.15)
    mouse.click()
    sleep(0.15)
    keyboard.press_and_release('backspace')
    sleep(0.25)
    keyboard.press_and_release('e')
    if keyboard.is_pressed('capslock'): break