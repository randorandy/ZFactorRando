import random
import sys
from typing import Literal, Optional, Type
import argparse

from connection_data import SunkenNestL, VanillaAreas
from fillInterface import FillAlgorithm
from game import Game, GameOptions
from item_data import Item, Items, items_unpackable
from loadout import Loadout
from location_data import Location, pullCSV, spacePortLocs
from logicExpert import Expert
import logic_updater
import fillAssumed
import areaRando
from romWriter import RomWriter
from solver import solve
import ipspatch


def plmidFromHiddenness(itemArray, hiddenness, visible = True) -> bytes:
    if hiddenness == "open":
        plmid = itemArray[1]
    elif hiddenness == "chozo":
        plmid = itemArray[2]
    else:
        plmid = itemArray[3]
    if visible:
        plmid = itemArray[1]
    return plmid

def write_location(romWriter: RomWriter, location: Location, visible = True) -> None:
    """
    provide a location with an ['item'] value, such as Missile, Super, etc
    write all rom locations associated with the item location
    """
    item = location["item"]
    assert item, f"{location['fullitemname']} didn't get an item"
    # TODO: support locations with no items?
    plmid = plmidFromHiddenness(item, location['hiddenness'], visible)
    for address in location['locids']:
        romWriter.writeItem(address, plmid, item[4])
    for address in location['alternateroomlocids']:
        if location['alternateroomdifferenthiddenness'] == "":
            # most of the alt rooms go here, having the same item hiddenness
            # as the corresponding "pre-item-move" item had
            plmid_altroom = plmid
        else:
            plmid_altroom = plmidFromHiddenness(item, location['alternateroomdifferenthiddenness'], visible)
        romWriter.writeItem(address, plmid_altroom, item[4])


fillers: dict[str, Type[FillAlgorithm]] = {
    "AF": fillAssumed.FillAssumed,
}


# main program
def Main(argv: list[str], romWriter: Optional[RomWriter] = None) -> None:
    options = GameOptions(False)
    game = generate(options)
    rom_name = write_rom(game)
    write_spoiler_file(game, rom_name)

def generate(options: GameOptions) -> Game:
    #print("started generate with options ",options)
    logicChoice = "E"
    fillChoice = "D"
    areaA = ""
    
    seeeed = random.randint(0, 9999999)
    random.seed(seeeed)

    
    csvdict = pullCSV()
    #print("pulled csv")
    locArray = list(csvdict.values())
    
    seedComplete = False
    randomizeAttempts = 0
    game = Game(Expert,
                csvdict,
                options.visibility,
                VanillaAreas(),
                seeeed)
    #print("Just so you know, visibility is set to ",options.visibility)
    while not seedComplete :
        
        
        randomizeAttempts += 1
        if randomizeAttempts > 100:
            print("Giving up after 100 attempts. Help?")
            break
        print("Starting randomization attempt:", randomizeAttempts)
        game.item_placement_spoiler = ""
        game.item_placement_spoiler += f"Starting randomization attempt: {randomizeAttempts}\n"
        game.item_placement_spoiler += f"Seed: {seeeed}"
        # now start randomizing
        seedComplete = assumed_fill(game)
        
    #_got_all, solve_lines, _locs = solve(game)
    #^ what is this?
            
    return game




def assumed_fill(game: Game) -> tuple[bool]:
    for loc in game.all_locations.values():
        loc["item"] = None
    dummy_locations: list[Location] = []
    loadout = Loadout(game)
    fill_algorithm = fillAssumed.FillAssumed(game.connections)
    n_items_to_place = fill_algorithm.count_items_remaining()
    assert n_items_to_place <= len(game.all_locations), \
        f"{n_items_to_place} items to put in {len(game.all_locations)} locations"
    print(f"Start {fill_algorithm.count_items_remaining()} items to place")
    while fill_algorithm.count_items_remaining():
        placePair = fill_algorithm.choose_placement(dummy_locations, loadout)
        if placePair is None:
            message = ('Item placement was not successful in assumed. '
                       f'{fill_algorithm.count_items_remaining()} items remaining.')
            print(message)

            break
        placeLocation, placeItem = placePair
        placeLocation["item"] = placeItem

        if fill_algorithm.count_items_remaining() == 0:
            # Normally, assumed fill will always make a valid playthrough,
            # but dropping from spaceport can mess that up,
            # so it needs to be checked again.
            #completable, _, _ = solve(game)
            completable = game.all_locations["Morph Ball"]["item"] == Items.Morph
            #completable = True
            if completable:
                print("Item placements successful.")
            return completable

    return False

def write_rom(game: Game, romWriter: Optional[RomWriter] = None) -> str:
    
    logicChoice = "E"



    rom_name = f"ZFactor{game.seed}.sfc"
    rom1_path = f"roms/{rom_name}"
    rom_clean_path = "roms/Z Factor.sfc"

    if romWriter is None :
        romWriter = RomWriter.fromFilePaths(origRomPath=rom_clean_path)
    else :
        # remove .sfc extension and dirs
        romWriter.setBaseFilename(rom1_path[:-4].split("/")[-1])

    for loc in game.all_locations.values():
        write_location(romWriter, loc, game.visibility)
    
    
    
    # Remove gravity suit heat protection #test
    romWriter.writeBytes(0x6e37d, b"\x01")
    romWriter.writeBytes(0x869dd, b"\x01")    
    romWriter.writeBytes(0x8b629, b"\x01") #hellrun speed echoes patch?? ##verify

    # early awakening patch
    romWriter.writeBytes(0x787c3, b"\x09\x05\xE0\xAD\x20\x8D\xBA")
    romWriter.writeBytes(0x787d3, b"\xcd")
    romWriter.writeBytes(0x7812b, b"\x09\x03\x70")
    romWriter.writeBytes(0x7813b, b"\xbf")

    romWriter.finalizeRom(rom1_path)

    patches_list = ["Patches/Level Patch.IPS",
                    "Patches/Zebes Awakens Patch.IPS",
                    "Patches/max_ammo_display.ips",
                    "Patches/Disable Suit Animation.IPS",
                    "Patches/JAMMorphingBallFix.IPS"]
    for patch_path in patches_list :
        ipspatch.apply_patch(rom1_path,patch_path)

    print("Done!")
    print(f"Filename is {rom_name}")



    return rom_name

def get_spoiler(game: Game) -> str:
    """ the text in the spoiler file """

    spoilerSave = game.item_placement_spoiler + '\n'

    _completable, play_through, _locs = solve(game)
    #solve_lines = spoil_play_through(play_through)

    #s = f"RNG Seed: {game.seed}\n\n"
    s = "\n Spoiler \n\n Spoiler \n\n Spoiler \n\n Spoiler \n\n"
    s += spoilerSave
    s += '\n\n'
    for solve_line in play_through:
        s += solve_line + '\n'

    return s

def write_spoiler_file(game: Game, rom_name: str) -> None:
    text = get_spoiler(game)
    with open(f"spoilers/{rom_name}.spoiler.txt", "w") as spoiler_file:
        spoiler_file.write(text)
    print(f"Spoiler file is spoilers/{rom_name}.spoiler.txt")

def forward_fill(game: Game,
                 fillChoice: Literal["M", "S", "MM"],
                 spoilerSave: str) -> tuple[bool, str]:
    unusedLocations : list[Location] = []
    unusedLocations.extend(game.all_locations.values())
    availableLocations: list[Location] = []
    # visitedLocations = []
    loadout = Loadout(game)
    loadout.append(SunkenNestL)  # starting area
    # use appropriate fill algorithm for initializing item lists
    fill_algorithm = fillers[fillChoice](game.connections)
    while len(unusedLocations) != 0 or len(availableLocations) != 0:
        # print("loadout contains:")
        # print(loadout)
        # for a in loadout:
        #     print("-",a[0])
        # update logic by updating unusedLocations
        # using helper function, modular for more logic options later
        # unusedLocations[i]['inlogic'] holds the True or False for logic
        logic_updater.updateAreaLogic(loadout)
        logic_updater.updateLogic(unusedLocations, loadout)

        # update unusedLocations and availableLocations
        for i in reversed(range(len(unusedLocations))):  # iterate in reverse so we can remove freely
            if unusedLocations[i]['inlogic'] is True:
                # print("Found available location at",unusedLocations[i]['fullitemname'])
                availableLocations.append(unusedLocations[i])
                unusedLocations.pop(i)
        # print("Available locations sits at:",len(availableLocations))
        # for al in availableLocations :
        #     print(al[0])
        # print("Unused locations sits at size:",len(unusedLocations))
        # print("unusedLocations:")
        # for u in unusedLocations :
        #     print(u['fullitemname'])

        if availableLocations == [] and unusedLocations != [] :
            print(f'Item placement was not successful. {len(unusedLocations)} locations remaining.')
            spoilerSave += f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
            # for i in loadout:
            #     print(i[0])
            # for u in unusedLocations :
            #     print("--",u['fullitemname'])

            break

        placePair = fill_algorithm.choose_placement(availableLocations, loadout)
        if placePair is None:
            print(f'Item placement was not successful due to majors. {len(unusedLocations)} locations remaining.')
            spoilerSave += f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
            break
        # it returns your location and item, which are handled here
        placeLocation, placeItem = placePair
        if (placeLocation in unusedLocations) :
            unusedLocations.remove(placeLocation)
        placeLocation["item"] = placeItem
        availableLocations.remove(placeLocation)
        fill_algorithm.remove_from_pool(placeItem)
        loadout.append(placeItem)
        if not ((placeLocation['fullitemname'] in spacePortLocs) or (Items.spaceDrop in loadout)):
            loadout.append(Items.spaceDrop)
        spoilerSave += f"{placeLocation['fullitemname']} - - - {placeItem[0]}\n"
        # print(placeLocation['fullitemname']+placeItem[0])

        if availableLocations == [] and unusedLocations == [] :
            print("Item placements successful.")
            spoilerSave += "Item placements successful.\n"
            return True, spoilerSave
    return False, spoilerSave


if __name__ == "__main__":
    import time
    t0 = time.perf_counter()
    Main(sys.argv)
    t1 = time.perf_counter()
    print(f"time taken: {t1 - t0}")
