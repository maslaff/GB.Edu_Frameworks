"""� Напишите программу на Python, которая будет находить
сумму элементов массива из 1000000 целых чисел.
� Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
� Массив должен быть заполнен случайными целыми числами
от 1 до 100.
� При решении задачи нужно использовать многопоточность,
многопроцессорность и асинхронность.
� В каждом решении нужно вывести время выполнения
вычислений."""

import time
import random


min_value = 1
max_value = 100
numcount = 1_000_000


def timeof(func):
    def wrapper(*args, **kwargs):
        start_time = time.time_ns()
        func_result = func(*args, **kwargs)
        exec_time = time.time_ns() - start_time
        print(f"Function {func.__name__} executed in \n{f'{exec_time:_}':>25} ns")
        return func_result, exec_time

    return wrapper


class func:
    def __init__(self):
        self.final_numlist = []

    def sum_func(self, numlist):
        # self.final_numlist.append(sum(numlist))
        self.final_numlist.append(synch_sum(numlist))


def synch_sum(numlist):
    acc = 0
    for i in numlist:
        acc += i
    # print(f"Final sum is {acc}")
    return acc


@timeof
def thread_sum(numlist, part_size=100):
    import threading

    print(f"\n\nThread------")

    while len(numlist) > 1:
        threads = []
        main_func = func()
        for i in range(0, len(numlist), part_size):
            thread = threading.Thread(
                target=main_func.sum_func,
                args=[numlist[i : i + part_size]],
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        numlist = main_func.final_numlist

    print(f"Final sum is {main_func.final_numlist[0]}")


def m_func(numlist, acc_list):
    acc_list.append(synch_sum(numlist))


@timeof
def thread_sum2(numlist, parts=5):
    import threading

    acc_list = []

    print(f"\n\nThread------")

    while len(numlist) > parts:
        threads = []

        for i in range(parts):
            part_len = len(numlist) // parts
            thread = threading.Thread(
                target=m_func,
                args=[numlist[part_len * i : part_len * (i + 1)], acc_list],
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        numlist = acc_list

    print(f"Final sum is {synch_sum(acc_list)}")


@timeof
def multiproc_sum(numlist, parts=5):
    from multiprocessing import Process, Manager

    manager = Manager()
    acc_list = manager.list()

    print(f"\n\nMultiproc------")

    while len(numlist) > parts:
        processes = []

        for i in range(parts):
            part_len = len(numlist) // parts
            process = Process(
                target=m_func,
                args=(numlist[part_len * i : part_len * (i + 1)], acc_list),
            )
            processes.append(process)
            process.start()
        for process in processes:
            process.join()
        numlist = acc_list

    print(f"Final sum is {synch_sum(acc_list)}")


@timeof
def async_sum(numlist, parts=5):
    import asyncio

    print(f"\n\nAsync------")

    acc_list = []

    async def synch_sum(numlist):
        acc = 0
        for i in numlist:
            acc += i
        acc_list.append(acc)

        return acc

    async def main():
        part_len = len(numlist) // parts
        tasks = [
            asyncio.create_task(synch_sum(numlist[part_len * i : part_len * (i + 1)]))
            for i in range(parts)
        ]
        await asyncio.gather(*tasks)

    asyncio.run(main())
    # print(asyncio.run(synch_sum(acc_list)))

    print(f"Final sum is {asyncio.run(synch_sum(acc_list))}")


@timeof
def printsum(lst):
    print(f"Final sum is {sum(lst)}")


if __name__ == "__main__":
    rand_list = [random.randint(min_value, max_value) for _ in range(numcount)]
    # rand_list = [i for i in range(min_value, max_value + 1)]
    rl = rand_list
    tme_sum = printsum(rl)[1]

    print(f"\n\nSync------")
    sync_sum_func = timeof(synch_sum)
    rl = rand_list
    tme_sync_sum_result, tme_sync_sum = sync_sum_func(rl)
    print(f"Final sum is {tme_sync_sum_result}")
    print(f"Longer than 'sum' times:\n{tme_sync_sum / tme_sum:>25.02f}")
    del sync_sum_func

    rl = rand_list
    tme_thread_sum = thread_sum2(rl)[1]
    print(f"Longer than Synch times:\n{tme_thread_sum / tme_sync_sum:>25.02f}")

    rl = rand_list
    tme_multiproc_sum = multiproc_sum(rl)[1]
    print(f"Longer than Synch times:\n{tme_multiproc_sum / tme_sync_sum:>25.02f}")
    tme_async_sum = async_sum(rl)[1]
    print(f"Longer than Synch times:\n{tme_async_sum / tme_sync_sum:>25.02f}")
