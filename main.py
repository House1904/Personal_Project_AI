import pygame
import copy
from search_algorithms import (
    bfs_solve,
    dfs_solve,
    ucs_solve,
    ids_solve,
    a_star_solve,
    greedy_solve,
    ida_star_solve,
    simple_hill_climbing,
    steepest_ascent_hill_climbing,
    stochastic_hill_climbing,
    beam_search_solve,
    simulated_annealing_solve,
    genetic_algorithm_solve,
    and_or_graph_search,
    belief_bfs_solve,
    belief_a_star_solve,
    belief_greedy_solve,
    backtracking_solve,
)

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8 - Puzzle Solver")

# Màu sắc
WHITE = (255, 255, 255)
BLUE = (50, 130, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RESULT_BG = (255, 190, 0)
BUTTON_PRESS_COLOR = (200, 200, 0)
BACKGROUND_COLOR = (200, 230, 255)
CONTROL_BG = (150, 200, 255)  # Màu nền Control khác
CONTROL_CLICK = (100, 170, 255)  # Màu nhấp vào Control


# Font
title_font = pygame.font.Font(None, 50)
matrix_title_font = pygame.font.Font(None, 30)
matrix_font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 20)
button_font = pygame.font.Font(None, 30)
algo_label_font = pygame.font.Font(None, 25)

# Kích thước ô
cell_size = 60
gap = 5

# Nhập ma trận dữ liệu
start_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
current_state = copy.deepcopy(start_state)

# Vị trí ma trận
start_pos = (100, 120)
step_pos = (350, 120)
goal_pos = (600, 120)

# Biến lưu thông tin kết quả
runtime_duration = 0
nodes_expanded = 0
search_depth = 0
steps_count = 0

# Biến điều khiển animation
solution_steps = []
step_index = 0
is_playing = False
no_solution_message = False
solution_found_message = False
current_algo_name = ""


# Hàm in ra kết quả
def print_solution(solution):
    print("Solution Path:")
    for i, step in enumerate(solution):
        print(f"Step {i + 1}:")
        for row in step:
            print(row)
        print()


clock = pygame.time.Clock()


# Hàm bắt đầu animation
def start_animation(solution):
    global solution_steps, step_index, is_playing, current_state
    solution_steps = solution
    step_index = 0
    is_playing = True
    current_state = copy.deepcopy(solution_steps[0])


# Hàm vẽ ma trận
def draw_matrix(matrix, pos, title):
    x, y = pos
    title_text = matrix_title_font.render(title, True, BLACK)
    title_rect = title_text.get_rect(
        center=(x + (3 * cell_size + 2 * gap) // 2, y - 20)
    )
    screen.blit(title_text, title_rect)
    for i in range(3):
        for j in range(3):
            value = matrix[i][j]
            rect = pygame.Rect(
                x + j * (cell_size + gap),
                y + i * (cell_size + gap),
                cell_size,
                cell_size,
            )
            pygame.draw.rect(screen, BLUE, rect, border_radius=10)
            if value != 0:
                text = matrix_font.render(str(value), True, WHITE)
                screen.blit(text, text.get_rect(center=rect.center))


# Danh sách các thuật toán
algorithms = [
    "BFS",
    "DFS",
    "UCS",
    "IDS",
    "Greedy",
    "A Star",
    "IDA Star",
    "SHC",
    "S-AHC",
    "StoHC",
    "Beam",
    "SA",
    "Gen",
    "And-Or",
    "B-BFS",
    "B-A Star",
    "B-Greedy",
    "BackTrack",
]

button_width, button_height = 120, 40
button_width_control, button_height_control = 135, 40
button_padding = 5
start_x = 100

buttons_row1 = [
    (start_x + i * (button_width + button_padding), 400, algo)
    for i, algo in enumerate(algorithms[:4])
]
buttons_row2 = [
    (start_x + i * (button_width + button_padding), 450, algo)
    for i, algo in enumerate(algorithms[4:7])
]
buttons_row3 = [
    (start_x + i * (button_width + button_padding), 500, algo)
    for i, algo in enumerate(algorithms[7:10])
]
buttons_row4 = [
    (start_x + i * (button_width + button_padding), 550, algo)
    for i, algo in enumerate(algorithms[10:13])
]

buttons_row5 = [
    (start_x + i * (button_width + button_padding), 600, algo)
    for i, algo in enumerate(algorithms[13:])
]

buttons = buttons_row1 + buttons_row2 + buttons_row3 + buttons_row4 + buttons_row5

# Các nút điều khiển StepByStep
control_buttons = [
    (100, 330, "Previous"),
    (250, 330, "Stop"),
    (400, 330, "Next"),
    (550, 330, "Play"),
    (700, 330, "Reset"),
]


# Vẽ giao diện
def draw_interface(state_override=None):
    screen.fill(BACKGROUND_COLOR)
    title = title_font.render("8 - Puzzle Solver", True, BLACK)
    screen.blit(title, (WIDTH // 2 - 130, 20))

    draw_matrix(start_state, start_pos, "Start")
    draw_matrix(
        state_override if state_override else current_state, step_pos, "StepbyStep"
    )
    draw_matrix(goal_state, goal_pos, "Goal")

    for x, y, label in buttons:
        rect = pygame.Rect(x, y, button_width, button_height)
        pygame.draw.rect(screen, BLACK, rect, 2)
        pygame.draw.rect(screen, YELLOW, rect.inflate(-4, -4))
        text = button_font.render(label, True, BLACK)
        screen.blit(text, text.get_rect(center=rect.center))

    result_rect = pygame.Rect(600, 400, 200, 120)
    pygame.draw.rect(screen, BLACK, result_rect, 5)
    pygame.draw.rect(screen, RESULT_BG, result_rect.inflate(-4, -4))

    result_title = button_font.render("Details", True, BLACK)
    screen.blit(result_title, (result_rect.x + 70, result_rect.y + 5))
    result_texts = [
        f"Runtime: {runtime_duration:.4f}s",
        f"Nodes Expanded: {nodes_expanded}",
        f"Search Depth: {search_depth}",
        f"Steps: {steps_count}",
    ]
    for i, text in enumerate(result_texts):
        label = small_font.render(text, True, BLACK)
        screen.blit(label, (result_rect.x + 10, result_rect.y + 30 + i * 20))

    for x, y, label in control_buttons:
        rect = pygame.Rect(x, y, button_width_control, button_height_control)
        pygame.draw.rect(screen, BLACK, rect, 2)  # Viền đen
        pygame.draw.rect(screen, CONTROL_BG, rect.inflate(-4, -4))  # Nền Control khác
        text = button_font.render(label, True, BLACK)
        screen.blit(text, text.get_rect(center=rect.center))

    if no_solution_message:
        warning_text = matrix_title_font.render("No Solution Found!", True, (255, 0, 0))
        screen.blit(warning_text, (600, 530))

    if solution_found_message:
        success_text = matrix_title_font.render("Solution Found!", True, (0, 180, 0))
        screen.blit(success_text, (600, 530))

    if current_algo_name:
        algo_label = algo_label_font.render(
            f"Algorithm running: {current_algo_name}", True, BLACK
        )
        screen.blit(algo_label, (20, 665))  # Vị trí góc trên bên trái

    pygame.display.update()


# Vòng lặp chính
running = True
while running:
    draw_interface()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Xử lý nút thuật toán
            for x, y, label in buttons:
                rect = pygame.Rect(x, y, button_width, button_height)
                if rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, BUTTON_PRESS_COLOR, rect)
                    pygame.display.flip()
                    pygame.time.delay(100)

                    if label == "BFS":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            bfs_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "DFS":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            dfs_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "UCS":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            ucs_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "IDS":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            ids_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "A Star":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            a_star_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "Greedy":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            greedy_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "IDA Star":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            ida_star_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "SHC":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            simple_hill_climbing(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "S-AHC":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            steepest_ascent_hill_climbing(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "StoHC":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            stochastic_hill_climbing(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "Beam":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            beam_search_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "SA":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            simulated_annealing_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "Gen":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            genetic_algorithm_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "And-Or":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            and_or_graph_search(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "B-BFS":
                        # Khởi tạo Belief với 2 trạng thái khác nhau (giả lập không chắc chắn)
                        start1 = copy.deepcopy(start_state)
                        start2 = copy.deepcopy(start_state)
                        start2[0][0], start2[0][1] = (
                            start2[0][1],
                            start2[0][0],
                        )  # hoán đổi 2 ô đầu để khác nhau

                        solution, runtime_duration, nodes_expanded, steps_count = (
                            belief_bfs_solve([start1, start2], goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "B-A Star":
                        # Khởi tạo Belief với 2 trạng thái khác nhau (giả lập không chắc chắn)
                        start1 = copy.deepcopy(start_state)
                        start2 = copy.deepcopy(start_state)
                        start2[0][0], start2[0][1] = (
                            start2[0][1],
                            start2[0][0],
                        )  # hoán đổi 2 ô đầu để khác nhau
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            belief_a_star_solve([start1, start2], goal_state)
                        )
                        current_algo_name = label

                    elif label == "B-Greedy":
                        # Khởi tạo Belief với 2 trạng thái khác nhau (giả lập không chắc chắn)
                        start1 = copy.deepcopy(start_state)
                        start2 = copy.deepcopy(start_state)
                        start2[0][0], start2[0][1] = (
                            start2[0][1],
                            start2[0][0],
                        )  # hoán đổi 2 ô đầu để khác nhau
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            belief_greedy_solve([start1, start2], goal_state)
                        )
                        current_algo_name = label
                    elif label == "BackTrack":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            backtracking_solve(start_state, goal_state)
                        )
                        current_algo_name = label
                    else:
                        continue

                    search_depth = steps_count
                    print(f"Algorithm: {label}")
                    print(f"Runtime: {runtime_duration:.4f}s")
                    print(f"Nodes expanded: {nodes_expanded}")
                    print(f"Search depth: {search_depth}")
                    print_solution(solution)

                    if solution:
                        start_animation(solution)
                        if solution[-1] == goal_state:
                            no_solution_message = False
                            solution_found_message = True
                            print("Solution found!")
                        else:
                            print("No solution found!")
                            no_solution_message = True
                            solution_found_message = False
                    else:
                        print("No solution found!")
                        no_solution_message = True

            # Xử lý nút Control StepByStep
            for x, y, label in control_buttons:
                rect = pygame.Rect(x, y, button_width_control, button_height_control)
                if rect.collidepoint(mouse_x, mouse_y):
                    # Vẽ hiệu ứng nhấp
                    pygame.draw.rect(screen, BLACK, rect, 2)
                    pygame.draw.rect(screen, CONTROL_CLICK, rect.inflate(-4, -4))
                    text = button_font.render(label, True, BLACK)
                    screen.blit(text, text.get_rect(center=rect.center))
                    pygame.display.update()
                    pygame.time.delay(100)

                    # Xử lý chức năng
                    if label == "Previous" and solution_steps:
                        step_index = max(0, step_index - 1)
                        current_state = copy.deepcopy(solution_steps[step_index])
                    elif label == "Stop":
                        is_playing = False
                    elif label == "Next" and solution_steps:
                        step_index = min(len(solution_steps) - 1, step_index + 1)
                        current_state = copy.deepcopy(solution_steps[step_index])
                    elif label == "Play":
                        is_playing = True
                    elif label == "Reset":
                        current_state = copy.deepcopy(start_state)
                        solution_steps.clear()
                        is_playing = False
                        step_index = 0
                        runtime_duration = 0
                        nodes_expanded = 0
                        search_depth = 0
                        steps_count = 0
                        no_solution_message = False
                        solution_found_message = False
                        current_algo_name = ""

    # Nếu đang Play tự động
    if is_playing and solution_steps:
        if step_index < len(solution_steps) - 1:
            step_index += 1
            current_state = copy.deepcopy(solution_steps[step_index])
            pygame.time.delay(300)
        else:
            is_playing = False

    clock.tick(30)
pygame.quit()
