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


def synch_sum(numlist):
    acc = 0
    for i in numlist:
        acc += i
    return acc


def m_func(numlist, acc_list):
    acc_list.append(synch_sum(numlist))


@timeof
def thread_sum(numlist, parts=5):
    import threading

    acc_list = []

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

    return synch_sum(acc_list)


@timeof
def multiproc_sum(numlist, parts=5):
    from multiprocessing import Process, Manager

    manager = Manager()
    acc_list = manager.list()

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

    return synch_sum(acc_list)


@timeof
def async_sum(numlist, parts=5):
    import asyncio

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

    return asyncio.run(synch_sum(acc_list))


def main():
    fin_str = "Final sum is {}"
    tme_str = "Longer than {} times:\n{:>25.02f}"

    randnum_list = [random.randint(min_value, max_value) for _ in range(numcount)]

    sum_func = timeof(sum)
    tme_sum_result, tme_sum = sum_func(randnum_list)
    print(fin_str.format(tme_sum_result))

    print("\n\nSync------")
    sync_sum_func = timeof(synch_sum)
    tme_sync_sum_result, tme_sync_sum = sync_sum_func(randnum_list)
    print(fin_str.format(tme_sync_sum_result))
    print(tme_str.format("'str'", tme_sync_sum / tme_sum))

    print("\n\nThread------")
    tme_thread_sum_result, tme_thread_sum = thread_sum(randnum_list)
    print(fin_str.format(tme_thread_sum_result))
    print(tme_str.format("Sync", tme_thread_sum / tme_sync_sum))

    print("\n\nMultiproc------")
    tme_multiproc_sum_result, tme_multiproc_sum = multiproc_sum(randnum_list)
    print(fin_str.format(tme_multiproc_sum_result))
    print(tme_str.format("Sync", tme_multiproc_sum / tme_sync_sum))

    print("\n\nAsync------")
    tme_async_sum_result, tme_async_sum = async_sum(randnum_list)
    print(fin_str.format(tme_async_sum_result))
    print(tme_str.format("Sync", tme_async_sum / tme_sync_sum))

    print("\n")
    if (
        tme_sum_result
        == tme_sync_sum_result
        == tme_thread_sum_result
        == tme_multiproc_sum_result
        == tme_async_sum_result
    ):
        print("sums is OK")
    else:
        print("one or more sums is bad")


if __name__ == "__main__":
    main()
