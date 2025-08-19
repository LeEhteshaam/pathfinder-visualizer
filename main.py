import pygame
pygame.init()

from config import WIDTH, HEIGHT, FPS
from screens import home_screen_loop, visualizer_loop, Screen

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shaam's Pathfinding Visualizer")
    clock = pygame.time.Clock()

    current_screen = Screen.HOME
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if current_screen == Screen.HOME:
            current_screen = home_screen_loop(screen, events)
        elif current_screen == Screen.VISUALIZER:
            current_screen = visualizer_loop(screen, events)
        
        if current_screen == Screen.QUIT:
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()