# CREDIT: alexcoplan wrote this in javascript:
# (https://github.com/alexcoplan/scrambler),
# I just translated it to python.

import random

def choose(arr):
    index = random.randint(0, len(arr) - 1)
    return arr[index]

def scramble(length):
    planes = {'x': ['L', 'R'], 'y': ['U', 'D'], 'z': ['F', 'B']}
    planeMap = {}
    for plane in planes:
        sides = planes[plane]
        for i in range(len(sides)):
            planeMap[sides[i]] = plane
    sides = ['F', 'B', 'R', 'L', 'U', 'D']
    modifiers = ['2', '\'', '']
    weakBuffer = []
    moves = []
    for i in range(length):
        mod = choose(modifiers)
        if len(weakBuffer) == 0:
            side = choose(sides)
        elif len(weakBuffer) == 1:
            badSide = weakBuffer[0]
            newSides = sides.copy()
            badIndex = newSides.index(badSide)
            newSides.pop(badIndex)
            side = choose(newSides)
            if planeMap[side] != planeMap[badSide]:
                weakBuffer = []
        else:
            newSides = sides.copy()
            for a in range(len(weakBuffer)):
                badSide = weakBuffer[a]
                badIndex = newSides.index(badSide)
                newSides.pop(badIndex)
            side = choose(newSides)
            weakBuffer = []
        moves.append(side + mod)
        weakBuffer.append(side)
    return ' '.join(moves)
