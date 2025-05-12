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
    mutation_rate=0.05,
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


# Lớp môi trường niềm tin
class BeliefState:
    def __init__(self, states):
        self.states = states  # Danh sách các trạng thái có thể xảy ra

    def is_goal(self, goal):
        # Tất cả trạng thái trong belief đạt goal là thành công
        return all(s == goal for s in self.states)

    def apply_action(self, action_fn):
        next_states = set()
        for s in self.states:
            neighbors = action_fn(s)  # [(dx, dy, new_state), ...]
            for _, _, ns in neighbors:
                next_states.add(tuple(map(tuple, ns)))  # dùng tuple để loại trùng
        # Trả lại belief mới (danh sách ma trận)
        return BeliefState([list([list(row) for row in s]) for s in next_states])


# Hàm phụ để hiển thị các trạng thái niềm tin đại diện
def print_sample_beliefs(belief, max_display=50):
    print(f"\nBelief Size: {len(belief.states)}")
    for idx, state in enumerate(belief.states[:max_display]):
        print(f"State {idx + 1}:")
        for row in state:
            print(row)
        print()


# Thuật toán BFS trong môi trường niềm tin
def belief_bfs_solve(start_states, goal, max_depth=30):
    print("Start State:")
    for row in start_states[0]:
        print(row)

    print("\nInitial Belief States:")
    for idx, state in enumerate(start_states):
        print(f"Belief State {idx + 1}:")
        for row in state:
            print(row)
        print()

    start_time = time.time()
    initial_belief = BeliefState(start_states)
    queue = deque([(initial_belief, [])])
    visited = set()
    nodes_expanded = 0
    last_belief = initial_belief  # lưu lại trạng thái cuối cùng để debug

    while queue:
        belief, path = queue.popleft()
        if len(path) > max_depth:
            continue  # Bỏ qua nếu quá sâu

        # Chuẩn hóa để kiểm tra visited
        belief_key = tuple(sorted(tuple(map(tuple, s)) for s in belief.states))
        if belief_key in visited:
            continue
        visited.add(belief_key)
        nodes_expanded += 1

        if belief.is_goal(goal):
            print("\nGoal found in belief!")
            print_sample_beliefs(belief)
            return (
                path + [belief.states[0]],
                round(time.time() - start_time, 4),
                nodes_expanded,
                len(path) + 1,
            )

        new_belief = belief.apply_action(get_neighbors)
        queue.append((new_belief, path + [belief.states[0]]))
        last_belief = new_belief

    # Không tìm được lời giải
    print("\nGoal NOT found in belief.")
    print_sample_beliefs(last_belief)
    return [], 0, nodes_expanded, 0


#  Thuật toán A* cho môi trường niềm tin
def belief_a_star_solve(start_states, goal):
    print("Start State:")
    for row in start_states[0]:
        print(row)

    print("\nInitial Belief States:")
    for idx, state in enumerate(start_states):
        print(f"Belief State {idx + 1}:")
        for row in state:
            print(row)
        print()

    start_time = time.time()
    nodes_expanded = 0

    def belief_heuristic(belief):
        return sum(heuristic(s, goal) for s in belief.states) / len(belief.states)

    initial_belief = BeliefState(start_states)
    heap = [(belief_heuristic(initial_belief), 0, initial_belief, [])]
    visited = set()
    last_belief = initial_belief

    while heap:
        _, g, belief, path = heapq.heappop(heap)
        belief_key = tuple(sorted(tuple(map(tuple, s)) for s in belief.states))
        if belief_key in visited:
            continue
        visited.add(belief_key)
        nodes_expanded += 1

        if belief.is_goal(goal):
            print("\nGoal reached in belief!")
            print_sample_beliefs(belief)
            return (
                path + [belief.states[0]],
                round(time.time() - start_time, 4),
                nodes_expanded,
                len(path) + 1,
            )

        next_belief = belief.apply_action(get_neighbors)
        f = g + 1 + belief_heuristic(next_belief)
        heapq.heappush(heap, (f, g + 1, next_belief, path + [belief.states[0]]))
        last_belief = next_belief

    print("\nGoal NOT found. Last Belief State:")
    print_sample_beliefs(last_belief)
    return [], 0, nodes_expanded, 0


# Thuật toán Greedy Best-First Search cho môi trường niềm tin
def belief_greedy_solve(start_states, goal):
    print("Start State:")
    for row in start_states[0]:
        print(row)

    print("\nInitial Belief States:")
    for idx, state in enumerate(start_states):
        print(f"Belief State {idx + 1}:")
        for row in state:
            print(row)
        print()

    start_time = time.time()
    nodes_expanded = 0

    def belief_heuristic(belief):
        return sum(heuristic(s, goal) for s in belief.states) / len(belief.states)

    initial_belief = BeliefState(start_states)
    heap = [(belief_heuristic(initial_belief), initial_belief, [])]
    visited = set()
    last_belief = initial_belief

    while heap:
        _, belief, path = heapq.heappop(heap)
        belief_key = tuple(sorted(tuple(map(tuple, s)) for s in belief.states))
        if belief_key in visited:
            continue
        visited.add(belief_key)
        nodes_expanded += 1

        if belief.is_goal(goal):
            print("\nGoal reached in belief!")
            print_sample_beliefs(belief)
            return (
                path + [belief.states[0]],
                round(time.time() - start_time, 4),
                nodes_expanded,
                len(path) + 1,
            )

        next_belief = belief.apply_action(get_neighbors)
        h = belief_heuristic(next_belief)
        heapq.heappush(heap, (h, next_belief, path + [belief.states[0]]))
        last_belief = next_belief

    print("\nGoal NOT found. Last Belief State:")
    print_sample_beliefs(last_belief)
    return [], 0, nodes_expanded, 0


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
