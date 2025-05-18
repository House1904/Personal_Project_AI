import pygame
import copy
import random
import numpy as np
from search_algorithms import (
    bfs_solve,
    dfs_solve,
    ucs_solve,
    ids_solve,
    a_star_solve,
    greedy_solve,
    ida_star_solve,
    beam_search_solve,
    simple_hill_climbing,
    steepest_ascent_hill_climbing,
    stochastic_hill_climbing,
    simulated_annealing_solve,
    genetic_algorithm_solve,
    and_or_graph_search,
    belief_bfs_solve,
    belief_ids_solve,
    belief_a_star_solve,
    belief_greedy_solve,
    belief_beam_solve,
    backtracking_solve,
    forward_checking_solve,
    q_learning_solve,
)

import matplotlib.pyplot as plt

results_log = {}

import csv
import os


def log_result_to_csv(start_state_str, algorithm_name, runtime, nodes, depth):
    filename = "algorithm_results_log.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(
                [
                    "Start State",
                    "Algorithm",
                    "Runtime",
                    "Nodes Expanded",
                    "Search Depth",
                ]
            )
        writer.writerow([start_state_str, algorithm_name, runtime, nodes, depth])


def flatten_matrix(matrix):
    return "".join(
        str(cell) if cell is not None else "-" for row in matrix for cell in row
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
start_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]  # start_state mặc định
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
current_state = copy.deepcopy(start_state)

# Input box nhập start_state từ bàn phím
input_active = False
input_text = ""
input_rect = pygame.Rect(600, 550, 240, 35)
input_color_active = pygame.Color("dodgerblue2")
input_color_inactive = pygame.Color("gray70")
input_color = input_color_inactive


def parse_input_to_matrix(text):
    if len(text) == 9 and all(ch in "012345678" for ch in text):
        if len(set(text)) == 9:  # Không trùng số
            nums = [int(ch) for ch in text]
            return [nums[i : i + 3] for i in range(0, 9, 3)]
    return None


def parse_input_to_belief_matrix(text):
    if len(text) != 9:
        return None  # Không đủ 9 ký tự

    nums = []
    seen = set()

    for ch in text:
        if ch == "-":
            nums.append(None)
        elif ch.isdigit():
            val = int(ch)
            if val in seen:
                return None  # Bị trùng số
            seen.add(val)
            nums.append(val)
        else:
            return None  # Ký tự không hợp lệ

    if len(seen) + nums.count(None) != 9:
        return None  # Thiếu hoặc dư số

    return [nums[i : i + 3] for i in range(0, 9, 3)]


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
belief_matrix = None


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
    "Beam",
    "SHC",
    "S-AHC",
    "StoHC",
    "SA",
    "Gen",
    "And-Or",
    "B-BFS",
    "B-IDS",
    "B-A Star",
    "B-Greedy",
    "B-Beam",
    "BackTrack",
    "ForCheck",
    "Q-Learn",
]

button_width, button_height = 120, 40
button_width_control, button_height_control = 125, 40
button_padding = 5
start_x = 100

buttons_row1 = [
    (start_x + i * (button_width + button_padding), 400, algo)
    for i, algo in enumerate(algorithms[:4])
]
buttons_row2 = [
    (start_x + i * (button_width + button_padding), 450, algo)
    for i, algo in enumerate(algorithms[4:8])
]
buttons_row3 = [
    (start_x + i * (button_width + button_padding), 500, algo)
    for i, algo in enumerate(algorithms[8:11])
]
buttons_row4 = [
    (start_x + i * (button_width + button_padding), 550, algo)
    for i, algo in enumerate(algorithms[11:13])
]

buttons_row5 = [
    (start_x + i * (button_width + button_padding), 600, algo)
    for i, algo in enumerate(algorithms[13:19])
]

buttons_row6 = [
    (start_x + i * (button_width + button_padding), 650, algo)
    for i, algo in enumerate(algorithms[19:])
]

buttons = (
    buttons_row1
    + buttons_row2
    + buttons_row3
    + buttons_row4
    + buttons_row5
    + buttons_row6
)

# Các nút điều khiển StepByStep
control_buttons = [
    (15, 330, "Previous"),
    (165, 330, "Stop"),
    (315, 330, "Next"),
    (465, 330, "Play"),
    (615, 330, "Reset"),
    (765, 330, "Compare"),
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
        screen.blit(algo_label, (650, 665))  # Vị trí góc trên bên trái

    # Ô nhập liệu
    pygame.draw.rect(screen, input_color, input_rect, 2)
    if input_text == "" and not input_active:
        # Hiển thị placeholder nếu ô rỗng và chưa được chọn
        placeholder = small_font.render(
            "Enter 9 digits (0-8) for Start", True, (150, 150, 150)
        )
        screen.blit(placeholder, (input_rect.x + 5, input_rect.y + 5))
    else:
        # Hiển thị nội dung người dùng nhập
        input_surface = button_font.render(input_text, True, BLACK)
        screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

    pygame.display.update()


# Vòng lặp chính
running = True
while running:
    draw_interface()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                input_active = True
                input_color = input_color_active
            else:
                input_active = False
                input_color = input_color_inactive
        if event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_RETURN:
                if "-" in input_text:  # Nếu là belief input
                    belief_matrix = parse_input_to_belief_matrix(input_text)
                    if belief_matrix:
                        print("New Belief Input:", belief_matrix)
                        # Không cập nhật start_state ở đây
                    else:
                        print(
                            "Invalid belief input. Use format like '2-6--870-' with no duplicates."
                        )
                        belief_matrix = None  # Reset nếu sai
                else:  # Nếu là input đầy đủ
                    matrix = parse_input_to_matrix(input_text)
                    if matrix:
                        start_state[:] = matrix
                        current_state[:] = matrix
                        solution_steps.clear()
                        step_index = 0
                        print("New Start State:", start_state)
                    else:
                        print("Invalid input! Must be 9 digits 0-8 (no duplicates)")
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif len(input_text) < 9:
                if event.unicode in "012345678-":
                    input_text += event.unicode

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
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "DFS":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            dfs_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "UCS":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            ucs_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "IDS":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            ids_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "A Star":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            a_star_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "Greedy":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            greedy_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "IDA Star":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            ida_star_solve(start_state, goal_state)
                        )
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                    elif label == "SHC":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            simple_hill_climbing(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "S-AHC":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            steepest_ascent_hill_climbing(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "StoHC":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            stochastic_hill_climbing(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "Beam":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            beam_search_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "SA":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            simulated_annealing_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "Gen":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            genetic_algorithm_solve(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "And-Or":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            and_or_graph_search(start_state, goal_state)
                        )
                        current_algo_name = label  # Lưu tên thuật toán hiện tại
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "B-BFS":
                        if not belief_matrix:
                            print(
                                "Please enter a valid belief input before running this algorithm."
                            )
                            no_solution_message = True
                            solution_found_message = False
                            continue

                        solution, runtime_duration, nodes_expanded, steps_count = (
                            belief_bfs_solve(belief_matrix, goal_state)
                        )
                        current_algo_name = label

                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(belief_matrix),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "B-IDS":
                        if not belief_matrix:
                            print(
                                "Please enter a valid belief input before running this algorithm."
                            )
                            no_solution_message = True
                            solution_found_message = False
                            continue

                        solution, runtime_duration, nodes_expanded, steps_count = (
                            belief_ids_solve(belief_matrix, goal_state)
                        )
                        current_algo_name = label

                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(belief_matrix),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "B-A Star":
                        if not belief_matrix:
                            print(
                                "Please enter a valid belief input before running this algorithm."
                            )
                            no_solution_message = True
                            solution_found_message = False
                            continue

                        solution, runtime_duration, nodes_expanded, steps_count = (
                            belief_a_star_solve(belief_matrix, goal_state)
                        )
                        current_algo_name = label

                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(belief_matrix),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "B-Greedy":
                        if not belief_matrix:
                            print(
                                "Please enter a valid belief input before running this algorithm."
                            )
                            no_solution_message = True
                            solution_found_message = False
                            continue

                        solution, runtime_duration, nodes_expanded, steps_count = (
                            belief_greedy_solve(belief_matrix, goal_state)
                        )
                        current_algo_name = label

                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(belief_matrix),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "B-Beam":
                        if not belief_matrix:
                            print(
                                "Please enter a valid belief input before running this algorithm."
                            )
                            no_solution_message = True
                            solution_found_message = False
                            continue

                        solution, runtime_duration, nodes_expanded, steps_count = (
                            belief_beam_solve(belief_matrix, goal_state)
                        )
                        current_algo_name = label

                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(belief_matrix),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "BackTrack":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            backtracking_solve(start_state, goal_state)
                        )
                        current_algo_name = label
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "ForCheck":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            forward_checking_solve(start_state, goal_state)
                        )
                        current_algo_name = label
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )

                    elif label == "Q-Learn":
                        solution, runtime_duration, nodes_expanded, steps_count = (
                            q_learning_solve(start_state, goal_state)
                        )
                        current_algo_name = label
                        results_log[label] = {
                            "Runtime": runtime_duration,
                            "Nodes Expanded": nodes_expanded,
                            "Search Depth": steps_count,
                        }
                        log_result_to_csv(
                            flatten_matrix(start_state),
                            label,
                            runtime_duration,
                            nodes_expanded,
                            steps_count,
                        )
                    else:
                        continue

                    search_depth = steps_count
                    print(f"Algorithm: {label}")
                    print(f"Runtime: {runtime_duration:.4f}s")
                    print(f"Nodes expanded: {nodes_expanded}")
                    print(f"Search depth: {search_depth}")
                    print_solution(solution)

                    if solution:
                        start_state[:] = solution[0]
                        current_state[:] = solution[0]
                        start_animation(solution)
                        if solution[-1] == goal_state:
                            no_solution_message = False
                            solution_found_message = True
                            print("Solution found!")
                        else:
                            print("No solution found!")
                            no_solution_message = True
                            solution_found_message = False
                    elif start_state == goal_state:
                        solution = [start_state]
                        start_animation(solution)
                        no_solution_message = False
                        solution_found_message = True
                        print("Already at goal!")
                    else:
                        print("No solution found!")
                        no_solution_message = True
                        solution_found_message = False

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
                    elif label == "Compare" and results_log:
                        # Lấy danh sách thuật toán đã chạy
                        algorithms_ran = list(results_log.keys())
                        x = np.arange(len(algorithms_ran))

                        # Dữ liệu
                        runtimes = [
                            results_log[algo]["Runtime"] for algo in algorithms_ran
                        ]
                        nodes = [
                            results_log[algo]["Nodes Expanded"]
                            for algo in algorithms_ran
                        ]
                        depths = [
                            results_log[algo]["Search Depth"] for algo in algorithms_ran
                        ]

                        bar_width = 0.25

                        fig, ax1 = plt.subplots(figsize=(12, 6))

                        # Trục thứ nhất - Runtime
                        ax1.set_xlabel("Algorithms")
                        ax1.set_ylabel("Runtime (s)", color="tab:blue")
                        bars1 = ax1.bar(
                            x - bar_width,
                            runtimes,
                            width=bar_width,
                            label="Runtime",
                            color="tab:blue",
                        )
                        ax1.tick_params(axis="y", labelcolor="tab:blue")

                        # Trục thứ hai - Nodes Expanded
                        ax2 = ax1.twinx()
                        ax2.set_ylabel("Nodes Expanded", color="tab:green")
                        bars2 = ax2.bar(
                            x,
                            nodes,
                            width=bar_width,
                            label="Nodes Expanded",
                            color="tab:green",
                        )
                        ax2.tick_params(axis="y", labelcolor="tab:green")

                        # Trục thứ ba - Search Depth
                        ax3 = ax1.twinx()
                        ax3.spines.right.set_position(
                            ("axes", 1.15)
                        )  # Đẩy trục thứ ba sang phải
                        ax3.set_ylabel("Search Depth", color="tab:red")
                        bars3 = ax3.bar(
                            x + bar_width,
                            depths,
                            width=bar_width,
                            label="Search Depth",
                            color="tab:red",
                        )
                        ax3.tick_params(axis="y", labelcolor="tab:red")

                        # Gán nhãn trục X
                        ax1.set_xticks(x)
                        ax1.set_xticklabels(algorithms_ran, rotation=45)

                        # Tiêu đề và hiển thị
                        plt.title("Comparison of Search Algorithms (Multi-axis)")
                        fig.tight_layout()
                        plt.show()

    # Nếu đang Play tự động
    if is_playing and solution_steps:
        if step_index < len(solution_steps) - 1:
            step_index += 1
            current_state = copy.deepcopy(solution_steps[step_index])
            pygame.time.delay(200)
        else:
            is_playing = False

    clock.tick(30)
pygame.quit()
