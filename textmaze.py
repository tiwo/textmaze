#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2007-2011 ${me}
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <http://www.gnu.org/licenses/>.

import random

class Equivalence(object):
    """
    Example::

        >>> e = Equivalence(range(14))
        >>> len(e)
        14
        >>> e[3]
        3
        >>> e.modulo(2,3)
        >>> e.modulo(4,5)
        >>> e.modulo(3,4)
        >>> len(e)
        11
        >>> e[5]
        2
        >>> e.equiv(2,4)
        True
        
    """
    def __init__(self, iterable=()):
        self._d = {}
        self._n = 0
        for i in iterable:
            self.isolate(i)

    def isolate(self, i):
        self._d[i] = i
        self._n += 1

    def __getitem__(self, key):
        return self._d[key]
    
    def __len__(self):
        return self._n

    def modulo(self, one, another):
        rep1 = self[one]
        rep2 = self[another]
        found = 0 
        for i in self._d.keys():
            if self._d[i] == rep2:
                self._d[i] = rep1
                found = 1
        self._n -= found

    def equiv(self, one, another):
        return self._d[one] == self._d[another]
            

import doctest
doctest.testmod()

_UP = 1 << 0
_LE = 1 << 1
_DN = 1 << 2
_RI = 1 << 3
_DIRS = {
         _UP: (-1, 0, _DN),
         _LE: (0, -1, _RI),
         _DN: (+1, 0, _UP),
         _RI: (0, +1, _LE)}
_CHARS = u" ╵╴┘╷│┐┤╶└─┴┌├┬┼"

def gen_maze(m, n):
    """generate a maze of size n×m"""
    maze = []
    for i in range(m):
        maze.append(n * [0])
    walls = []
    
    equiv = Equivalence()
    for i in range(m):
        for j in range(n):
            assert maze[i][j] == 0
            equiv.isolate((i, j))
            if i > 0:
                walls.append((i, j, _UP))
            if j > 0:
                walls.append((i, j, _LE))
    random.shuffle(walls)

    for i, j, direction in walls:
        _ = _DIRS[direction]
        I = i + _[0]
        J = j + _[1]
        Direction = _[2]
        assert 0 <= i <= m
        assert 0 <= j <= n
        assert 0 <= I <= m
        assert 0 <= J <= n
        if not equiv.equiv((i, j), (I, J)):
            maze[i][j] += direction
            maze[I][J] += Direction
            assert maze[i][j] < (2<<4)
            assert maze[I][J] < (2<<4)
            equiv.modulo((i, j), (I, J))

    return maze

            
if __name__ == "__main__":
    m, n = 20, 20
    maze = gen_maze(m, n)
    for i in range(m):
        print "".join(_CHARS[c] for c in maze[i])

