# Задание 3. Создайте программу, где родительский процесс создает
# два дочерних процесса: один читает содержимое текстового файла,
# а другой записывает в новый файл перевернутые строки из исходного файла.

from multiprocessing import Process, Queue
import os

def read_file(queue, filename):
    pid = os.getpid()
    print(f"Процесс-читатель (PID: {pid}) начал чтение файла '{filename}'")
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
    print(f"Процесс-читатель (PID: {pid}) прочитал {len(lines)} строку(и)")
    queue.put(lines)

def write_reversed(queue, filename):
    pid = os.getpid()
    lines = queue.get()
    print(f"Процесс-писатель (PID: {pid}) начал запись в файл '{filename}'")
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line[::-1] + "\n")
    print(f"Процесс-писатель (PID: {pid}) записал {len(lines)} перевернутую строку(и)")

def main():
    print("=== Родительский процесс: Управление дочерними процессами ===")
    print(f"Родительский процесс PID: {os.getpid()}")

    input_file = "input.txt"
    output_file = "output.txt"

    if not os.path.exists(input_file):
        with open(input_file, "w", encoding="utf-8") as f:
            f.write("Программа читает строку и создаёт перевернутую версию.\n")
        print(f"Создан пример файла '{input_file}'")

    queue = Queue()

    reader = Process(target=read_file, args=(queue, input_file))
    reader.start()
    print(f"Запущен процесс-читатель с PID: {reader.pid}")
    reader.join()
    print("Родительский процесс получил строки от процесса-читателя")

    writer = Process(target=write_reversed, args=(queue, output_file))
    writer.start()
    print(f"Запущен процесс-писатель с PID: {writer.pid}")
    writer.join()

    print("\n=== Содержимое файлов ===")
    print(f"Входной файл '{input_file}':")
    with open(input_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            print(f"  {i}: {line.strip()}")

    print(f"\nВыходной файл '{output_file}':")
    with open(output_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            print(f"  {i}: {line.strip()}")

if __name__ == "__main__":
    main()




