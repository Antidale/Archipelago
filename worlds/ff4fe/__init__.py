# world/mygame/__init__.py
import argparse
import json
import os
import pkgutil
import threading
from typing import Mapping, Any

import Utils
import settings
import typing

from .FreeEnterpriseForAP.FreeEnt.cmd_make import MakeCommand
from .options import FF4FEOptions  # the options we defined earlier
from .items import FF4FEItem, all_items, ItemData # data used below to add items to the World
from .locations import FF4FELocation, all_locations, LocationData  # same as above
from . import topology, flags
from .itempool import create_itempool
from . import events, items
from . import rules as FERules
from .Client import FF4FEClient
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Entrance, Item, ItemClassification, MultiWorld
from .rom import FF4FEProcedurePatch
from ..generic.Rules import set_rule, add_rule, forbid_item, add_item_rule


class FF4FEWebWorld(WebWorld):
    theme = "partyTime"


class FF4FESettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the MLSS US rom"""

        copy_to = "Final Fantasy II (USA) (Rev A).sfc"
        description = "FFII SNES 1.1 ROM File"
        md5s = ["27D02A4F03E172E029C9B82AC3DB79F7"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class FF4FEWorld(World):
    """Insert description of the world/game here."""
    game = "Final Fantasy IV Free Enterprise"
    options_dataclass = FF4FEOptions
    options: FF4FEOptions
    settings: typing.ClassVar[FF4FESettings]

    web = FF4FEWebWorld()
    topology_present = True
    base_id = 7191991
    item_name_to_id = {item.name: id for
                       id, item in enumerate(all_items, base_id)}
    location_name_to_id = {location.name: id for
                           id, location in enumerate(all_locations, base_id)}
    chosen_character = "None"
    item_name_groups = items.item_name_groups


    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.rom_name_available_event = threading.Event()

    def generate_early(self) -> None:
        self.options.local_items.value.update(
            ["Cecil", "Kain", "Rydia", "Tellah", "Edward", "Rosa",
             "Yang", "Palom", "Porom", "Cid", "Edge", "Fusoya", "None"])
        pass

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        overworld = Region("Overworld", self.player, self.multiworld)
        underworld = Region("Underworld", self.player, self.multiworld)
        moon = Region("Moon", self.player, self.multiworld)

        self.multiworld.regions.append(overworld)
        self.multiworld.regions.append(underworld)
        self.multiworld.regions.append(moon)

        menu.connect(overworld)
        overworld.connect(underworld, "Underworld Access", lambda state: state.has("Hook", self.player)
                                                                         or state.has("Magma Key", self.player))
        overworld.connect(moon, "Moon Access", lambda state: state.has("Darkness Crystal", self.player))


        for area in topology.areas:
            new_region = Region(area, self.player, self.multiworld)
            self.multiworld.regions.append(new_region)
            if area in topology.overworld_areas:
                overworld.connect(new_region, "Overworld to " + area)
            if area in topology.hook_areas:
                underworld.connect(new_region, "Hook route to " + area, lambda state: state.has("Hook", self.player))
            if area in topology.underworld_areas:
                underworld.connect(new_region, "Underworld to " + area)
            if area in topology.moon_areas:
                moon.connect(new_region, "Moon to " + area)

        for location in all_locations:
            region = self.multiworld.get_region(location.area, self.player)
            new_location = FF4FELocation(self.player, location.name, self.location_name_to_id[location.name], region)
            region.locations.append(new_location)

        for event in events.boss_events:
            region = self.multiworld.get_region(event.area, self.player)
            new_location = FF4FELocation(self.player, event.name, None, region)
            region.locations.append(new_location)

    def create_item(self, item: str) -> FF4FEItem:
        item_data: ItemData = [item_data for item_data in all_items if item_data.name == item].pop()
        return FF4FEItem(item, item_data.classification, self.item_name_to_id[item], self.player)

    def create_event(self, event: str) -> FF4FEItem:
        # while we are at it, we can also add a helper to create events
        return FF4FEItem(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        exclude = [item for item in self.multiworld.precollected_items[self.player] if item != "None"]
        item_pool_result = create_itempool(locations.all_locations, self)
        item_pool = item_pool_result[0]
        self.chosen_character = item_pool_result[1]
        chosen_character_placed = False

        for item in map(self.create_item, item_pool):
            if item.name == self.chosen_character and chosen_character_placed == False:
                chosen_character_placed = True
                continue
            if item in exclude:
                exclude.remove(item)  # this is destructive. create unique list above
                self.multiworld.push_precollected(self.create_item(self.multiworld.random.choice(items.filler_items).name))
            else:
                self.multiworld.itempool.append(item)

    def set_rules(self) -> None:
        # TODO: Add in restriction to useful or above for later game areas
        for location in locations.character_locations:
            add_item_rule(self.multiworld.get_location(location, self.player),
                     lambda item: item.name in items.characters and item.player == self.player)
            if self.options.NoFreeCharacters.current_key == "true":
                if location in locations.free_character_locations:
                    add_item_rule(self.multiworld.get_location(location, self.player),
                                  lambda item: item.name == "None")
            if self.options.NoEarnedCharacters.current_key == "true":
                if location in locations.earned_character_locations:
                    add_item_rule(self.multiworld.get_location(location, self.player),
                                  lambda item: item.name == "None")

        for location in locations.all_locations:
            if location.name not in locations.character_locations:
                add_item_rule(self.multiworld.get_location(location.name, self.player),
                              lambda item: item.name not in items.characters)

        if self.chosen_character != "None":
            self.multiworld.get_location("Starting Character 1", self.player).place_locked_item(
                self.create_item(self.chosen_character))

        set_rule(self.multiworld.get_location("Zeromus", self.player),
                 lambda state: (state.has("Pass", self.player)
                                or state.has("Darkness Crystal", self.player))
                               and state.has("Crystal", self.player))

        for location in [location for location in all_locations]:
            if location.area in topology.hook_areas:
                add_rule(self.multiworld.get_location(location.name, self.player),
                         lambda state: state.has("Hook", self.player))
            if location.area in topology.underworld_areas:
                add_rule(self.multiworld.get_location(location.name, self.player),
                         lambda state: state.has("Hook", self.player) or state.has("Magma Key", self.player))
            if location.area in topology.moon_areas:
                add_rule(self.multiworld.get_location(location.name, self.player),
                         lambda state: state.has("Darkness Crystal", self.player))
                if self.options.UnsafeKeyItemPlacement.current_key == "true":
                    add_rule(self.multiworld.get_location(location.name, self.player),
                             lambda state: state.has("Hook", self.player) or state.has("Magma Key", self.player))
            if location.area in FERules.area_rules.keys():
                for requirement in FERules.area_rules[location.area]:
                    add_rule(self.multiworld.get_location(location.name, self.player),
                             lambda state, true_requirement=requirement: state.has(true_requirement, self.player))
            if location.major_slot:
                add_item_rule(self.multiworld.get_location(location.name, self.player),
                         lambda item: (item.classification & (ItemClassification.useful | ItemClassification.progression)) > 0)
            for i in range(len(FERules.location_tiers.keys())):
                if location.area in FERules.location_tiers[i]:
                    add_rule(self.multiworld.get_location(location.name, self.player),
                             lambda state, tier=i: state.has_group("characters",
                                                           self.player,
                                                           FERules.logical_gating[tier]["characters"]) and
                                           state.has_group("key_items",
                                                           self.player,
                                                           FERules.logical_gating[tier]["key_items"]))

        for location in [event for event in events.boss_events]:
            if location.area in topology.hook_areas:
                add_rule(self.multiworld.get_location(location.name, self.player),
                         lambda state: state.has("Hook", self.player))
            if location.area in topology.underworld_areas:
                add_rule(self.multiworld.get_location(location.name, self.player),
                         lambda state: state.has("Hook", self.player) or state.has("Magma Key", self.player))
            if location.area in topology.moon_areas:
                add_rule(self.multiworld.get_location(location.name, self.player),
                         lambda state: state.has("Darkness Crystal", self.player))
                if self.options.UnsafeKeyItemPlacement.current_key == "true":
                    add_rule(self.multiworld.get_location(location.name, self.player),
                             lambda state: state.has("Hook", self.player) or state.has("Magma Key", self.player))
            if location.name in FERules.boss_rules.keys():
                for requirement in FERules.boss_rules[location.name]:
                    add_rule(self.multiworld.get_location(location.name, self.player),
                             lambda state, true_requirement=requirement: state.has(true_requirement, self.player))
            for i in range(len(FERules.location_tiers.keys())):
                if location.area in FERules.location_tiers[i]:
                    add_rule(self.multiworld.get_location(location.name, self.player),
                             lambda state, tier=i: state.has_group("characters",
                                                           self.player,
                                                           FERules.logical_gating[tier]["characters"]) and
                                           state.has_group("key_items",
                                                           self.player,
                                                           FERules.logical_gating[tier]["key_items"]))

        for location in FERules.individual_location_rules.keys():
            for requirement in FERules.individual_location_rules[location]:
                add_rule(self.multiworld.get_location(location, self.player),
                         lambda state, true_requirement=requirement: state.has(true_requirement, self.player))

        for event in events.boss_events:
            self.multiworld.get_location(event.name, self.player).place_locked_item((
                self.create_event(event.name + " Defeated")
            ))

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Zeromus Defeated", self.player)


    def generate_output(self, output_directory: str) -> None:
        self.rom_name_text = f'4FE{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}'
        self.rom_name_text = self.rom_name_text[:20]
        self.rom_name = bytearray(self.rom_name_text, 'utf-8')
        self.rom_name.extend([0] * (20 - len(self.rom_name)))
        self.rom_name_available_event.set()
        placement_dict = self.create_placement_file(str(self.rom_name_text))
        placement_dict["seed"] = self.player + self.multiworld.seed
        placement_dict["output_file"] = f'{self.multiworld.get_out_file_name_base(self.player)}' + '.sfc'
        placement_dict["flags"] = flags.create_flags_from_options(self.options)

        patch = FF4FEProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        patch.write_file("placement_file.json" , json.dumps(placement_dict).encode("UTF-8"))
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = {
            "DarkMatterHunt": self.options.HeroChallenge.current_key,
            "NoEarnedCharacters": self.options.NoEarnedCharacters.current_key,
            "NoFreeCharacters": self.options.NoEarnedCharacters.current_key,
            "PassEnabled": self.options.PassEnabled.current_key
        }
        return slot_data

    def create_flags_from_options(self):
        hero_challenge_flags = ""
        if self.options.HeroChallenge.current_key != "none":
            hero_challenge_flags = f"hero/start:{self.options.HeroChallenge.current_key.lower()}/"
        dark_matter_flags = "Onone"
        if self.options.DarkMatterHunt.current_key == "true":
            dark_matter_flags = f"Omode:dkmatter"
        free_character_flags = ""
        if self.options.NoFreeCharacters.current_key == "true":
            free_character_flags += "nofree/"
        if self.options.NoEarnedCharacters.current_key == "true":
            free_character_flags += "noearned/"
        default_flags = (f"{dark_matter_flags} "
                         f"Kmain/summon/moon/unsafe "
                         f"Pshop/key "
                         f"Crelaxed/{hero_challenge_flags}{free_character_flags}j:spells,abilities "
                         f"Twild/junk "
                         f"Swild "
                         f"Bstandard/alt:gauntlet/whichburn "
                         f"Etoggle/keep:doors,behemoths "
                         f"Gnone "
                         f"-spoon")
        return default_flags

    def create_placement_file(self, rom_name):
        placement_dict = {"rom_name": rom_name}
        for location in self.multiworld.get_filled_locations(self.player):
            if location.name in events.boss_slot_names:
                continue
            location_data = [loc for loc in all_locations if loc.name == location.name].pop()
            if location.item.player == self.player:
                item_data = [item for item in all_items if item.name == location.item.name].pop()
                placement_dict[location_data.fe_id] = {
                    "location_data": location_data.to_json(),
                    "item_data": item_data.to_json()
                }
            else:
                placement_dict[location_data.fe_id] = {
                    "location_data": location_data.to_json(),
                    "item_data": ItemData.create_ap_item().to_json()
                }
        return placement_dict

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def check_exclusive_slot(self, item, member):
        if item.player != self.player or item.name == "None":
            return True
        location = self.multiworld.get_location(member, self.player)
        if location.item is not None:
            if location.item.name == item.name:
                return False
        return True