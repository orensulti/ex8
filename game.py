############################################
# FILE: game.py
# WRITER: OREN SULTAN, orens, 201557972
# EXERCISE: intro2cs ex8 2015-2016
# DESCRIPTION: Implementation of class Game methods
############################################


############################################################
# Imports
############################################################
import game_helper as gh


# definitions of constants:

TURNS_TO_KEEP_BOMB = 3

GAME_STATUS_ONGOING = 0
GAME_STATUS_ENDED = 1

############################################################
# Class definition
############################################################


class Game:
    """
    A class representing a battleship game.
    A game is composed of ships that are moving on a square board and a user
    which tries to guess the locations of the ships by guessing their
    coordinates.
    """

    def __init__(self, board_size, ships):
        """
        Initialize a new Game object.
        :param board_size: Length of the side of the game-board
        :param ships: A list of ships that participate in the game.
        :return: A new Game object.
        """

        # private attributes to protect on the game attributes

        self.__board_size = board_size
        self.__ships = ships

        # dictionary for bombs with tuples representing the (x, y) coordinates
        # that contain active bombs as keys and an int representing
        # the numbers of turns remaining for the current bomb (1-3) as values
        self.__bombs = {}
        # all of the hits on all of the ships
        self.__hits = []

    def __ship_intact_coordinates(self):

        ship_intact_coords = []
        for ship in self.__ships:
            for coord in ship.coordinates():
                if coord not in ship.damaged_cells():
                    ship_intact_coords.append(coord)
        return ship_intact_coords

    def __play_one_round(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. The logic defined by this function must be implemented
        but if you wish to do so in another function (or some other functions)
        it is ok.

        Te function runs one round of the game :
            1. Get user coordinate choice for bombing.
            2. Move all game's ships.
            3. Update all ships and bombs.
            4. Report to the user the result of current round (number of hits
            and terminated ships)
        :return:
            (some constant you may want implement which represents) Game status
            GAME_STATUS_ONGOING if there are still ships on the board or
            GAME_STATUS_ENDED otherwise.
        """

        # 1. update the bombs
        bombs_to_remove = []

        for bomb_coord, bomb_turns in self.__bombs.items():
            if bomb_turns == 1:
                bombs_to_remove.append(bomb_coord)
            else:
                self.__bombs[bomb_coord] -= 1

        # remove bombs which are expired
        # we will do it outside the for loop because we can not shrink the
        # dictionary in the loop

        for bomb_coord in bombs_to_remove:
            self.__bombs.pop(bomb_coord)

        # 2. ask the user where he wants to put the bomb in the board
        user_coord_for_bomb = gh.get_target(self.__board_size)

        # 3. append the bomb to bombs dictionary
        self.__bombs[user_coord_for_bomb] = TURNS_TO_KEEP_BOMB

        # 4. move all of the ships which do not have damaged cells in the last
        # turns of the game
        for ship in self.__ships:
            if len(ship.damaged_cells()) == 0:
                ship.move()

        # 5. update hits on ships and
        # remove bombs that exploded in last turn
        # and populate hits_from_cur_turn list

        hits_from_cur_turn = []
        for bomb_coord, bomb_turns in self.__bombs.items():
            for ship in self.__ships:
                if bomb_coord in ship.coordinates():
                        ship.hit(bomb_coord)
                        hits_from_cur_turn.append(bomb_coord)

        # again, remove from dictionary outside the loop
        for coord in hits_from_cur_turn:
            if coord in self.__bombs:
                self.__bombs.pop(coord)

        # 6. print the board to screen by calling board_to_string
        # first, I should prepare the params to the function

        # add to list hits from curr turn
        self.__hits += hits_from_cur_turn

        # all of the coordinates of ships which are intact
        ship_intact_coords = self.__ship_intact_coordinates()

        print(gh.board_to_string(self.__board_size, hits_from_cur_turn,
                                 self.__bombs, self.__hits,
                                 ship_intact_coords))

        # 7. remove from hits list hits, if ship was terminated

        for ship in self.__ships:
            if ship.terminated():
                for ship_coord in ship.coordinates():
                    if ship_coord in self.__hits:
                        self.__hits.remove(ship_coord)

        # 8. remove from board ships which have been totally terminated
        count_terminations = 0

        alive_ships = []
        for index_of_ship in range(len(self.__ships)):
            if self.__ships[index_of_ship].terminated():
                count_terminations += 1
            else:
                alive_ships.append(self.__ships[index_of_ship])

        self.__ships = alive_ships

        # 9. report to the user about the number of hits and terminations of
        # ships
        gh.report_turn(len(hits_from_cur_turn), count_terminations)

        if len(self.__ships) > 0:
            return GAME_STATUS_ONGOING
        else:
            return GAME_STATUS_ENDED

    def __repr__(self):
        """
        Return a string representation of the board's game
        :return: A tuple converted to string. The tuple should contain
        (maintain the following order):
            1. Board's size.
            2. A dictionary of the bombs found on the board
                 {(pos_x, pos_y) : remaining turns}
                For example :
                 {(0, 1) : 2, (3, 2) : 1}
            3. A list of the ships found on the board (each ship should be
                represented by its __repr__ string).
        """

        my_tuple = (self.__board_size, self.__bombs, self.__ships)

        return str(my_tuple)

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        completion.
        :return: None
        """

        # 1. print signs of board to screen
        gh.report_legend()
        # 2. print the board
        print(gh.board_to_string(self.__board_size, [],
                                 {}, [], self.__ship_intact_coordinates()))

        # 3. start first round
        game_status = self.__play_one_round()
        # 4. while there is alive ship on board(game_status == 0), play round
        while game_status == 0:
            game_status = self.__play_one_round()
        # 5. in the end report to the user that game is over
        gh.report_gameover()


if __name__=="__main__":
    game = Game(5, gh.initialize_ship_list(4, 2))
    game.play()