#!/usr/bin/env python
# coding=utf-8

import filecmp
import minimax_test

for i in range(100):
    minimax_test.main('../testcases/{0}.in'.format(i),
                      '../testcases_output/{0}.out'.format(i))
    isSame = filecmp.cmp('../testcases/{0}.out'.format(i), '../testcases_output/{0}.out'.format(i))
    if not isSame:
        print('Failed {0}.'.format(i))
    # os.system('./test_target > /dev/null')
    # print("-->On test case #{0}<--".format(i))
    # os.system('diff ./output.txt ./cases/output{0}.txt'.format(i))
    # os.system('cp ./output.txt ./results/output{0}.txt'.format(i))