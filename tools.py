import itertools
import time

def progressBar(iterable, decimals = 1, length = 100, iter_len = -1, prefix = 'Progress', suffix = '', fill = '█', time_interval = 0.1):
    if iter_len == -1:
        total = len(iterable)
    else:
        total = iter_len
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% ({iteration}/{total}) {suffix}', end = "\r")
    printProgressBar(0)
    t = time.time()
    for i, item in enumerate(iterable):
        yield item
        if time.time() > t + time_interval or (i == total - 1):
            printProgressBar(i + 1)
            t = time.time()
    print()
