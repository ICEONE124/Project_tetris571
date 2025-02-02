class Figures:
    def __init__(self, tile_size, number_of_tiles_x, number_of_tiles_y, shape, rotate_position):
        self.number_of_tiles_x = number_of_tiles_x
        self.number_of_tiles_y = number_of_tiles_y
        self.tile_size = tile_size
        self.window_width, self.window_height = (number_of_tiles_x + 2) * tile_size, (number_of_tiles_y + 2) * tile_size
        self.shape = shape
        self.first_tile_x = self.tile_size * self.number_of_tiles_x / 2
        self.first_tile_y = 0
        self.moving = True
        self.delay_move = 0
        self.rotate_position = rotate_position
        self.move_faster = False

    def undo_rotation(self):
        self.rotate_position = self.previous_rotate_position
        self.set_position(self.previous_tiles[0][0], self.previous_tiles[0][1])

    def move_down(self):
        if self.move_faster is True and self.moving and (self.delay_move == 7 or self.delay_move == 3):
            for tile in self.tiles:
                tile[1] += self.tile_size
        elif self.moving and self.delay_move == 7:
            for tile in self.tiles:
                tile[1] += self.tile_size
        self.delay_move += 1
        if self.delay_move == 8:
            self.delay_move = 0

    def move_right(self):
        can_move = True
        for tile in self.tiles:
            if tile[0] + self.tile_size >= self.window_width - self.tile_size:
                can_move = False
        if can_move:
            for tile in self.tiles:
                tile[0] += self.tile_size
        return self.tiles

    def move_left(self):
        can_move = True
        for tile in self.tiles:
            if tile[0] <= self.tile_size:
                can_move = False
        if can_move:
            for tile in self.tiles:
                tile[0] -= self.tile_size
        return self.tiles

    def get_tiles(self):
        return self.tiles

    def get_shape(self):
        return self.shape

    def set_moving(self, moving):
        self.moving = moving

    def get_rotate_postion(self):
        return self.rotate_position

    def get_first_tile_x(self):
        return self.first_tile_x

    def get_first_tile_y(self):
        return self.first_tile_y


class Figure1(Figures):
    def set_position(self, x, y):
        if self.rotate_position == 1:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 4
            rect1 = [x, y]
            rect2 = [x - self.tile_size, y + self.tile_size]
            rect3 = [x - self.tile_size, y]
            rect4 = [x + self.tile_size, y]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 2
            return self.tiles
        elif self.rotate_position == 2:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 1
            rect1 = [x, y]
            rect2 = [x, y - self.tile_size]
            rect3 = [x, y + self.tile_size]
            rect4 = [x + self.tile_size, y + self.tile_size]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 3
            return self.tiles
        elif self.rotate_position == 3:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 2
            rect1 = [x, y]
            rect2 = [x - self.tile_size, y]
            rect3 = [x + self.tile_size, y]
            rect4 = [x + self.tile_size, y - self.tile_size]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 4
            return self.tiles
        elif self.rotate_position == 4:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 3
            rect1 = [x, y]
            rect2 = [x, y - self.tile_size]
            rect3 = [x - self.tile_size, y - self.tile_size]
            rect4 = [x, y + self.tile_size]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 1
            return self.tiles


class Figure2(Figures):
    def set_position(self, x, y):
        rect1 = [x, y]
        rect2 = [x, y + self.tile_size]
        rect3 = [x + self.tile_size, y + self.tile_size]
        rect4 = [x + self.tile_size, y]
        self.tiles = [rect1, rect2, rect3, rect4]


class Figure3(Figures):
    def set_position(self, x, y):
        if self.rotate_position == 1:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 4
            rect1 = [x, y]
            rect2 = [x + self.tile_size, y - self.tile_size]
            rect3 = [x, y - self.tile_size]
            rect4 = [x, y + self.tile_size]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 2
        elif self.rotate_position == 2:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 1
            rect1 = [x, y]
            rect2 = [x - self.tile_size, y]
            rect3 = [x - self.tile_size, y - self.tile_size]
            rect4 = [x + self.tile_size, y]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 3
        elif self.rotate_position == 3:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 2
            rect1 = [x, y]
            rect2 = [x, y + self.tile_size]
            rect3 = [x, y - self.tile_size]
            rect4 = [x - self.tile_size, y + self.tile_size]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 4
        elif self.rotate_position == 4:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 3
            rect1 = [x, y]
            rect2 = [x - self.tile_size, y]
            rect3 = [x + self.tile_size, y]
            rect4 = [x + self.tile_size, y + self.tile_size]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 1


class Figure4(Figures):
    def set_position(self, x, y):
        if self.rotate_position == 1 or self.rotate_position == 3:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 2
            rect1 = [x, y]
            rect2 = [x - self.tile_size, y]
            rect3 = [x + self.tile_size, y]
            rect4 = [x + 2 * self.tile_size, y]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 2
        elif self.rotate_position == 2 or self.rotate_position == 4:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 1
            rect1 = [x, y]
            rect2 = [x, y - self.tile_size]
            rect3 = [x, y + self.tile_size]
            rect4 = [x, y + 2 * self.tile_size]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 1


class Figure5(Figures):
    def set_position(self, x, y):
        if self.rotate_position == 1 or self.rotate_position == 3:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 2
            rect1 = [x, y]
            rect2 = [x - self.tile_size, y]
            rect3 = [x, y + self.tile_size]
            rect4 = [x + self.tile_size, y + self.tile_size]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 2
        elif self.rotate_position == 2 or self.rotate_position == 4:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 1
            rect1 = [x, y]
            rect2 = [x, y + self.tile_size]
            rect3 = [x + self.tile_size, y - self.tile_size]
            rect4 = [x + self.tile_size, y]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 1


class Figure6(Figures):
    def set_position(self, x, y):
        if self.rotate_position == 1:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 4
            rect1 = [x, y]
            rect2 = [x, y - self.tile_size]
            rect3 = [x - self.tile_size, y]
            rect4 = [x + self.tile_size, y]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 2
        elif self.rotate_position == 2:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 1
            rect1 = [x, y]
            rect2 = [x, y + self.tile_size]
            rect3 = [x, y - self.tile_size]
            rect4 = [x - self.tile_size, y]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 3
        elif self.rotate_position == 3:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 2
            rect1 = [x, y]
            rect2 = [x, y + self.tile_size]
            rect3 = [x + self.tile_size, y]
            rect4 = [x - self.tile_size, y]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 4
        elif self.rotate_position == 4:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 3
            rect1 = [x, y]
            rect2 = [x, y - self.tile_size]
            rect3 = [x, y + self.tile_size]
            rect4 = [x + self.tile_size, y]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 1


class Figure7(Figures):
    def set_position(self, x, y):
        if self.rotate_position == 1 or self.rotate_position == 3:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 2
            rect1 = [x, y]
            rect2 = [x + self.tile_size, y]
            rect3 = [x, y + self.tile_size]
            rect4 = [x - self.tile_size, y + self.tile_size]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 2
        elif self.rotate_position == 2 or self.rotate_position == 4:
            if not y == self.first_tile_y:
                self.previous_tiles = self.tiles.copy()
                self.previous_rotate_position = 1
            rect1 = [x, y]
            rect2 = [x, y - self.tile_size]
            rect3 = [x + self.tile_size, y]
            rect4 = [x + self.tile_size, y + self.tile_size]
            self.tiles = [rect1, rect2, rect3, rect4]
            self.rotate_position = 1
