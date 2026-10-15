import pygame #type: ignore
import random

# Initialize Pygame
pygame.init()

# Window dimensions
WIDTH = 1200
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Leaderboard - Animation")

# ==========================================
# SECTION TO ADD OR MODIFY ATHLETES
# ==========================================
# You can add as many athletes as you want simply by adding elements to these lists.
ATHLETE_NAMES = [
    "Athlete 1", 
    "Athlete 2", 
    "Athlete 3", 
    "Athlete 4", 
    "Athlete 5", 
    "Athlete 6", 
    "Athlete 7", 
    "Athlete 8",
    "Athlete 9",
    "Athlete 10",
    "Athlete 11",
    "Athlete 12", 
    "Athlete 13"
]

INITIAL_POINTS = [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 2000, 300, 100]
POINTS_TO_ADD  = [600, 400, 500, 300, 700, 200, 450, 350, 550, 250, 500, 100, 50]

COLORS = [
    (231, 76, 60),    # Red
    (46, 204, 113),   # Green
    (52, 152, 219),   # Blue
    (241, 196, 15),   # Yellow
    (155, 89, 182),   # Purple
    (26, 188, 156),   # Turquoise
    (230, 126, 34),   # Orange
    (149, 165, 166),  # Light Gray
    (243, 156, 18),   # Extra Color
    (255, 255, 0),    # Extra Color
    (255, 0, 0), 
    (255, 0, 255),
    (255, 255, 255)
]
# ==========================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY_MARGIN = (127, 127, 127) # Left panel background
RED_ELIMINATED = (255, 0, 0)

# Fonts
large_font = pygame.font.SysFont("Arial", 26, bold=True)
normal_font = pygame.font.SysFont("Arial", 20)
eliminated_font = pygame.font.SysFont("Arial", 22, bold=True, italic=True)

# Dynamic layout parameters based on the number of athletes
TOTAL_ATHLETES = len(ATHLETE_NAMES)
X_NAMES = 130          # Fixed left position for athlete names
X_BAR = 250            # Starting position for the score bars
Y_INITIAL = 40  
SPACING_Y = min(50, (HEIGHT - 80) // max(TOTAL_ATHLETES, 1))
BAR_HEIGHT = max(10, SPACING_Y - 12)
MAX_BAR_WIDTH = 600
LEFT_MARGIN_WIDTH = 110

class AthleteData:
    def __init__(self, index):
        self.index = index
        self.name = ATHLETE_NAMES[index]
        self.initial_points = INITIAL_POINTS[index]
        self.target_points = self.initial_points + POINTS_TO_ADD[index]
        self.current_points = float(self.initial_points)
        # Color assignment is strictly tied to the athlete's original index
        self.color = COLORS[index % len(COLORS)]
        
        # Y positions for smooth sorting animation
        self.current_y_pos = float(Y_INITIAL + (index * SPACING_Y))
        self.target_y_pos = self.current_y_pos
        self.eliminated = False

# Create athlete list
athletes = [AthleteData(i) for i in range(TOTAL_ATHLETES)]

clock = pygame.time.Clock()

# Sequence state control:
# 0: Initial delay (3s)
# 1: Bar growth (3s)
# 2: Pause after growth (3s exact)
# 3: Smooth reordering from highest to lowest
# 4: 3s pause after sorting
# 5: Display "ELIMINATED" on the last place and hold state
sequence_state = 0
state_time = pygame.time.get_ticks()

def update_order_and_targets():
    # Sort from highest to lowest score (highest score goes to top, index 0 in Y)
    sorted_athletes = sorted(athletes, key=lambda a: a.current_points, reverse=True)
    for i, athlete in enumerate(sorted_athletes):
        athlete.target_y_pos = float(Y_INITIAL + (i * SPACING_Y))

def draw_scene():
    screen.fill(BLACK)
    
    # Left margin for rankings (visible gray panel)
    pygame.draw.rect(screen, GRAY_MARGIN, (0, 0, LEFT_MARGIN_WIDTH, HEIGHT))

    # Determine current rankings based on actual vertical position
    athletes_by_position = sorted(athletes, key=lambda a: a.current_y_pos)

    suffixes = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th", "15th"]

    for i, athlete in enumerate(athletes_by_position):
        y = int(athlete.current_y_pos)
        
        # 1. Draw ranking rank text (1st top, etc.)
        rank_text_str = suffixes[i] if i < len(suffixes) else f"{i+1}th"
        rank_text = large_font.render(rank_text_str, True, WHITE)
        rank_rect = rank_text.get_rect(center=(LEFT_MARGIN_WIDTH // 2, y + BAR_HEIGHT // 2))
        screen.blit(rank_text, rank_rect)

        # 2. Draw athlete's name on the left outside the bar
        name_text = normal_font.render(athlete.name, True, WHITE)
        name_rect = name_text.get_rect(left=X_NAMES, centery=y + BAR_HEIGHT // 2)
        screen.blit(name_text, name_rect)

        # 3. Draw proportional bar with its fixed original color
        max_possible = max([a.target_points for a in athletes]) if athletes else 1
        ratio = min(1.0, athlete.current_points / max_possible) if max_possible > 0 else 0
        bar_width = int(ratio * MAX_BAR_WIDTH)
        
        if bar_width > 0:
            pygame.draw.rect(screen, athlete.color, (X_BAR, y, bar_width, BAR_HEIGHT))

        # 4. Score text at the far right of the bar
        score_text = normal_font.render(str(int(athlete.current_points)), True, WHITE)
        score_rect = score_text.get_rect(left=X_BAR + bar_width + 15, centery=y + BAR_HEIGHT // 2)
        screen.blit(score_text, score_rect)

        # 5. Show "ELIMINATED" in the last position when state is reached
        if athlete.eliminated and sequence_state >= 5:
            elim_text = eliminated_font.render("ELIMINATED", True, RED_ELIMINATED)
            elim_rect = elim_text.get_rect(left=X_BAR + MAX_BAR_WIDTH + 100, centery=y + BAR_HEIGHT // 2)
            screen.blit(elim_text, elim_rect)

    pygame.display.flip()

running = True
while running:
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - state_time) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # --- ANIMATION STATE MACHINE ---
    if sequence_state == 0:
        # State 0: Initial 3-second wait
        if elapsed_time >= 3.0:
            sequence_state = 1
            state_time = pygame.time.get_ticks()

    elif sequence_state == 1:
        # State 1: Bar growth over 3 seconds
        progress = min(1.0, (pygame.time.get_ticks() - state_time) / 3000.0)
        for athlete in athletes:
            athlete.current_points = athlete.initial_points + (athlete.target_points - athlete.initial_points) * progress
        
        if progress >= 1.0:
            for athlete in athletes:
                athlete.current_points = athlete.target_points
            sequence_state = 2  # Move to exact 3-second pause before sorting
            state_time = pygame.time.get_ticks()

    elif sequence_state == 2:
        # State 2: Exact 3-second pause with full scores before sorting
        if elapsed_time >= 3.0:
            update_order_and_targets()
            sequence_state = 3
            state_time = pygame.time.get_ticks()

    elif sequence_state == 3:
        # State 3: Smooth reordering from highest to lowest score
        progress = min(1.0, (pygame.time.get_ticks() - state_time) / 2000.0)
        
        for athlete in athletes:
            athlete.current_y_pos += (athlete.target_y_pos - athlete.current_y_pos) * 0.15

        if progress >= 1.0:
            for athlete in athletes:
                athlete.current_y_pos = athlete.target_y_pos
            sequence_state = 4  # Move to 3-second pause after sorting
            state_time = pygame.time.get_ticks()

    elif sequence_state == 4:
        # State 4: Exact 3-second pause after sorting before showing eliminated label
        if elapsed_time >= 3.0:
            sequence_state = 5
            state_time = pygame.time.get_ticks()

    elif sequence_state == 5:
        # State 5: Mark the last athlete (bottom position) as eliminated
        sorted_by_y = sorted(athletes, key=lambda a: a.current_y_pos)
        if sorted_by_y:
            sorted_by_y[-1].eliminated = True
        sequence_state = 6 # Final static state

    draw_scene()
    clock.tick(60)

pygame.quit()