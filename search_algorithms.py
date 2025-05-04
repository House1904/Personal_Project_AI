import time
import copy
from collections import deque
import heapq
import random
import math


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


# Hàm lấy các trạng thái hàng xóm của ô trống
def get_neighbors(state):
    moves = []
    empty_x, empty_y = None, None

    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                empty_x, empty_y = i, j
                break

    directions = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]

    for dx, dy, move in directions:
        new_x, new_y = empty_x + dx, empty_y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = [row[:] for row in state]
            new_state[empty_x][empty_y], new_state[new_x][new_y] = (
                new_state[new_x][new_y],
                new_state[empty_x][empty_y],
            )
            moves.append((move, new_state))

    return moves


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

        for dx, dy in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]:
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

        for move, neighbor in neighbors:
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

        for move, neighbor in neighbors:
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
            (move, neighbor)
            for move, neighbor in neighbors
            if heuristic(neighbor, goal) < heuristic(state, goal)
        ]
        nodes_expanded += len(neighbors)

        if not better_neighbors:
            return path, round(time.time() - start_time, 4), nodes_expanded, len(path)

        move, state = random.choice(better_neighbors)
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
        frontier.sort(key=lambda x: x[0])
        next_frontier = []

        for _, state, path in frontier[:beam_width]:
            if state == goal:
                return (
                    path,
                    round(time.time() - start_time, 4),
                    nodes_expanded,
                    len(path),
                )

            x, y = find_blank(state)
            for dx, dy in moves:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 3 and 0 <= ny < 3:
                    new_state = copy.deepcopy(state)
                    new_state[x][y], new_state[nx][ny] = (
                        new_state[nx][ny],
                        new_state[x][y],
                    )
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
    start, goal, initial_temperature=3000, cooling_rate=0.999, min_temperature=1e-5
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

        _, next_state = random.choice(neighbors)
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
    mutation_rate=0.05,
    sequence_length=50,
    elitism_size=2,
    restart_limit=3,
):
    start_time = time.time()

    moves_name = ["Up", "Down", "Left", "Right"]
    move_dict = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}

    def apply_moves(state, moves_sequence):
        current = copy.deepcopy(state)
        for move in moves_sequence:
            x, y = find_blank(current)
            dx, dy = move_dict[move]
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                current[x][y], current[nx][ny] = current[nx][ny], current[x][y]
        return current

    def fitness(moves_sequence):
        result_state = apply_moves(start, moves_sequence)
        return heuristic(result_state, goal)

    nodes_expanded = 0
    attempts = 0

    while attempts < restart_limit:
        population = [
            [random.choice(moves_name) for _ in range(sequence_length)]
            for _ in range(population_size)
        ]

        for generation in range(generations):
            population.sort(key=lambda individual: fitness(individual))
            nodes_expanded += len(population)

            best_individual = population[0]
            if fitness(best_individual) == 0:
                runtime = round(time.time() - start_time, 4)
                path = [start]
                current = copy.deepcopy(start)
                for move in best_individual:
                    x, y = find_blank(current)
                    dx, dy = move_dict[move]
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 3 and 0 <= ny < 3:
                        current[x][y], current[nx][ny] = current[nx][ny], current[x][y]
                        path.append(copy.deepcopy(current))
                        if current == goal:
                            break
                return path, runtime, nodes_expanded, len(path)

            survivors = population[: population_size // 2]
            elites = population[:elitism_size]  # giữ nguyên cá thể tốt nhất

            children = elites.copy()
            while len(children) < population_size:
                parent1 = random.choice(survivors)
                parent2 = random.choice(survivors)
                split = random.randint(1, sequence_length - 2)
                child = parent1[:split] + parent2[split:]
                children.append(child)

            for individual in children[elitism_size:]:  # không đột biến cá thể elite
                if random.random() < mutation_rate:
                    idx = random.randint(0, sequence_length - 1)
                    individual[idx] = random.choice(moves_name)

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

        for _, next_state in get_neighbors(state):
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


# Lớp môi trường niềm tin (Belief State) - để quản lý trạng thái niềm tin
class BeliefState:
    def __init__(self, states):
        self.states = states

    def is_goal(self, goal):
        return all(s == goal for s in self.states)

    def apply_action(self, action_fn):
        next_states = set()
        for s in self.states:
            neighbors = action_fn(s)
            for _, ns in neighbors:
                next_states.add(tuple(map(tuple, ns)))
        return BeliefState([list([list(row) for row in s]) for s in next_states])


# Thuật toán BFS cho trạng thái niềm tin
def belief_bfs_solve(start_states, goal):
    start_time = time.time()
    initial_belief = BeliefState(start_states)
    queue = deque([(initial_belief, [])])
    visited = set()
    nodes_expanded = 0

    while queue:
        belief, path = queue.popleft()
        belief_key = tuple(sorted(tuple(map(tuple, s)) for s in belief.states))
        if belief_key in visited:
            continue
        visited.add(belief_key)
        nodes_expanded += 1

        if belief.is_goal(goal):
            return (
                path + [belief.states[0]],
                round(time.time() - start_time, 4),
                nodes_expanded,
                len(path) + 1,
            )

        new_belief = belief.apply_action(get_neighbors)
        queue.append((new_belief, path + [belief.states[0]]))

    return [], 0, nodes_expanded, 0


# Thuật toán DFS cho trạng thái niềm tin
def belief_a_star_solve(start_states, goal):

    start_time = time.time()
    nodes_expanded = 0

    def belief_heuristic(belief):
        return sum(heuristic(s, goal) for s in belief.states) / len(belief.states)

    initial_belief = BeliefState(start_states)
    heap = [(belief_heuristic(initial_belief), 0, initial_belief, [])]
    visited = set()

    while heap:
        _, g, belief, path = heapq.heappop(heap)
        belief_key = tuple(sorted(tuple(map(tuple, s)) for s in belief.states))
        if belief_key in visited:
            continue
        visited.add(belief_key)
        nodes_expanded += 1

        if belief.is_goal(goal):
            return (
                path + [belief.states[0]],
                round(time.time() - start_time, 4),
                nodes_expanded,
                len(path) + 1,
            )

        next_belief = belief.apply_action(get_neighbors)
        f = g + 1 + belief_heuristic(next_belief)
        heapq.heappush(heap, (f, g + 1, next_belief, path + [belief.states[0]]))

    return [], 0, nodes_expanded, 0


# Thuật toán Greedy Best-First Search cho trạng thái niềm tin
def belief_greedy_solve(start_states, goal):
    start_time = time.time()
    nodes_expanded = 0

    def belief_heuristic(belief):
        return sum(heuristic(s, goal) for s in belief.states) / len(belief.states)

    initial_belief = BeliefState(start_states)
    heap = [(belief_heuristic(initial_belief), initial_belief, [])]
    visited = set()

    while heap:
        _, belief, path = heapq.heappop(heap)
        belief_key = tuple(sorted(tuple(map(tuple, s)) for s in belief.states))
        if belief_key in visited:
            continue
        visited.add(belief_key)
        nodes_expanded += 1

        if belief.is_goal(goal):
            return (
                path + [belief.states[0]],
                round(time.time() - start_time, 4),
                nodes_expanded,
                len(path) + 1,
            )

        next_belief = belief.apply_action(get_neighbors)
        h = belief_heuristic(next_belief)
        heapq.heappush(heap, (h, next_belief, path + [belief.states[0]]))

    return [], 0, nodes_expanded, 0


# Thuật toán Backtracking - Tìm kiếm quay lui
def backtracking_solve(start, goal, max_depth=100):
    start_time = time.time()
    visited = set()
    solution = []
    nodes_expanded = 0

    def backtrack(state, path, depth):
        nonlocal solution, nodes_expanded
        if state == goal:
            solution = path[:]
            return True
        if depth > max_depth:
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

        return False

    found = backtrack(start, [start], 0)
    runtime = round(time.time() - start_time, 4)
    return (
        (solution, runtime, nodes_expanded, len(solution)) if found else ([], 0, 0, 0)
    )
