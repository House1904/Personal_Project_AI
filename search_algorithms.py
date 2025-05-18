import time
import copy
from collections import deque
import heapq
import random
import math
from itertools import permutations


# Hàm tìm vị trí của ô trống (0) trong ma trận 3x3
def find_blank(matrix):
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == 0:
                return i, j


# Các hướng di chuyển có thể của ô trống
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]


# Thuật toán BFS - Tìm kiếm theo chiều rộng
def bfs_solve(start, goal):
    start_time = time.time()
    queue = deque([(start, [])])
    visited = set()
    visited.add(tuple(map(tuple, start)))
    nodes_expanded = 0

    while queue:
        state, path = queue.popleft()
        nodes_expanded += 1
        if state == goal:
            return path, round(time.time() - start_time, 4), nodes_expanded, len(path)

        x, y = find_blank(state)
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = copy.deepcopy(state)
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                state_tuple = tuple(map(tuple, new_state))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    queue.append((new_state, path + [new_state]))

    return [], 0, 0, 0


# Thuật toán DFS - Tìm kiếm theo chiều sâu
def dfs_solve(start, goal, max_depth=50):
    start_time = time.time()
    stack = [(start, [], 0)]
    visited = set()
    visited.add(tuple(map(tuple, start)))
    nodes_expanded = 0

    while stack:
        state, path, depth = stack.pop()
        nodes_expanded += 1

        if state == goal:
            return path, round(time.time() - start_time, 4), nodes_expanded, len(path)

        if depth >= max_depth:
            continue

        x, y = find_blank(state)
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = copy.deepcopy(state)
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                state_tuple = tuple(map(tuple, new_state))

                if state_tuple not in visited:
                    visited.add(state_tuple)
                    stack.append((new_state, path + [new_state], depth + 1))

    return [], 0, 0, 0


# Thuật toán Uniform Cost Search (UCS) - Tìm kiếm theo chi phí đồng nhất
def ucs_solve(start, goal):
    start_time = time.time()
    queue = [(0, start, [])]
    visited = set()
    visited.add(tuple(map(tuple, start)))
    nodes_expanded = 0

    while queue:
        cost, state, path = heapq.heappop(queue)
        nodes_expanded += 1
        if state == goal:
            return path, round(time.time() - start_time, 4), nodes_expanded, len(path)

        x, y = find_blank(state)
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = copy.deepcopy(state)
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                state_tuple = tuple(map(tuple, new_state))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    heapq.heappush(queue, (cost + 1, new_state, path + [new_state]))

    return [], 0, 0, 0


def depth_limited_search(state, goal, depth, visited):
    if state == goal:
        return [state], True

    if depth == 0:
        return None, False

    x, y = find_blank(state)
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            state_tuple = tuple(map(tuple, new_state))

            if state_tuple not in visited:
                visited.add(state_tuple)
                path, found = depth_limited_search(new_state, goal, depth - 1, visited)
                if found:
                    return [state] + path, True

    return None, False


# Thuật toán Iterative Deepening Search (IDS) - Tìm kiếm theo chiều sâu lặp lại
def ids_solve(start, goal):
    start_time = time.time()
    depth = 0
    nodes_expanded = 0

    while True:
        visited = set()
        visited.add(tuple(map(tuple, start)))
        solution, found = depth_limited_search(start, goal, depth, visited)
        nodes_expanded += len(visited)

        if found:
            return (
                solution,
                round(time.time() - start_time, 4),
                nodes_expanded,
                len(solution),
            )

        depth += 1


def heuristic(state, goal):
    goal_positions = {goal[i][j]: (i, j) for i in range(3) for j in range(3)}

    return sum(
        abs(i - goal_positions[state[i][j]][0])
        + abs(j - goal_positions[state[i][j]][1])
        for i in range(3)
        for j in range(3)
        if state[i][j] != 0
    )


# Thuật toán A* Search - Tìm kiếm A*
def a_star_solve(start, goal):
    start_time = time.time()
    queue = [(heuristic(start, goal), start, [])]
    visited = set()
    visited.add(tuple(map(tuple, start)))
    nodes_expanded = 0

    while queue:
        _, state, path = heapq.heappop(queue)
        nodes_expanded += 1
        if state == goal:
            return path, round(time.time() - start_time, 4), nodes_expanded, len(path)

        x, y = find_blank(state)
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = copy.deepcopy(state)
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                state_tuple = tuple(map(tuple, new_state))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    heapq.heappush(
                        queue,
                        (
                            len(path) + 1 + heuristic(new_state, goal),
                            new_state,
                            path + [new_state],
                        ),
                    )

    return [], 0, 0, 0


# Thuật toán Greedy Best-First Search - Tìm kiếm tham lam tốt nhất
def greedy_solve(start, goal):
    start_time = time.time()
    queue = [(heuristic(start, goal), start, [])]
    visited = set()
    visited.add(tuple(map(tuple, start)))
    nodes_expanded = 0

    while queue:
        _, state, path = heapq.heappop(queue)
        nodes_expanded += 1
        if state == goal:
            return path, round(time.time() - start_time, 4), nodes_expanded, len(path)

        x, y = find_blank(state)
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = copy.deepcopy(state)
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                state_tuple = tuple(map(tuple, new_state))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    heapq.heappush(
                        queue,
                        (heuristic(new_state, goal), new_state, path + [new_state]),
                    )

    return [], 0, 0, 0


# Hàm tìm kiếm IDA* (Iterative Deepening A*)
def ida_star_solve(start, goal):
    start_time = time.time()

    def search(state, g, threshold, path):
        nonlocal nodes_expanded
        f = g + heuristic(state, goal)

        if f > threshold:
            return f, None
        if state == goal:
            return f, path

        min_cost = float("inf")
        x, y = find_blank(state)

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = copy.deepcopy(state)
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                state_tuple = tuple(map(tuple, new_state))

                if state_tuple not in visited:
                    visited.add(state_tuple)
                    nodes_expanded += 1

                    cost, new_path = search(
                        new_state, g + 1, threshold, path + [new_state]
                    )

                    if new_path:
                        return cost, new_path

                    min_cost = min(min_cost, cost)
                    visited.remove(state_tuple)

        return min_cost, None

    threshold = heuristic(start, goal)
    visited = set()
    visited.add(tuple(map(tuple, start)))
    nodes_expanded = 0

    while True:
        cost, path = search(start, 0, threshold, [])
        if path:
            runtime = round(time.time() - start_time, 4)
            return (
                path,
                runtime,
                nodes_expanded,
                len(path),
            )

        if cost == float("inf"):
            return [], 0, 0, 0

        threshold = cost


# Hàm lấy các trạng thái hàng xóm hợp lệ của ô trống trong ma trận 3x3
def get_neighbors(state):
    neighbors = []
    x, y = find_blank(state)  # Tận dụng lại hàm đã có

    for dx, dy in moves:  # moves đã định nghĩa sẵn
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]  # Deep copy từng dòng
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append((dx, dy, new_state))  # Nếu cần hướng thì trả về dx, dy

    return neighbors


# Thuật toán Simple Hill Climbing - Tìm kiếm đồi đơn giản
def simple_hill_climbing(start, goal):
    start_time = time.time()
    state = start
    path = [state]
    nodes_expanded = 0

    while state != goal:
        neighbors = get_neighbors(state)
        best_neighbor = None
        best_h = heuristic(state, goal)

        for _, _, neighbor in neighbors:  # unpack 3 phần tử
            h = heuristic(neighbor, goal)
            nodes_expanded += 1
            if h < best_h:
                best_neighbor = neighbor
                best_h = h

        if best_neighbor is None:
            return path, round(time.time() - start_time, 4), nodes_expanded, len(path)

        state = best_neighbor
        path.append(state)

    return path, round(time.time() - start_time, 4), nodes_expanded, len(path)


# Thuật toán Steepest Ascent Hill Climbing - Tìm kiếm đồi dốc
def steepest_ascent_hill_climbing(start, goal):
    start_time = time.time()
    state = start
    path = [state]
    nodes_expanded = 0

    while state != goal:
        neighbors = get_neighbors(state)
        best_neighbor = state
        best_h = heuristic(state, goal)

        for _, _, neighbor in neighbors:
            h = heuristic(neighbor, goal)
            nodes_expanded += 1
            if h < best_h:
                best_neighbor = neighbor
                best_h = h

        if best_neighbor == state:
            return path, round(time.time() - start_time, 4), nodes_expanded, len(path)

        state = best_neighbor
        path.append(state)

    return path, round(time.time() - start_time, 4), nodes_expanded, len(path)


# Thuật toán Stochastic Hill Climbing - Tìm kiếm đồi ngẫu nhiên
def stochastic_hill_climbing(start, goal):
    start_time = time.time()
    state = start
    path = [state]
    nodes_expanded = 0

    while state != goal:
        neighbors = get_neighbors(state)
        better_neighbors = [
            (_, _, neighbor)
            for (_, _, neighbor) in neighbors
            if heuristic(neighbor, goal) < heuristic(state, goal)
        ]
        nodes_expanded += len(neighbors)

        if not better_neighbors:
            return path, round(time.time() - start_time, 4), nodes_expanded, len(path)

        _, _, state = random.choice(better_neighbors)
        path.append(state)

    return path, round(time.time() - start_time, 4), nodes_expanded, len(path)


# Thuật toán Beam Search - Tìm kiếm chùm sáng
def beam_search_solve(start, goal, beam_width=7):  # Độ rộng của chùm sáng là 7
    start_time = time.time()
    frontier = [(heuristic(start, goal), start, [])]
    visited = set()
    visited.add(tuple(map(tuple, start)))
    nodes_expanded = 0

    while frontier:
        frontier.sort(
            key=lambda x: x[0]
        )  # Ưu tiên trạng thái tốt hơn (heuristic nhỏ hơn)
        next_frontier = []

        for _, state, path in frontier[:beam_width]:
            if state == goal:
                return (
                    path,
                    round(time.time() - start_time, 4),
                    nodes_expanded,
                    len(path),
                )

            for _, _, new_state in get_neighbors(state):
                state_tuple = tuple(map(tuple, new_state))

                if state_tuple not in visited:
                    visited.add(state_tuple)
                    nodes_expanded += 1
                    next_frontier.append(
                        (heuristic(new_state, goal), new_state, path + [new_state])
                    )

        frontier = next_frontier

    return [], 0, 0, 0


# Thuật toán Simulated Annealing - Tìm kiếm làm mát mô phỏng
def simulated_annealing_solve(
    start, goal, initial_temperature=1000, cooling_rate=0.95, min_temperature=1
):
    start_time = time.time()
    current = start
    path = [current]
    temperature = initial_temperature
    nodes_expanded = 0

    while temperature > min_temperature:
        if current == goal:
            return path, round(time.time() - start_time, 4), nodes_expanded, len(path)

        neighbors = get_neighbors(current)
        if not neighbors:
            break

        _, _, next_state = random.choice(neighbors)
        delta_e = heuristic(current, goal) - heuristic(next_state, goal)
        nodes_expanded += 1

        if delta_e > 0:
            current = next_state
            path.append(current)
        else:
            probability = math.exp(delta_e / temperature)
            if random.random() < probability:
                current = next_state
                path.append(current)

        temperature *= cooling_rate

    return path, round(time.time() - start_time, 4), nodes_expanded, len(path)


# Thuật toán Genetic Algorithm - Tìm kiếm di truyền
def genetic_algorithm_solve(
    start,
    goal,
    population_size=200,
    generations=1000,
    mutation_rate=0.1,
    sequence_length=50,
    elitism_size=2,
    restart_limit=3,
):
    start_time = time.time()
    nodes_expanded = 0
    attempts = 0

    while attempts < restart_limit:
        population = [
            [random.choice(moves) for _ in range(sequence_length)]
            for _ in range(population_size)
        ]

        def apply_moves(state, move_sequence):
            current = copy.deepcopy(state)
            for dx, dy in move_sequence:
                x, y = find_blank(current)
                nx, ny = x + dx, y + dy
                if 0 <= nx < 3 and 0 <= ny < 3:
                    current[x][y], current[nx][ny] = current[nx][ny], current[x][y]
            return current

        def fitness(move_sequence):
            result_state = apply_moves(start, move_sequence)
            return heuristic(result_state, goal)

        for _ in range(generations):
            population.sort(key=lambda individual: fitness(individual))
            nodes_expanded += len(population)

            best_individual = population[0]
            if fitness(best_individual) == 0:
                runtime = round(time.time() - start_time, 4)
                path = [start]
                current = copy.deepcopy(start)
                for dx, dy in best_individual:
                    x, y = find_blank(current)
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 3 and 0 <= ny < 3:
                        current[x][y], current[nx][ny] = current[nx][ny], current[x][y]
                        path.append(copy.deepcopy(current))
                        if current == goal:
                            break
                return path, runtime, nodes_expanded, len(path)

            survivors = population[: population_size // 2]
            elites = population[:elitism_size]
            children = elites.copy()

            while len(children) < population_size:
                parent1 = random.choice(survivors)
                parent2 = random.choice(survivors)
                split = random.randint(1, sequence_length - 2)
                child = parent1[:split] + parent2[split:]
                children.append(child)

            for individual in children[elitism_size:]:
                if random.random() < mutation_rate:
                    idx = random.randint(0, sequence_length - 1)
                    individual[idx] = random.choice(moves)

            population = children

        attempts += 1

    return [], 0, 0, 0


# Mô phỏng tìm kiếm AND-OR graph
def and_or_graph_search(start, goal, max_depth=50):
    start_time = time.time()
    nodes_expanded = 0

    def or_search(state, path, visited, depth):
        nonlocal nodes_expanded
        if depth > max_depth:
            return None
        if state == goal:
            return [state]
        if tuple(map(tuple, state)) in visited:
            return None

        visited.add(tuple(map(tuple, state)))
        nodes_expanded += 1

        for _, _, next_state in get_neighbors(state):  # unpack 3 phần tử
            result = and_search(next_state, path + [state], visited.copy(), depth + 1)
            if result:
                return [state] + result
        return None

    def and_search(state, path, visited, depth):
        return or_search(state, path, visited, depth)

    solution = or_search(start, [], set(), 0)
    if solution:
        return (
            solution,
            round(time.time() - start_time, 4),
            nodes_expanded,
            len(solution),
        )
    else:
        return [], 0, nodes_expanded, 0


# BFS - Belief Search - Tìm kiếm theo chiều rộng trên trạng thái tin tưởng
def belief_bfs_solve(belief_state, goal):
    start_time = time.time()
    known = []
    unknown_pos = []

    # Tìm các vị trí đã biết và chưa biết
    for i in range(3):
        for j in range(3):
            val = belief_state[i][j]
            if val is None:
                unknown_pos.append((i, j))
            else:
                known.append(val)

    # Các giá trị còn thiếu (0-8 trừ đi các số đã biết)
    missing = [x for x in range(9) if x not in known]

    # Nếu không hợp lệ thì trả về
    if len(known) + len(unknown_pos) != 9:
        return [], 0, 0, 0

    nodes_expanded_total = 0

    for perm in permutations(missing):
        filled = copy.deepcopy(belief_state)
        for idx, (i, j) in enumerate(unknown_pos):
            filled[i][j] = perm[idx]

        # Lưu trạng thái đã được điền đầy đủ để trả về làm start
        first_state = copy.deepcopy(filled)

        result = bfs_solve(filled, goal)
        nodes_expanded_total += result[2]

        if result[0]:
            full_path = [first_state] + result[
                0
            ]  # Chèn trạng thái đầu vào đầu đường đi
            runtime = round(time.time() - start_time, 4)
            return full_path, runtime, nodes_expanded_total, len(full_path) - 1

    return [], round(time.time() - start_time, 4), nodes_expanded_total, 0


def is_valid_state(matrix):
    flat = sum(matrix, [])
    return sorted(flat) == list(range(9))  # đủ 0-8, không trùng


def generate_all_states(belief_matrix):
    flat = sum(belief_matrix, [])
    missing = [i for i in range(9) if i not in flat if i is not None]
    none_indices = [i for i, v in enumerate(flat) if v is None]

    for perm in permutations(missing):
        new_flat = flat[:]
        for idx, val in zip(none_indices, perm):
            new_flat[idx] = val
        state = [new_flat[i : i + 3] for i in range(0, 9, 3)]
        yield state


# IDS - Belief Search - Tìm kiếm theo chiều sâu lặp lại trên trạng thái tin tưởng
def belief_ids_solve(belief_matrix, goal_state):

    start_time = time.time()
    total_nodes = 0

    for complete_state in generate_all_states(belief_matrix):
        if not is_valid_state(complete_state):
            continue

        # Lưu lại trạng thái belief hoàn chỉnh để gắn đầu đường đi
        first_state = copy.deepcopy(complete_state)

        solution, rt, nodes, depth = ids_solve(complete_state, goal_state)
        total_nodes += nodes

        if solution:
            full_path = [first_state] + solution  # chèn trạng thái đầu tiên
            return (
                full_path,
                round(time.time() - start_time, 4),
                total_nodes,
                len(full_path) - 1,
            )

    return [], round(time.time() - start_time, 4), total_nodes, 0


# A* - Belief Search - Tìm kiếm A* trên trạng thái tin tưởng
def belief_a_star_solve(belief_matrix, goal_state):

    start_time = time.time()
    nodes_total = 0

    for complete_state in generate_all_states(belief_matrix):
        if not is_valid_state(complete_state):
            continue

        first_state = copy.deepcopy(complete_state)

        solution, rt, nodes, depth = a_star_solve(complete_state, goal_state)
        nodes_total += nodes

        if solution:
            full_path = [first_state] + solution
            return (
                full_path,
                round(time.time() - start_time, 4),
                nodes_total,
                len(full_path) - 1,
            )

    return [], round(time.time() - start_time, 4), nodes_total, 0


# Greedy - Belief Search - Tìm kiếm Greedy trên trạng thái tin tưởng
def belief_greedy_solve(belief_matrix, goal_state):

    start_time = time.time()
    nodes_total = 0

    for complete_state in generate_all_states(belief_matrix):
        if not is_valid_state(complete_state):
            continue

        first_state = copy.deepcopy(complete_state)

        solution, rt, nodes, depth = greedy_solve(complete_state, goal_state)
        nodes_total += nodes

        if solution:
            full_path = [first_state] + solution
            return (
                full_path,
                round(time.time() - start_time, 4),
                nodes_total,
                len(full_path) - 1,
            )

    return [], round(time.time() - start_time, 4), nodes_total, 0


# Beam - Belief Search - Tìm kiếm Beam trên trạng thái tin tưởng
def belief_beam_solve(belief_matrix, goal_state):

    start_time = time.time()
    total_nodes = 0

    for complete_state in generate_all_states(belief_matrix):
        if not is_valid_state(complete_state):
            continue

        first_state = copy.deepcopy(complete_state)
        solution, rt, nodes, depth = beam_search_solve(complete_state, goal_state)
        total_nodes += nodes

        if solution:
            full_path = [first_state] + solution
            return (
                full_path,
                round(time.time() - start_time, 4),
                total_nodes,
                len(full_path) - 1,
            )

    return [], round(time.time() - start_time, 4), total_nodes, 0


# Thuật toán Backtracking - Tìm kiếm quay lui
def backtracking_solve(start, goal, max_depth=25):
    start_time = time.time()
    visited = set()
    solution = []
    nodes_expanded = 0

    def backtrack(state, path, depth):
        nonlocal solution, nodes_expanded
        if state == goal:
            solution = path[:]
            return True
        if depth >= max_depth:
            return False

        state_tuple = tuple(map(tuple, state))
        visited.add(state_tuple)
        nodes_expanded += 1

        x, y = find_blank(state)
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = [row[:] for row in state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                new_tuple = tuple(map(tuple, new_state))
                if new_tuple not in visited:
                    if backtrack(new_state, path + [new_state], depth + 1):
                        return True

        visited.remove(state_tuple)
        return False

    found = backtrack(start, [start], 0)
    runtime = round(time.time() - start_time, 4)
    return (
        (solution, runtime, nodes_expanded, len(solution)) if found else ([], 0, 0, 0)
    )


# Thuật toán Forward Checking - Tìm kiếm kiểm tra tiến
def forward_checking_solve(start, goal, max_depth=25):
    start_time = time.time()
    visited = set()
    solution = []
    nodes_expanded = 0

    def is_consistent(state):
        # Kiểm tra AllDifferent
        flat = sum(state, [])
        return len(set(flat)) == 9

    def forward_check(state, path, depth):
        nonlocal solution, nodes_expanded
        if state == goal:
            solution = path[:]
            return True
        if depth > max_depth:
            return False

        state_tuple = tuple(map(tuple, state))
        visited.add(state_tuple)
        nodes_expanded += 1

        for dx, dy in moves:
            x, y = find_blank(state)
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = copy.deepcopy(state)
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                new_tuple = tuple(map(tuple, new_state))

                if new_tuple not in visited and is_consistent(new_state):
                    if forward_check(new_state, path + [new_state], depth + 1):
                        return True

        visited.remove(state_tuple)
        return False

    found = forward_check(start, [start], 0)
    runtime = round(time.time() - start_time, 4)
    return (
        (solution, runtime, nodes_expanded, len(solution)) if found else ([], 0, 0, 0)
    )


# Thuật toán Q-Learning - Tìm kiếm học tăng cường
def state_to_tuple(state):
    return tuple(tuple(row) for row in state)


def get_valid_actions_q(state_tuple):
    state = [list(row) for row in state_tuple]
    x, y = next((r, c) for r in range(3) for c in range(3) if state[r][c] == 0)
    actions = []
    if x > 0:
        actions.append(0)  # lên
    if x < 2:
        actions.append(1)  # xuống
    if y > 0:
        actions.append(2)  # trái
    if y < 2:
        actions.append(3)  # phải
    return actions


def apply_action_q(state_tuple, action):
    state = [list(row) for row in state_tuple]
    x, y = next((r, c) for r in range(3) for c in range(3) if state[r][c] == 0)
    nx, ny = x, y
    if action == 0:
        nx -= 1
    elif action == 1:
        nx += 1
    elif action == 2:
        ny -= 1
    elif action == 3:
        ny += 1
    if not (0 <= nx < 3 and 0 <= ny < 3):
        return state_tuple, (x, y)
    state[x][y], state[nx][ny] = state[nx][ny], state[x][y]
    return state_to_tuple(state), (nx, ny)


def path_to_states(start_state, move_path):
    current = [row[:] for row in start_state]
    states = [copy.deepcopy(current)]
    for move in move_path:
        x, y = next((r, c) for r in range(3) for c in range(3) if current[r][c] == 0)
        nx, ny = move
        current[x][y], current[nx][ny] = current[nx][ny], current[x][y]
        states.append(copy.deepcopy(current))
    return states


def q_learning_solve(
    start,
    goal,
    episodes=100000,
    alpha=0.1,
    gamma=0.9,
    epsilon_start=1.0,
    max_steps=150,
    max_path_len=150,
):

    start_time = time.time()
    Q = {}
    start_tuple = state_to_tuple(start)
    goal_tuple = state_to_tuple(goal)

    for episode in range(episodes):
        state = start_tuple
        epsilon = epsilon_start * math.exp(-episode / (episodes / 5))
        for _ in range(max_steps):
            actions = get_valid_actions_q(state)
            if not actions:
                break
            q_vals = Q.get(state, [0.0] * 4)
            if random.random() < epsilon:
                action = random.choice(actions)
            else:
                action = max(actions, key=lambda a: q_vals[a])

            next_state, _ = apply_action_q(state, action)
            reward = 100 if next_state == goal_tuple else -1
            max_q_next = (
                max(Q.get(next_state, [0.0] * 4)) if next_state != goal_tuple else 0
            )

            q_vals[action] = q_vals[action] + alpha * (
                reward + gamma * max_q_next - q_vals[action]
            )
            Q[state] = q_vals
            state = next_state
            if state == goal_tuple:
                break

    # Truy vết đường đi tốt nhất từ Q-table
    state = start_tuple
    path = []
    for _ in range(max_path_len):
        if state == goal_tuple:
            break
        actions = get_valid_actions_q(state)
        if not actions:
            break
        q_vals = Q.get(state, [0.0] * 4)
        action = max(actions, key=lambda a: q_vals[a])
        next_state, next_pos = apply_action_q(state, action)
        path.append(next_pos)
        state = next_state

    if state != goal_tuple:
        return [], 0, 0, 0

    full_path = path_to_states(start, path)
    return full_path, round(time.time() - start_time, 4), len(Q), len(full_path)
