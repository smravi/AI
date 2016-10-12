import sys
from math import factorial

def permutation(depth, freetiles):
    total = 0
    val = factorial(freetiles)
    for i in range(freetiles, freetiles - depth -1, -1):
        print(i)
        total += val // factorial(i)
    return total
print(permutation(8, 25))