#!/usr/bin/env python
# coding=utf-8

import filecmp
import minimax_beta


from timeit import Timer
fwrite = open('../testcases_output_5000/report.txt', 'w')
failed = []
for i in range(1, 5000):
    if i not in [449, 2767, 1371, 821]:
        t = Timer(lambda: minimax_beta.main('../testcases-5000/INPUT/{0}.in'.format(i),
                          '../testcases_output_5000/{0}.out'.format(i)))
        exec_time = '{:.2f}s'.format(t.timeit(number=1))
        print('Input{0}----{1}'.format(i, exec_time))
        isSame = filecmp.cmp('../testcases-5000/OUTPUT/{0}.out'.format(i), '../testcases_output_5000/{0}.out'.format(i))
        # with open('../testcases-5000/OUTPUT/{0}.out'.format(i), 'r') as f:
        #     reference = f.read()
        #
        # with open('../testcases-5000/OUTPUT/{0}.out'.format(i), 'r') as f1:
        #     generated = f1.read()

        #if generated != reference:
        if not isSame:
            fwrite.write('Failed {0}.'.format(i))
            fwrite.write('\n')
            failed.append(i)
    # if not isSame:
    #     print('Failed {0}.'.format(i))
print(failed)
fwrite.close()