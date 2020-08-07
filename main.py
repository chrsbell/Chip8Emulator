from interpreter import Interpreter
from renderer import Renderer
import pygame


def update_fps(clock):
    fps = str(int(clock.get_fps()))
    return fps


def main():
    # Routine set-up
    pygame.init()
    display = Renderer()
    screen = pygame.display.set_mode((display.window_width, display.window_height),
                                     pygame.OPENGL | pygame.DOUBLEBUF)
    interpreter = Interpreter()
    clock = pygame.time.Clock()
    i = 0
    # Context manager handles deallocation of OpenGL resources
    with display.initialize_display():
        interpreter.set_display(display)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    return
            if (i < (display.width * display.height)):
                display.set_pixel(i, 0, 1)
                i += 1
            print(update_fps(clock))
            clock.tick(display.max_fps)
            display.render()
            pygame.display.flip()


if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
