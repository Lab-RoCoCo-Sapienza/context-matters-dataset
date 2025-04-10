from pathlib import Path
from typing import Dict, Set, List, Tuple
import random

import numpy as np

from agent import llm_call

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
    Adds the "description" property to each object in the graph.

    :param graph: Dictionary containing the 3DSG
    :return: Updated graph with descriptions for the objects
    """
    print("Adding descriptions to objects")
    for obj_id, obj in graph["object"].items():
        print("the object is: ", obj["class_"])
        obj["description"] = llm_call("Given an input object, add a color and a material.\
                    Your output will be a line with the description: a color object name made of material. Answer with only \
                                    the description with material and color using the name of the object in the question and nothing else.", 
                                    temperature=0.1,question="the object is " + obj["class_"])
        print("the description is: ", obj["description"])
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
    Adds random objects to random rooms in the graph.

    :param graph: Dictionary containing the 3DSG
    :param dict_objects: Dictionary of objects to add, where keys are categories and values are lists of object names
    :return: Updated graph with new objects
    """
    
    possible_objects = []
    for _, obj_value in dict_objects.items():
        for obj in obj_value:
            possible_objects.append({"class_": obj, "action_affordance": []})

    # Find max ID
    if graph["object"]:
        max_id = max(graph["object"].keys())
    else:
        max_id = 0

    # get existing rooms
    room_ids = list(graph["room"].keys())

    # add random objects
    for obj_data in possible_objects:
        obj_id = max_id + 1
        obj_type = obj_data["class_"]
        room_id = random.choice(room_ids)  # get random room

        # create an (x,yz) location for the object, doesnt matter where
        location = np.array([
            np.zeros(3),
            np.zeros(3),
            np.zeros(3)
        ])

        # create new object
        new_object = {
            "id": obj_id,
            "class_": obj_data["class_"],
            "action_affordance": obj_data["action_affordance"],
            "location": location,
            "parent_room": room_id,
        }

        # add to the graph
        graph["object"][obj_id] = new_object
        max_id += 1  # update max_id

    return graph


def choose_random_room(graph):
    return random.choice(get_room_names(graph))


def get_room_names(graph):
    return [room_data["scene_category"] + "_" + str(room_id) for room_id, room_data in graph["room"].items()]