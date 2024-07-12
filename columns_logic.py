# columns_logic.py
# Aizza Romo
# 84701141

NONE = '   '

FROZEN = 'FR'
MOVING = 'M'
MATCH = '*'
LANDED = 'L'

BOARD_PIECE = 'BP'
FALLER = 'F'

HORIZONAL = 'H'
VERTICAL = 'V'

class ColumnsGame ():
    def __init__ (self, rows, cols) -> None:
        self._running = True
        self._rows = rows
        self._cols = cols
        self._faller = None
        self._faller_column = 0
        self._count = 3
        self._already_landed = False
        
    def new_board (self) -> [['BoardSpot']]:
        '''Creates an empty board.'''
        empty_board = []
        for i in range (self._rows):
            empty_board.append ([])
            for j in range (self._cols):
                empty_board [-1].append (BoardSpot (i, j))
        return empty_board

    def set_count (self, n) -> None:
        '''Sets the count value.'''
        self._count = n
        
    def get_count (self) -> int:
        '''Returns the count.'''
        return self._count

    def get_cols (self) -> int:
        '''Returns the number of columns in the board.'''
        return self._cols

    def get_rows (self) -> int:
        '''Returns the number of rows in the board.'''
        return self._rows

    def set_faller (self, n: str) -> None:
        '''Sets the current faller and starting column.'''
        faller = []
        faller_colors = list (n[3:])
        col_num = int (n [2]) - 1
            
        for color in faller_colors: 
            if color != ' ': 
                faller.append (color)
                    
        self._faller = faller
        self._faller_column = col_num
            
    def is_running (self) -> bool:
        '''Returns False if the game is over. True otherwise.'''
        if self._running:
            return True
        else:
            return False

    def end_game (self):
        '''Ends the game.'''
        self._running = False
        
    def has_landed (self, board: [['BoardSpot']]) -> bool:
        '''Determines if the faller has landed.'''
        landed = False
        try: 
            for location in self.faller_locations (board):
                r = location [0]
                c = location [1]
                if board [r + 1][c].get_type () == BOARD_PIECE and board [r + 1][c].get_view () != NONE:
                    landed = True
                elif board [r][c].get_row () == self._rows - 1:
                    landed = True
        except IndexError:
            landed = True
        return landed 
        
    def jewel_gravity (self, board: [['BoardSpot']]) -> [['BoardSpot']]:
        '''Brings the jewels down when there are empty spaces below them.'''
        while self._empty_spaces_filled (board) == False: 
            count = -1
            while count != (-self._rows):
                for i in range (self._cols):
                    if board [count][i].get_view () == '   ' and board [count - 1][i].get_view () != '   ':
                        board [count][i].set_view (board [count - 1][i].get_view ())
                        board [count - 1][i].set_view (NONE)
                count -= 1
        return board
    
    def _empty_spaces_filled (self, board: [['BoardSpot']]) -> [['BoardSpot']]:
        '''Checks if there are empty spaces below a jewel in the board.'''
        all_fallen = True
        count = -1
        while count != (-self._rows): 
            for i in range (self._cols):
                if board [count][i].get_view () == '   ' and board [count - 1][i].get_view () != '   ':
                    all_fallen = False
            count -= 1
        return all_fallen

    def take_command (self, board: [['BoardSpot']], command: str) -> [['BoardSpot']]:
        '''Receives an input and performs a specific action on the board.'''
        if command [:1] == 'F':
            if self._faller == None:
                try: 
                    self.set_faller (command)
                    self.set_count (3)
                    board = self.add_faller (board)
                    if self.has_landed (board):
                        board = self._make_landed (board)
                except IndexError:
                    self.set_count (0)
                    self._faller = None
        elif command == 'R':
            if self._faller != None: 
                board = self.rotate_faller (board)
        elif command == '':
            if self._faller != None:
                board = self.move_down (board)
        elif command == '>':
            if self._faller != None:
                board = self.move_right (board)
        elif command == '<':
            if self._faller != None:
                board = self.move_left (board)
        elif command == 'Q':
            self.end_game ()
            board = None
            
        return board

    def add_faller (self, board: [['BoardSpot']]) -> [['BoardSpot']]:
        '''Adds a piece of the faller to the board.'''
        self._count -= 1 
        board [0][self._faller_column].set_state (MOVING)
        board [0][self._faller_column].set_view (self._faller [self._count])
        board [0][self._faller_column].set_type (FALLER)
        return board
    
    def remove_matches (self, board: [['BoardSpot']]) -> [['BoardSpot']]:
        '''Removes matches from the board.'''
        for i in range (len (board)):
            for j in range (len (board [i])):
                if board[i][j].get_state () == MATCH:
                    board [i][j].set_state (FROZEN)
                    board[i][j].set_view (NONE)
        return self.jewel_gravity (board)
    
    def move_down (self, board: [['BoardSpot']]) -> [['BoardSpot']]:
        '''Moves the faller down.'''
        if not self.has_landed (board): 
            for location in reversed (self.faller_locations (board)):
                r = location [0]
                c = location [1]
                board [r + 1][c].set_state (MOVING) 
                board [r + 1][c].set_view (board [r][c].get_view ())
                board [r + 1][c].set_type (FALLER)
                board [r][c].set_state (FROZEN)
                board [r][c].set_view (NONE)
                board [r][c].set_type (BOARD_PIECE)
            if self._count > 0:
                board = self.add_faller (board)
                
            if self.has_landed (board):
                board = self._make_landed (board)
                
        elif self.has_landed (board) and self.already_landed (board):
            for location in self.faller_locations (board):
                r = location [0]
                c = location [1]
                if board [r][c].get_type () == FALLER:
                    board [r][c].set_state (FROZEN)
                    board [r][c].set_view (board [r][c].get_view ())
                    board [r][c].set_type (BOARD_PIECE)

        if len (self.faller_locations (board)) == 0:
                self._faller = None
                self._count == 0

        return board

    def already_landed (self, board: [['BoardSpot']]) -> bool:
        '''Determines if the faller has already landed.'''
        already = False
        for location in self.faller_locations (board):
            r = location [0]
            c = location [1]
            if board [r][c].get_state () == LANDED:
                already = True 
            else:
                already = False
            
        return already 
            
    def _make_landed (self, board: [['BoardSpot']]) -> [['BoardSpot']]:
        '''Changes all the fallers in the board to a 'LANDED' state.'''
        for location in self.faller_locations (board):
            r = location [0]
            c = location [1]
            board [r][c].set_state (LANDED)
            board [r][c].set_view (board [r][c].get_view ())
            
        return board

    def move_right (self, board: [['BoardSpot']]) -> [['BoardSpot']]:
        '''Moves the faller right.'''
        if self.can_move (board, 1):
            for location in self.faller_locations (board): 
                r = location [0]
                c = location [1]
                board [r][c + 1].set_type (FALLER)
                board [r][c + 1].set_state (MOVING)
                board [r][c + 1].set_view (board [r][c].get_view ())
                board [r][c].set_type (BOARD_PIECE)
                board [r][c].set_state (FROZEN)
                board [r][c].set_view (NONE)
            self._faller_column += 1
        if self.has_landed (board):
            board = self._make_landed (board)
        else:
            pass
        
        return board

    def move_left (self, board: [['BoardSpot']]) -> [['BoardSpot']]:
        '''Moves the faller left.'''
        if self.can_move (board, -1):
            for location in self.faller_locations (board):
                r = location [0]
                c = location [1]
                board [r][c - 1].set_type (FALLER)
                board [r][c - 1].set_state (MOVING)
                board [r][c - 1].set_view (board [r][c].get_view ())
                board [r][c].set_type (BOARD_PIECE)
                board [r][c].set_state (FROZEN)
                board [r][c].set_view (NONE)
            self._faller_column -= 1
            
        if self.has_landed (board):
            board = self._make_landed (board)
        else:
            pass
        return board
    
    def rotate_faller (self, board: [['BoardSpot']]) -> [['BoardSpot']]:
        '''Rotates the faller.'''
        self._faller = self._flip_faller ()
        if self._count > 0:
            count = 3 - self._count
            for location in reversed (self.faller_locations (board)):
                r = location [0]
                c = location [1]
                board [r][c].set_view (self._faller [-count])
                count -= 1
        else:
            count = 2 
            for location in reversed (self.faller_locations (board)): 
                r = location [0]
                c = location [1]
                board [r][c].set_view (self._faller [count])
                count -= 1
        return board

    def identify_matches (self, board: [['BoardSpot']]) -> [['BoardSpot']]:
        '''Identifies horizontal and vertical matches in the board.'''
        horizontal = self._horizontal_matches (board)
        vertical = self._vertical_matches (board)
        for i in range (len (horizontal)):
            for j in range (len (horizontal [i])):
                start = horizontal [i][j][0]
                count = horizontal [i][j][1] + 1
                num = 0 
                while num < count:
                    board [i][start + num].set_state (MATCH)
                    board [i][start + num].set_view (board [i][start + num].get_view ())
                    num += 1

        for l in range (len (vertical)):
            for k in range (len (vertical [l])):
                start = vertical [l][k][0]
                count = vertical [l][k][1] + 1
                num = 0
                while num < count:
                    board [start + num][l].set_state (MATCH)
                    board [start + num][l].set_view (board [start + num][l].get_view ())
                    num += 1
        return board

    def _horizontal_matches (self, board: [['BoardSpot']]) -> [[(int, int)]]:
        '''Returns a 2-Dimensional list of tuples describing the locations of horizontal matches in the board.'''
        matches = []
        count = 0
        for r in range (self._rows):
            matches.append ([])
            count = 0
            for c in range (self._cols):
                if board [r][c].get_view () != NONE:
                    try:
                        if board [r][c].get_state () == FROZEN: 
                            if board [r][c].get_view () == board [r][c + 1].get_view ():
                                count += 1
                            else:
                                if count >= 2:
                                    if c - count < 0:
                                        start = 0
                                        matches [r].append ((start, count))
                                    else:
                                        start = c - count
                                        matches [r].append ((start, count))
                                count = 0
                            
                    except IndexError:
                        if count >= 2:
                            if c - count < 0:
                                start = 0
                                matches [r].append ((start, count))
                            else:
                                start = c - count
                                matches [r].append ((start, count))
        return matches

    def _vertical_matches (self, board: [['BoardSpot']]) -> [[(int, int)]]:
        '''Returns a 2-Dimensional list of tuples describing the locations of vertical matches in the board.'''
        matches = []
        count = 0
        for c in range (self._cols):
            matches.append ([])
            count = 0
            for r in range (self._rows):
                if board [r][c].get_view () != NONE:
                    try:
                        if board [r][c].get_state () == FROZEN:
                            if board [r][c].get_view () == board [r + 1][c].get_view ():
                                count += 1
                            else:
                                if count >= 2:
                                    if r - count < 0:
                                        start = 0
                                        matches [c].append ((start, count))
                                    else:
                                        start = r - count
                                        matches [c].append ((start, count))
                                count = 0
                    except IndexError:
                        if count >= 2:
                            if r - count < 0:
                                start = 0
                                matches [c].append ((start, count))
                            else:
                                start = r - count
                                matches [c].append ((start, count))
        return matches

    def matches_present (self, board: [['BoardSpot']]) -> [['BoardSpot']]:
        '''Determines if there are vertical and/or horizontal matches in the board.'''
        all_horizontal_matches = []
        all_vertical_matches = []
        for horizontal in self._horizontal_matches (board):
            for match in horizontal:
                all_horizontal_matches.append (match)

        for vertical in self._vertical_matches (board):
            for match in vertical:
                all_vertical_matches.append (match)

        if len (all_vertical_matches) == 0 and len (all_horizontal_matches) == 0:
            return False
        else:
            return True
    
    def _flip_faller (self) -> None:
        '''Reverses the faller.'''
        rotated_faller = []
        temp_faller = self._faller [-1]
        remaining_fallers = self._faller [:2]
        for color in remaining_fallers:
            rotated_faller.append (color)
        rotated_faller.insert (0, temp_faller)
        return rotated_faller 
            
    def faller_locations (self, board: [['BoardSpot']]) -> (int, int):
        '''Returns a list of (r, c) tuples representing the locations of all the fallers in the board.'''
        locations = []
        for i in range (self._rows):
            for j in range (self._cols):
                if board [i][j].get_type () == FALLER:
                    locations.append ((i, j))
        return locations
    
    def can_move (self, board: [['BoardSpot']] , direction: int) -> bool:
        '''Determines if the faller is able to move in the given direction.'''
        movable = False
        try:
            for location in self.faller_locations (board):
                r = location [0]
                c = location [1]
                if board [r][c + direction].get_view () == NONE: 
                    movable = True
                elif board [r][c + direction].get_view () != NONE:
                    movable = False
            if self._faller_column + direction < 0:
                movable = False
        except IndexError:
            movable = False
        return movable

class BoardSpot ():
    def __init__ (self, row, col) -> None:
        self._row = row
        self._col = col
        self._state = FROZEN
        self._view = '   '
        self._type = BOARD_PIECE

    def get_row (self) -> int:
        '''Returns the row value of the BoardSpot.'''
        return self._row

    def get_col (self) -> int:
        '''Returns the column value of the BoardSpot.'''
        return self._col

    def get_view (self) -> str:
        '''Returns a string representing the view of the BoardSpot.'''
        return self._view

    def set_view (self, n: str) -> None:
        '''Sets the BoardSpot's view.'''
        if len (n) >= 3:
                length = len (n) // 2
                n = n[length]
                
        if self._state == MATCH: 
            self._view = f'*{n}*'
        elif self._state == MOVING:
            self._view = f'[{n}]'
        elif self._state == LANDED:
            self._view = f'|{n}|'
        elif self._state == FROZEN:
            self._view = f' {n} '
            
    def set_state (self, n: str) -> None:
        '''Sets the state of the BoardSpot.'''
        self._state = n

    def get_state (self) -> str:
        '''Returns a string representing the state of the BoardSpot.'''
        return self._state

    def get_type (self) -> str:
        '''Returns a string representing the type of the BoardSpot.'''
        return self._type

    def set_type (self, n) -> None:
        '''Sets the type of the BoardSpot.'''
        self._type = n
