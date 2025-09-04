from pathlib import Path
from dataset_utils import read_graph_from_path

graph = read_graph_from_path(Path("general/Lakeville/problem_1/Lakeville.npz"))

# Find the room ID for 'kitchen_16'
kitchen_room_id = None
for room_id, room_info in graph['room'].items():
    label = room_info.get('label') or f"{room_info.get('scene_category', 'UnnamedRoom')}_{room_id}"
    if label == "kitchen_16":
        kitchen_room_id = room_id
        break

if kitchen_room_id is not None:
    print(f"Objects in kitchen_16:")
    for obj_id, obj_info in graph['object'].items():
        if obj_info.get('parent_room') == kitchen_room_id:
            print(f"- {obj_info.get('class_', 'UnnamedObject')} (ID: {obj_id})")
else:
    print("Room 'kitchen_16' not found.")