# starter file : optional 
# feel free to start from scratch
import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 360  # extra vertical space for scoreboard
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 4
BOARD_OFFSET_Y = 60  # leave space at top for score

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)

# Fonts
FONT = pygame.font.SysFont('arial', 32)
SMALL_FONT = pygame.font.SysFont('arial', 18)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BG_COLOR)

# Game state
board = []

# Scores
wins = 0
losses = 0
draws = 0

# Control flags
selecting_size = True
selected_size = None
player = 'X'
game_over = False


def set_board_size(size):
    global BOARD_ROWS, BOARD_COLS, SQUARE_SIZE, CIRCLE_RADIUS, SPACE, board
    BOARD_ROWS = BOARD_COLS = size
    SQUARE_SIZE = WIDTH // BOARD_COLS
    CIRCLE_RADIUS = SQUARE_SIZE // 3
    SPACE = SQUARE_SIZE // 4
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]


def draw_score():
    # Draw score and instructions at top area
    score_text = f'W: {wins}   L: {losses}   D: {draws}   Size: {BOARD_ROWS}x{BOARD_COLS if BOARD_ROWS==BOARD_COLS else f"{BOARD_ROWS}x{BOARD_COLS}"}'
    instr_text = 'R: replay same size   N: reset scores & choose size'

    text_surf = SMALL_FONT.render(score_text, True, TEXT_COLOR)
    instr_surf = SMALL_FONT.render(instr_text, True, TEXT_COLOR)

    # Clear top area
    top_rect = pygame.Rect(0, 0, WIDTH, BOARD_OFFSET_Y)
    pygame.draw.rect(screen, BG_COLOR, top_rect)

    screen.blit(text_surf, (8, 8))
    screen.blit(instr_surf, (8, 30))


def draw_lines():
    # draw board grid lines with vertical offset
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, BOARD_OFFSET_Y + row * SQUARE_SIZE),
                         (WIDTH, BOARD_OFFSET_Y + row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, BOARD_OFFSET_Y),
                         (col * SQUARE_SIZE, BOARD_OFFSET_Y + BOARD_ROWS * SQUARE_SIZE), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            val = board[row][col]
            center_x = int(col * SQUARE_SIZE + SQUARE_SIZE / 2)
            center_y = int(BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE / 2)
            if val == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif val == 'X':
                start_desc = (col * SQUARE_SIZE + SPACE, BOARD_OFFSET_Y + row * SQUARE_SIZE + SPACE)
                end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                start_asc = (col * SQUARE_SIZE + SPACE, BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, BOARD_OFFSET_Y + row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)


def mark_square(row, col, player_char):
    board[row][col] = player_char


def available_square(row, col):
    return 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS and board[row][col] is None


def is_board_full():
    return all(all(cell is not None for cell in r) for r in board)


def check_win(player_char):
    # rows
    for row in board:
        if all(cell == player_char for cell in row):
            return True
    # cols
    for col in range(BOARD_COLS):
        if all(board[row][col] == player_char for row in range(BOARD_ROWS)):
            return True
    # diagonal
    if all(board[i][i] == player_char for i in range(BOARD_ROWS)):
        return True
    if all(board[i][BOARD_ROWS - i - 1] == player_char for i in range(BOARD_ROWS)):
        return True
    return False


def ai_move():
    empty_cells = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] is None]
    return random.choice(empty_cells) if empty_cells else None


def show_message(message, duration=1200):
    # Draw a semi-transparent rect behind the text for visibility
    overlay = pygame.Surface((WIDTH, 60))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, HEIGHT//2 - 30))

    text = FONT.render(message, True, (255, 255, 255))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)
    pygame.display.update()
    pygame.time.wait(duration)


def show_prompt(message):
    # show a small prompt at the bottom of the screen
    text = SMALL_FONT.render(message, True, (255, 255, 255))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 20))
    # draw a small semi-transparent background for readability
    bg = pygame.Surface((rect.width + 10, rect.height + 6))
    bg.set_alpha(180)
    bg.fill((0, 0, 0))
    screen.blit(bg, (rect.x - 5, rect.y - 3))
    screen.blit(text, rect)
    pygame.display.update()


def restart_board_keep_size():
    global board, game_over, player
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    draw_score()
    game_over = False
    player = 'X'


def reset_scores_and_choose_size():
    global wins, losses, draws, selecting_size, selected_size
    wins = losses = draws = 0
    selecting_size = True
    selected_size = None
    screen.fill(BG_COLOR)
    draw_score()


def draw_selection_screen():
    # Clear screen
    screen.fill(BG_COLOR)
    title = FONT.render('Select board size', True, TEXT_COLOR)
    opts = SMALL_FONT.render('Press 3, 4 or 5 to select a board size (3x3 - 5x5)', True, TEXT_COLOR)
    note = SMALL_FONT.render('Current scores will reset when you choose a new size.', True, TEXT_COLOR)
    screen.blit(title, title.get_rect(center=(WIDTH//2, 80)))
    screen.blit(opts, opts.get_rect(center=(WIDTH//2, 140)))
    screen.blit(note, note.get_rect(center=(WIDTH//2, 170)))
    pygame.display.update()


# Initial state: selection screen
screen.fill(BG_COLOR)
draw_selection_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if selecting_size:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    selected_size = 3
                elif event.key == pygame.K_4:
                    selected_size = 4
                elif event.key == pygame.K_5:
                    selected_size = 5

                if selected_size:
                    set_board_size(selected_size)
                    selecting_size = False
                    screen.fill(BG_COLOR)
                    draw_lines()
                    draw_figures()
                    draw_score()
                    pygame.display.update()
        else:
            # Normal gameplay
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                # only consider clicks inside board area
                if BOARD_OFFSET_Y <= mouseY < BOARD_OFFSET_Y + BOARD_ROWS * SQUARE_SIZE:
                    clicked_row = (mouseY - BOARD_OFFSET_Y) // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE

                    if available_square(clicked_row, clicked_col):
                        mark_square(clicked_row, clicked_col, player)
                        draw_figures()

                        if check_win(player):
                            wins += 1
                            draw_score()
                            show_message("You win!")
                            show_prompt("Press R to play again (same size) or N to reset scores & choose size")
                            game_over = True
                        elif is_board_full():
                            draws += 1
                            draw_score()
                            show_message("Draw!")
                            show_prompt("Press R to play again (same size) or N to reset scores & choose size")
                            game_over = True
                        else:
                            move = ai_move()
                            if move:
                                ai_r, ai_c = move
                                mark_square(ai_r, ai_c, 'O')
                                draw_figures()
                                if check_win('O'):
                                    losses += 1
                                    draw_score()
                                    show_message("AI wins!")
                                    show_prompt("Press R to play again (same size) or N to reset scores & choose size")
                                    game_over = True
                                elif is_board_full():
                                    draws += 1
                                    draw_score()
                                    show_message("Draw!")
                                    show_prompt("Press R to play again (same size) or N to reset scores & choose size")
                                    game_over = True

            if event.type == pygame.KEYDOWN:
                # R: restart board with same size (keep scores)
                if event.key == pygame.K_r and not selecting_size:
                    restart_board_keep_size()
                # N: reset scores and go back to selection to pick a new size
                if event.key == pygame.K_n:
                    reset_scores_and_choose_size()
                    draw_selection_screen()

    # Always update score area when not selecting
    if not selecting_size:
        draw_score()

    pygame.display.update()
