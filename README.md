# Household PDDL scenarios for Gibson 3D Scene Graphs
Disclaimer: Dataset used in the paper "[Context Matters](https://github.com/Lab-RoCoCo-Sapienza/context-matters)" @ IROS 2025

Tested on Ubuntu 24.04

## Directory structure

The dataset comprises a selection of tasks that can be performed on splits of the Gibson 3D Scene graphs dataset (with the relaxation that all rooms are interconnected, as we expect this issue to be managed by a lower-level path planner). 
The directory structure is:
- `TASK_1`:
  + `task_1_domain.pddl` (PDDL domain of the task)
  + `3D_SCENE_GRAPH_1_NAME`:
    * `PROBLEM_1`:
      - `3D_SCENE_GRAPH_1_NAME.npz` (3D scene graph with the addition of objects as per task description file (see "Dataset generation"))
      - `description.txt` (Natural language description of the task)
      - `init_loc.txt` (Randomly chosen initial room in the agent in the 3D scene graph)
      - `task.txt` (Natural language imperative task)
    * ...
    * `PROBLEM_N`:
      * ...
  + ...
  + `3D_SCENE_GRAPH_N_NAME`:
    * ...
- ...
- `TASK_N`:
  + ...  


The dataset comprises several splits, each associateds to task:

* `dining_setup`: tasks about setting a dining table.
* `house_cleaning`: household cleaning tasks.
* `laundry`: laundry related tasks, with or without a washing machine.
* `pc_assembly`: tasks related to gathering the necessary parts to assemble a working PC (or a sub-optimal solution if not all parts are available).
* `office_setup`: tasks related to decluttering an office. 
* `other_1`: various tasks related to pick-and-place operations.
* `other_2`: various tasks related to pick-and-place operations.

\(\*\) Some tasks are impossible as the corresponding scene graph lacks the necessary objects, therefore require adapting the goal to the available objects.


## Dataset generation

### Install

1) Make sure git-lfs is installed:
```
sudo apt-get install git-lfs
```

2) Clone this repo
```
git clone --recurse-submodules https://github.com/Lab-RoCoCo-Sapienza/context-matters.git
```

3) Install ollama
```
sudo snap install ollama
```

4) Install requirements
```
pip install -r requirements.txt
```

5) Add a `key.txt` file in the root folder with your OpenAI API key


### Download Gibson dataset
Check [this link](https://github.com/StanfordVL/GibsonEnv/blob/master/gibson/data/README.md) for the process of downloading the dataset.

This step is only required to generate the dataset splits. Our dataset contains reduced `.npz` scene graph files, in json format, adapted to the problem defined in the corresponding `TASK_NAME.json` configuration file. 

### Run
Choose the splits to generate by modifying the `DATASET_SPLITS` list in `dataset_creation.py`, then:

```
python3 dataset_creation.py
```

### Configuration files

The settings to generate each split are contained in the `TASK_NAME.json` settings file, which can be modified to change the problems and domains.

Each JSON file describes a dataset for various dining setup tasks. The structure of the file is as follows:

#### Structure

- `problems`: List of problems related to this task.
  - Each problem has the following properties:
    - `description`: A brief description of the task.
    - `graph`: An array of 3D scene graphs from the Gibson dataset involved in the task. 
    - `goal`: The goal to be achieved for the task.
    - `objects`: Items available for the task. They will be scattered randomly in the scene.
      - `object_category`: A list of items of the same category to be scattered randomly in the scene.

- `domain`: Description of the planning domain.
  - `actions`: Actions that can be performed. They should mirror the PDDL domain corresponding to this task.
    - Each action has the following properties:
      - `name`: The name of the action.
      - `description`: A detailed description of the action, including arguments, preconditions, and postconditions.
  - `objects`: An array of object types.
    - Each object type has the following properties:
      - `type`: The type of the object.
      - `description`: A brief description of the object type.

### Example

Here is an example of a problem entry:

```json
"problem_1": {
  "description": "Task related to setting a table, nothing romantic",
  "graph": ["Shelbiana", "Allensville", "Parole"],
  "goal": "set the table for two people, try adding something romantic",
  "objects": {
    "kitchenware": ["plate", "fork", "knife", "spoon", "glass", "napkin", "fork", "knife", "spoon", "glass", "napkin"]
  }
}
```

And an example of an action entry:

```json
{
  "name": "move_to",
  "description": "This action moves a robot from one room to another. Arguments: robot (the robot to be moved), from (the room the robot is currently in), to (the room the robot will move to). Preconditions: the robot must be in the 'from' room. Postconditions: the robot is no longer in the 'from' room and is now in the 'to' room."
}
```


