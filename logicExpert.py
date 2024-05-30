from typing import ClassVar

from connection_data import area_doors_unpackable
from door_logic import canOpen
from item_data import items_unpackable, Items
from loadout import Loadout
from logicInterface import AreaLogicType, LocationLogicType, LogicInterface
from logic_shortcut import LogicShortcut

# TODO: There are a bunch of places where where Expert logic needed energy tanks even if they had Varia suit.
# Need to make sure everything is right in those places. 
# (They will probably work right when they're combined like this,
#  but they wouldn't have worked right when casual was separated from expert.)

# TODO: There are also a bunch of places where casual used icePod, where expert only used Ice. Is that right?

(
    CraterR, SunkenNestL, RuinedConcourseBL, RuinedConcourseTR, CausewayR,
    SporeFieldTR, SporeFieldBR, OceanShoreR, EleToTurbidPassageR, PileAnchorL,
    ExcavationSiteL, WestCorridorR, FoyerR, ConstructionSiteL, AlluringCenoteR,
    FieldAccessL, TransferStationR, CellarR, SubbasementFissureL,
    WestTerminalAccessL, MezzanineConcourseL, VulnarCanyonL, CanyonPassageR,
    ElevatorToCondenserL, LoadingDockSecurityAreaL, ElevatorToWellspringL,
    NorakBrookL, NorakPerimeterTR, NorakPerimeterBL, VulnarDepthsElevatorEL,
    VulnarDepthsElevatorER, HiveBurrowL, SequesteredInfernoL,
    CollapsedPassageR, MagmaPumpL, ReservoirMaintenanceTunnelR, IntakePumpR,
    ThermalReservoir1R, GeneratorAccessTunnelL, ElevatorToMagmaLakeR,
    MagmaPumpAccessR, FieryGalleryL, RagingPitL, HollowChamberR, PlacidPoolR,
    SporousNookL, RockyRidgeTrailL, TramToSuziIslandR
) = area_doors_unpackable

(
    Missile, Super, PowerBomb, Morph, Springball, Bombs, HiJump,
    Varia, GravitySuit, Wave, SpeedBooster, Spazer, Ice,
    Plasma, Screw, Charge, Grapple, SpaceJump, Energy, Reserve, Xray
) = items_unpackable

energy200 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 1
))

energy300 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 2
))
energy400 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 3
))
energy500 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 4
))
energy600 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 5
))
energy700 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 6
))
energy800 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 7
))
energy900 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 8
))
energy1000 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve)) >= 9
))
energy1200 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve))  >= 11
))
energy1500 = LogicShortcut(lambda loadout: (
    (loadout.count(Items.Energy) + loadout.count(Items.Reserve))  >= 14
))
hellrun1 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy200 in loadout)
))
hellrun3 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy400 in loadout)
))
hellrun4 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy500 in loadout)
))
hellrun5 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy600 in loadout)
))
hellrun7 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy600 in loadout)
))
hellrun8 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy900 in loadout)
))


missile10 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Missile) * 5 >= 10
))
missile20 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Missile) * 5 >= 20
))


super10 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Super) * 5 >= 10
))
super15 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Super) * 5 >= 15
))
super30 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Super) * 5 >= 30
))
powerBomb10 = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    loadout.count(Items.PowerBomb) >= 2
))
powerBomb15 = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    loadout.count(Items.PowerBomb) >= 3
))
powerBomb25 = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    loadout.count(Items.PowerBomb) >= 5
))
canUseBombs = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    ((Bombs in loadout) or (PowerBomb in loadout))
))
canUsePB = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (PowerBomb in loadout)
))
canCF = LogicShortcut(lambda loadout: (
    (missile10 in loadout) and
    (super10 in loadout) and
    (powerBomb15 in loadout)
))
canBreakBlocks = LogicShortcut(lambda loadout: (
    #with bombs or screw attack, maybe without morph
    (canUseBombs in loadout) or
    (Screw in loadout)
))
pinkDoor = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (
        (Missile in loadout) or
        (Super in loadout)
        )
))
canIBJ = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (Bombs in loadout)
))
canSBJ = LogicShortcut(lambda loadout: (
    (Springball in loadout) and
    (Morph in loadout)
))
canHighSBJ = LogicShortcut(lambda loadout: (
    (Springball in loadout) and
    (Morph in loadout) and
    (HiJump in loadout)
))
canFly = LogicShortcut(lambda loadout: (
    (canIBJ in loadout) or
    (SpaceJump in loadout)
))
canSpeedOrFly = LogicShortcut(lambda loadout: (
    (canIBJ in loadout) or
    (SpaceJump in loadout) or
    (SpeedBooster in loadout)
))
canHop = LogicShortcut(lambda loadout: (
    (canUseBombs in loadout) or
    (
        (Morph in loadout) and
        (Springball in loadout)
    )
))
canFreezeOrangeFish = LogicShortcut(lambda loadout: (
    (Ice in loadout) and
    (
        (Charge in loadout) or
        (Plasma in loadout)
    )
))
leftSideCrateria = LogicShortcut(lambda loadout: (
    (pinkDoor in loadout) and
    (
        (canUseBombs in loadout) or
        (SpeedBooster in loadout)
    )
))
accessWS = LogicShortcut(lambda loadout: (
    (leftSideCrateria in loadout) and
    (Super in loadout) and
    ( #2 paths
        ( # from moat
            (
                (GravitySuit in loadout) and
                (
                    (Grapple in loadout) or
                    (SpeedBooster in loadout) or
                    (SpaceJump in loadout) or
                    (canIBJ in loadout) or
                    (HiJump in loadout)
                )
            ) or
            (   #can enter without gravity
                (HiJump in loadout) and
                (canSBJ in loadout) and
                (SpaceJump in loadout)
            ) or
            (
                (HiJump in loadout) and
                (Ice in loadout) and
                (SpaceJump in loadout)
            ) or
            (
                (HiJump in loadout) and
                (Ice in loadout) and
                (canIBJ in loadout) #epic spongebath
            )
        ) or
        ( #2nd path intended pancake house
            (SpeedBooster in loadout) and
            (
                (Grapple in loadout) or
                (SpaceJump in loadout)
            ) and
            (canUseBombs in loadout) #canHop?
        )
    )
)) 
eastBrinstar = LogicShortcut(lambda loadout: (
    #top route
    (
        (
            (canUseBombs in loadout) or
            (SpeedBooster in loadout)
        ) and
        (pinkDoor in loadout)
    ) or
    #creep highway
    (canUsePB in loadout)
    #red tower is implied by bomb/speed and missile doors
))
redTower = LogicShortcut(lambda loadout: (
    (
        (canUseBombs in loadout) or
        (SpeedBooster in loadout)
    ) and
    (pinkDoor in loadout)
))
twinStatues = LogicShortcut(lambda loadout: (
    (canUsePB in loadout) and
    (pinkDoor in loadout) and
    #flowerhead / poo balls options
    (
        (
            (
                (Grapple in loadout) or
                (SpaceJump in loadout) or
                (Ice in loadout) or
                (HiJump in loadout) or
                (canSBJ in loadout)
            ) and
            (
                (super10 in loadout) or
                (
                    (Charge in loadout) and
                    (Wave in loadout)
                ) or
                (Plasma in loadout)
            )
        ) or
        (
            (GravitySuit in loadout) and
            (SpeedBooster in loadout)
        )
    )
    #wave optional?
))
eastMaridia = LogicShortcut(lambda loadout: (
    (twinStatues in loadout) and
    (HiJump in loadout)
))
kraid = LogicShortcut(lambda loadout: (
    (twinStatues in loadout) and
    (SpeedBooster in loadout) and
    (Super in loadout) and
    (
        (Missile in loadout) or
        (Charge in loadout)
    )
))
phantoon = LogicShortcut(lambda loadout: (
    (accessWS in loadout) and
    (energy200 in loadout) and
    #pulverizer
    (
        (Ice in loadout) or
        (SpaceJump in loadout) or
        (canSBJ in loadout) or
        (
            (GravitySuit in loadout) and
            (canUsePB in loadout)
        )
    ) and
    #morph options
    # might be based on bad intel
    (
        (canUseBombs in loadout) or
        (
            (Morph in loadout) and
            (SpeedBooster in loadout) and
            (Wave in loadout)
        )
    )
))
upperNorfair = LogicShortcut(lambda loadout: (
    #from borderlands
    (leftSideCrateria in loadout) and
    (canUseBombs in loadout)
))
backdoorMaridia = LogicShortcut(lambda loadout: (
    (phantoon in loadout) and
    (
        (GravitySuit in loadout) or
        (
            (SpaceJump in loadout) and
            (HiJump in loadout) and
            (Grapple in loadout)
        )
    )
))
crabStairway = LogicShortcut(lambda loadout: (
    (
        (backdoorMaridia in loadout) and
        (canUsePB in loadout)
    ) or
    (
        (eastMaridia in loadout) and
        ( # from super chozo
            (GravitySuit in loadout) or
            ( # suitless aquaman
                (HiJump in loadout) and
                (canFreezeOrangeFish in loadout)
            )
        )
    )
))
fortress = LogicShortcut(lambda loadout: (
    (crabStairway in loadout) and
    #can grav jump crab stairway 
    (
        (GravitySuit in loadout) or
        (
        # crab stairway to fortress suitless, options:
            (HiJump in loadout) and
            (
                (
                    (canFreezeOrangeFish in loadout) and
                    (Grapple in loadout)
                ) or
                (
                    (canSBJ in loadout) and
                    (Grapple in loadout)
                ) or
                (
                    (canSBJ in loadout) and
                    (canFreezeOrangeFish in loadout)
                )
            )
        )
    )
))
suitlessMaridia = LogicShortcut(lambda loadout: (
    # to pass fortress
    (fortress in loadout) and
    (
        (GravitySuit in loadout) or
        (
            (HiJump in loadout) and
            (Grapple in loadout)
        )
        # are there others? they probably failed...
        # double SBJ fortress? doubt
    )
))
draygon = LogicShortcut(lambda loadout: (
    (suitlessMaridia in loadout) and
    (SpeedBooster in loadout) and
    (Super in loadout) and
    (energy500 in loadout)
))
lavaDive = LogicShortcut(lambda loadout: (
    (leftSideCrateria in loadout) and
    (canUseBombs in loadout) and
    (
        # old draygon option OUT
        # here are the real lava dive options
        (
            (Varia in loadout) and
            (energy900 in loadout) and
            (HiJump in loadout)
        ) or
        (  
            (GravitySuit in loadout) and
            (Varia in loadout) and
            (energy400 in loadout)
        )
    )
))
defeatGT = LogicShortcut(lambda loadout: (
    (lavaDive in loadout) and
    # need space & speed or supers to GGG
    (
        (
            (SpaceJump in loadout) and
            (SpeedBooster in loadout)
        ) or
        (Super in loadout)
    ) and
    # also defeat GT
    (
        (Charge in loadout) or
        (super10 in loadout)
    )
))
lowerNorfair = LogicShortcut(lambda loadout: (
    (lavaDive in loadout) and
    (SpaceJump in loadout) and
    (energy800 in loadout)
))


area_logic: AreaLogicType = {
    "Early": {
        # using SunkenNestL as the hub for this area, so we don't need a path from every door to every other door
        # just need at least a path with sunken nest to and from every other door in the area
        ("CraterR", "SunkenNestL"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "CraterR"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "RuinedConcourseBL"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "RuinedConcourseTR"): lambda loadout: (
            True
            # TODO: Expert needs energy and casual doesn't? And Casual can do it with supers, but expert can't?
        ),   
    },
}


location_logic: LocationLogicType = {
    "Bomb Torizo Bombs": lambda loadout: (
        (Morph in loadout) and
        (pinkDoor in loadout) and
        (Bombs in loadout)
    ),
    "Varia Elevator Top Missile": lambda loadout: (
        (leftSideCrateria in loadout) and
        (canUseBombs in loadout)
    ),
    "Cliff Chozo Missile": lambda loadout: (
        ( #get there
            (canUseBombs in loadout) or
            (SpeedBooster in loadout)
        ) and
        # get up there
        (
            (SpeedBooster in loadout) or
            (SpaceJump in loadout) or
            (canIBJ in loadout) or
            (HiJump in loadout)
        )
    ),
    "Crateria Power Bomb": lambda loadout: (
        (canUsePB in loadout) and
        (Super in loadout)
    ),
    "Old Mother Brain Missile": lambda loadout: (
        (leftSideCrateria in loadout) and
        (pinkDoor in loadout)
    ),
    "Mushroom Cave Energy Tank": lambda loadout: (
        (eastBrinstar in loadout)
    ),
    "Mushroom Cave Missile": lambda loadout: (
        (eastBrinstar in loadout) and
        (SpeedBooster in loadout)
    ),
    "Lake Tank Energy Tank": lambda loadout: (
        (leftSideCrateria in loadout)
    ),
    "Grapple Cave Missile": lambda loadout: (
        (leftSideCrateria in loadout) and
        (Grapple in loadout)
    ),
    "Ocean Missile": lambda loadout: (
        (phantoon in loadout) and
        (SpeedBooster in loadout) and
        (GravitySuit in loadout)
    ),
    "Pancake House Missile": lambda loadout: (
        (leftSideCrateria in loadout) and
        (canUseBombs in loadout) and
        (
            (
                #traditional
                (SpeedBooster in loadout) and
                (Super in loadout)
            ) or
            # enter above the water
            # copied from moat :D
            (
                (GravitySuit in loadout) and
                (
                    (Grapple in loadout) or
                    (SpeedBooster in loadout) or
                    (SpaceJump in loadout) or
                    (canIBJ in loadout) or
                    (HiJump in loadout)
                )
            ) or
            (   #can enter without gravity
                (HiJump in loadout) and
                (canSBJ in loadout) and
                (SpaceJump in loadout)
            ) or
            (
                (HiJump in loadout) and
                (Ice in loadout) and
                (SpaceJump in loadout)
            ) or
            (
                (HiJump in loadout) and
                (Ice in loadout) and
                (canIBJ in loadout) #epic spongebath
            )
        )
    ),
    "Creep Highway Missile": lambda loadout: (
        (SpeedBooster in loadout) or
        (canIBJ in loadout) or
        (SpaceJump in loadout) or
        (HiJump in loadout) or
        (canSBJ in loadout) or
        (Ice in loadout)
    ),
    "Red Bluff Super Missile": lambda loadout: (
        (canUsePB in loadout) and
        (Super in loadout)
    ),
    "Varia Suit": lambda loadout: (
        (leftSideCrateria in loadout) and
        (pinkDoor in loadout)
    ),
    "Retro Brinstar Power Bomb": lambda loadout: (
        (SpeedBooster in loadout)
    ),
    "Retro Brinstar Super Missile": lambda loadout: (
        (SpeedBooster in loadout) or
        (
            (eastBrinstar in loadout) and
            (Super in loadout) and
            (Morph in loadout)
        ) 
        # no treasure island needed ...blame rusty
    ),
    "Construction Zone Missile": lambda loadout: (
        (Morph in loadout)
    ),
    "Morph Ball": lambda loadout: (
        True
    ),
    "Chozo Stash Missile": lambda loadout: (
        (Morph in loadout)
    ),
    "Brinstar Pirate Cage Missile": lambda loadout: (
        (twinStatues in loadout) and
        (SpeedBooster in loadout)
    ),
    "Clubhouse Super Missile": lambda loadout: (
        (eastBrinstar in loadout) and
        ( # treasure island side
            (Ice in loadout) or
            (SpaceJump in loadout) or
            (canHighSBJ in loadout) or
            (SpeedBooster in loadout) or
            # clubhouse pink door
            (pinkDoor in loadout)
        ) and
        (Morph in loadout) and
        (
            (Super in loadout) or
            (
                (SpeedBooster in loadout) and
                (canUsePB in loadout)
            )
        )
    ),
    "Xray": lambda loadout: (
        (leftSideCrateria in loadout) and
        (canUsePB in loadout)
    ),
    "Sidehopper Alley Missile": lambda loadout: (
        (eastBrinstar in loadout) and
        (canUseBombs in loadout) and
        (pinkDoor in loadout)
    ),
    "Spazer": lambda loadout: (
        (twinStatues in loadout) and
        (pinkDoor in loadout) and
        (canUseBombs in loadout)
    ),
    "Hellraiser Missile": lambda loadout: (
        (twinStatues in loadout) and
        (Super in loadout) and
        (SpeedBooster in loadout)
    ),
    "Irrigation Energy Tank": lambda loadout: (
        (eastBrinstar in loadout) and
        (canUsePB in loadout) and
        (GravitySuit in loadout) and
        (SpeedBooster in loadout)
        # no backdoor allowed >:(
    ),
    "Grapple Beam": lambda loadout: (
        (kraid in loadout)
    ),
    "Kraid Energy Tank": lambda loadout: (
        (kraid in loadout)
    ),
    "Four Punks Power Bomb": lambda loadout: (
        (kraid in loadout)
    ),
    "Ripper Hangout Missile": lambda loadout: (
        (leftSideCrateria in loadout)
    ),
    "Red Tower Secret Missile": lambda loadout: (
        (leftSideCrateria in loadout) and
        (canUsePB in loadout)
    ),
    "Red Tower Secret Power Bomb": lambda loadout: (
        (leftSideCrateria in loadout) and
        (canUsePB in loadout) and
        (Super in loadout)
    ),
    "Red Bull Missile": lambda loadout: (
        (leftSideCrateria in loadout) and
        (Morph in loadout) and
        (
            (SpeedBooster in loadout) or
            (SpaceJump in loadout) or
            (Springball in loadout)
        )
    ),
    "Red Bull Energy Tank": lambda loadout: (
        (leftSideCrateria in loadout) and
        (Morph in loadout) and
        (
            (SpeedBooster in loadout) or
            (SpaceJump in loadout) or
            (Springball in loadout)
        )
    ),
    "Cactus Trap Energy Tank": lambda loadout: (
        (leftSideCrateria in loadout) and
        (canUsePB in loadout)
        # maybe a way with wave beam and bombs -___-
    ),
    "Dragon Spark Missile": lambda loadout: (
        (eastBrinstar in loadout) and
        (SpeedBooster in loadout)
    ),
    "Wife Missile": lambda loadout: (
        (eastBrinstar in loadout) and
        (Super in loadout) and
        (
            (canUseBombs in loadout) or
            (
                (Morph in loadout) and
                (
                    (Spazer in loadout) or
                    (Wave in loadout)
                )
            )
        )
    ),
    "Husband Missile": lambda loadout: (
        (eastBrinstar in loadout) and
        (Morph in loadout) and
        (Super in loadout)
    ),
    "Flowerhead Power Bomb": lambda loadout: (
        (canUsePB in loadout) and
        (Grapple in loadout) and
        # boss skip
        (
            (
                (GravitySuit in loadout) and
                (SpeedBooster in loadout)
            ) or
            # poo balls
            (
                (
                    (Charge in loadout) and
                    (Wave in loadout)
                ) or
                (Plasma in loadout) or
                (super10 in loadout)
            )
        )
    ),
    "Charge Beam": lambda loadout: (
        (eastBrinstar in loadout) and
        (canUseBombs in loadout) and
        (pinkDoor in loadout)
    ),
    "Elevator Cave Power Bomb": lambda loadout: (
        (canUsePB in loadout)
    ),
    "Pet Slug Missile": lambda loadout: (
        (eastBrinstar in loadout) and
        (canUseBombs in loadout)
    ),
    "Crumble Bridge Super Missile": lambda loadout: (
        (canUsePB in loadout)
    ),
    "Kihunter Alley Missile": lambda loadout: (
        (eastBrinstar in loadout) and
        (Morph in loadout)
        # big green dboost with nothing
    ),
    "Treasure Island Missile": lambda loadout: (
        (eastBrinstar in loadout) and
        (Morph in loadout) and
        ( # left side
            (Ice in loadout) or
            (SpaceJump in loadout) or
            (canHighSBJ in loadout) or
            (SpeedBooster in loadout) or
            # clubhouse moat 2
            (pinkDoor in loadout)
        )
    ),
    "Super Secret Save Energy Tank": lambda loadout: (
        (eastBrinstar in loadout)
    ),
    "Brinstar Reserve Tank": lambda loadout: (
        (eastBrinstar in loadout) and
        (
            (canUseBombs in loadout) or
            (SpeedBooster in loadout) or
            (SpaceJump in loadout)
        )
        # rip springball bop
    ),
    "Crocomire Missile": lambda loadout: (
        (upperNorfair in loadout) and
        (hellrun8 in loadout) and
        (Super in loadout) and
        (
            (Wave in loadout) or
            (canUsePB in loadout) or
            (SpeedBooster in loadout)
        )
    ),
    "Bubble Road of Pain Missile": lambda loadout: (
        (lowerNorfair in loadout) and
        (canUsePB in loadout)
    ),
    "Bird Cage Missile": lambda loadout: (
        (lowerNorfair in loadout)
    ),
    "Screw Attack": lambda loadout: (
        (defeatGT in loadout) and
        (Super in loadout)
    ),
    "Kago Missile": lambda loadout: (
        (lowerNorfair in loadout) and
        (Super in loadout) and
        (SpeedBooster in loadout)
    ),
    "Pink Cage Missile": lambda loadout: (
        (lowerNorfair in loadout) and
        (Super in loadout) and
        (SpeedBooster in loadout) and
        (
            (Grapple in loadout) or
            (Xray in loadout)
        )
    ),
    "Ridley Energy Tank": lambda loadout: (
        (lowerNorfair in loadout) and
        (Super in loadout) and
        (SpeedBooster in loadout) and
        (
            (Grapple in loadout) or
            (Xray in loadout)
        ) and
        (Charge in loadout) and
        (energy400 in loadout) # cowards
    ),
    "Lava Dive Energy Tank": lambda loadout: (
        (leftSideCrateria in loadout) and
        (canUsePB in loadout) and
        (Varia in loadout) and
        (GravitySuit in loadout)
        # easy
    ),
    "Crocomire Power Bomb": lambda loadout: (
        (upperNorfair in loadout) and
        (canUsePB in loadout)
    ),
    "Factory Energy Tank": lambda loadout: (
        (upperNorfair in loadout) and
        (Super in loadout)
    ),
    "Borderlands Missile": lambda loadout: (
        (upperNorfair in loadout) and
        (hellrun4 in loadout)
    ),
    "Pool Party Missile": lambda loadout: (
        (upperNorfair in loadout) and
        (hellrun8 in loadout) and
        (SpeedBooster in loadout) and
        (Super in loadout)
    ),
    "Norfair Entrance Missile": lambda loadout: (
        (leftSideCrateria in loadout) and
        (
            (canUseBombs in loadout) or
            (
                (SpeedBooster in loadout) and
                (HiJump in loadout)
            )
        )
    ),
    "Pain Missile": lambda loadout: (
        (leftSideCrateria in loadout) and
        (canUsePB in loadout) and
        (
            (
                (hellrun4 in loadout) and
                (SpaceJump in loadout) and
                (Screw in loadout)
            ) or
            (
                (Varia in loadout) and
                (energy500 in loadout)
            )
        )
    ),
    "HiJump Missile": lambda loadout: (
        (leftSideCrateria in loadout) and
        (canUseBombs in loadout)
    ),
    "HiJump Boots": lambda loadout: (
        (leftSideCrateria in loadout) and
        (canUseBombs in loadout)
    ),
    "Norfair Reserve Tank": lambda loadout: (
        (upperNorfair in loadout) and
        (Super in loadout) and
        (canUsePB in loadout) and
        (hellrun4 in loadout)
    ),
    "Lava Chozo Missile": lambda loadout: (
        (upperNorfair in loadout) and
        (Super in loadout) and
        (hellrun4 in loadout)
    ),
    "Early Super Missile": lambda loadout: (
        (upperNorfair in loadout) and
        (hellrun4 in loadout)
    ),
    "Dentist Missile": lambda loadout: (
        (upperNorfair in loadout) and
        (hellrun8 in loadout) and
        (Super in loadout)
    ),
    "Spikesuit Power Bomb": lambda loadout: (
        (upperNorfair in loadout) and
        (hellrun4 in loadout) and
        (canUsePB in loadout) and
        (Super in loadout)
    ),
    "Hideout Energy Tank": lambda loadout: (
        (upperNorfair in loadout) and
        (hellrun4 in loadout) and
        (canUseBombs in loadout)
    ),
    "Fire Island Missile": lambda loadout: (
        (upperNorfair in loadout) and
        (hellrun4 in loadout) and
        (Super in loadout)
    ),
    "Thats Cool Missile": lambda loadout: (
        (upperNorfair in loadout) and
        (hellrun8 in loadout) and
        (Super in loadout)
    ),
    "Dragon Lake Missile": lambda loadout: (
        (upperNorfair in loadout) and
        (Super in loadout) and
        (hellrun4 in loadout)
    ),
    "Ice Beam": lambda loadout: (
        (upperNorfair in loadout) and
        (Super in loadout) and
        (hellrun4 in loadout)
    ),
    "Farm Chozo Missile": lambda loadout: (
        (upperNorfair in loadout) and
        (hellrun8 in loadout) and
        (Super in loadout) and 
        (SpeedBooster in loadout) and
        (
            (Wave in loadout) or
            (canFly in loadout)
        ) # wave area, no projection
    ),
    "Wave Beam": lambda loadout: (
        (upperNorfair in loadout) and
        (hellrun8 in loadout) and
        (Super in loadout) and
        (
            (Wave in loadout) or
            (canFly in loadout)
        ) # wave area, no projection
    ),
    "Gravity Suit": lambda loadout: (
        (phantoon in loadout) and
        (canUseBombs in loadout) and
        (
            (
                (Grapple in loadout) and
                (Ice in loadout) and
                (HiJump in loadout)
            ) or
            (SpaceJump in loadout) or
            (GravitySuit in loadout)
        )
    ),
    "Gutterball Super Missile": lambda loadout: (
        (phantoon in loadout) and
        (canUsePB in loadout)
    ),
    "Chozo Jail Missile": lambda loadout: (
        (phantoon in loadout)
    ),
    "Wrecked Ship Reserve Tank": lambda loadout: (
        (phantoon in loadout) and
        (Super in loadout) and
        (canFly in loadout) and
        (
            (GravitySuit in loadout) or
            (
                (SpaceJump in loadout) and
                (HiJump in loadout) and
                (Grapple in loadout)
            )
        )
    ),
    "Broken Hold Missile": lambda loadout: (
        (phantoon in loadout) and
        (canUseBombs in loadout)
    ),
    "Tenderizer Power Bomb": lambda loadout: (
        (accessWS in loadout) and
        (canUseBombs in loadout) and
        (
            (HiJump in loadout) or
            (SpeedBooster in loadout) or
            (canSBJ in loadout) or
            (GravitySuit in loadout)
        )
    ),
    "Pancake Drop Energy Tank": lambda loadout: (
        (phantoon in loadout) and
        (canUsePB in loadout)
    ),
    "Poopdeck Missile": lambda loadout: (
        (phantoon in loadout) and
        (
            (
                (canUseBombs in loadout) or
                (SpaceJump in loadout)
            ) or
            (
                (canUsePB in loadout) and
                (HiJump in loadout)
            ) or
            (GravitySuit in loadout)
        ) # might be wrong, consider ship off or post-phan
    ),
    "Piranha Tank Super Missile": lambda loadout: (
        (phantoon in loadout) and
        (canUsePB in loadout) and
        (
            (HiJump in loadout) or
            (GravitySuit in loadout)
        )
    ),
    "Kitchen Missile": lambda loadout: (
        (accessWS in loadout) and
        (canUseBombs in loadout) and
        (
            (Springball in loadout) or
            (GravitySuit in loadout)
        )
    ),
    "Shaktool Reserve Tank": lambda loadout: (
        (eastMaridia in loadout)
    ),
    "Sandfall Secret Missile": lambda loadout: (
        (eastMaridia in loadout)
    ),
    "Speed Booster": lambda loadout: (
        (eastMaridia in loadout)
    ),
    "Sandpit Power Bomb": lambda loadout: (
        (suitlessMaridia in loadout)
    ),
    "Farmhouse Energy Tank": lambda loadout: (
        (fortress in loadout) and
        (
            (Plasma in loadout) or
            (
                (GravitySuit in loadout) and
                (Screw in loadout)
            )
        )
    ),
    "Springball": lambda loadout: (
        (
            (suitlessMaridia in loadout) or
            (backdoorMaridia in loadout)
        ) and
        (GravitySuit in loadout) and
        (Super in loadout) and
        (SpeedBooster in loadout)
    ),
    "Aquaman Super Missile": lambda loadout: (
        (eastMaridia in loadout)
    ),
    "Sunken Save Station Missile": lambda loadout: (
        (crabStairway in loadout)
    ),
    "Tor Missile": lambda loadout: (
        (suitlessMaridia in loadout) or
        (
            (backdoorMaridia in loadout) and
            (canUsePB in loadout)
        )
    ),
    "Pink Pirate House Missile": lambda loadout: (
        (fortress in loadout) and
        (
            (canSBJ in loadout) or
            (GravitySuit in loadout)
        )

    ),
    "Everest Missile": lambda loadout: (
        (
            (eastMaridia in loadout) and
            (GravitySuit in loadout)
        ) or
        (
            (fortress in loadout) and
            (Grapple in loadout)
        )
    ),
    "Mama Turtle Right Missile": lambda loadout: (
        (fortress in loadout)
    ),
    "Mama Turtle Left Missile": lambda loadout: (
        (fortress in loadout) and
        (GravitySuit in loadout) and
        (SpeedBooster in loadout)
    ),
    "Blue Bull Missile": lambda loadout: (
        (fortress in loadout) and
        (Super in loadout)
    ),
    "Fortress Missile": lambda loadout: (
        (fortress in loadout)
    ),
    "Eden Missile": lambda loadout: (
        (fortress in loadout) and
        (canUsePB in loadout) and
        (HiJump in loadout) and
        (canFly in loadout)

    ),
    "Purple Guy Missile": lambda loadout: (
        (fortress in loadout) and
        (
            (GravitySuit in loadout) or
            (Springball in loadout)
        )
    ),
    "Tube Spark Super Missile": lambda loadout: (
        (
            (suitlessMaridia in loadout) or
            (backdoorMaridia in loadout)
        ) and
        (canUsePB in loadout) and
        (GravitySuit in loadout) and
        (
            (SpeedBooster in loadout) or
            (Xray in loadout)
        ) and
        (Super in loadout)
    ),
    "Pipe Dream Super Missile": lambda loadout: (
        (draygon in loadout) and
        (GravitySuit in loadout)
    ),
    "Grapple Climb Missile": lambda loadout: (
        (suitlessMaridia in loadout)
    ),
    "Space Jump": lambda loadout: (
        (draygon in loadout)
    ),
    "Jailbird Missile": lambda loadout: (
        (
            (suitlessMaridia in loadout) or
            (backdoorMaridia in loadout)
        ) and
        (GravitySuit in loadout) and
        (
            (SpaceJump in loadout) or
            (canIBJ in loadout) or
            (canHighSBJ in loadout)   
        )

    ),
    "Evidence Energy Tank": lambda loadout: (
        (fortress in loadout)
    ),
    "Pre Crumble City Missile": lambda loadout: (
        (suitlessMaridia in loadout) or
        (backdoorMaridia in loadout)
    ),
    "Plasma Beam": lambda loadout: (
        (draygon in loadout)
    ),

}


class Expert(LogicInterface):
    area_logic: ClassVar[AreaLogicType] = area_logic
    location_logic: ClassVar[LocationLogicType] = location_logic

    @staticmethod
    def can_fall_from_spaceport(loadout: Loadout) -> bool:
        return True
