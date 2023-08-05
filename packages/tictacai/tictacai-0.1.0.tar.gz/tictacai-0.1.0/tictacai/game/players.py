"""
Contains Player classes which will know which move to make
"""
from abc import ABCMeta, abstractmethod
import time

from ..logic.exceptions import InvalidMove
from ..logic.models import Mark, GameState, Move
from ..logic.minimax import find_best_move


class Player(metaclass=ABCMeta):
    """
    Base class for concrete players to extend
    """

    def __init__(self, mark: Mark) -> None:
        self.mark = mark

    def make_move(self, game_state: GameState) -> GameState:
        if self.mark is game_state.current_mark:
            if move := self.get_move(game_state):
                return move.after_state
            raise InvalidMove("No more possible moves")
        else:
            raise InvalidMove("It's the other player's turn")

    @abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """Return the current player's move in the given game state"""


class ComputerPlayer(Player, metaclass=ABCMeta):
    def __init__(self, mark: Mark, delay_seconds: float = 0.25) -> None:
        """
        Abstract base class for Computer players that extends Player base class by adding a 'delay_seconds' property
        which by default is 0.25 seconds equal to 250 milliseconds. This provides a delay before the computer player
        makes a move.
        :param mark: Initial mark
        :param delay_seconds: the wait time for a computer player before it has to make a move. defaulted to 0.25 seconds
        """
        super().__init__(mark)
        self.delay_seconds = delay_seconds

    def get_move(self, game_state: GameState) -> Move | None:
        time.sleep(self.delay_seconds)
        return self.get_computer_move(game_state)

    @abstractmethod
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """Return the computer's move in the given game state"""


class RandomComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        return game_state.make_random_move()


class MinimaxComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        if game_state.game_not_started:
            return game_state.make_random_move()
        else:
            return find_best_move(game_state)
