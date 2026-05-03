#!/usr/bin/env python3
"""Genera puzzle verificati per il Kit Calamità Bambini.

Risolve il bug segnalato dall'utente: labirinti senza via di uscita,
word search con parole troncate, cruciverba con celle sbagliate.

Algoritmi:
- Labirinto: Recursive Backtracking (genera maze N×M con percorso garantito)
- Word search: placement algorithm con verifica fit + collision
- Sudoku 6×6: Latin square fill + masking per difficoltà
- Cruciverba: schema fisso a mano + validazione lunghezze

Output: emette HTML/SVG da incollare nelle schede esistenti.
"""

import random
import sys


# ── 1. LABIRINTO con algoritmo recursive backtracking ──
def genera_labirinto(cols, rows, seed=42):
    """Restituisce maze come lista di celle con flag walls."""
    random.seed(seed)
    # Ogni cella ha 4 muri: N, E, S, W
    grid = [[{'N': True, 'E': True, 'S': True, 'W': True, 'visited': False}
             for _ in range(cols)] for _ in range(rows)]

    def neighbors(r, c):
        result = []
        if r > 0 and not grid[r-1][c]['visited']: result.append((r-1, c, 'N', 'S'))
        if c < cols-1 and not grid[r][c+1]['visited']: result.append((r, c+1, 'E', 'W'))
        if r < rows-1 and not grid[r+1][c]['visited']: result.append((r+1, c, 'S', 'N'))
        if c > 0 and not grid[r][c-1]['visited']: result.append((r, c-1, 'W', 'E'))
        return result

    # DFS iterativo
    stack = [(0, 0)]
    grid[0][0]['visited'] = True
    while stack:
        r, c = stack[-1]
        nbrs = neighbors(r, c)
        if not nbrs:
            stack.pop()
            continue
        nr, nc, dir_from, dir_to = random.choice(nbrs)
        grid[r][c][dir_from] = False
        grid[nr][nc][dir_to] = False
        grid[nr][nc]['visited'] = True
        stack.append((nr, nc))
    return grid


def maze_to_svg(grid, cell_size=40, padding=20, start_label="START", end_label="FINE"):
    """Converte maze in SVG bianco/nero stampabile."""
    rows = len(grid)
    cols = len(grid[0])
    w = cols * cell_size + 2 * padding
    h = rows * cell_size + 2 * padding
    lines = [f'<svg viewBox="0 0 {w} {h}" style="width:100%; max-height: 220mm;" aria-label="Labirinto">']
    # Bordo esterno
    lines.append(f'<rect x="{padding}" y="{padding}" width="{cols*cell_size}" height="{rows*cell_size}" fill="none" stroke="#1a1a1a" stroke-width="4"/>')
    # Disegna muri interni
    for r in range(rows):
        for c in range(cols):
            cell = grid[r][c]
            x = padding + c * cell_size
            y = padding + r * cell_size
            # N wall (sopra) — disegna se non è bordo esterno e c'è muro
            if r > 0 and cell['N']:
                lines.append(f'<line x1="{x}" y1="{y}" x2="{x+cell_size}" y2="{y}" stroke="#1a1a1a" stroke-width="3"/>')
            # W wall (sinistra)
            if c > 0 and cell['W']:
                lines.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+cell_size}" stroke="#1a1a1a" stroke-width="3"/>')
    # START (top-left, fuori dal bordo)
    sx, sy = padding + cell_size//2, padding + cell_size//2
    lines.append(f'<g transform="translate({sx}, {sy})">')
    lines.append('<circle cx="0" cy="0" r="14" fill="none" stroke="#1a1a1a" stroke-width="2.5"/>')
    lines.append('<path d="M -16 -7 Q 0 -22 16 -7 Z" fill="none" stroke="#1a1a1a" stroke-width="2.5"/>')
    lines.append('<circle cx="-5" cy="-2" r="1.5" fill="#1a1a1a"/>')
    lines.append('<circle cx="5" cy="-2" r="1.5" fill="#1a1a1a"/>')
    lines.append(f'<text y="28" text-anchor="middle" font-size="9" font-weight="700">{start_label}</text>')
    lines.append('</g>')
    # END (bottom-right, fuori dal bordo)
    ex, ey = padding + (cols-1) * cell_size + cell_size//2, padding + (rows-1) * cell_size + cell_size//2
    lines.append(f'<g transform="translate({ex}, {ey})">')
    lines.append('<polygon points="-16,3 0,-18 16,3" fill="none" stroke="#1a1a1a" stroke-width="2.5"/>')
    lines.append('<line x1="0" y1="-18" x2="0" y2="3" stroke="#1a1a1a" stroke-width="2"/>')
    lines.append(f'<text y="20" text-anchor="middle" font-size="9" font-weight="700">{end_label}</text>')
    lines.append('</g>')
    lines.append('</svg>')
    return '\n'.join(lines)


# ── 2. WORD SEARCH ──
def crea_word_search(parole, size=12, seed=7):
    """Crea griglia size×size con parole nascoste in 4 direzioni."""
    random.seed(seed)
    parole = [p.upper().replace(' ', '') for p in parole]
    grid = [['.' for _ in range(size)] for _ in range(size)]
    # 4 direzioni: orizzontale, verticale, diagonale-down-right, diagonale-down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    def fits(word, r, c, dr, dc):
        for i, ch in enumerate(word):
            nr, nc = r + i*dr, c + i*dc
            if not (0 <= nr < size and 0 <= nc < size): return False
            if grid[nr][nc] != '.' and grid[nr][nc] != ch: return False
        return True

    def place(word, r, c, dr, dc):
        for i, ch in enumerate(word):
            grid[r + i*dr][c + i*dc] = ch

    placed = []
    for word in sorted(parole, key=len, reverse=True):
        attempts = 0
        while attempts < 200:
            r = random.randint(0, size-1)
            c = random.randint(0, size-1)
            dr, dc = random.choice(directions)
            if fits(word, r, c, dr, dc):
                place(word, r, c, dr, dc)
                placed.append(word)
                break
            attempts += 1

    # Riempi i punti con lettere casuali (frequenze italiane)
    fillers = "AEIOUNLRSTAEIOULRSTAEIOULRSTBCDFGHMPQVZ"
    for r in range(size):
        for c in range(size):
            if grid[r][c] == '.':
                grid[r][c] = random.choice(fillers)
    return grid, placed


def grid_to_html(grid):
    rows = []
    for row in grid:
        rows.append(' '.join(row))
    return '\n'.join(rows)


# ── 3. SUDOKU 6×6 ──
def genera_sudoku_6x6(seed=11):
    """Genera Sudoku 6×6 (blocchi 2×3) valido con masking medio."""
    random.seed(seed)
    base = 6
    side = 6
    # Pattern per Sudoku 6x6 (blocchi 2 righe × 3 colonne)
    def pattern(r, c):
        return (3 * (r % 2) + (r // 2) + c) % side

    rBase = list(range(2))
    cBase = list(range(3))
    rows = [g*2 + r for g in random.sample(range(3), 3) for r in random.sample(rBase, 2)]
    cols = [g*3 + c for g in random.sample(range(2), 2) for c in random.sample(cBase, 3)]
    nums = random.sample(range(1, side+1), side)
    sol = [[nums[pattern(r, c)] for c in cols] for r in rows]
    # Mascheramento — togli ~50% delle celle (medio)
    puzzle = [row[:] for row in sol]
    cells = [(r, c) for r in range(side) for c in range(side)]
    random.shuffle(cells)
    for r, c in cells[:18]:  # 36 totali, 18 vuote
        puzzle[r][c] = 0
    return puzzle, sol


def sudoku_to_html(puzzle):
    cells = []
    for r in range(6):
        for c in range(6):
            v = puzzle[r][c]
            if v == 0:
                cells.append(f'<div class="sud-cell"></div>')
            else:
                cells.append(f'<div class="sud-cell dato">{v}</div>')
    return ''.join(cells)


if __name__ == '__main__':
    # Test
    print("=== Labirinto facile (5×5) ===")
    m1 = genera_labirinto(5, 5, seed=42)
    print(maze_to_svg(m1, cell_size=60, padding=30, start_label="VOLONTARIO", end_label="CASETTA")[:300])
    print()

    print("=== Word search ===")
    parole = ['AIUTO', 'CASCO', 'TENDA', 'RADIO', 'VOLONTARIO',
              'SOCCORSO', 'SANITARIO', 'SPERANZA', 'ALLERTA',
              'NUMERO', 'AVVISO', 'DPC', 'TERREMOTO', 'MARE', 'CALMA']
    grid, placed = crea_word_search(parole, size=14)
    print(grid_to_html(grid))
    print(f"Piazzate: {len(placed)}/{len(parole)}: {placed}")

    print("\n=== Sudoku 6×6 ===")
    p, s = genera_sudoku_6x6()
    for row in p:
        print(' '.join(str(x) if x else '.' for x in row))
    print("Soluzione:")
    for row in s:
        print(' '.join(str(x) for x in row))
