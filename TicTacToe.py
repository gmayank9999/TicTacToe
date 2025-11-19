import sys
import pygame
import numpy as np
import time

pygame.init()

# ----------------------------- Constants
# Enhanced Color Palette
WHITE = (255, 255, 255)
BG_COLOR = (245, 245, 250)
LIGHT_GRAY = (220, 220, 220)
MEDIUM_GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)
BLACK = (20, 20, 20)

# Player colors
PLAYER_COLOR = (66, 133, 244)  # Nice blue
AI_COLOR = (234, 67, 53)  # Nice red

# Game state colors
WIN_GREEN = (52, 211, 153)
LOSE_RED = (239, 68, 68)
DRAW_GRAY = (156, 163, 175)
WIN_HIGHLIGHT = (34, 197, 94)

# UI Colors
GRID_COLOR = (80, 80, 80)
STATUS_BG = (250, 250, 252)
BORDER_COLOR = (200, 200, 210)

# Sizes (Larger window for better UI)
width = 450
height = 550  # extra space for enhanced status bar
line_width = 6
board_rows = 3
board_cols = 3
square_size = width // board_cols
board_height = width  # playable board area (square)
status_height = height - board_height
circle_radius = square_size // 3
circle_width = 18
cross_width = 20
space = 50  # spacing for X symbol

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

board = np.zeros((board_rows, board_cols))

def draw_lines(color=GRID_COLOR):
    """Draw grid lines with better styling"""
    for i in range(1, board_rows):
        # Horizontal lines
        pygame.draw.line(screen, color, (0, square_size * i), (width, square_size * i), line_width)
        # Vertical lines
        pygame.draw.line(screen, color, (i * square_size, 0), (i * square_size, board_height), line_width)
        
def draw_figures(color=BLACK, player_color=PLAYER_COLOR, ai_color=AI_COLOR):
    """Draw X's and O's with player-specific colors"""
    for row in range(board_rows):
        for col in range(board_cols):
            center_x = int(col * square_size + square_size // 2)
            center_y = int(row * square_size + square_size // 2)
            if board[row][col] == 1:  # Player (O)
                pygame.draw.circle(screen, player_color if color == BLACK else color, 
                                 (center_x, center_y), circle_radius, circle_width)
            elif board[row][col] == 2:  # AI (X)
                draw_cross(screen, ai_color if color == BLACK else color, 
                          col * square_size + space, row * square_size + space,
                          (col + 1) * square_size - space, (row + 1) * square_size - space, cross_width)

def draw_cross(surface, color, start_x, start_y, end_x, end_y, width):
    """Draw a styled X/cross symbol"""
    pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), width)
    pygame.draw.line(surface, color, (start_x, end_y), (end_x, start_y), width)
                
def mark_square(row, col, player):
    board[row][col] = player
    
def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=board):
    for row in range(board_rows):
        for col in range(board_cols):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board=board):
    """Check if player has won"""
    # Check rows
    for row in range(board_rows):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
    # Check columns
    for col in range(board_cols):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
    # Check diagonals
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    return False

def minimax(minimax_board, depth, is_max):
    """
    MINIMAX ALGORITHM (PURE):
    
    This is a recursive algorithm that explores ALL possible game states to find the optimal move.
    
    How it works:
    1. BASE CASES (Terminal states):
       - If AI wins: return positive score (10 - depth) - prefers faster wins
       - If Player wins: return negative score (depth - 10) - prefers slower losses
       - If draw: return 0 (neutral)
    
    2. RECURSIVE CASES:
       - When is_max=True (AI's turn): Maximize score - find best move for AI
       - When is_max=False (Player's turn): Minimize score - assume player plays optimally
    
    3. DEPTH: Used to prefer shorter paths to victory (faster wins are better)
    
    4. BACKTRACKING: After evaluating a move, it undoes it (sets to 0) to try other moves
    
    Time Complexity: O(b^d) where b=branching factor, d=depth
    This makes the AI UNBEATABLE because it can see all possible future moves!
    """
    # Base case: terminal states
    if check_win(2, minimax_board):  # AI wins
        return 10 - depth  # Prefer faster wins (higher score)
    elif check_win(1, minimax_board):  # Player wins
        return depth - 10  # Prefer slower losses (less negative)
    elif is_board_full(minimax_board):  # Draw
        return 0
    
    # Recursive case: explore all possible moves
    if is_max:  # AI's turn - maximize score
        best_score = -float('inf')
        for row in range(board_rows):
            for col in range(board_cols):
                if minimax_board[row][col] == 0:  # Empty square
                    minimax_board[row][col] = 2  # Try AI move
                    score = minimax(minimax_board, depth + 1, False)  # Player's turn next
                    minimax_board[row][col] = 0  # Undo move (backtrack)
                    best_score = max(score, best_score)
        return best_score
    else:  # Player's turn - minimize score (assume optimal play)
        best_score = float('inf')
        for row in range(board_rows):
            for col in range(board_cols):
                if minimax_board[row][col] == 0:  # Empty square
                    minimax_board[row][col] = 1  # Try player move
                    score = minimax(minimax_board, depth + 1, True)  # AI's turn next
                    minimax_board[row][col] = 0  # Undo move (backtrack)
                    best_score = min(score, best_score)
        return best_score

def minimax_alpha_beta(minimax_board, depth, is_max, alpha=-float('inf'), beta=float('inf')):
    """
    MINIMAX WITH ALPHA-BETA PRUNING (OPTIMIZED):
    
    Same as Minimax but with ALPHA-BETA PRUNING to improve performance!
    
    How Alpha-Beta Pruning works:
    1. ALPHA: Best value that the maximizer (AI) can guarantee
    2. BETA: Best value that the minimizer (Player) can guarantee
    3. PRUNING: If we find a move that's worse than what we've already seen, 
                we can skip evaluating the rest of the branch (prune it!)
    
    Benefits:
    - Same optimal results as pure Minimax
    - MUCH faster - can reduce nodes evaluated by 50-90%
    - Time Complexity: O(b^d) worst case, but typically O(b^(d/2)) in practice
    - Still unbeatable - same perfect play, just optimized!
    
    The pruning happens when:
    - In MAX node: if score >= beta, prune (alpha >= beta)
    - In MIN node: if score <= alpha, prune (alpha >= beta)
    """
    # Base case: terminal states (same as pure minimax)
    if check_win(2, minimax_board):  # AI wins
        return 10 - depth
    elif check_win(1, minimax_board):  # Player wins
        return depth - 10
    elif is_board_full(minimax_board):  # Draw
        return 0
    
    # Recursive case with pruning
    if is_max:  # AI's turn - maximize score
        best_score = -float('inf')
        for row in range(board_rows):
            for col in range(board_cols):
                if minimax_board[row][col] == 0:  # Empty square
                    minimax_board[row][col] = 2  # Try AI move
                    score = minimax_alpha_beta(minimax_board, depth + 1, False, alpha, beta)
                    minimax_board[row][col] = 0  # Undo move (backtrack)
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)  # Update alpha
                    if beta <= alpha:  # PRUNING: This branch can't improve the result
                        return best_score  # Prune remaining branches (early return)
        return best_score
    else:  # Player's turn - minimize score
        best_score = float('inf')
        for row in range(board_rows):
            for col in range(board_cols):
                if minimax_board[row][col] == 0:  # Empty square
                    minimax_board[row][col] = 1  # Try player move
                    score = minimax_alpha_beta(minimax_board, depth + 1, True, alpha, beta)
                    minimax_board[row][col] = 0  # Undo move (backtrack)
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)  # Update beta
                    if beta <= alpha:  # PRUNING: This branch can't improve the result
                        return best_score  # Prune remaining branches (early return)
        return best_score

# Global toggle for algorithm selection
use_alpha_beta = False  # False = Pure Minimax, True = Minimax with Alpha-Beta Pruning

def best_move():
    """
    Uses selected algorithm (Minimax or Minimax with Alpha-Beta Pruning) to find the BEST move for the AI.
    Tries every possible move and picks the one with the highest score.
    Toggle with 'P' key to switch between algorithms.
    """
    best_score = -float('inf')
    move = (-1, -1)
    
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 0:  # Empty square
                board[row][col] = 2  # Try AI move
                # Use selected algorithm
                if use_alpha_beta:
                    score = minimax_alpha_beta(board.copy(), 0, False)  # With pruning
                else:
                    score = minimax(board.copy(), 0, False)  # Pure minimax
                board[row][col] = 0  # Undo move
                if score > best_score:
                    best_score = score
                    move = (row, col)
    
    if move != (-1, -1):
        mark_square(move[0], move[1], player=2)
        return True
    return False
        
def restart_game():
    """Reset the game to initial state"""
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(board_rows):
        for col in range(board_cols):
            board[row][col] = 0
    draw_figures()
    pygame.display.update()

def draw_status_bar(status_text, status_color, bg_color):
    """Draw enhanced status bar with better styling"""
    status_rect = pygame.Rect(0, board_height, width, status_height)
    
    # Draw background with border
    pygame.draw.rect(screen, bg_color, status_rect)
    pygame.draw.line(screen, BORDER_COLOR, (0, board_height), (width, board_height), 2)
    
    # Use better font
    try:
        font_large = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 22)
    except:
        font_large = pygame.font.SysFont('arial', 32, bold=True)
        font_small = pygame.font.SysFont('arial', 22)
    
    # Split text into main message and instruction
    if "Press R" in status_text:
        parts = status_text.split("Press R")
        main_text = parts[0].strip()
        instruction = "Press R" + parts[1] if len(parts) > 1 else ""
    else:
        main_text = status_text
        instruction = ""
    
    # Render main text
    text_surf = font_large.render(main_text, True, status_color)
    text_rect = text_surf.get_rect(center=(width//2, board_height + status_height//2 - 8 if instruction else board_height + status_height//2))
    screen.blit(text_surf, text_rect)
    
    # Render instruction text (smaller)
    if instruction:
        inst_surf = font_small.render(instruction, True, DARK_GRAY)
        inst_rect = inst_surf.get_rect(center=(width//2, board_height + status_height//2 + 15))
        screen.blit(inst_surf, inst_rect)

def draw_game_over_overlay(result_type):
    """Draw a prominent overlay when game ends"""
    overlay = pygame.Surface((width, board_height))
    overlay.set_alpha(180)  # Semi-transparent
    
    if result_type == "win":
        overlay.fill(WIN_GREEN)
    elif result_type == "lose":
        overlay.fill(LOSE_RED)
    else:  # draw
        overlay.fill(DRAW_GRAY)
    
    screen.blit(overlay, (0, 0))
    
    # Draw large message
    try:
        big_font = pygame.font.Font(None, 72)
        small_font = pygame.font.Font(None, 28)
    except:
        big_font = pygame.font.SysFont('arial', 72, bold=True)
        small_font = pygame.font.SysFont('arial', 28)
    
    if result_type == "win":
        message = "YOU WIN!"
        color = WHITE
    elif result_type == "lose":
        message = "YOU LOSE!"
        color = WHITE
    else:
        message = "DRAW!"
        color = WHITE
    
    text_surf = big_font.render(message, True, color)
    text_rect = text_surf.get_rect(center=(width//2, board_height//2 - 20))
    screen.blit(text_surf, text_rect)
    
    # Draw subtitle
    subtitle = "Press R to play again"
    sub_surf = small_font.render(subtitle, True, WHITE)
    sub_rect = sub_surf.get_rect(center=(width//2, board_height//2 + 40))
    screen.blit(sub_surf, sub_rect)

# Initialize game
draw_lines()
draw_figures()
pygame.display.update()
player = 1
game_over = False
game_result = None  # "win", "lose", or "draw"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 1:
            mouseX = event.pos[0] // square_size
            mouseY = event.pos[1] // square_size
            
            # Check bounds
            if mouseX < 3 and mouseY < 3 and available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                    game_result = "win"
                elif is_board_full():
                    game_over = True
                    game_result = "draw"
                else:
                    player = 2  # AI's turn
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                game_result = None
                player = 1
            elif event.key == pygame.K_p:
                # Toggle between Minimax and Alpha-Beta Pruning
                use_alpha_beta = not use_alpha_beta

    # AI's turn
    if not game_over and player == 2:
        # Small delay for better UX
        time.sleep(0.3)
        if best_move():
            if check_win(2):
                game_over = True
                game_result = "lose"
            elif is_board_full():
                game_over = True
                game_result = "draw"
            else:
                player = 1
    
    # Clear screen
    screen.fill(BG_COLOR)
    draw_lines()
    
    # Draw figures and game over overlay
    if not game_over:
        draw_figures()
    else:
        # Draw figures with appropriate colors
        if game_result == "win":
            draw_figures(WIN_GREEN, WIN_GREEN, WIN_GREEN)
            draw_lines(WIN_GREEN)
        elif game_result == "lose":
            draw_figures(LOSE_RED, LOSE_RED, LOSE_RED)
            draw_lines(LOSE_RED)
        else:  # draw
            draw_figures(DRAW_GRAY, DRAW_GRAY, DRAW_GRAY)
            draw_lines(DRAW_GRAY)
        
        # Draw prominent overlay
        draw_game_over_overlay(game_result)

    # Draw status bar with algorithm indicator
    algo_indicator = " [Alpha-Beta]" if use_alpha_beta else " [Minimax]"
    algo_color = (100, 200, 255) if use_alpha_beta else (150, 150, 150)
    
    if game_over:
        if game_result == "win":
            draw_status_bar("🎉 YOU WIN! 🎉" + algo_indicator, WIN_GREEN, STATUS_BG)
        elif game_result == "lose":
            draw_status_bar("😢 YOU LOSE! 😢" + algo_indicator, LOSE_RED, STATUS_BG)
        else:
            draw_status_bar("🤝 IT'S A DRAW! 🤝" + algo_indicator, DRAW_GRAY, STATUS_BG)
    else:
        if player == 1:
            main_text = "Your Turn (O) - Click a square"
            draw_status_bar(main_text + algo_indicator, PLAYER_COLOR, STATUS_BG)
        else:
            main_text = "AI Thinking..." + algo_indicator
            draw_status_bar(main_text, AI_COLOR, STATUS_BG)
    
    # Draw algorithm indicator in corner
    try:
        info_font = pygame.font.Font(None, 16)
    except:
        info_font = pygame.font.SysFont('arial', 16)
    
    algo_text = "Algorithm: " + ("Alpha-Beta Pruning" if use_alpha_beta else "Pure Minimax")
    algo_surf = info_font.render(algo_text, True, algo_color)
    screen.blit(algo_surf, (5, 5))
    
    # Draw controls hint
    controls_text = "Press P: Toggle Algorithm | Press R: Restart"
    controls_surf = info_font.render(controls_text, True, DARK_GRAY)
    controls_rect = controls_surf.get_rect(bottomright=(width - 5, height - 5))
    screen.blit(controls_surf, controls_rect)

    pygame.display.update()
