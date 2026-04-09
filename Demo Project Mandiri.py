import pygame
import random

# Inisialisasi
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Training")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

hit_sound = pygame.mixer.Sound("click.wav")

# Parent Class
class GameObject:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self):
        pass

    def update(self):
        pass

# Inheritance Class
class Target(GameObject):
    def __init__(self):
        x = random.randint(0, WIDTH - 30)
        y = random.randint(0, HEIGHT - 30)
        super().__init__(x, y, 30)

        self.velocity_x = random.choice([-2, -1, 1, 2])
        self.velocity_y = random.choice([-2, -1, 1, 2])

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Pantul dari dinding
        if self.x <= 0 or self.x >= WIDTH - self.size:
            self.velocity_x *= -1
        if self.y <= 0 or self.y >= HEIGHT - self.size:
            self.velocity_y *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (self.x, self.y), self.size // 2)

    def is_hit(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        return (self.x - mouse_x) ** 2 + (self.y - mouse_y) ** 2 <= (self.size // 2) ** 2

# Class Game
class AimTrainerGame:
    def __init__(self):
        self.targets = [Target() for _ in range(5)]
        self.score = 0

        self.font = pygame.font.SysFont(None, 30)
        self.large_font = pygame.font.SysFont(None, 50)

        self.is_running = True
        self.is_game_over = False

        # Timer
        self.start_time = pygame.time.get_ticks()
        self.game_duration = 60  # detik

    def run(self):
        clock = pygame.time.Clock()

        while self.is_running:
            screen.fill(WHITE)

            # Time Counter
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.start_time) / 1000
            remaining_time = max(0, self.game_duration - int(elapsed_time))

            if remaining_time <= 0:
                self.is_game_over = True

            # Quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.MOUSEBUTTONDOWN and not self.is_game_over:
                    self.handle_shot(pygame.mouse.get_pos())

            # Update & Draw
            if not self.is_game_over:
                for target in self.targets:
                    target.update()
                    target.draw(screen)
            else:
                self.display_game_over()

            # UI Score
            score_text = self.font.render(f"Score: {self.score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            # UI Timer
            time_text = self.font.render(f"Time: {remaining_time}", True, BLACK)
            screen.blit(time_text, (480, 10))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def handle_shot(self, mouse_pos):
        for target in self.targets:
            if target.is_hit(mouse_pos):
                self.score += 1
                hit_sound.play()
                self.targets.remove(target)
                self.targets.append(Target())
                break

    def display_game_over(self):
        game_over_text = self.large_font.render("GAME OVER", True, BLACK)
        score_text = self.font.render(f"Final Score: {self.score}", True, BLACK)

        screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 40))
        screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2 + 10))

# Main Program
if __name__ == "__main__":
    game = AimTrainerGame()
    game.run()