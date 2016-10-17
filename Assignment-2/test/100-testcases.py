#!/usr/bin/env python
# coding=utf-8

import filecmp
import minimax_tie_test
from timeit import Timer
for i in range(100):
    t = Timer(lambda: minimax_tie_test.main('../testcases/{0}.in'.format(i),
                      '../testcases_output/{0}.out'.format(i)))
    exec_time = '{:.2f}s'.format(t.timeit(number=1))
    print('Input{0}----{1}'.format(i, exec_time))
    isSame = filecmp.cmp('../testcases/{0}.out'.format(i), '../testcases_output/{0}.out'.format(i))
    if not isSame:
        print('Failed {0}.'.format(i))
