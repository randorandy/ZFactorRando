from typing import Iterable

Item = tuple[str, bytes, bytes, bytes, bytes]
""" Name, Visible, Chozo, Hidden, AmmoQty """


class Items:
    Missile = ("Missile",
               b"\xdb\xee",
               b"\x2f\xef",
               b"\x83\xef",
               b"\x00")
    Super = ("Super Missile",
             b"\xdf\xee",
             b"\x33\xef",
             b"\x87\xef",
             b"\x00")
    PowerBomb = ("Power Bomb",
                 b"\xe3\xee",
                 b"\x37\xef",
                 b"\x8b\xef",
                 b"\x00")
    Morph = ("Morph Ball",
             b"\x23\xef",
             b"\x77\xef",
             b"\xcb\xef",
             b"\x00")
    Springball = ("Springball", 
                 b"\x03\xef",
                 b"\x57\xef",
                 b"\xab\xef",
                 b"\x00")
    Bombs = ("Bombs",
             b"\xe7\xee",
             b"\x3b\xef",
             b"\x8f\xef",
             b"\x00")
    HiJump = ("HiJump", 
              b"\xf3\xee",
              b"\x47\xef",
              b"\x9b\xef",
              b"\x00")
    Varia = ("Varia Suit",
             b"\x07\xef",
             b"\x5b\xef",
             b"\xaf\xef",
             b"\x00")
    GravitySuit = ("Gravity Suit",
                   b"\x0b\xef",
                   b"\x5f\xef",
                   b"\xb3\xef",
                   b"\x00")
    Wave = ("Wave Beam",
            b"\xfb\xee",
            b"\x4f\xef",
            b"\xa3\xef",
            b"\x00")
    SpeedBooster = ("Speed Booster",
                    b"\xf7\xee",
                    b"\x4b\xef",
                    b"\x9f\xef",
                    b"\x00")
    Spazer = ("Spazer",
              b"\xff\xee",
              b"\x53\xef",
              b"\xa7\xef",
              b"\x00")
    Ice = ("Ice Beam",
           b"\xef\xee",
           b"\x43\xef",
           b"\x97\xef",
           b"\x00")
    Grapple = ("Grapple Beam",
               b"\x17\xef",
               b"\x6b\xef",
               b"\xbf\xef",
               b"\x00")
    Plasma = ("Plasma Beam",
              b"\x13\xef",
              b"\x13\xef",
              b"\xbb\xef",
              b"\x00")
    Screw = ("Screw Attack",
             b"\x1f\xef",
             b"\x73\xef",
             b"\xc7\xef",
             b"\x00")
    Charge = ("Charge Beam",
              b"\xeb\xee",
              b"\x3f\xef",
              b"\x93\xef",
              b"\x00")
    SpaceJump = ("Space Jump",
                 b"\x1b\xef",
                 b"\x6f\xef",
                 b"\xc3\xef",
                 b"\x00")
    Energy = ("Energy Tank",
              b"\xd7\xee",
              b"\x2b\xef",
              b"\x7f\xef",
              b"\x00")
    Reserve = ("Reserve Tank",
              b"\x27\xef",
              b"\x7b\xef",
              b"\xcf\xef",
              b"\x00")
    Xray = ("Xray",
            b"\x0f\xef",
            b"\x63\xef",
            b"\xb7\xef",
            b"\x00")

items_unpackable: Iterable[Item] = (
    Items.Missile, Items.Super, Items.PowerBomb, Items.Morph, Items.Springball, Items.Bombs,
    Items.HiJump, Items.Varia, Items.GravitySuit, Items.Wave, Items.SpeedBooster, Items.Spazer,
    Items.Ice, Items.Plasma, Items.Screw, Items.Charge, Items.Grapple,
    Items.SpaceJump, Items.Energy, Items.Reserve, Items.Xray
)

all_items: dict[str, Item] = {
    item[0]: item
    for item in items_unpackable
}
