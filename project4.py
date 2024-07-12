# project4.py
# Aizza Romo
# 84701141

import columns_logic as logic

def run () -> None:
    num_rows = int (input ())
    num_cols = int (input ())
    start_option = input ().strip ().upper ()  
    game = logic.ColumnsGame (num_rows, num_cols)
    board = game.new_board () 
    
    if start_option == 'CONTENTS':
        board = _add_contents_to_board (_ask_for_contents (num_rows), board)
    elif start_option == 'EMPTY':
        pass

    board = game.jewel_gravity (board)
    
    while game.matches_present (board): 
        board = game.jewel_gravity (board)
        board = game.identify_matches (board)
        _print_board (board, game.get_cols ())
        board = game.remove_matches (board)
    
    _print_board (board, game.get_cols ())

    while game.is_running ():
        command = input ().strip ()
        board = game.take_command (board, command)
        
        if board != None and game.matches_present (board):
            while game.matches_present (board): 
                board = game.jewel_gravity (board)
                board = game.identify_matches (board)
                _print_board (board, game.get_cols ())
                board = game.remove_matches (board)
                
        if board != None: 
            _print_board (board, game.get_cols ())
            
        try: 
            if len (game.faller_locations (board)) == 0 and game.get_count () > 0:
                print ('GAME OVER')
                game.end_game ()
                
        except TypeError:
            pass
       
def _ask_for_contents (rows: int) -> [str]:
    '''Asks the user to specify what contents to append to the board.'''
    contents = []
    for num in range (rows):
        content = list (input ())
        contents.append (content)
    return contents

def _add_contents_to_board (contents: [[str]], board: [['BoardSpot']]) -> [['BoardSpot']]:
    '''Appends a list of contents to the board.'''
    for i in range (len (board)):
        for j in range (len (board [i])):
            board [i][j].set_view (contents [i][j])
    return board

def _print_board (board: [['BoardSpot']], cols: int) -> None:
    '''Prints the board.'''
    for element in board:
        print ('|', end = '')
        for item in element:
            print (f'{item.get_view ()}', end = '') 
        print ('|', end = '')
        print ('')
    print (' ' + '-' * cols * 3 + ' ')
            
if __name__ == '__main__':
    run () 
