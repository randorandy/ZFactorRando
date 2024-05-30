from typing import TYPE_CHECKING

from item_data import Item, Items
from logic_shortcut import LogicShortcut

if TYPE_CHECKING:
    from loadout import Loadout

STARTING_ENERGY = 99
ENERGY_PER_TANK = 100
FOR_N_TANKS = 12
LATER_ENERGY_PER_TANK = 50

canUsePB = LogicShortcut(lambda loadout: (
    loadout.has_all(Items.Morph, Items.PowerBomb)
))


