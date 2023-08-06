# The Bidding Game

This is a client-side bot for the "bidding game". 

# Rules

This game consists of two people (or bots) that are "bidding" for a high value item, usually described as a bottle of scotch.

There are 11 "places" between each player with the bottle of scotch sitting in the middle. If a player wins a round, the bottle
of scotch moves towards the player by one place. If the bottle gets all the way to the end (slot 0 or 10) then that player 
wins the bottle. If by the end of 10 rounds neither player wins, the game is considered a draw.

To win a round, each player must secretly bid some amount of money. The player with the biggest bid wins that round, and 
the bottle of scotch moves one position towards them. Each player starts with $100, and must bid in $1 increments. The 
player who wins the round has their bid deducted from their total, and the player who lost keeps their bid.

In the case of both bids being equal, the player with "draw advantage" wins the round. "Draw advantage" starts with player A,
and every time there is a draw, "draw advantage" is switched to the other player. 

Finally, you must bid at least $1, unless you're out of money in which case you may bid $0. **Make sure you include
this as part of your bot or your bids will be invalid and the game will be abandoned.**

# Making A Bot

The following is necessary to make a bot:

1. Install this library. This is easily done by running: ```pip3 install bidbot```
2. Extend the BidBot object.
3. Connect to a server.


# Example bot:

The following is  full example of a bot. Note that the only thing a play can really do is pick a bid, you only
need to override one object. The following is a bot that randomly picks an amount to play.

```python3
from bidbot.BidBot import BidBot
from bidbot.GameState import GameState
from bidbot.BotClient import connect
import random

class RandomBot(BidBot):

    def get_bid(self, game_state: GameState):
        if game_state.my_money <= 1:
            return game_state.my_money
        else:
            return random.randrange(1, game_state.my_money)


def main():

    username = "your_username"
    bot = RandomBot(username)
    host = "your_sever.hostname.com"
    port = 8080

    connect(host, port, username, bot)

if __name__ == "__main__":
    main()
```

# GameState

There's lots of information that can be used to assist you in picking a bid. The following fields are some useful ones:
- `game_state.self.opponent_username` - The opponents username.
- `game_state.self.player_identifier` - Determines if we are GameState.PLAYER_A or GameState.PLAYER_B
- `game_state.opponent_money` - The amount of money the opponent has left.
- `game_state.my_money` - The amount of money your bot has left.
- `game_state.bottle_position` - The current bottle position.
- `game_state.opponents_bids` - A list of the bids the opponent has made up until now.
- `game_state.my_bids` - A list of bids that your bot has made up until now.
- `game_state.start_money` - The amount of money the game was started with. Typically, this is $100.
- `game_state.rounds_won` - The number of rounds that have been won.
- `game_state.rounds_lost` - The number of rounds that have been lost.

