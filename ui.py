import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 8
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
FPS = 10

# Colors (replace these with candy images if available)
CANDY_COLORS = {
    'r': (255, 0, 0),   # Red
    'b': (0, 0, 255),   # Blue
    'g': (0, 255, 0),   # Green
    'p': (255, 0, 255), # Pink
    'o': (255, 165, 0)  # Orange
}

CANDY_TYPES = list(CANDY_COLORS.keys())

# Initialize screen
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Candy Crush")

# Clock for FPS
clock = pygame.time.Clock()

class CandyCrush:
    def __init__(self, size):
        self.size = size
        self.board = [[random.choice(CANDY_TYPES) for _ in range(size)] for _ in range(size)]
        self.selected = None  # Track selected candy
        self.matches_to_remove = []  # Track candies to remove

    def draw_board(self):
        screen.fill((0, 0, 0))  # Black background
        for row in range(self.size):
            for col in range(self.size):
                candy_type = self.board[row][col]
                if candy_type is not None:
                    color = CANDY_COLORS[candy_type]
                    pygame.draw.circle(
                        screen,
                        color,
                        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 3
                    )

    def swap_candies(self, pos1, pos2):
        r1, c1 = pos1
        r2, c2 = pos2
        self.board[r1][c1], self.board[r2][c2] = self.board[r2][c2], self.board[r1][c1]

    def handle_click(self, mouse_pos):
        row, col = mouse_pos[1] // CELL_SIZE, mouse_pos[0] // CELL_SIZE
        if self.selected:
            pos1 = self.selected
            pos2 = (row, col)
            if self.is_valid_swap(pos1, pos2):
                self.swap_candies(pos1, pos2)
                self.matches_to_remove = self.find_matches()
                if not self.matches_to_remove:
                    # Revert swap if no matches
                    self.swap_candies(pos1, pos2)
                self.selected = None
            else:
                self.selected = None  # Deselect if invalid
        else:
            self.selected = (row, col)

    def is_valid_swap(self, pos1, pos2):
        """Check if the swap is valid."""
        r1, c1 = pos1
        r2, c2 = pos2
        return abs(r1 - r2) + abs(c1 - c2) == 1

    def find_matches(self):
        matches = []
        for row in range(self.size):
            for col in range(self.size):
                # Check horizontal match
                if col <= self.size - 3 and self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2]:
                    matches.append([(row, col), (row, col + 1), (row, col + 2)])
                # Check vertical match
                if row <= self.size - 3 and self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col]:
                    matches.append([(row, col), (row + 1, col), (row + 2, col)])
        return matches

    def update_board(self):
        # Remove matched candies
        for match in self.matches_to_remove:
            for row, col in match:
                self.board[row][col] = None

        # Make candies fall
        for col in range(self.size):
            candies = [self.board[row][col] for row in range(self.size) if self.board[row][col] is not None]
            for row in range(self.size):
                self.board[row][col] = candies[row] if row < len(candies) else random.choice(CANDY_TYPES)

        self.matches_to_remove = []  # Clear matches after updating

    def animate_removal(self):
        """Fade out matched candies."""
        for _ in range(5):  # Number of fade steps
            for match in self.matches_to_remove:
                for row, col in match:
                    pygame.draw.circle(
                        screen,
                        (0, 0, 0),
                        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 3
                    )
            pygame.display.flip()
            clock.tick(FPS)

# Main loop
def main():
    game = CandyCrush(GRID_SIZE)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(pygame.mouse.get_pos())

        if game.matches_to_remove:
            game.animate_removal()
            game.update_board()

        game.draw_board()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
