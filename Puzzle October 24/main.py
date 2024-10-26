import itertools
import time

knight_moves = [
    (-2, -1), (-2, 1), (2, -1), (2, 1),
    (-1, -2), (-1, 2), (1, -2), (1, 2)
]

def create_grid(A, B, C):
    return [
        [A, A, A, B, B, C],
        [A, A, A, B, B, C],
        [A, A, B, B, C, C],
        [A, B, B, C, C, C],
        [B, B, C, C, C, C],
        [A, B, B, C, C, C]
    ]

def in_bounds(x, y):
    return 0 <= x < 6 and 0 <= y < 6

def knight_tour(grid, x, y, score, path, visited):
    if len(path) > 1 and score == 2024:
        return True, path
    for move in knight_moves:
        new_x, new_y = x + move[0], y + move[1]
        if in_bounds(new_x, new_y) and (new_x, new_y) not in visited:
            new_value = grid[new_x][new_y]
            if grid[x][y] != new_value:
                new_score = score * new_value
            else:
                new_score = score + new_value
            if new_score <= 2024:
                visited.add((new_x, new_y))
                path.append((new_x, new_y))
                found, result_path = knight_tour(grid, new_x, new_y, new_score, path, visited)
                if found:
                    return True, result_path
                path.pop()
                visited.remove((new_x, new_y))
    
    return False, []

def solve_knight_problem():
    for A, B, C in itertools.permutations(range(1, 50), 3): 
        if A + B + C >= 50: 
            continue
        grid = create_grid(A, B, C)
        found1, path1 = knight_tour(grid, 0, 0, grid[0][0], [(0, 0)], {(0, 0)})
        if found1:
            found2, path2 = knight_tour(grid, 5, 0, grid[5][0], [(5, 0)], {(5, 0)})
            if found2:
                print(f"A = {A}, B = {B}, C = {C}")
                print("a1 to f6 : ", path1)
                print("a6 to f1 : ", path2)
                return A, B, C, path1, path2
    return None

start_time = time.time()  
solution = solve_knight_problem()
end_time = time.time() 

print(f"Time : {end_time - start_time:.2f}")