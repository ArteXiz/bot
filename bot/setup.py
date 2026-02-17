import os

#com_type_deleted = False

print("(----------------------------------------)")
print("(------------Настройка бота--------------)")
print("(----------------------------------------)")
print("")

print("Введите имя бота, пробелы будут удалены.")
bot_name = input("Имя: ").replace(" ", "")

print("Введите то, какой тон общения вы хотите с ботом, например Дружелюбный (кратко)")
comunnication_type = input("Тон общения: ")

if os.path.isfile("bot/data/name.txt"):
    os.remove("bot/data/name.txt")
with open("bot/data/name.txt", "a", encoding="utf-8") as file: #read - "r"
    file.write(bot_name)

if os.path.isfile("bot/data/comtype.txt"):
    os.remove("bot/data/comtype.txt")
with open("bot/data/comtype.txt", "a", encoding="utf-8") as file: #read - "r"
    file.write(comunnication_type)