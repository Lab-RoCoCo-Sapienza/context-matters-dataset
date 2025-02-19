from pathlib import Path
from typing import Dict, Set, List, Tuple
import random

import numpy as np

from agent import local_llm_call

def read_graph_from_path(path: Path) -> Dict:
    """
    Read 3DSG from file (.npz) and returns it stored in a dictionary
    
    :param path: Path to the .npz file 
    :return: Dictionary containing the 3DSG
    """
    
    #print(path)
    assert (
        isinstance(path, Path)
    ), "Input file is not a Path"
    assert (
        str(path).endswith(".npz")
    ), "Input file is not .npz object"
    
    graph = np.load(path, allow_pickle=True)['output'].item()
    
    keeps = set(["object", "room"])
    graph = filter_graph(graph, keeps)
    
    return graph

def add_descriptions_to_objects(graph):
    """
    Aggiunge la proprietà "description" a ogni oggetto nel grafo.

    :param graph: Dizionario contenente il 3DSG
    :return: Grafo aggiornato con descrizioni per gli oggetti
    """
    
    for obj_id, obj in graph["object"].items():
        obj["description"] = local_llm_call("Describe the object in one sentence in the following format A <color> <name of object> made of <material>\
        in which you replace <color> with the color of the object, <name of object> with the name of the object and <material> with the material of the\
        object. For example A brown table made of wood. Do not add other information.", obj["class_"])
    return graph

def save_graph(graph: Dict, path: str):
    """
    Save the 3DSG graph to a file
    
    :param graph: Dictionary containing the 3DSG
    :param path: Path to the file
    """
    print(path)
    np.savez(path, output=graph)


def filter_graph(graph: Dict, labels: Set[str]) -> Dict:
    """
    Filter the 3DSG graph to only include objects with labels in the 'labels' set
    
    :param graph: Dictionary containing the 3DSG
    :param labels: Set of labels (strings) to consider, e.g. {"room", "object"}
    :return new_graph: Dictionary containing the filtered 3DSG
    """
    new_graph = {}
    for key, item in graph.items():
        if key in labels:
            new_graph[key] = item
    return new_graph


def add_objects(graph, dict_objects):
    """
    Aggiunge oggetti casuali a stanze casuali nel grafo.

    :param graph: Dizionario contenente il 3DSG
    :param num_objects: Numero di oggetti da aggiungere
    :return: Grafo aggiornato con nuovi oggetti
    """
    
    possible_objects = []
    for _, obj_value in dict_objects.items():
        for obj in obj_value:
            possible_objects.append({"class_": obj, "action_affordance": []})

    # Trova ID massimo attuale per evitare conflitti
    if graph["object"]:
        max_id = max(graph["object"].keys())
    else:
        max_id = 0

    # Ottieni stanze esistenti
    room_ids = list(graph["room"].keys())

    # Aggiungi oggetti random (scegli a caso il numero di oggetti uguali)
    for obj_data in possible_objects:
        obj_id = max_id + 1
        obj_type = obj_data["class_"]
        room_id = random.choice(room_ids)  # Scegli una stanza casuale

        # Genera posizione casuale all'interno della stanza scelta
        location = np.array([
            np.zeros(3),
            np.zeros(3),
            np.zeros(3)
        ])

        # Crea nuovo oggetto
        new_object = {
            "id": obj_id,
            "class_": obj_data["class_"],
            "action_affordance": obj_data["action_affordance"],
            "location": location,
            "parent_room": room_id,
        }

        # Aggiungi al grafo
        graph["object"][obj_id] = new_object
        max_id += 1  # Aggiorna ID massimo

    return graph


def choose_random_room(graph):
    return random.choice(get_room_names(graph))


def get_room_names(graph):
    return [room_data["scene_category"] + "_" + str(room_id) for room_id, room_data in graph["room"].items()]