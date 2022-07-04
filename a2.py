EMPTY_TILE = "tile"
START_PIPE = "start"
END_PIPE = "end"
LOCKED_TILE = "locked"

TILE_ID = 'tile'
PIPE_ID = 'pipe'
SPECIAL_PIPE_ID = 'special_pipe'

SPECIAL_TILES = {
    "S": START_PIPE,
    "E": END_PIPE,
    "L": LOCKED_TILE
}

PIPES = {
    "ST": "straight",
    "CO": "corner",
    "CR": "cross",
    "JT": "junction-t",
    "DI": "diagonals",
    "OU": "over-under"
}

PIPE_CONNECTIONS = {
    "straight": {0: (2,), 1: (), 2: (0,), 3: ()},
    "corner": {0: (1,), 1: (0,), 2: (), 3: ()},
    "cross": {0: (1,2,3), 1: (0,2,3), 2: (0,1,3), 3: (0,1,2)},
    "junction-t": {0: (), 1: (2,3), 2: (1,3), 3: (1,2)},
    "diagonals": {0: (1,), 1: (0,), 2: (3,), 3: (2,)},
    "over-under": {0: (2,), 1: (3,), 2: (0,), 3: (1,)}
}

DIRECTION_NUMBERS = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
DIRECTION_LETTERS = 'NESW'

### add code here ###

class Tile(object):

    """ Representaion of a tile (available space) in the game board."""
    
    def __init__(self, name, selectable=True):
        """
        Constructs a new tile object.
        
        Parameters:
            name (str): Name of tile object. 
            selectable (bool): Whether tile is able to have pipes placed on it. 
        """
        self._name =  name
        self._selectable = selectable
        self._id = TILE_ID


    def get_name(self):
        """(str): Returns the name of the object."""
        return self._name


    def get_id(self):
        """(str): Returns the id of the class."""
        return self._id


    def set_select(self, select):
        """
        Sets the status of the select switch to True or False

        Parameters:
            select (bool): value to which the select switch should be set to. 
        """
        self._selectable = select


    def can_select(self):
        """(bool): Returns True if the tile is selectable, and false if not."""
        return self._selectable


    def __str__(self):
        """(str): Returns a string representation of a Tile object."""
        return "Tile('{0}', {1})".format(self._name, self._selectable)

    def __repr__(self):
        """(str) Same as str(self)"""
        return str(self)




class Pipe(Tile):
    
    """ A class representing a pipe in the game."""
    
    def __init__(self, name, orientation=0, selectable=True):
        """ Constructs a new pipe object.

        Parameters:
            name (str): name of pipe object (indicates type of pipe).
            orientation (int): Number of clockwise rotations from default position.
            selectable (bool): Whether the pipe is able to be rotated or
                               removed from the board.
       """
        
        super().__init__(name, selectable)
        self._orientation = orientation
        self._id = PIPE_ID


    def get_connected(self, side):
        """Determines the sides that are connceted to the given side of a Pipe.

        Parameters:
            side (str): side of pipe in which directions need to be determiend.
            
        Return:
            (list<str>): Returns a list of all sides that are connceted to the
                         given side of a specified Pipe.
        """
        
        side_number = DIRECTION_NUMBERS[side]
        connection_location = (side_number - self._orientation) % 4 
        connection_numbers = PIPE_CONNECTIONS[self._name][connection_location]
        
        connection_sides = []
        
        if len(connection_numbers) != 0:
            for numbers in connection_numbers:
                connection_sides.append(DIRECTION_LETTERS[(numbers+self._orientation) % 4])
        return connection_sides


    def rotate(self, direction):
        """ Rotates a pipe (changes a pipes orientation)

        Parameters:
            direction (int): The number of times, and direction, the pipe should
                             be rotated (+; clockwise, -; anticlockwise).
        """
        if self._selectable == True:
            self._orientation = (self._orientation + direction) % 4


    def get_orientation(self):
        """(int): Returns the orientation of the pipe (in the range [0,3])."""
        return self._orientation


    def __str__(self):
        """(str): Returns the string representation of the Pipe"""
        return "Pipe('{0}', {1})".format(self._name, self._orientation)


    def __repr__(self):
        """(str): Same as str(self)"""
        return str(self)




class SpecialPipe(Pipe):
    
    """Abstract class used to represent the start and end pipes in the game."""
    
    def __init__(self, name, orientation=0, selectable=False):
        """Constructs a special pipe.

        Parameters:
            name (str): name of the speical pipe object.
            orientation (int): Number of clockwise rotations from default position.
            selectable (bool): Whether the special pipe is avaliable to be
                               rotated or removed from the board.
        """
        super().__init__(name, orientation, selectable)
        self._id = SPECIAL_PIPE_ID

       
    def __str__(self):
        """(str): Returns a string representation of a special pipe"""
        return "SpecialPipe({0})".format(self._orientation)


    def __repr__(self):
        """(str): Same as str(self)"""
        return str(self)
        
    

class StartPipe(SpecialPipe):
    
    """Class which represents the start pipe in the game"""
    
    def __init__(self, orientation=0, selectable = False):
        """Constructs a start pipe.

        Parameters:
            orientation (int): Number of clockwise rotations from default position.
            selectable (bool): Whether the start pipe is avaliable to be rotated
                               or removed from the board.
        """
        name = START_PIPE
        super().__init__(name, orientation, selectable)
        

    def get_connected(self, side=None):
        """Determines the sides connected to the given side of a StartPipe.

        Parameters:
            side (str): side of pipe in which directions need to be determiend. 
        Return:
            (list<str>): Returns the direction that the start pipe is facing. 
        """
        connected_directions = []
        connected_directions.append(DIRECTION_LETTERS[self._orientation])
        return connected_directions

    def __str__(self):
        """(str): Returns the string representation of a start pipe"""
        return "StartPipe({0})".format(self._orientation)

    def __repr__(self):
        """(str): Same as str(self)"""
        return str(self)
    

class EndPipe(SpecialPipe):
    
    """Class which represents the end pipe in the game."""
    
    def __init__(self, orientation=0, selectable = False):
        """Constructs an end pipe.

        Parameters:
            orientation (int): Number of clockwise rotations from defult position.
            selectable (bool): Whether the end pipe is avaliable to be rotated
                               or removed from the board.
        """
        name = END_PIPE
        super().__init__(name, orientation, selectable)


    def get_connected(self, side=None):
        """Determines the sides connected to the given side of the EndPipe.

        Parameters:
            side (str): side of pipe in which directions need to be determiend.
            
        Return:
            (list<str>): Returns the opposite direction that the start pipe is facing. 
        """
        connected_directions = []
        connected_directions.append(DIRECTION_LETTERS[(self._orientation + 2) % 4])
        return connected_directions


    def __str__(self):
        """(str): Returns the string representation of an end pipe."""
        return "EndPipe({0})".format(self._orientation)


    def __repr__(self):
        """(str): Same as str(self)"""
        return str(self)


            
class PipeGame:
    """
    A game of Pipes.
    """
    
    def __init__(self, game_file='game_1.csv'):
        """
        Construct a game of Pipes from a file name.

        Parameters:
            game_file (str): name of the game file.
        """
    
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        #board_layout = [[Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        #Tile('tile', True), Tile('tile', True)], [StartPipe(1), Tile('tile', True), Tile('tile', True), \
        #Tile('tile', True), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), \
        #Tile('tile', True), Pipe('junction-t', 0, False), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), \
        #Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('locked', False), Tile('tile', True)], \
        #[Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), EndPipe(3), \
        #Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        #Tile('tile', True), Tile('tile', True)]]
        #
        #playable_pipes = {'straight': 1, 'corner': 1, 'cross': 1, 'junction-t': 1, 'diagonals': 1, 'over-under': 1}
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        
        board_info = self.load_file(game_file)
        self._playable_pipes =  board_info[0]
        self._board_layout = board_info[1]

        
        end_pipe_positions = self.end_pipe_positions()
        self._start_position = end_pipe_positions[0]
        self._end_position = end_pipe_positions[1]

                    
    def load_file(self, filename):
        """ Function which determines the playable pipes and board layout for a
        Pipe Game given a file in an appropriate format.
        
        Parameters:
            filename (str): name of file which is to be loaded into the game.
            
        Returns:
             (tuple<dict<str:int>, list<list<tile,..>):
              Values for ​playable_pipes​ and board_layout​ respectively. 
        """

        board = open(filename)
        board_layout = []
        playable_pipes = []
        row_lists=[]
        
        #converts game file into a list of lists.
        #each list is a row in the gamefile.
        for line in board:   
                board_row = line.split(',')
                board_row[-1] = board_row[-1][:-1]
                row_lists.append(board_row)


        for row_number, row in enumerate(row_lists):
            
            #Determines orieintation and type of tile from board section of the file.
            #Adds tile type with given orientation to board_layout.
            if row_number < len(row_lists) - 1:
                board_row_lists = []
                for tile in row:
                    if tile[-1].isdigit():
                        tile_type = tile[:-1]
                        orientation = int(tile[-1])

                    else:
                        tile_type = tile
                        orientation = 0

                        
                    if tile_type in PIPES:
                        board_row_lists.append(Pipe(PIPES[tile_type], orientation, False))

                    else:
                        other_tiles = {'#': Tile('tile', True),
                                        'L': Tile(LOCKED_TILE, False),
                                        'S': StartPipe(orientation),
                                        'E': EndPipe(orientation)
                                        }

                        board_row_lists.append(other_tiles[tile_type])
                board_layout.append(board_row_lists)

            #converts final row into playable pipes. 
            else:
                playable_nums = row_lists[row_number]
                playable_pipes = {'straight': int(playable_nums[0]),
                                  'corner': int(playable_nums[1]),
                                  'cross': int(playable_nums[2]),
                                  'junction-t': int(playable_nums[3]),
                                  'diagonals': int(playable_nums[4]),
                                  'over-under': int(playable_nums[5])
                                 }   
        board.close()
        return (playable_pipes, board_layout)


    def end_pipe_positions(self):
        """
        (tuple<tuple<int, int>, tuple<int, int>):
        Returns the start and end pipe positions from the game board in a tuple.
        """
        #searches each tile in the board and saves if tile is start or end pipe. 
        for row_number, rows in enumerate(self._board_layout):
            for column_number, tiles in enumerate(rows):
                if tiles._name == START_PIPE:
                    start_position = (row_number, column_number)

                elif tiles._name == END_PIPE:
                    end_position = (row_number, column_number)
        return (start_position, end_position)


    def get_board_layout(self):
        """
        (list<list<Tile,...>>): Returns a list of lists (where each element of
                        a list represents a tile within a row of the game grid).
        """
        return self._board_layout


    def get_playable_pipes(self):
        """(dict<str:int>)​: Returns a dictionary of all the playable pipe types
                            and number of times each pipe can be played.
        """
        return self._playable_pipes


    def change_playable_amount(self, pipe_name, number):
        """​Adds​ the quantity of playable pipes of type specified by pipe_name
        to number (in the selection panel).
        
        Parameters:
            pipe_name (str): name of pipe whose quanity needs altering.
            number (int): quanity which the playble pipes needs to be changed.
        """
        self._playable_pipes[pipe_name] += number


    def get_pipe(self, position):
        """ Determines the pipe/tile at the given position of the game board.

        Parameters:
            position (tuple<int, int>): row, col represenation of a tile/pipe in
                                        the game board. 
        Returns:
            The Pipe at the position or tile if there is no pipe at that position. 
        """
        return self._board_layout[position[0]][position[1]]


    def set_pipe(self, pipe, position):
        """ Place the specified pipe at the given position (row, col) in the game
        board. The number of available pipes of the relevant type is also updated.

        Parameters:
            pipe (str): pipe to be placed at the given position
            position (tuple<int, int>): position on gameboard (row, col) where
                                        pipe is to be placed. 
        """
        tile = self.get_pipe(position)
        if self._playable_pipes[pipe._name] > 0 and tile.can_select() == True \
        and tile.get_id() == TILE_ID:
            self._board_layout[position[0]][position[1]] = pipe
            self.change_playable_amount(pipe._name, -1)


    def pipe_in_position(self, position):
        """
        Parameters:
            position (tuple<int, int>): row, col represenation of a tile/pipe in
                                        the game board. 
        Returns:
            Returns the pipe in the given position (row, col) of the game board.
            Returns none if there is no pipe at the given position.
        """
        if position == None or self._board_layout[position[0]][position[1]].get_id() ==  TILE_ID:
            return None
        else:
            return self._board_layout[position[0]][position[1]]


    def remove_pipe(self, position):
        """ ​Removes the pipe at the given position from the board.

        Parameters:
            position (tuple<int, int>): position on gameboard (row, col) where
                                        pipe is to be removed. 
        """
        pipe = self.pipe_in_position(position)
        
        if pipe != None and pipe._selectable == True:
            removed_pipe = self.get_pipe(position)._name
            self.change_playable_amount(removed_pipe, 1)
            self._board_layout[position[0]][position[1]] = Tile('tile', True)


    def position_in_direction(self, direction, position):
        """Determines the direction and position (row, col) in the given direction
        from the given position. Returns none if 'neighbouring' position is not
        in the game board.
        
        Parameters:
            direction (str): direction in  which neighbouring position
                             needs to be determined.
            position (tuple<int, int>): position in which the neighbouring
                                        position needs to be determined.
                                        
        Returns:
            (tuple<int, int>): a tuple containting the direction and position
                    (row, col) in the given direction from the given position. 
        """
        
        row_length = len(self._board_layout)
        column_length = len(self._board_layout[0])

        conditions = {'N': (position[0] > 0, ('S',(position[0] - 1, position[1]))),
                      'E': (position[1] + 1 < column_length, ('W',(position[0], position[1]+1))),
                      'S': (position[0] + 1 < row_length, ('N',(position[0] + 1, position[1]))),
                      'W': (position[1] > 0, ('E',(position[0], position[1]-1)))
                      }

        if conditions[direction][0] == True:
            return conditions[direction][1]

        else:
            return None

    def get_starting_position(self):
        """
        (tuple<int, int>): Returns the position of the start pipe on the game board.
        """
        return self._start_position

    def get_ending_position(self):
        """
        (tuple<int, int>): Returns the position of the end pipe on the game board.
        """
        return self._end_position


    def check_win(self):
         """
         (bool) Returns True  if the player has won the game False otherwise.
         """
         position = self.get_starting_position()
         pipe = self.pipe_in_position(position)
         queue = [(pipe, None, position)]
         discovered = [(pipe, None)]
         while queue:
             pipe, direction, position = queue.pop()
             for direction in pipe.get_connected(direction):
               
                 if self.position_in_direction(direction, position) is None:
                     new_direction = None 
                     new_position = None
                 else:
                     new_direction, new_position = self.position_in_direction(direction, position)
                 if new_position == self.get_ending_position() and direction == self.pipe_in_position(
                         new_position).get_connected()[0]:
                    return True

                 pipe = self.pipe_in_position(new_position)
                 if pipe is None or (pipe, new_direction) in discovered:
                     continue
                 discovered.append((pipe, new_direction))
                 queue.append((pipe, new_direction, new_position))
         return False



def main():
    print("Please run gui.py instead")


if __name__ == "__main__":
    main()
