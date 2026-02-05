# Задание 2. Напишите программу, которая использует 3 процесса
# для поиска максимального значения в трех разных массивах
# случайных чисел (каждый массив размером 100 элементов).

from multiprocessing import Process, Queue
import random

def find_max(numbers, queue, array_name):
    max_value = max(numbers)
    queue.put((array_name, max_value))

def main():
    queue = Queue()
    processes = []

    arrays = {
        "Массив 1": [random.randint(1, 1000) for _ in range(100)],
        "Массив 2": [random.randint(1, 1000) for _ in range(100)],
        "Массив 3": [random.randint(1, 1000) for _ in range(100)]
    }

    for name, arr in arrays.items():
        p = Process(target=find_max, args=(arr, queue, name))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    results = [queue.get() for _ in range(3)]
    results.sort(key=lambda x: x[0])

    for array_name, max_value in results:
        print(f"{array_name}: Максимум = {max_value}")

    all_max = [max_value for _, max_value in results]
    print("Общий максимум всех массивов:", max(all_max))

if __name__ == "__main__":
    main()


