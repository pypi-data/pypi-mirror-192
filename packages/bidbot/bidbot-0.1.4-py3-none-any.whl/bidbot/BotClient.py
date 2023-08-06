import socket
import argparse
import random
import sys
from rich.console import Console
from bidbot.protos.Comms_pb2 import ServerRequest
import logging
from rich.logging import RichHandler
import asyncio
from bidbot.varint import decode_stream, encode
from bidbot.BidBot import BidBot
#from bots import HalfBot, RandomBot, LastPlusOne, StingyBot, TwentyBot
from bidbot.GameState import GameState
import signal
console = Console()

FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler(markup=True)]
)

log = logging.getLogger("rich")

SHOULD_QUIT = False
PROTO_VERSION_MAJOR = 0
PROTO_VERSION_MINOR = 2


def handler(signum, frame):
    global SHOULD_QUIT
    logging.warning("Caught Ctrl+c")
    SHOULD_QUIT = True


signal.signal(signal.SIGINT, handler)

def read_until_newline(sock: socket.socket):
    c = bytes()
    result = bytes()
    while c != b'\n':
        c = sock.recv(1)
        result += c
    return result


async def read_proto(reader) -> ServerRequest:

    try:
        size = await decode_stream(reader)
    except EOFError:
        log.error("The server has closed the connection.")
        sys.exit(1)

    log.debug(f"Message received of size {size}")

    try:
        msg = await reader.read(size)
    except EOFError:
        log.error("The server has closed the connection.")
        sys.exit(1)

    request: ServerRequest = ServerRequest()
    request.ParseFromString(msg)
    return request

async def send_proto(writer, msg: ServerRequest):
    encoded_msg = msg.SerializeToString()
    response_len = encode(len(encoded_msg))
    writer.write(response_len)
    writer.write(encoded_msg)


def sock_read_newline_str(sock: socket.socket):
    line = read_until_newline(sock)
    return line.decode('utf-8').rstrip()


def sock_send_line(sock: socket.socket, message: str):
    message += '\n'
    sock.sendall(message.encode())


async def do_bid(reader, writer, game_state: GameState, bot: BidBot):

    bid_amount = bot.get_bid(game_state)
    log.info(f"Bidding {bid_amount}")
    bid_request: ServerRequest = ServerRequest()
    bid_request.msgType = bid_request.BID_RESPONSE
    bid_request.bidResponse.money = bid_amount

    await send_proto(writer, bid_request)

    response: ServerRequest = await read_proto(reader)

    if response.msgType == response.BID_REJECT:
        log.error(f"Bid of {bid_amount} was rejected")
        bot.bid_rejected(game_state, bid_amount)
    elif response.msgType == response.ACK:
        log.debug(f"Bid accepted.")
    else:
        log.error(f"I got a strange response when I sent in a bid: {response.msgType}")


async def do_login(reader, writer, bot: BidBot):
    player_name = bot.get_creds()[0]
    log.info(f"logging in with the name {player_name}")
    response: ServerRequest = ServerRequest()
    response.msgType = response.AUTH_RESPONSE
    response.authResponse.player_name = player_name
    await send_proto(writer, response)

    resp = await read_proto(reader)
    if resp.msgType == resp.ACK:
        log.info("Login succeeded.")
        bot.set_authenticated(True)
    else:
        log.error("Authentication rejeted.")
        bot.set_authenticated(False)
        sys.exit(1)


def do_start_game(sock, proto: ServerRequest, bot: BidBot) -> GameState:
    game_state = GameState()
    my_name = bot.get_creds()[0]
    game_state.opponent_username = proto.gameStart.player1_name if my_name == proto.gameStart.player2_name else proto.gameStart.player2_name
    bot.play_opponent(game_state.opponent_username)
    game_state.my_money = proto.gameStart.player1_start_money if my_name == proto.gameStart.player1_name else proto.gameStart.player2_start_money
    if proto.gameStart.player1_name == my_name:
        game_state.player_identifier = GameState.PLAYER_A
    else:
        game_state.player_identifier = GameState.PLAYER_B

    log.info("I am " + ("Player A" if game_state.player_identifier == GameState.PLAYER_A else "Player B"))
    log.info(f"Player A name: {proto.gameStart.player1_name} player A money: {proto.gameStart.player1_start_money}")
    log.info(f"Player A name: {proto.gameStart.player2_name} player B money: {proto.gameStart.player2_start_money}")

    return game_state

def show_position(sock, command):
    final_str = ''
    position = int(command.split(' ')[1])
    for x in range(-5, 5):
        final_str += '['
        final_str += 'X' if x == position else ' '
        final_str += ']'

    log.info(final_str)


async def show_result(proto, game_state: GameState, bot: BidBot):

    if proto.msgType != proto.MsgType.BID_RESULT:
        log.error(f"Somehow I got an invalid result type of {proto.msgType} in bid_result")
        return

    if game_state.is_player_a():
        game_state.add_my_bid(proto.bidResult.player_a_bid)
        game_state.add_opponent_bid(proto.bidResult.player_b_bid)
    else:
        game_state.add_my_bid(proto.bidResult.player_b_bid)
        game_state.add_opponent_bid(proto.bidResult.player_a_bid)


    log.info(f"Bid A {proto.bidResult.player_a_bid} Bid B {proto.bidResult.player_b_bid}")

    if proto.bidResult.winner_name == bot.get_username():
        game_state.inc_rounds_won()

        if proto.bidResult.result_type == proto.bidResult.DRAW:
            log.info("I won by draw advantage")
        else:
            log.info("I won that round!")
    else:
        game_state.inc_rounds_lost()
        log.info("I lost that round")


def do_game_end(proto, bot: BidBot):
    if proto.gameEnd.result == proto.gameEnd.WIN:
        log.info("I won!")
    elif proto.gameEnd.result == proto.gameEnd.LOSS:
        log.info("[bold red]I lost![/bold red]")
    else:
        log.info("[bold yellow]We drew![/bold yellow]")

    bot.set_elo(proto.gameEnd.elo)
    log.info(f"My new elo: [bold green]{proto.gameEnd.elo}[bold green]")

def do_round_start(proto, game_state: GameState, bot: BidBot):

    str = ""

    if game_state.is_player_a():
        str += game_state.get_opponent_name() + " - "
        game_state.my_money = proto.roundStart.player_a_money
    else:
        game_state.my_money = proto.roundStart.player_b_money
        str += bot.username + " - "

    game_state.set_bottle_position(proto.roundStart.bottle_pos)

    for x in range(10):
        if x != proto.roundStart.bottle_pos:
            str += "[ ]"
        else:
            str += "[X]"

    if game_state.is_player_a():
        str += " - " + bot.get_username()
    else:
        str += " - " + game_state.get_opponent_username()

    log.info(str)


async def game_loop(host: str, port: int, username: str, bot: BidBot):
    game_state = dict()

    try:
        reader, writer = await asyncio.open_connection(host, port)
    except ConnectionRefusedError:
        log.error(f"Could not connect to server at {host}:{port} Please check your parameters.")
        sys.exit(1)

    while True:
        if SHOULD_QUIT:
            log.warning("Got signal to quit. Exiting.")
            break
        proto = await read_proto(reader)

        if proto.msgType == proto.AUTH_REQUEST:
            log.debug("Found auth request!")
            await do_login(reader, writer, bot)
        elif proto.msgType == proto.BID_RESULT:
            log.debug("Found bid result")
            await show_result(proto, game_state, bot)
        elif proto.msgType == proto.BID_REQUEST:
            log.debug("Bid request received.")
            await do_bid(reader, writer, game_state, bot)
        elif proto.msgType == proto.GAME_START:
            log.info("The game is starting!")
            game_state = do_start_game(reader, proto, bot)
        elif proto.msgType == proto.GAME_ABORT:
            log.error("The game was aborted!")
        elif proto.msgType == proto.GAME_END:
            log.info("The game has ended.")
            do_game_end(proto, bot)
        elif proto.msgType == proto.ROUND_START:
            log.debug("Got round start")
            do_round_start(proto, game_state, bot)
        elif proto.msgType == proto.ALIVE:
            resp = ServerRequest()
            resp.msgType = resp.ACK
            await send_proto(writer, resp)
        elif proto.msgType == proto.VERSION:
            if proto.version_major == PROTO_VERSION_MAJOR and proto.version_minor == PROTO_VERSION_MINOR:
                log.info(f"Server protocol version {PROTO_VERSION_MAJOR}.{PROTO_VERSION_MINOR} "
                         f"matches client protocol version.")
            else:
                log.info(f"Server protocol version {proto.version_major}.{proto.version_minor} does not match the "
                         f"client version of {PROTO_VERSION_MAJOR}.{PROTO_VERSION_MINOR}. You need to update the "
                         f"bidbot client library.")
                return
        else:
            log.info(f"Got {proto.msgType}")

    log.info("My Results:")
    for name, times in bot.opponents_played.items():
        log.info(f"{name} {times} / {bot.total_games}")


def connect(host: str, port: int, username: str, bot: BidBot):
     
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        asyncio.run(game_loop(host, port, username, bot))


