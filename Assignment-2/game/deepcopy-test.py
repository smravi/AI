import sys
import copy
import timeit


def deepcopytest(A):
    B = copy.deepcopy(A)


def main():
    A = [[20, 16, 1, 32, 30], [20, 12, 2, 11, 8], [28, 48, 9, 1, 1], [20, 12, 10, 6, 2], [25, 30, 23, 21, 10]]
    deepcopytest(A)

if __name__ == '__main__':
    # main()
    exec_time = '{:.2f}s'.format(timeit.timeit("main()",
                                               setup="from __main__ import main", number=6000))
    print(exec_time)