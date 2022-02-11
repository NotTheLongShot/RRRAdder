""" Various helper functions for converting vehicle placements made in STEditor to a locations JSON file. """

import json
import re

from pathlib import Path
from typing import List


# def read_to_vehicle_dict(string) -> list:
#
#     wanted_keys = "name", "country", "vehicle_type", "location_tuple", "rotation_tuple"
#
#     vehicles = []
#
#     lines = iter(string.split("\n"))
#
#     for line in lines:
#         if line == "Vehicle":
#             veh = {}
#             while '}' not in line:
#                 line = next(lines)
#                 parts = line.split(" = ")
#                 if len(parts) == 2:
#                     veh[parts[0].strip().lower()] = parts[1].strip(';')
#             veh["location_tuple"] = tuple(map(float, (veh["xpos"], veh["ypos"], veh["zpos"])))
#             veh["rotation_tuple"] = tuple(map(float, (veh["xori"], veh["yori"], veh["zori"])))
#
#             veh["name"] = veh["name"].replace('"', "")
#             veh["country"] = int(veh["country"])
#             veh["vehicle_type"] = veh["model"].split("\\")[-1][:-5]
#
#             vehicles.append({k: v for k, v in veh.items() if k in wanted_keys})
#
#     return vehicles


def read_to_vehicle_dict(mission_text: str) -> List[dict]:

    wanted_keys = "name", "country", "vehicle_type", "location_tuple", "rotation_tuple"

    from RRRAdder import get_mission_element

    vehicles = get_mission_element("Vehicle", mission_text)
    munged_vehicles = []

    for veh in vehicles:
        veh["location_tuple"] = tuple(map(float, (veh["xpos"], veh["ypos"], veh["zpos"])))
        veh["rotation_tuple"] = tuple(map(float, (veh["xori"], veh["yori"], veh["zori"])))

        veh["country"] = int(veh["country"])
        veh["vehicle_type"] = veh["model"].split("\\")[-1][:-5]
        munged_vehicles.append(
            {k: v for k, v in veh.items() if k in wanted_keys}
        )

    return munged_vehicles


def cull_vehicle_dict_rotation(vehicle_list: list) -> list:

    for i, v in enumerate(vehicle_list):
        vehicle_list[i]["rotation_y"] = round(v["rotation_tuple"][1], 0)
        vehicle_list[i].pop("rotation_tuple")

    return vehicle_list


def make_vehicle_location_dict(vehicle_list):

    from collections import defaultdict

    vehicle_dict = defaultdict(list)

    for veh in vehicle_list:
        location = veh["name"].split("(")[1][:-1]
        vehicle_dict[location].append(veh)

    return dict(vehicle_dict)

if __name__ == "__main__":
    vehicle_list = read_to_vehicle_dict(
        Path(
            r"data\ammo_trucks.Mission"
        ).read_text()
    )

    vehicle_list = cull_vehicle_dict_rotation(vehicle_list)

    vehicle_dict = make_vehicle_location_dict(vehicle_list)

    with open("data/vehicle_locations.json", 'w') as f:
        json.dump(vehicle_dict, f, indent=4)


    airfield_names = {
        "Lille North": "St. Marguerite",
        "Lille West": "Fromelles",
        "Seclin": "Houplin",
        "Phalempin": "Laneuville",
        "Orchies": "Coutiches",
        "Douai North": "La Brayelle",
        "Douai South": "Guisnan",
        "Auberchicourt": "Roucourt",
        "Somain": "Aniche",
        "Bugincourt": "Emerchicourt",
        "Avesnes Le Sec 1": "Lieu St. Amand",
        "Avesnes Le Sec 2": "Avesnes-le-Sec Est",
        "Avesnes Le Sec 3": "Avesnes-le-Sec Ouest",
        "Iwuy": "Eswars",
        "Cambrai North": "Epinoy",
        "Vauix Vracourt": "Bullecourt",
        "Cambrai East": "Cauroir",
        "Solesmes": "Briastre",
        "Esnes": "Awoingt",
        "Inchy": "Beauvois-en-Cambrai",
        "Le Cateau": "Neuvilly",
        "Cambrai South": "Noyelles",
        "Fremicourt": "Beugnatre",
        "Gouzeaucourt": "Gonnelieu",
        "Bertry": "Reumont",
        "Bertry South": "Busigny",
        "Nurlu": "Moislains",
        "Frasnoy Le Grand": "Fontane-Uterte",
        "Vermand": "Hancourt",
        "Mesnit Brunei": "Mesnil-Bruntel",
        "Fiscourt": "Flaucourt",
        "Dompierre": "Cappy",
        "Saint Gratien": "Allonville",
        "Talmas": "Berlangles",
        "Warley Bailion": "Braizieux",
        "Warloy Bailion": "Braizieux",
        "Warloy Baillon": "Braizieux",
        "Acheux": "Lealvillers",
        "Beauvalt East": "Marieux",
        "Beauvalt": "Vert Galant",
        "Beauquesne": "Valheureux",
        "Doullens": "Fienvillers",
        "Mondicourt": "Bellevue",
        "Grand Ruilecourt": "Soncamp",
        "Grand Rullecourt": "Soncamp",
        "Le Hameau": "Filescamp",
        "Izel Le Hameau": "Le Hameaux",
        "Izel-les-Hameau": "Le Hameaux",
        "Herlin le Sec": "Herlin-le-Sec",
        "Mont St Eloi": "Beauvois",
        "Arras North 1": "Mont St. Eloi",
        "Arras North 2": "La Targette",
        "Estee Blanche": "Estree-Blanche",
        "Mametz": "Serny",
        "Aire": "Treizennes",
    }

    with open(r"data\airfield_names.json", "w") as f:
        json.dump(airfield_names, f, indent=4)