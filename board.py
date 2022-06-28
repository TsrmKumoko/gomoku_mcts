from typing import Literal, List, Set
import warnings

class ChessBoard(object):
    '''
    Chess Board
    A gomoku board class.
    '''
    def __init__(self, size:int=15, win_len:int=5) -> None:
        '''
        Initialize a board.
        ## Parameters\n
        size: int, optional
            Size of the gomoku board. Default is 15, which is the standard size. 
            Don't passed a number greater than 15.
        win_len: int, optional
            Number of stones in a line needed to win a game. Default is 5.
        '''
        self.size = size
        self.win_len = win_len
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.moves: List[tuple] = []
        self.now_playing: Literal[1, -1] = 1
        self.winner = 0

    def is_legal(self, move:tuple) -> bool:
        '''
        Judge whether a stone can be placed at given coordinate.
        ## Parameters\n
        move: tuple
            The coordinate of move about to be judged.
        '''
        i, j = move
        is_inside = i >= 0 and i < self.size and j >= 0 and j < self.size
        is_vacancy = self.board[i][j] == 0
        return is_inside and is_vacancy

    def play_stone(self, move:tuple) -> None:
        '''
        Play a stone at the given coordinate.
        ## Parameters\n
        move: tuple
            The coordinate of move to be played.
        '''
        if not self.is_legal(move):
            warnings.warn(f'Cannot play a stone at {move}.', Warning, 3)
        else:
            self.board[move[0]][move[1]] = self.now_playing
            self.moves.append(move)
            self.now_playing = -self.now_playing
        return

    def display_board(self) -> None:
        '''
        Print all placed stone.
        '''
        if self.moves == []:
            return
        else:
            i_ticks = '  0 1 2 3 4 5 6 7 8 9 A B C D E'
            i_ticks = i_ticks[0:1+2*self.size]
            print(i_ticks)
            for j in range(self.size):
                if j < 10:
                    print(j, end='')
                else:
                    print(chr(55 + j), end='')
                for i in range(self.size):
                    print(' ', end='')
                    if self.board[i][j] > 0:
                        print('o', end='')
                    elif self.board[i][j] < 0:
                        print('x', end='')
                    else:
                        print(' ', end='')
                    if i == self.size - 1:
                        print()
        return

    def adjacent_vacancies(self) -> Set[tuple]:
        '''
        ## Returns\n
        out: Set[tuple]
        A set which contains all available moves around existed stones. \
        'Around' means the horizontal AND vertival distance between a vacancy and \
        the nearest stone is no greater than 1.
        '''
        vacancies = set()
        if self.moves != []:
            bias = range(-1, 2)
            for move in self.moves:
                for i in bias:
                    if move[0]-i < 0 or move[0]-i >= self.size:
                        continue
                    for j in bias:
                        if move[1]-j < 0 or move[1]-j >= self.size:
                            continue
                        vacancies.add((move[0]-i, move[1]-j))
            occupied = set(self.moves)
            vacancies -= occupied
        return vacancies

    def is_ended(self) -> bool:
        '''
        Judge whether the game is ended or not. The winner will be passed to `self.winner`. \
        The algorithm is not easy to understand. You can check it by traverse the `for` loop.
        ## Returns\n
        out: bool
            Return `True` if the game ended, otherwise `False`.
        '''
        if self.moves == []:
            return False
        loc_i, loc_j = self.moves[-1]
        color = -self.now_playing
        sgn_i = [1, 0, 1, 1]
        sgn_j = [0, 1, 1, -1]
        for iter in range(4):
            length = 0
            prm1 = loc_i if sgn_i[iter] == 1 else loc_j
            prm2 = loc_j if sgn_j[iter] == 1 else (loc_i if sgn_j[iter] == 0 else self.size - 1 - loc_j)
            start_bias = -min(prm1, prm2) if min(prm1, prm2) < self.win_len-1 else -self.win_len+1
            end_bias = self.size - 1 - max(prm1, prm2) if max(prm1, prm2) > self.size-self.win_len else self.win_len-1
            for k in range(start_bias, end_bias+1):
                stone = self.board[loc_i + k * sgn_i[iter]][loc_j + k * sgn_j[iter]]
                if color > 0 and stone > 0 or color < 0 and stone < 0:
                    length += 1
                else:
                    length = 0
                if length == self.win_len:
                    self.winner = 1 if color > 0 else -1
                    return True
        if len(self.moves) == self.size ** 2:
            return True
        else:
            return False
