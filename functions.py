import pygame
import sys
import json
import tetrisclasses


def done_falling(figure_tiles, bottom_line, floor_tiles):
    not_moving = False
    for i in figure_tiles:
        if i.bottom == bottom_line.top:
            not_moving = True
            break
        for j in floor_tiles:
            if i.bottom == j.top and ((i.left >= j.left and i.left < j.right) or (
                    i.right <= j.right and i.right > j.left)):
                not_moving = True
                break
    return not_moving


def handle_line_fill(floor_tiles, tile_size, number_of_tiles_x, number_of_tiles_y, floor_tiles_colors, score):
    for screen_y in range(tile_size, (number_of_tiles_y + 1) * tile_size, tile_size):
        line_filled = False
        for screen_x in range(tile_size, (number_of_tiles_x + 1) * tile_size, tile_size):
            found_tile = False
            for i in floor_tiles:
                if i.x == screen_x and i.y == screen_y:
                    found_tile = True
                    break
            if not found_tile:
                line_filled = False
                break
            line_filled = True
        if line_filled:
            score += 10
            floor_tiles_copy = floor_tiles.copy()
            for i in floor_tiles_copy:
                if i.y == screen_y:
                    floor_tiles.remove(i)
                if i.y < screen_y:
                    color = floor_tiles_colors[(i.x, i.y)]
                    i.y += tile_size
                    floor_tiles_colors[(i.x, i.y)] = color
    return score


def handle_figure_movement(figure, key_pressed, tiles_on_the_floor, bottom_border, left_border, right_border,
                           tile_size):
    collision_right = False
    collision_left = False
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_DOWN]:
        figure.move_faster = True
    else:
        figure.move_faster = False
    figure_tiles = update_tiles(figure, tile_size)
    for tile in figure_tiles:
        for tile_on_the_floor in tiles_on_the_floor:
            if tile_on_the_floor.right == tile.left and (
                    (tile.top >= tile_on_the_floor.top and tile.top < tile_on_the_floor.bottom) or (
                    tile.bottom > tile_on_the_floor.top and tile.bottom <= tile_on_the_floor.bottom)):
                collision_left = True
            if tile_on_the_floor.left == tile.right and (
                    (tile.top >= tile_on_the_floor.top and tile.top < tile_on_the_floor.bottom) or (
                    tile.bottom > tile_on_the_floor.top and tile.bottom <= tile_on_the_floor.bottom)):
                collision_right = True
    if key_pressed == pygame.K_LEFT and not collision_left:
        pop_sound_func()
        figure.move_left()
    if key_pressed == pygame.K_RIGHT and not collision_right:
        pop_sound_func()
        figure.move_right()
    if key_pressed == pygame.K_SPACE:
        pop_sound_func()
        figure.set_position(figure_tiles[0].x, figure_tiles[0].y)
        figure_tiles = update_tiles(figure, tile_size)
        for tile in figure_tiles:
            collision = False
            for tile_on_the_floor in tiles_on_the_floor:
                if pygame.Rect.colliderect(tile, tile_on_the_floor):
                    collision = True
                    figure.undo_rotation()
                    break
            if pygame.Rect.colliderect(tile, bottom_border) \
                    or pygame.Rect.colliderect(tile, left_border) \
                    or pygame.Rect.colliderect(tile, right_border):
                collision = True
                figure.undo_rotation()
            if collision:
                break


def check_end_game(tiles_on_the_floor, top_line):
    running = True
    for i in tiles_on_the_floor:
        if top_line.bottom > i.top:
            running = False
    return running


def ending_screen(win, background_color, screen_frame_color, score, font, width, height, border_tiles, tile_size):
    running = True
    again = False
    game_over_font = pygame.font.SysFont('consolas', 13 * tile_size // 10, True)
    again_font = pygame.font.SysFont('consolas', tile_size // 3, True)
    score_text = font.render(f'Вы набрали {str(score)} очков', 1, (255, 0, 0))
    again_text = again_font.render("Играть снова (Space)    Закрыть (Escape)", 1, (255, 0, 0))
    game_over_text = game_over_font.render("Игра окончена!", 1, (255, 0, 0))

    outfile = open('highscore.json')
    highscore = json.load(outfile)

    highscore_dictionary = json.loads(highscore)

    if highscore_dictionary['highscore'] < score:
        highscore_dictionary['highscore'] = score
        highscore = json.dumps(highscore_dictionary)
        save_res = open('highscore.json', 'w')
        json.dump(highscore, save_res)
    highscore_text = again_font.render(f" Рекорд: {str(highscore_dictionary['highscore'])} очков", 1, (255, 0, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    again = True
                    running = False

        win.fill(background_color)
        for i in border_tiles:
            pygame.draw.rect(win, screen_frame_color, i, border_radius=tile_size // 10)
            pygame.draw.rect(win, (255, 255, 255), i, border_radius=tile_size // 10, width=1)
        win.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2))
        win.blit(highscore_text, (width // 2 - highscore_text.get_width() // 2, height // 2 + height // 8))
        win.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))
        win.blit(again_text, (width // 2 - again_text.get_width() // 2, height // 2 + height // 4))
        pygame.display.update()
    return again


def update_window(figure_tiles, win, background_color, screen_frame_color, top_border, tiles_on_the_floor, color,
                  left_border, right_border, floor_tiles_colors, font, score, border_tiles, tile_size):
    win.fill(background_color)
    for i in figure_tiles:
        pygame.draw.rect(win, color, i, border_radius=tile_size // 10)
        pygame.draw.rect(win, (255, 255, 255), i, border_radius=tile_size // 10, width=1)
    for i in tiles_on_the_floor:
        pygame.draw.rect(win, floor_tiles_colors[(i.x, i.y)], i, border_radius=tile_size // 10)
        pygame.draw.rect(win, (255, 255, 255), i, border_radius=tile_size // 10, width=1)
    for i in border_tiles:
        pygame.draw.rect(win, screen_frame_color, i, border_radius=tile_size // 10)
        pygame.draw.rect(win, (255, 255, 255), i, border_radius=tile_size // 10, width=1)
    score_text = font.render("Очки: " + str(score), 1, (255, 0, 0))
    win.blit(score_text, (right_border.right - score_text.get_width() - 10, (top_border.bottom - top_border.top) // 4))
    pygame.display.update()


def CreateFigure(tile_size, number_of_tiles_x, number_of_tiles_y, shape, rotate_pos, figure_num):
    if figure_num == 0:
        figure = tetrisclasses.Figure1(tile_size, number_of_tiles_x, number_of_tiles_y, shape, rotate_pos)
    elif figure_num == 1:
        figure = tetrisclasses.Figure2(tile_size, number_of_tiles_x, number_of_tiles_y, shape, rotate_pos)
    elif figure_num == 2:
        figure = tetrisclasses.Figure3(tile_size, number_of_tiles_x, number_of_tiles_y, shape, rotate_pos)
    elif figure_num == 3:
        figure = tetrisclasses.Figure4(tile_size, number_of_tiles_x, number_of_tiles_y, shape, rotate_pos)
    elif figure_num == 4:
        figure = tetrisclasses.Figure5(tile_size, number_of_tiles_x, number_of_tiles_y, shape, rotate_pos)
    elif figure_num == 5:
        figure = tetrisclasses.Figure6(tile_size, number_of_tiles_x, number_of_tiles_y, shape, rotate_pos)
    elif figure_num == 6:
        figure = tetrisclasses.Figure7(tile_size, number_of_tiles_x, number_of_tiles_y, shape, rotate_pos)
    figure.set_position(figure.get_first_tile_x(), figure.get_first_tile_y())
    return figure


def update_tiles(figure, tile_size):
    figure_tiles = figure.get_tiles()
    rect1 = pygame.Rect(figure_tiles[0][0], figure_tiles[0][1], tile_size, tile_size)
    rect2 = pygame.Rect(figure_tiles[1][0], figure_tiles[1][1], tile_size, tile_size)
    rect3 = pygame.Rect(figure_tiles[2][0], figure_tiles[2][1], tile_size, tile_size)
    rect4 = pygame.Rect(figure_tiles[3][0], figure_tiles[3][1], tile_size, tile_size)
    return (rect1, rect2, rect3, rect4)


def pop_sound_func():
    pygame.mixer.init()
    pop_sound = pygame.mixer.Sound('pop.ogg')
    pop_sound.play()
