#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2015-10-26 15:56:26
# @Last Modified by:   anchen
# @Last Modified time: 2015-10-26 16:16:49

import sys
from numpy import mat, mean, power

def read_input(file):
    for line in file:
        yield line.strip()

input = read_input(sys.stdin)
result = [subresult.strip().split('\t') for subresult in input]
total_num = 0
total_mean = 0.0
total_var = 0.0
for each in result:
    total_num+=float(each[0])
    total_mean+=float(each[0])*float(each[1])
    total_var+=float(each[0])*float(each[2])
real_mean = total_mean/total_num
real_var = (total_var+total_num*real_mean*real_mean-2*real_mean*total_mean)/total_num
print '%d\t%f\t%f ' % (total_num, real_mean, real_var)
print >> sys.stderr, 'report: still working'
