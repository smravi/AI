#!/usr/bin/env python
# coding=utf-8

import filecmp
import minimax_beta
from timeit import Timer
for i in range(5,6):
    t = Timer(lambda: minimax_beta.main('../input/input{0}.txt'.format(i),
                      'dev-test-output/output{0}.txt'.format(i)))
    exec_time = '{:.2f}s'.format(t.timeit(number=1))
    print('Input{0}----{1}'.format(i, exec_time))
    isSame = filecmp.cmp('../output/output{0}.txt'.format(i), 'dev-test-output/output{0}.txt'.format(i))
    if not isSame:
        print('Failed {0}.'.format(i))
