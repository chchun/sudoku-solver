#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2016 David Shi (dcmshi)

import sudoku

# Some example puzzles

examples = ([
    1,3,0, 0,0,6, 0,0,0,
    0,7,4, 0,0,2, 5,8,0,
    0,0,0, 0,5,0, 3,0,0,

    0,8,0, 0,1,0, 0,0,0,
    0,0,0, 0,6,0, 0,2,9,
    0,0,0, 0,0,0, 4,3,0,

    0,0,0, 0,3,0, 0,5,0,
    9,0,3, 0,0,0, 7,0,4,
    0,0,0, 0,7,5, 8,0,0,
], [
    0,0,8, 0,1,0, 0,0,0,
    0,0,1, 3,0,7, 0,0,9,
    0,0,0, 9,0,6, 0,3,0,

    0,2,0, 7,9,0, 1,0,0,
    4,0,0, 0,0,0, 0,0,2,
    0,0,5, 0,3,8, 0,9,0,

    0,5,0, 8,0,2, 0,0,0,
    2,0,0, 6,0,9, 3,0,0,
    0,0,0, 0,4,0, 2,0,0,
], [
    8,5,0, 0,0,2, 4,0,0,
    7,2,0, 0,0,0, 0,0,9,
    0,0,4, 0,0,0, 0,0,0,

    0,0,0, 1,0,7, 0,0,2,
    3,0,5, 0,0,0, 9,0,0,
    0,4,0, 0,0,0, 0,0,0,

    0,0,0, 0,8,0, 0,7,0,
    0,1,7, 0,0,0, 0,0,0,
    0,0,0, 0,3,6, 0,4,0,
], [
    8,0,0, 0,0,0, 0,0,0,
    0,0,3, 6,0,0, 0,0,0,
    0,7,0, 0,9,0, 2,0,0,

    0,5,0, 0,0,7, 0,0,0,
    0,0,0, 0,4,5, 7,0,0,
    0,0,0, 1,0,0, 0,3,0,

    0,0,1, 0,0,0, 0,6,8,
    0,0,8, 5,0,0, 0,1,0,
    0,9,0, 0,0,0, 4,0,0,
])

for example in examples:
    print "EXAMPLE:"
    problem = sudoku.Sudoku(example)
    print problem.ascii
    solution = problem.solve()
    if solution:
        print "Solution:"
        print solution.ascii
    else:
        print "Invalid puzzle."
print