# Задание 1. При старте приложения запускаются три потока. Первый поток
# заполняет список случайными числами. Два других потока ожидают заполнения.
# Когда список заполнен оба потока запускаются. Первый поток находит сумму
# элементов списка, второй поток среднеарифметическое значение в
# списке. Полученный список, сумма и среднеарифметическое выводятся на экран.

print("Задание №1.\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")

import threading
import random

numbers = []
lock = threading.Lock()
event = threading.Event()


def fill_list():
    global numbers
    with lock:
        numbers = [random.randint(1, 100) for _ in range(10)]
        print(f"Полученный список: {numbers}")
    event.set()


def sum_num():
    event.wait()
    with lock:
        s = sum(numbers)
    print(f"Сумма элементов списка: {s}")


def avg_num():
    event.wait()
    with lock:
        avg = sum(numbers) / len(numbers)
    print(f"Среднее арифметическое: {avg}")


th1 = threading.Thread(target=fill_list)
th2 = threading.Thread(target=sum_num)
th3 = threading.Thread(target=avg_num)

th1.start()
th2.start()
th3.start()

th1.join()
th2.join()
th3.join()

# Задание 2. Пользователь с клавиатуры вводит путь к файлу. После чего запускаются
# три потока. Первый поток заполняет файл случайными числами. Два других потока
# ожидают заполнения. Когда файл заполнен оба потока стартуют. Первый поток находит
# все простые числа, второй поток - факториал каждого числа в файле. Результаты поиска
# каждый поток должен записать в новый файл. На экран необходимо отобразить
# статистику выполненных операций.

print("\nЗадание №2.\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")

import threading
import random
import math

event2 = threading.Event()
path_to_file = input("Введите путь к файлу: ")


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def fill_file():
    with open(path_to_file, "w") as f:
        nums = [random.randint(1, 25) for _ in range(10)]
        f.write(" ".join(map(str, nums)))
        print("Файл заполнен числами:", nums)
    event2.set()


def find_primes():
    event2.wait()
    with open(path_to_file, "r") as f:
        nums = list(map(int, f.read().split()))
    primes = [n for n in nums if is_prime(n)]
    with open("primes.txt", "w") as f:
        f.write(" ".join(map(str, primes)))
    print("Простые числа записаны в primes.txt:", primes)


def find_factorials():
    event2.wait()
    with open(path_to_file, "r") as f:
        nums = list(map(int, f.read().split()))
    facts = {n: math.factorial(n) for n in nums}
    with open("factorials.txt", "w") as f:
        for n, fc in facts.items():
            f.write(f"{n}! = {fc}\n")
    print("\nФакториалы записаны в factorials.txt\n")

    print("\nФакториалы чисел:")
    for n, fc in facts.items():
        print(f"{n}! = {fc}")


th1 = threading.Thread(target=fill_file)
th2 = threading.Thread(target=find_primes)
th3 = threading.Thread(target=find_factorials)

th1.start()
th2.start()
th3.start()

th1.join()
th2.join()
th3.join()

# Задание 3. Пользователь с клавиатуры вводит путь к существующей директории и к
# новой директории. После чего запускается поток, который должен скопировать
# содержимое директории в новое место. Необходимо сохранить структуру директории.
# На экран необходимо отобразить статистику выполненных операций.


print("\nЗадание №3.\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")

import threading
import shutil
import os

src = input("Введите путь к существующей директории: ")
dst = input("Введите путь к новой директории: ")


def copy_dir():
    shutil.copytree(src, dst, dirs_exist_ok=True)

    total_files = 0
    total_dirs = 0
    total_size = 0

    for root, dirs, files in os.walk(dst):
        total_dirs += len(dirs)
        total_files += len(files)
        for f in files:
            total_size += os.path.getsize(os.path.join(root, f))

    print(f"\nДиректория {src} успешно скопирована в {dst}")
    print("\nСтатистика выполненных операций:")
    print(f"Создано директорий: {total_dirs}")
    print(f"Скопировано файлов: {total_files}")
    print(f"Общий размер файлов: {total_size} байт")


th = threading.Thread(target=copy_dir)
th.start()
th.join()

# Задание 4. Пользователь с клавиатуры вводит путь к существующей директории и слово
# для поиска. После чего запускаются два потока. Первый должен найти файлы, содержащие
# искомое слово и слить их содержимое в один файл. Второй поток ожидает завершения
# работы первого потока. После чего проводит вырезание всех запрещенных слов (список
# этих слов нужно считать из файла с запрещенными словами) из полученного файла.
# На экран необходимо отобразить статистику выполненных операций.

print("\nЗадание №4.\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")

import threading
import os

src_dir = input("Введите путь к директории: ").strip()
search_word = input("Введите слово для поиска: ").strip()

event3 = threading.Event()

forbidden_words_list = [
    "плохой",
    "дерьмо",
    "ненавижу",
    "глупый",
    "ругательство",
    "неприемлемо",
    "оскорбление",
    "запрещено",
    "гордость",
    "самолюбие"
]

with open("forbidden.txt", "w", encoding="utf-8") as f1:
    f1.write("\n".join(forbidden_words_list))

print("Файл 'forbidden.txt' создан с запрещёнными словами.\n")


def merge_files():
    merged_content = ""
    count_files = 0
    for root, _, files in os.walk(src_dir):
        for file_name in files:
            path = os.path.join(root, file_name)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f2:
                    content = f2.read()
                    if search_word in content:
                        merged_content += content + "\n"
                        count_files += 1
            except (FileNotFoundError, PermissionError, OSError):
                pass

    with open("merged.txt", "w", encoding="utf-8") as f3:
        f3.write(merged_content)

    print(f"\nНайдено файлов со словом '{search_word}': {count_files}")
    print("Содержимое объединено в 'merged.txt'")
    event3.set()


def remove_forbidden():
    event3.wait()
    try:
        with open("forbidden.txt", "r", encoding="utf-8") as f4:
            forbidden_words = f4.read().split()
    except FileNotFoundError:
        print("Файл 'forbidden.txt' не найден. Очистка не выполнена.")
        return

    with open("merged.txt", "r", encoding="utf-8") as f5:
        content = f5.read()

    total_replacements = 0
    for word in forbidden_words:
        count = content.count(word)
        total_replacements += count
        content = content.replace(word, "***")

    with open("cleaned.txt", "w", encoding="utf-8") as f6:
        f6.write(content)

    print(f"Файл очищен от запрещённых слов ({total_replacements} замен) и сохранён в 'cleaned.txt'")


th1 = threading.Thread(target=merge_files)
th2 = threading.Thread(target=remove_forbidden)

th1.start()
th2.start()

th1.join()
th2.join()
