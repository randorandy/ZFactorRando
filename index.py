# pyscript entry point

import json
from typing import Any, Literal, Optional, TypedDict

# pyscript library
import js  # type: ignore

from game import Game, GameOptions
from romWriter import RomWriter
from Main import generate, get_spoiler, write_rom

Element: Any  # pyscript built-in



class WebParams(TypedDict):
    visibility: bool


# the roll process is divided up to make the ui more responsive,
# because there's no way to run it asynchronously in js
# https://github.com/pyscript/pyscript/discussions/1406

# global state between roll functions
rom_writer: Optional[RomWriter] = None
options: Optional[GameOptions] = None
game: Optional[Game] = None


def roll1() -> bool:
    global rom_writer
    print("roll1 initiated")
    try:
        base64_data: str = js.rom_data  # type: ignore
    except AttributeError:
        base64_data = ""

    if len(base64_data) == 0:
        print("no rom loaded")
        return False

    rom_writer = RomWriter.fromBase64(base64_data)
    return True


def roll2(params_str: str) -> None:
    global options
    print("roll2 initiated")
    print(params_str)
    params: WebParams = json.loads(params_str)

    #tricks: frozenset[Trick] = frozenset([getattr(Tricks, trick_name) for trick_name in params["tricks"]])

    # romWriter = RomWriter.fromBlankIps()  # TODO
    options = GameOptions(
        bool(params["visibility"]))
    #


def roll3() -> bool:
    global game
    print("roll3 initiated")
    #print(options)
    assert options
    #print(options)
    game = generate(options)
    return all(not (loc["item"] is None) for loc in game.all_locations.values())


def roll4() -> None:
    # see if hint_data is None to know if it failed
    print("roll4 initiated")
    if rom_writer and game:
        rom_name = write_rom(game, rom_writer)
        js.modified_rom_data = rom_writer.getBase64RomData().decode()
        js.rom_name = rom_name

        js.spoiler_text = get_spoiler(game)
    else:
        js.modified_rom_data = ""
