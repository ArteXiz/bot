import itertools

with open("codes.txt", "w", encoding="utf-8") as file:
    for code in itertools.product(range(6), repeat=5):
        file.write("".join(map(str, code)) + "\n")

print("Файл codes.txt создан. Все коды записаны построчно.")
