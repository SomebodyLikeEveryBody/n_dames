BOARD_SIZE = 8
BLOCKED_CHAR = 'X'
DAME_CHAR = 'P'
EMPTY_CHAR = '0'

class Board:
    def __init__(self, p_size):
        self.size = p_size
        self.board_array = self.generate_board_array(p_size)
        self.placed_dames_coords = []

    def generate_board_array(self, p_size):
        ret_arr = []
        for i in range(0, p_size):
            ret_arr.append([])
            for j in range(0, p_size):
                ret_arr[i].append(EMPTY_CHAR)

        return ret_arr

    def print(self):
        print('')
        for line in self.board_array:
            for cell in line:
                print(cell, end=' ')
            print('')
        print('')

    def get_content_of(self, *p_coords):
        x_coord, y_coord = p_coords
        if (0 <= x_coord < self.size) and (0 <= y_coord < self.size):
            return (self.board_array[y_coord][x_coord])

    def set_content_of(self, p_content, *p_coords):
        x_coord, y_coord = p_coords
        if (0 <= x_coord < self.size) and (0 <= y_coord < self.size):
            self.board_array[y_coord][x_coord] = p_content

    def is_cell_approachable(self, *p_coords):
        return (self.get_content_of(p_coords[0], p_coords[1]) == EMPTY_CHAR)

    def fill_vertical_of(self, p_char, *p_coords):
        x_coord, y_coord = p_coords
        for y in [el for el in range(0, self.size) if el != y_coord]:
            self.set_content_of(p_char, x_coord, y)

    def fill_horizontal_of(self, p_char, *p_coords):
        x_coord, y_coord = p_coords
        for x in [el for el in range(0, self.size) if el != x_coord]:
            self.set_content_of(p_char, x, y_coord)

    def fill_diagonals_of(self, p_char, *p_coords):
        x_coord, y_coord = p_coords
        #block diagonal down_right
        count = 1
        while (x_coord + count < self.size and y_coord + count < self.size):
            self.set_content_of(p_char, x_coord + count, y_coord + count)
            count += 1

        #block diagonal up_right
        count = 1
        while (x_coord + count < self.size and y_coord - count >= 0):
            self.set_content_of(p_char, x_coord + count, y_coord - count)
            count += 1

        #block diagonal down_left
        count = 1
        while (x_coord - count >= 0 and y_coord + count < self.size):
            self.set_content_of(p_char, x_coord - count, y_coord + count)
            count += 1

        #block diagonal up_left
        count = 1
        while (x_coord - count >= 0 and y_coord - count >= 0):
            self.set_content_of(p_char, x_coord - count, y_coord - count)
            count += 1

    def block_vertical_of(self, *p_coords):
        x_coord, y_coord = p_coords
        self.fill_vertical_of(BLOCKED_CHAR, x_coord, y_coord)
            
    def block_horizontal_of(self, *p_coords):
        x_coord, y_coord = p_coords
        self.fill_horizontal_of(BLOCKED_CHAR, x_coord, y_coord)

    def block_diagonals_of(self, *p_coords):
        x_coord, y_coord = p_coords
        self.fill_diagonals_of(BLOCKED_CHAR, x_coord, y_coord)

    def block_cells(self, *p_coords):
        x_coord, y_coord = p_coords
        self.block_horizontal_of(x_coord, y_coord)
        self.block_vertical_of(x_coord, y_coord)
        self.block_diagonals_of(x_coord, y_coord)

    def free_vertical_of(self, *p_coords):
        x_coord, y_coord = p_coords
        self.fill_vertical_of(EMPTY_CHAR, x_coord, y_coord)
            
    def free_horizontal_of(self, *p_coords):
        x_coord, y_coord = p_coords
        self.fill_horizontal_of(EMPTY_CHAR, x_coord, y_coord)

    def free_diagonals_of(self, *p_coords):
        x_coord, y_coord = p_coords
        self.fill_diagonals_of(EMPTY_CHAR, x_coord, y_coord)

    def free_cells(self, *p_coords):
        x_coord, y_coord = p_coords
        self.free_horizontal_of(x_coord, y_coord)
        self.free_vertical_of(x_coord, y_coord)
        self.free_diagonals_of(x_coord, y_coord)

    def place_dame(self, *p_coords):
        x_coord, y_coord = p_coords
        if (self.is_cell_approachable(x_coord, y_coord)):
            self.placed_dames_coords.append((x_coord, y_coord))
            self.set_content_of(DAME_CHAR, x_coord, y_coord)
            self.block_cells(x_coord, y_coord)
        else:
            print('ACCESS DENIED')

    def remove_dame(self, *p_coords):
        x_coord, y_coord = p_coords
        if (self.get_content_of(x_coord, y_coord) == DAME_CHAR):
            self.placed_dames_coords.remove((x_coord, y_coord))
            self.set_content_of(EMPTY_CHAR, x_coord, y_coord)
            self.free_cells(x_coord, y_coord)
            for x, y in self.placed_dames_coords:
                self.block_cells(x, y)

    def solve(self):
        ret_solvelist = []
        current_config = []

        temp_x = 0
        temp_y = 0
        while True:
            while temp_x < self.size:
                if (self.is_cell_approachable(temp_x, temp_y)):
                    self.place_dame(temp_x, temp_y)
                    current_config.append((temp_x, temp_y))
                    temp_x = 0
                    temp_y += 1
                else:
                    temp_x += 1

            print('Trying config : ' + str(current_config))
            if len(current_config) == self.size:
                ret_solvelist.append(current_config.copy())
                print('--> Working config !\n')

            if not current_config:
                break

            a, temp_y = current_config.pop()
            self.remove_dame(a, temp_y)
            temp_x = a + 1

        return ret_solvelist

if __name__ == "__main__":
    board = Board(BOARD_SIZE)
    l = board.solve()

    print('\nSolve done ! \nRésults: \n')
    for el in l:
        print(el)
