# Задание 4. Реализуйте параллельное вычисление суммы элементов
# большого списка (минимум 1000 элементов), разделив список между
# несколькими процессами и объединив результаты.

from multiprocessing import Process, Queue
import random

def partial_sum(numbers, queue, process_num):
    s = sum(numbers)
    print(f"Процесс-{process_num} вычислил сумму = {s}")
    queue.put(s)

def main():
    total_elements = 1000  # минимум 1000 элементов
    num_processes = 4

    numbers = [random.randint(1, 100) for _ in range(total_elements)]
    print(f"Список создан: {total_elements} элементов")
    print(f"Список будет разделен на {num_processes} процессов\n")

    chunk_size = total_elements // num_processes

    queue = Queue()
    processes = []

    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_processes - 1 else total_elements
        chunk = numbers[start:end]
        p = Process(target=partial_sum, args=(chunk, queue, i+1))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    partial_sums = [queue.get() for _ in range(num_processes)]
    total_sum = sum(partial_sums)

    print(f"\nОбщая сумма элементов списка: {total_sum}")

if __name__ == "__main__":
    main()



