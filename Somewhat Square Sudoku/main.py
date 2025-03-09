from itertools import permutations
from math import gcd

# Définir la grille initiale avec les valeurs existantes
# Les zéros représentent les cases vides
initial_grid = [
    [0, 0, 0, 0, 0, 2, 0, 0, 5],
    [0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 5, 0, 0, 0, 0, 0, 0]
]

def is_valid(grid, row, col, num):
    # Vérifie si le chiffre peut être placé dans la case
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    
    # Vérifie dans le bloc 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    return True

def solve(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def compute_gcd_of_rows(grid):
    row_numbers = [int(''.join(map(str, row))) for row in grid]
    gcd_value = gcd(gcd(row_numbers[0], row_numbers[1]), row_numbers[2])
    return gcd_value

# Résolution de la grille
solved_grid = [row[:] for row in initial_grid]
if solve(solved_grid):
    middle_row_number = int(''.join(map(str, solved_grid[4])))
    gcd_value = compute_gcd_of_rows(solved_grid)

    print("Grille résolue :")
    for row in solved_grid:
        print(row)

    print("\nNombre de la ligne centrale :", middle_row_number)
    print("Plus grand diviseur commun (GCD) :", gcd_value)
else:
    print("Impossible de résoudre la grille.")
