class GameState(object):

    PLAYER_A = 0
    PLAYER_B = 1
    UNKNOWN = 3

    def __init__(self):
        # The name of the current opponent.
        self.opponent_username = ""

        # Whether we are playing as player A or player B
        self.player_identifier = GameState.UNKNOWN

        # The amount of money our opponent has left.
        self.opponent_money = 0

        # The amount of money the bot has left.
        self.my_money = 0

        # The current position of the bottle. The position ranges from
        # 0 - 10.
        self.bottle_position = 0

        # All of the historical bids of the opponent.
        self.opponents_bids = list()

        # All of my historical bids.
        self.my_bids = list()

        # The money I have to start with.
        self.start_money = 0

        # The number of rounds I've won in this game. There are 10 rounds max.
        self.rounds_won = 0

        # The number of rounds I've lost in this game. There are 10 rounds max.
        self.rounds_lost = 0

    def is_player_a(self) -> bool:
        """
        :return: true of we are player A, false otherwise.
        """
        return self.player_identifier == GameState.PLAYER_A

    def get_opponent_name(self) -> str:
        """
        :return: The opponents name
        """
        return self.opponent_username

    def set_bottle_position(self, pos: int) -> None:
        """
        Helper function for updating the bottle position.
        """
        if pos < 0 or pos > 10:
            raise Exception(f"The bottle exception was invalid: {pos}.")
        self.bottle_position = pos

    def get_opponent_username(self) -> str:
        """
        Gets the opponents username.

        TODO This is redundent with get_opponent_name. Clean this up.
        """
        return self.opponent_username

    def add_opponent_bid(self, bid: int) -> None:
        """
        Update the list of opponent bids.
        """
        self.opponents_bids.append(bid)

    def add_my_bid(self, bid: int) -> None:
        """
        Add my own bid to my list of historical bids.
        """
        self.my_bids.append(bid)

    def set_start_money(self, start_money: int) -> None:
        """
        The game usually starts with each player having $100, however this is server
        controlled, and could be any number.
        """
        self.start_money = start_money

    def inc_rounds_lost(self) -> None:
        self.rounds_lost += 1

    def inc_rounds_won(self) -> None:
        self.rounds_won += 1

