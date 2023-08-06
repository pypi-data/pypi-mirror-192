from typing import Tuple
from bidbot.GameState import GameState

class BidBot(object):

    def __init__(self, username: str):
        # Indicates if we are authenticated or not
        self.authenticated = False

        # Not used
        self.token = None

        # The username to log in as
        self.username: str = username

        # A list of the opponents that have been played, and the number of times
        self.opponents_played = dict()

        # Total number of games played
        self.total_games = 0

        # Current ELO rating.
        self.elo = 400

    def get_bid(self, game_state: GameState) -> int:
        """
        The main function to determine how the bot should play.

        This should be overridden to play the game. By default it always bids 1 which I can assure you is a bad
        strategy.

        :param game_state: The game state. This provides the bot with the relevant information
        about the current game.
        """
        return 1

    def get_creds(self) -> Tuple[str, str]:
        """
        A function called to get any credentials needed.

        As of right now token isn't used.
        :return: A tuple of (username, token)
        """
        return self.username, self.token

    def set_authenticated(self, new_val: bool) -> None:
        """
        Sets whether we are authenticated.

        :param new_val: Whether we should be considered authenticated.
        :return: True if we are authenticated. False otherwise.
        """
        self.authenticated = new_val

    def get_username(self) -> str:
        """
        Get the players username.
        :return: A string representing the users username.
        """
        return self.username

    def bid_rejected(self, game_state, bid) -> None:
        """
        What to do when a bid is rejected.
        """
        pass

    def play_opponent(self, opponent_name: str) -> None:
        """
        A helper function to update what opponents have been
        played and how often.

        :param opponent_name: The name of the opponent.
        """
        self.total_games += 1
        if opponent_name in self.opponents_played.keys():
            self.opponents_played[opponent_name] += 1
        else:
            self.opponents_played[opponent_name] = 1

    def set_elo(self, new_elo: int) -> None:
        """
        Sets the current elo.
        """
        self.elo = new_elo

