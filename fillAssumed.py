import random
from typing import Optional

from connection_data import AreaDoor
from fillInterface import FillAlgorithm
from item_data import Item, Items
from loadout import Loadout
from location_data import Location, spacePortLocs
from solver import solve

_minor_items = {
    Items.Missile: 55,
    Items.Super: 9,
    Items.PowerBomb: 9,
    Items.Energy: 13,
    Items.Reserve: 3
}
# TODO: verify item counts


class FillAssumed(FillAlgorithm):
    connections: list[tuple[AreaDoor, AreaDoor]]

    # earlyItemList: list[Item]
    prog_items: list[Item]
    extra_items: list[Item]
    itemLists: list[list[Item]]

    def __init__(self,
                 connections: list[tuple[AreaDoor, AreaDoor]]) -> None:
        self.connections = connections

        # self.earlyItemList = [
        #     Missile,
        #     Morph,
        #     GravityBoots
        # ]
        self.prog_items = [
            Items.Missile,
            Items.Morph,
            Items.Super,
            Items.PowerBomb,
            Items.Springball, 
            Items.Bombs,
            Items.HiJump,
            Items.Grapple,
            Items.Varia,
            Items.GravitySuit,
            Items.Wave,
            Items.SpeedBooster,
            Items.Spazer,
            Items.Ice,
            Items.Plasma,
            Items.Screw,
            Items.SpaceJump,
            Items.Charge,
            Items.Energy,
            Items.Reserve,
            Items.Xray
        ]
        #assert len([it for it in self.prog_items if (it != Items.Energy and it != Items.Artifact)]) + 1 == len(set(self.prog_items)), \
        #    "duplicate majors?"
        self.extra_items = []
        for it, n in _minor_items.items():
            self.extra_items.extend([it for _ in range(n)])

        self.itemLists = [self.prog_items, self.extra_items]

    def _get_accessible_locations(self, loadout: Loadout) -> list[Location]:
        _, _, locs = solve(loadout.game, loadout)
        return locs

    def _get_available_locations(self, loadout: Loadout) -> list[Location]:
        return [loc for loc in self._get_accessible_locations(loadout) if loc["item"] is None]

    def _get_empty_locations(self, all_locations: dict[str, Location]) -> list[Location]:
        return [loc for loc in all_locations.values() if loc["item"] is None]

    @staticmethod
    def _choose_location(locs: list[Location], spaceport_deprio: int) -> Location:
        """
        to work against spaceport front-loading,
        because 1 progression item in space port
        will lead to more progression items in spaceport
        """
        distribution = locs.copy()
        for _ in range(spaceport_deprio):
            for loc in locs:
                if loc["fullitemname"] not in spacePortLocs:
                    distribution.append(loc)
        return random.choice(distribution)

    def choose_placement(self,
                         availableLocations: list[Location],
                         loadout: Loadout) -> Optional[tuple[Location, Item]]:
        """ returns (location to place an item, which item to place there) """

        from_items = (
            self.prog_items if len(self.prog_items) else (
                self.extra_items
            )
        )

        assert len(from_items), "tried to place item when placement algorithm has 0 items left in item pool"

        item_to_place = random.choice(from_items)

        from_items.remove(item_to_place)

        if from_items is self.prog_items:
            loadout = Loadout(loadout.game)
            for item in from_items:
                loadout.append(item)
            available_locations = self._get_available_locations(loadout)
        else:  # extra
            available_locations = self._get_empty_locations(loadout.game.all_locations)
        if len(available_locations) == 0:
            return None

        # This magic number 2 could be an option for "How loaded do you want the spaceport to be?"
        # (lower number means more progression items in spaceport)
        return self._choose_location(available_locations, 2), item_to_place

    def count_items_remaining(self) -> int:
        return sum(len(li) for li in self.itemLists)

    def remove_from_pool(self, item: Item) -> None:
        """ removes this item from the item pool """
        pass  # removed in placement function
