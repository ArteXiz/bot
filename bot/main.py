#запускать в кмд т.к. пайчарм не поймет директорию
from functions import *
from groq import Groq
import os
import subprocess

with open("bot/data/name.txt", "r", encoding="utf-8") as file:
    bot_name = file.read()
with open("bot/data/comtype.txt", "r", encoding="utf-8") as file:
    com_type = file.read()

if os.path.isfile("bot/data/name.txt") == False or os.path.isfile("bot/data/comtype.txt") == False:
    subprocess.run(["python", "bot/setup.py"])

#вторая проверка на их содержимое
with open("bot/data/name.txt", "r", encoding="utf-8") as file:
    bot_name = file.read()
    if len(bot_name) == 0:
        subprocess.run(["python", "bot/setup.py"])

with open("bot/data/comtype.txt", "r", encoding="utf-8") as file:
    com_type = file.read()
    if len(com_type) == 0:
        subprocess.run(["python", "setup.py"])

menu = f"""
Привет, я {bot_name}!

Выберите действие:
1. Задать вопрос
2. Угадай слово
3. Калькулятор

Off - Закончить работу.
"""
print(menu)

choose = input().lower()
while choose != "off":
    choose = input().lower()

    if choose == "1" or choose == "вопрос":
        sys_prompt = None
        user_ask = input("Введите вопрос: ")
        add_sys_prompt = input("Хотите ли вы задать системный промпт? ").lower()
        if add_sys_prompt == "да":
            sys_prompt = input("Введите системный промпт: ")
        else: pass

        print(chat.ask(user_ask, bot_name, com_type, sys_prompt, model="openai/gpt-oss-20b"))

    elif choose == "2" or choose == "слово" or choose == "угадай слово" or choose == "слово":
        print("""   В этой игре нужно угадать слово. Правила игры:
        Вы вводите 1 слово и оценивается его близость по лексическому значению с секретным
        загаданным словом от 0 до 100. 0 - абсолюнто разные слова, 100 - то же слово. 
        Цель игры: Угадать загаданное слово.
        Напишите "Сдаться" для выхода из игры.""")

        secret_word = wordgame.get_word()
        rate = None
        guessed = None
        #print(secret_word)
        while rate != 100 or guessed == "сдаться":
            guessed = input("Введите слово: ").lower()
            rate = int(wordgame.rate_range(guessed, secret_word))
            print("Близость ответа к загаданному слову: ", rate, " из 100")
            print(guessed)
        print("Загаданное слово: ", secret_word)

    elif choose == "3" or choose == "калькулятор":
        num1 = int(input("Первое число: "))
        num2 = int(input("Второе число: "))
        oper = input("Оператор (*, /, +, -): ")

        print(calculator.calcul(num1, num2, oper))
    else:
        print("Действие не распознано")

