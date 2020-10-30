from math import ceil
from random import randint
import sys


def removeAll(arr, n, m, pos=0):
    while arr[pos // m][pos % m] != '#':
        pos += 1
    arr[pos // m][pos % m] = '.'
    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i + j) == 2:
                continue
            if arr[pos // m + i][pos % m + j] == '#':
                removeAll(arr, n, m, pos + i * m + j)


def solve(s):
    for n in range(5, len(s) - 5):
        if len(s) % n == 0:
            m = len(s) // n
            arr = [['.'] * (m + 2)] + [['.'] + list(s[i * m: (i + 1) * m]) + ['.'] for i in range(n)] + [
                ['.'] * (m + 2)]
            removeAll(arr, n + 2, m + 2)
            flag = True
            for i in arr:
                if i.count('#'):
                    flag = False
                    break
            if flag:
                for i in range(n):
                    print(s[i * m: (i + 1) * m])
                break


def main():
    sys.setrecursionlimit(5185)
    for i in range(10000):
        n = randint(5, 100)
        m = randint(5, 100)
        s = ''
        for j in range(n * m):
            s += '#' if randint(0, 1) else '.'
        solve(s)


if __name__ == '__main__':
    main()
