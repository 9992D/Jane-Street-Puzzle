#!/usr/bin/env python3
import sys
sys.setrecursionlimit(10000)

# --- Board Parameters ---
MIN_COORD = -0.5
MAX_COORD = 10.5

# --- Utility Functions ---

def distance_to_boundary(x, y, dx, dy):
    """
    Calculates the number of units (steps) before reaching the boundary
    from the position (x, y) in the direction (dx, dy).
    """
    if dx > 0:
        return int(MAX_COORD - x)
    if dx < 0:
        return int(x - MIN_COORD)
    if dy > 0:
        return int(MAX_COORD - y)
    if dy < 0:
        return int(y - MIN_COORD)
    return 0

def can_place_mirror(board, x, y):
    """
    Checks if a mirror can be placed at (x, y):
    the cell must be empty and no adjacent cell (up, down, left, right)
    should already contain a mirror.
    """
    if (x, y) in board:
        return False
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if (nx, ny) in board:
            return False
    return True

def reflect(direction, mirror_type):
    """
    Calculates the new direction after reflection on a mirror.
    For a "/" mirror:
      (-1, 0) -> (0, -1)
      (0, -1) -> (-1, 0)
      (1, 0)  -> (0, 1)
      (0, 1)  -> (1, 0)

    For a "\" mirror:
      (-1, 0) -> (0, 1)
      (0, 1)  -> (-1, 0)
      (1, 0)  -> (0, -1)
      (0, -1) -> (1, 0)
    """
    dx, dy = direction
    if mirror_type == '/':
        if (dx, dy) == (-1, 0):
            return (0, -1)
        elif (dx, dy) == (0, -1):
            return (-1, 0)
        elif (dx, dy) == (1, 0):
            return (0, 1)
        elif (dx, dy) == (0, 1):
            return (1, 0)
    elif mirror_type == '\\':
        if (dx, dy) == (-1, 0):
            return (0, 1)
        elif (dx, dy) == (0, 1):
            return (-1, 0)
        elif (dx, dy) == (1, 0):
            return (0, -1)
        elif (dx, dy) == (0, -1):
            return (1, 0)
    return direction

def compute_laser_path_product(board, start, direction):
    """
    Traces the path of a laser on the final board from 'start'
    in the direction 'direction' until it exits, and returns the product
    of the lengths of the segments traveled.
    """
    x, y = start
    dx, dy = direction
    total_product = 1

    while True:
        dist_boundary = distance_to_boundary(x, y, dx, dy)
        mirror_found = False
        dist_to_mirror = dist_boundary
        for step in range(1, dist_boundary):
            mx = x + step * dx
            my = y + step * dy
            if (mx, my) in board:
                mirror_found = True
                dist_to_mirror = step
                break

        total_product *= dist_to_mirror
        x += dist_to_mirror * dx
        y += dist_to_mirror * dy

        if mirror_found:
            mirror_type, _ = board[(x, y)]
            dx, dy = reflect((dx, dy), mirror_type)
        else:
            break

    return total_product

def simulate_laser(board, x, y, dx, dy, current_product, expected_product):
    """
    Recursively explores all possible configurations for a laser,
    launched from (x, y) in the direction (dx, dy) with an accumulated product current_product,
    to reach the expected product 'expected_product'.

    This function yields all configurations (boards) that
    satisfy the constraint for this laser.
    """
    D_exit = distance_to_boundary(x, y, dx, dy)
    if current_product * D_exit == expected_product:
        yield board
    for k in range(1, D_exit):
        new_x = x + k * dx
        new_y = y + k * dy
        new_product = current_product * k
        if expected_product % new_product != 0:
            continue
        if (new_x, new_y) in board:
            mirror_type, _ = board[(new_x, new_y)]
            new_dir = reflect((dx, dy), mirror_type)
            yield from simulate_laser(board, new_x, new_y, new_dir[0], new_dir[1],
                                      new_product, expected_product)
        else:
            if not can_place_mirror(board, new_x, new_y):
                continue
            for mirror in ['/', '\\']:
                new_board = board.copy()
                new_board[(new_x, new_y)] = (mirror, None)
                new_dir = reflect((dx, dy), mirror)
                yield from simulate_laser(new_board, new_x, new_y, new_dir[0], new_dir[1],
                                          new_product, expected_product)

def solve_system(puzzles, board, index=0):
    """
    Solves the set of puzzles (here already sorted by restrictiveness)
    using backtracking.
    For each mirror placement for the current puzzle, all previously validated
    puzzles are re-simulated to verify that their path has not been modified.
    """
    if index == len(puzzles):
        return board

    puzzle = puzzles[index]
    start = puzzle["start"]
    direction = puzzle["dir"]
    expected = puzzle["expected"]

    for new_board in simulate_laser(board, start[0], start[1], direction[0], direction[1],
                                    1, expected):
        valid = True
        for old_idx in range(index):
            old_puzzle = puzzles[old_idx]
            prod_old = compute_laser_path_product(new_board, old_puzzle["start"], old_puzzle["dir"])
            if prod_old != old_puzzle["expected"]:
                valid = False
                break

        if not valid:
            continue

        result = solve_system(puzzles, new_board, index+1)
        if result is not None:
            return result

    return None

def draw_global_board(board):
    """
    Displays the 10x10 board with the placed mirrors.
    Each cell corresponds to the cell whose center is (i+0.5, j+0.5).
    A dot (.) indicates an empty cell.
    """
    grid = [['.' for _ in range(10)] for _ in range(10)]
    for (x, y), (mirror, _) in board.items():
        col = int(x - 0.5)
        row = int(y - 0.5)
        grid[row][col] = mirror
    for r in range(9, -1, -1):
        print(' '.join(grid[r]))
    print()

def main():
    puzzles = [
        { "start": (10.5, 8.5), "dir": (-1, 0), "expected": 4 },
        { "start": (10.5, 7.5), "dir": (-1, 0), "expected": 27 },
        { "start": (10.5, 3.5), "dir": (-1, 0), "expected": 16 },
        { "start": (7.5, -0.5), "dir": (0, 1), "expected": 405 },
        { "start": (5.5, -0.5), "dir": (0, 1), "expected": 5 },
        { "start": (4.5, -0.5), "dir": (0, 1), "expected": 64 },
        { "start": (3.5, -0.5), "dir": (0, 1), "expected": 12 },
        { "start": (0.5, -0.5), "dir": (0, 1), "expected": 2025 },
        { "start": (-0.5, 1.5), "dir": (1, 0), "expected": 225 },
        { "start": (-0.5, 2.5), "dir": (1, 0), "expected": 12 },
        { "start": (-0.5, 6.5), "dir": (1, 0), "expected": 27 },
        { "start": (2.5, 10.5), "dir": (0, -1), "expected": 112 },
        { "start": (4.5, 10.5), "dir": (0, -1), "expected": 48 },
        { "start": (5.5, 10.5), "dir": (0, -1), "expected": 3087 },
        { "start": (6.5, 10.5), "dir": (0, -1), "expected": 9 },
    ]

    puzzles.sort(key=lambda p: p["expected"])

    initial_board = {}
    solution_board = solve_system(puzzles, initial_board, 0)
    if solution_board is None:
        print("No global solution found.")
    else:
        print("Global solution found:")
        draw_global_board(solution_board)

if __name__ == "__main__":
    main()
