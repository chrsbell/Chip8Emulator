from renderer import Renderer
import pygame


def update_fps(clock):
    fps = str(int(clock.get_fps()))
    return fps


def main():
    # Routine set-up
    pygame.init()
    renderer = Renderer()
    screen = pygame.display.set_mode((renderer.window_width, renderer.window_height), pygame.OPENGL | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    # Context manager will handle deallocation of resources
    with renderer.create_program():
        renderer.set_pixel(0, 0, 0)
        renderer.set_pixel(1, 0, 0)
        renderer.set_pixel(1, 1, 0)
        renderer.set_pixel(renderer.display_width - 1, renderer.display_height - 1, 0)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    return

            print(update_fps(clock))
            clock.tick()
            renderer.display()
            pygame.display.flip()


if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
