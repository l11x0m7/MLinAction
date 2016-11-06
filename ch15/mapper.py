import sys
from numpy import mean,mat,power

def read_input(file):
    for line in file:
        yield line.rstrip()

input = read_input(sys.stdin)
numbers = [float(line) for line in input]
count = len(numbers)
mean_num = mean(numbers)
numbers = mat(numbers)
square_num = power(numbers,2)
print '%d\t%f\t%f ' % (count, mean_num, mean(square_num))
print >> sys.stderr, 'report: still working'
