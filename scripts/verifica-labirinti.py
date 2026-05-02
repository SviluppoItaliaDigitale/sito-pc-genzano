#!/usr/bin/env python3
"""Verifica risolvibilità dei labirinti."""

from collections import deque

WALL = '#'
TRAPS = set('AFB')
ARROW_DIRS = {'U': 'up', 'D': 'down', 'L': 'left', 'R': 'right'}
DELTAS = [('up', -1, 0), ('down', 1, 0), ('left', 0, -1), ('right', 0, 1)]


def shortest_path(maze):
    rows = len(maze)
    cols = len(maze[0])
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)
    if not start:
        return -1, 'manca S'
    if not end:
        return -1, 'manca E'

    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        (r, c), d = queue.popleft()
        if (r, c) == end:
            return d, None
        here = maze[r][c]
        for dname, dr, dc in DELTAS:
            if here in ARROW_DIRS and ARROW_DIRS[here] != dname:
                continue
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            ch = maze[nr][nc]
            if ch == WALL or ch in TRAPS:
                continue
            if (nr, nc) in visited:
                continue
            visited.add((nr, nc))
            queue.append(((nr, nc), d + 1))
    return -1, 'nessun percorso'


def verifica(label, maze, max_budget):
    lens = {len(r) for r in maze}
    if len(lens) > 1:
        print(f'  [BUG] {label}: righe di lunghezza diversa: {sorted(lens)}')
        return
    cols = lens.pop()
    rows = len(maze)
    border_ok = (
        all(c == '#' for c in maze[0]) and
        all(c == '#' for c in maze[-1]) and
        all(maze[r][0] == '#' and maze[r][cols - 1] == '#' for r in range(rows))
    )
    if not border_ok:
        print(f'  [BUG] {label}: bordi non chiusi ({rows}x{cols})')
        return
    d, err = shortest_path(maze)
    if err:
        print(f'  [BUG] {label}: {err} ({rows}x{cols})')
        return
    slack = max_budget - d
    flag = 'OK ' if slack >= 0 else 'STR'
    n_traps = sum(1 for row in maze for ch in row if ch in TRAPS)
    n_stairs = sum(1 for row in maze for ch in row if ch == 'X')
    n_arrows = sum(1 for row in maze for ch in row if ch in ARROW_DIRS)
    print(f'  [{flag}] {label}: {rows}x{cols}, shortest={d}, budget={max_budget}, '
          f'slack={slack}, trappole={n_traps}, scale={n_stairs}, frecce={n_arrows}')


SCENARI = [
    ('S1 Aula primo piano', [
        '#########',
        '#S......#',
        '#.#####.#',
        '#.#...#.#',
        '#.###.#X#',
        '#A#...#.#',
        '###.#.#.#',
        '#.#.B.#.#',
        '#.....#E#',
        '#########',
    ], 16),

    ('S2 Fuoco corridoio', [
        '##########',
        '#S.B.....#',
        '#.######.#',
        '#.#......#',
        '#.#.####.#',
        '#...AF.#.#',
        '#.#.####.#',
        '#........#',
        '#.######X#',
        '#......BE#',
        '##########',
    ], 18),

    ('S3 Evacuazione completa', [
        '###########',
        '#S.B......#',
        '#.#######.#',
        '#........A#',
        '#.#######.#',
        '#....X....#',
        '#.#######.#',
        '#...B.....#',
        '#.#######.#',
        '#...B.....#',
        '#.###F###.#',
        '#.#######.#',
        '#........E#',
        '###########',
    ], 22),

    ('S4 Fumo che si propaga', [
        '##########',
        '#S.B...A.#',
        '#.######.#',
        '#...F.B..#',
        '###.######',
        '#X......##',
        '#.######.#',
        '#..B.....#',
        '#.......E#',
        '##########',
    ], 22),

    ('S5 Doppio incendio', [
        '##########',
        '#S.B.....#',
        '#.######.#',
        '#.....F#.#',
        '#.####.#.#',
        '#.#X.#.#.#',
        '#.#.######',
        '#.#.B.F..#',
        '#.######.#',
        '#......RE#',
        '##########',
    ], 18),

    ('S6 Finale completa', [
        '############',
        '#S.B.......#',
        '#.##########',
        '#.#....A...#',
        '#.#.######.#',
        '#.#.#X..B#.#',
        '#.#.######D#',
        '#.#.B......#',
        '#.####F#####',
        '#..........#',
        '#.########.#',
        '#.#......#.#',
        '#.#.#####F.#',
        '#...#......#',
        '#####.######',
        '#.........E#',
        '############',
    ], 38),
]


if __name__ == '__main__':
    print('Verifica labirinti:')
    for label, maze, max_b in SCENARI:
        verifica(label, maze, max_b)
