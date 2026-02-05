# Задание 1. Создайте программу, которая параллельно вычисляет
# квадраты чисел от 1 до 10 и выводит результаты в консоль.

from multiprocessing import Process

def square_number(n):
    print(f"Квадрат числа {n} = {n**2}")

def main():
    processes = []
    for i in range(1, 11):
        p = Process(target=square_number, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
