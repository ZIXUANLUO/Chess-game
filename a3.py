import sys

class Chezz:
    def __init__(self, init_colour, i1, i2, i3, init_board):
        self.colour = init_colour
        self.board = init_board
        self.current_index = 0
        self.i1 = i1
        self.i2 = i2
        self.i3 = i3
        # self.result = ''

    def get_all_possible(self):
        for i in range(8):
            for j in range(8):
                self.move_step(i, j)
        # print(self.result)

    def move_step(self, i, j):
        piece = self.board[(i, j)]
        if piece == ' ':
            return
        if piece[0] != self.colour:
            return

        self.try_catapult(i, j)

        if piece[1] == 'N':
            self.try_jump(i, j)
        elif piece[1] == 'B':
            self.try_oblique(i, j)
        elif piece[1] == 'R':
            self.try_straight(i, j)
        elif piece[1] == 'Q':
            self.try_straight(i, j)
            self.try_oblique(i, j)
        elif piece[1] == 'F':
            self.try_move_around(i, j, is_special=True)
        elif piece[1] == 'P':
            self.pawn_move(i, j)
        elif piece[1] == 'Z':
            self.try_move_near_around(i, j)
        elif piece[1] == 'K':
            self.try_move_around(i, j)
        elif piece[1] == 'C':
            self.try_move_near_around(i, j, is_special=True)
            self.fire_cannonball(i, j)

    def pawn_move(self, i, j):
        if self.colour == 'w':
            if (i, j + 1) in self.board and self.board[(i, j + 1)] == ' ':
                self.try_drop_piece(i, j, i, j + 1)
            if (i - 1, j + 1) in self.board and self.board[(i - 1, j + 1)][0] == 'b':
                self.try_drop_piece(i, j, i - 1, j + 1)
            if (i + 1, j + 1) in self.board and self.board[(i + 1, j + 1)][0] == 'b':
                self.try_drop_piece(i, j, i + 1, j + 1)
        else:
            if (i, j - 1) in self.board and self.board[(i, j - 1)] == ' ':
                self.try_drop_piece(i, j, i, j + 1)
            if (i - 1, j - 1) in self.board and self.board[(i - 1, j - 1)][0] == 'b':
                self.try_drop_piece(i, j, i - 1, j - 1)
            if (i + 1, j - 1) in self.board and self.board[(i + 1, j - 1)][0] == 'b':
                self.try_drop_piece(i, j, i + 1, j - 1)

    def fire_cannonball(self, i, j):
        flag = False
        temp_board = self.board.copy()
        for step_num in range(-8, 8):
            if step_num != 0:
                if (i - step_num, j - step_num) in temp_board:
                    if temp_board[(i - step_num, j - step_num)] != ' ':
                        flag = True
                        temp_board[(i - step_num, j - step_num)] = ' '
                if (i - step_num, j + step_num) in temp_board:
                    if temp_board[(i - step_num, j + step_num)] != ' ':
                        flag = True
                        temp_board[(i - step_num, j + step_num)] = ' '
        if flag:
            self.save_board(temp_board)

    def try_catapult(self, i, j):
        dire = self.catapult_in_around(i, j)
        if dire != -2:
            for num in range(2, 8):
                self.try_drop_piece(i, j, i + dire[0] * num, j + dire[1] * num, is_flung=True)

    def catapult_in_around(self, i, j):
        for i_index in range(-1, 2):
            for j_index in range(-1, 2):
                if (i + i_index, j + j_index) in self.board and self.board[
                    (i + i_index, j + j_index)] == self.colour + 'F':
                    if i_index == 0 and j_index == 0:
                        continue
                    else:
                        return i_index, j_index
        return -2

    def try_move_around(self, i, j, is_special=False):
        self.try_move_near_around(i, j, is_special)
        self.try_drop_piece(i, j, i - 1, j - 1, is_special)
        self.try_drop_piece(i, j, i - 1, j + 1, is_special)
        self.try_drop_piece(i, j, i + 1, j - 1, is_special)
        self.try_drop_piece(i, j, i + 1, j + 1, is_special)

    def try_move_near_around(self, i, j, is_special=False):
        self.try_drop_piece(i, j, i - 1, j, is_special)
        self.try_drop_piece(i, j, i + 1, j, is_special)
        self.try_drop_piece(i, j, i, j - 1, is_special)
        self.try_drop_piece(i, j, i, j + 1, is_special)

    def try_move_left_and_up(self, i, j):
        for step_num in range(1, 8):
            result = self.try_drop_piece(i, j, i - step_num, j + step_num)
            if result == 0:
                break

    def try_move_left_and_down(self, i, j):
        for step_num in range(1, 8):
            result = self.try_drop_piece(i, j, i - step_num, j - step_num)
            if result == 0:
                break

    def try_move_right_and_up(self, i, j):
        for step_num in range(1, 8):
            result = self.try_drop_piece(i, j, i + step_num, j + step_num)
            if result == 0:
                break

    def try_move_right_and_down(self, i, j):
        for step_num in range(1, 8):
            result = self.try_drop_piece(i, j, i + step_num, j - step_num)
            if result == 0:
                break

    def try_oblique(self, i, j):
        self.try_move_left_and_down(i, j)
        self.try_move_left_and_up(i, j)
        self.try_move_right_and_down(i, j)
        self.try_move_right_and_up(i, j)

    def try_move_left(self, i, j):
        for step_num in range(1, 8):
            result = self.try_drop_piece(i, j, i - step_num, j)
            if result == 0:
                break

    def try_move_right(self, i, j):
        for step_num in range(1, 8):
            result = self.try_drop_piece(i, j, i + step_num, j)
            if result == 0:
                break

    def try_move_up(self, i, j):
        for step_num in range(1, 8):
            result = self.try_drop_piece(i, j, i, j + step_num)
            if result == 0:
                break

    def try_move_down(self, i, j):
        for step_num in range(1, 8):
            result = self.try_drop_piece(i, j, i, j - step_num)
            if result == 0:
                break

    def try_straight(self, i, j):
        self.try_move_left(i, j)
        self.try_move_down(i, j)
        self.try_move_up(i, j)
        self.try_move_right(i, j)

    def try_jump(self, i, j):
        self.try_drop_piece(i, j, i - 1, j + 2)
        self.try_drop_piece(i, j, i - 1, j - 2)
        self.try_drop_piece(i, j, i + 1, j + 2)
        self.try_drop_piece(i, j, i + 1, j - 2)
        self.try_drop_piece(i, j, i - 2, j + 1)
        self.try_drop_piece(i, j, i - 2, j - 1)
        self.try_drop_piece(i, j, i + 2, j + 1)
        self.try_drop_piece(i, j, i + 2, j - 1)

    def zombies_infect(self, temp_board, i, j):
        if temp_board[(i, j)] == self.colour + 'Z':
            if self.is_op_piece(temp_board, i - 1, j):
                temp_board[(i - 1, j)] = temp_board[(i - 1, j)][0] + 'Z'
            if self.is_op_piece(temp_board, i + 1, j):
                temp_board[(i - 1, j)] = temp_board[(i + 1, j)][0] + 'Z'
            if self.is_op_piece(temp_board, i, j - 1):
                temp_board[(i - 1, j)] = temp_board[(i, j - 1)][0] + 'Z'
            if self.is_op_piece(temp_board, i, j + 1):
                temp_board[(i - 1, j)] = temp_board[(i, j + 1)][0] + 'Z'

        if temp_board[(i, j)] == self.colour + 'P':
            if self.colour == 'w' and j == 7:
                temp_board[(i, j)] = 'wZ'
            if self.colour == 'b' and j == 0:
                temp_board[(i, j)] = 'bZ'

    def is_op_piece(self, temp_board, i, j):
        if (i, j) in temp_board and temp_board[(i, j)] != ' ' and temp_board[(i, j)][0] != self.colour and \
                temp_board[(i, j)][1] != 'K' and temp_board[(i, j)][1] != 'Z':
            return True
        else:
            return False

    def try_drop_piece(self, pre_i, pre_j, after_i, after_j, is_special=False, is_flung=False):
        temp_board = self.board.copy()
        if after_i > 7 or after_i < 0 or after_j > 7 or after_j < 0:
            return 0
        if temp_board[(after_i, after_j)][0] == self.colour:
            return 0
        if temp_board[(after_i, after_j)][0] != ' ':
            if is_special:
                return 0
            result = 0
        else:
            result = 1

        if is_flung and result == 0 and temp_board[(after_i, after_j)][1] != 'K':
            temp_board[(after_i, after_j)] = ' '
            temp_board[(pre_i, pre_j)] = ' '
        else:
            temp_board[(after_i, after_j)] = temp_board[(pre_i, pre_j)]
            temp_board[(pre_i, pre_j)] = ' '

        self.zombies_infect(temp_board, after_i, after_j)
        self.save_board(temp_board)
        return result

    def save_board(self, temp_board):
        # self.result += str(temp_board) + '\n\n'

        fo = open("board." + self.get_current_index_str(), "w")
        if self.colour == 'w':
            fo.write('b ' + str(self.i1) + ' ' + str(self.i2) + ' ' + str(self.i3) + '\n{\n')
        else:
            fo.write('w ' + self.i1 + ' ' + self.i2 + ' ' + self.i3 + '\n{\n')
        for i in range(8):
            for j in range(8):
                if temp_board[(i, j)] != ' ':
                    fo.write("  " + chr(ord('a') + i) + str(1 + j) + ": '" + temp_board[(i, j)] + "',\n")
        fo.write('}')
        fo.close()
        self.current_index += 1

    def get_current_index_str(self):
        if self.current_index < 10:
            return '00%d' % self.current_index
        elif self.current_index < 100:
            return '0%d' % self.current_index
        else:
            return str(self.current_index)


# colour, i1, i2, i3 = 'w', 0, 60000, 0
# board = {(0, 0): 'wF', (0, 1): 'wP', (0, 2): ' ', (0, 3): ' ', (0, 4): ' ', (0, 5): ' ', (0, 6): 'bP', (0, 7): 'bF',
#          (1, 0): 'wN', (1, 1): 'wP', (1, 2): ' ', (1, 3): ' ', (1, 4): ' ', (1, 5): ' ', (1, 6): 'bP', (1, 7): 'bN',
#          (2, 0): 'wC', (2, 1): 'wP', (2, 2): ' ', (2, 3): ' ', (2, 4): ' ', (2, 5): ' ', (2, 6): 'bP', (2, 7): 'bC',
#          (3, 0): 'wQ', (3, 1): 'wP', (3, 2): ' ', (3, 3): ' ', (3, 4): ' ', (3, 5): ' ', (3, 6): 'bP', (3, 7): 'bQ',
#          (4, 0): 'wK', (4, 1): 'wZ', (4, 2): ' ', (4, 3): ' ', (4, 4): ' ', (4, 5): ' ', (4, 6): 'bZ', (4, 7): 'bK',
#          (5, 0): 'wB', (5, 1): 'wP', (5, 2): ' ', (5, 3): ' ', (5, 4): ' ', (5, 5): ' ', (5, 6): 'bP', (5, 7): 'bB',
#          (6, 0): 'wN', (6, 1): 'wP', (6, 2): ' ', (6, 3): ' ', (6, 4): ' ', (6, 5): ' ', (6, 6): 'bP', (6, 7): 'bN',
#          (7, 0): 'wR', (7, 1): 'wP', (7, 2): ' ', (7, 3): ' ', (7, 4): ' ', (7, 5): ' ', (7, 6): 'bP', (7, 7): 'bR'}
a8 = (0, 7)
b8 = (1, 7)
c8 = (2, 7)
d8 = (3, 7)
e8 = (4, 7)
f8 = (5, 7)
g8 = (6, 7)
h8 = (7, 7)
a7 = (0, 6)
b7 = (1, 6)
c7 = (2, 6)
d7 = (3, 6)
e7 = (4, 6)
f7 = (5, 6)
g7 = (6, 6)
h7 = (7, 6)
a6 = (0, 5)
b6 = (1, 5)
c6 = (2, 5)
d6 = (3, 5)
e6 = (4, 5)
f6 = (5, 5)
g6 = (6, 5)
h6 = (7, 5)
a5 = (0, 4)
b5 = (1, 4)
c5 = (2, 4)
d5 = (3, 4)
e5 = (4, 4)
f5 = (5, 4)
g5 = (6, 4)
h5 = (7, 4)
a4 = (0, 3)
b4 = (1, 3)
c4 = (2, 3)
d4 = (3, 3)
e4 = (4, 3)
f4 = (5, 3)
g4 = (6, 3)
h4 = (7, 3)
a3 = (0, 2)
b3 = (1, 2)
c3 = (2, 2)
d3 = (3, 2)
e3 = (4, 2)
f3 = (5, 2)
g3 = (6, 2)
h3 = (7, 2)
a2 = (0, 1)
b2 = (1, 1)
c2 = (2, 1)
d2 = (3, 1)
e2 = (4, 1)
f2 = (5, 1)
g2 = (6, 1)
h2 = (7, 1)
a1 = (0, 0)
b1 = (1, 0)
c1 = (2, 0)
d1 = (3, 0)
e1 = (4, 0)
f1 = (5, 0)
g1 = (6, 0)
h1 = (7, 0)

colour, i1, i2, i3 = sys.stdin.readline().split()
board = {(i, j): ' ' for i in range(0, 8) for j in range(0, 8)}
line = sys.stdin.read()
a = eval(line)
board.update(a)

c = Chezz(colour, i1, i2, i3, board)
c.get_all_possible()
