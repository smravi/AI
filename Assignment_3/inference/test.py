import filecmp
import Assignment_3.inference.resolve as resolve
from timeit import Timer
passed = []
for i in range(0, 24):
    #if i in [20]:
        t = Timer(lambda: resolve.main('input/input{0}.txt'.format(i),
                          'try_output/output{0}.txt'.format(i)))
        exec_time = '{:.2f}s'.format(t.timeit(number=1))
        print('Input{0}----{1}'.format(i, exec_time))
        isSame = filecmp.cmp('try_output/output{0}.txt'.format(i), 'output/output{0}.txt'.format(i))
        if not isSame:
            passed.append('False')
        else:
            passed.append('True')
print(passed)