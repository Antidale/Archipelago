from BaseClasses import ItemClassification
from typing import TypedDict, Dict


class ItemDict(TypedDict):
    classification: ItemClassification
    count: int
    name: str


item_table: Dict[int, ItemDict] = {
    # Things
    200622: {'classification': ItemClassification.filler,
             'count': 1,
             'name': 'DUBIOUS BERRY'},
    200623: {'classification': ItemClassification.filler,
             'count': 11,
             'name': 'BURRITO'},
    200624: {'classification': ItemClassification.filler,
             'count': 1,
             'name': 'COFFEE'},
    200625: {'classification': ItemClassification.filler,
             'count': 6,
             'name': 'SOUL SPONGE'},
    200626: {'classification': ItemClassification.useful,
             'count': 7,
             'name': 'MUSCLE APPLIQUE'},
    200627: {'classification': ItemClassification.filler,
             'count': 1,
             'name': 'POOLWINE'},
    200628: {'classification': ItemClassification.filler,
             'count': 3,
             'name': 'CUPCAKE'},
    200629: {'classification': ItemClassification.filler,
             'count': 3,
             'name': 'COOKIE'},
    200630: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'HOUSE KEY'},
    200631: {'classification': ItemClassification.filler,
             'count': 2,
             'name': 'MEAT'},
    200632: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'PNEUMATOPHORE'},
    200633: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'CAVE KEY'},
    200634: {'classification': ItemClassification.filler,
             'count': 6,
             'name': 'JUICE'},
    200635: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'DOCK KEY'},
    200636: {'classification': ItemClassification.filler,
             'count': 14,
             'name': 'BANANA'},
    200637: {'classification': ItemClassification.progression,
             'count': 3,
             'name': 'PAPER CUP'},
    200638: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'JAIL KEY'},
    200639: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'PADDLE'},
    200640: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'WORM ROOM KEY'},
    200641: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'BRIDGE KEY'},
    200642: {'classification': ItemClassification.filler,
             'count': 2,
             'name': 'STEM CELL'},
    200643: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'UPPER CHAMBER KEY'},
    200644: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'VESSEL ROOM KEY'},
    200645: {'classification': ItemClassification.filler,
             'count': 3,
             'name': 'CLOUD GERM'},
    200646: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'SKULL BOMB'},
    200647: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'TOWER KEY'},
    200648: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'DEEP KEY'},
    200649: {'classification': ItemClassification.filler,
             'count': 1,
             'name': 'MULTI-COFFEE'},
    200650: {'classification': ItemClassification.filler,
             'count': 4,
             'name': 'MULTI-JUICE'},
    200651: {'classification': ItemClassification.filler,
             'count': 3,
             'name': 'MULTI STEM CELL'},
    200652: {'classification': ItemClassification.filler,
             'count': 6,
             'name': 'MULTI SOUL SPONGE'},
    #200653: {'classification': ItemClassification.filler,
    #         'count': 1,
    #         'name': 'ANTENNA'},
    200654: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'UPPER HOUSE KEY'},
    200655: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'BOTTOMLESS JUICE'},
    200656: {'classification': ItemClassification.progression,
             'count': 3,
             'name': 'SAGE TOKEN'},
    200657: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'CLICKER'},

    # Garbs > Gloves
    200658: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'CURSED GLOVES'},
    200659: {'classification': ItemClassification.useful,
             'count': 5,
             'name': 'LONG GLOVES'},
    200660: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'BRAIN DIGITS'},
    200661: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'MATERIEL MITTS'},
    200662: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'PLEATHER GAGE'},
    200663: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'PEPTIDE BODKINS'},
    200664: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'TELESCOPIC SLEEVE'},
    200665: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'TENDRIL HAND'},
    200666: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'PSYCHIC KNUCKLE'},
    200667: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'SINGLE GLOVE'},

    # Garbs > Accessories
    200668: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'FADED PONCHO'},
    200669: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'JUMPSUIT'},
    200670: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'BOOTS'},
    200671: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'CONVERTER WORM'},
    200672: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'COFFEE CHIP'},
    200673: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'RANCHER PONCHO'},
    200674: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'ORGAN FORT'},
    200675: {'classification': ItemClassification.useful,
             'count': 2,
             'name': 'LOOPED DOME'},
    200676: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'DUCTILE HABIT'},
    200677: {'classification': ItemClassification.useful,
             'count': 2,
             'name': 'TARP'},

    # Bones
    200686: {'classification': ItemClassification.filler,
             'count': 1,
             'name': '100 Bones'},
    200687: {'classification': ItemClassification.filler,
             'count': 1,
             'name': '50 Bones'}
}


gesture_item_table: Dict[int, ItemDict] = {
    200678: {'classification': ItemClassification.useful,
            'count': 1,
            'name': 'POROMER BLEB'},
    200679: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'SOUL CRISPER'},
    200680: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'TIME SIGIL'},
    200681: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'CHARGE UP'},
    200682: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'FATE SANDBOX'},
    200683: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'TELEDENUDATE'},
    200684: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'LINK MOLLUSC'},
    200685: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'BOMBO - GENESIS'},
    200688: {'classification': ItemClassification.useful,
             'count': 1,
             'name': 'NEMATODE INTERFACE'},
}


party_item_table: Dict[int, ItemDict] = {
    200689: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'Pongorma'},
    200690: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'Dedusmuln'},
    200691: {'classification': ItemClassification.progression,
             'count': 1,
             'name': 'Somsnosa'}
}

medallion_item_table: Dict[int, ItemDict] = {
    200692: {'classification': ItemClassification.filler,
             'count': 30,
             'name': '10 Bones'}
}