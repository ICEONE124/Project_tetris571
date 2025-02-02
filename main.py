import pygame
import sys
import functions
from random import randint


# стрелка влево - движение влево
# cтрелка вправо - движение вправо
# стрелка вниз - более быстрый спуск
# стрелка вверх - более медленный спуск (если уже нажал кнопку вниз)
# Пробел -> поворот фигуры

def main():
    pygame.font.init()
    pygame.display.set_caption("Тетрис")
    pygame.mixer.init()
    music = pygame.mixer_music.load('music.ogg')
    pygame.mixer.music.play(-1)

    number_of_tiles_x = 10
    number_of_tiles_y = 20
    title_size = 30
    fps = 30
    back_color = (0, 0, 0)
    screen_frame_color = (0, 51, 102)

    colors = [(0, 204, 255), (0, 0, 255), (255, 0, 0), (51, 204, 51), (255, 255, 0), (255, 0, 255)]
    font = pygame.font.SysFont('consolas', 7 * title_size // 10, True)
    width, height = (number_of_tiles_x + 2) * title_size, (number_of_tiles_y + 2) * title_size
    bottom_border = pygame.Rect(0, height - title_size, width, title_size)
    top_border = pygame.Rect(0, 0, width, title_size)
    left_border = pygame.Rect(0, 0, title_size, height)
    right_border = pygame.Rect(width - title_size, 0, title_size, height)

    border_tiles = []
    floor_tiles = []
    floor_tiles_colors = {}
    score = 0
    for i in range(0, height, title_size):
        for j in range(0, width, title_size):
            if i == 0 or i == height - title_size:
                border_tiles.append(pygame.Rect(j, i, title_size, title_size))
            elif j == 0 or j == width - title_size:
                border_tiles.append(pygame.Rect(j, i, title_size, title_size))

    win = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    runnung = True
    figure = functions.CreateFigure(title_size, number_of_tiles_x, number_of_tiles_y, randint(0, 6), randint(1, 4),
                                    randint(0, 4))
    figure_tiles = functions.update_tiles(figure, title_size)
    tile_color = colors[randint(0, len(colors) - 1)]

    while runnung:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runnung = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                functions.handle_figure_movement(figure, event.key, floor_tiles, bottom_border, left_border,
                                                 right_border, title_size)
                figure_tiles = functions.update_tiles(figure, title_size)
        if functions.done_falling(figure_tiles, bottom_border, floor_tiles):
            figure.set_moving(False)
            score += 5
            for i in figure_tiles:
                floor_tiles.append(i)
                floor_tiles_colors[(i.x, i.y)] = tile_color
            tile_color = colors[randint(0, len(colors) - 1)]
            figure = functions.CreateFigure(title_size, number_of_tiles_x, number_of_tiles_y, randint(0, 6),
                                            randint(1, 4), randint(0, 6))
            figure_tiles = functions.update_tiles(figure, title_size)
            score = functions.handle_line_fill(floor_tiles, title_size, number_of_tiles_x, number_of_tiles_y,
                                               floor_tiles_colors, score)
        functions.update_window(figure_tiles, win, back_color, screen_frame_color, top_border, floor_tiles,
                                tile_color, left_border, right_border, floor_tiles_colors, font, score,
                                border_tiles, title_size)
        runnung = functions.check_end_game(floor_tiles, top_border)
        figure.move_down()
        figure_tiles = functions.update_tiles(figure, title_size)
    if functions.ending_screen(win, back_color, screen_frame_color, score, font, width, height,
                               border_tiles, title_size):
        main()


if __name__ == "__main__":
    main()
