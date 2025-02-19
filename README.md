# Household PDDL scenarios for Gibson 3D Scene Graphs
Disclaimer: Dataset used in the paper "[Context Matters](https://github.com/Lab-RoCoCo-Sapienza/context-matters)" @ IROS 2025

Tested on Ubuntu 24.04

## Directory structure

The dataset comprises a selection of PDDL domains (one for each task) and for each a series of PDDL problems, obtained by randomly distributing objects in 3D Scene Graphs of the Gibson dataset.

The dataset comprises several tasks:

*`dining_setup`: tasks about setting a dining table.
*`house_cleaning`: household cleaning tasks.
*`laundry`: laundry related tasks, with or without a washing machine.
*`pc_assembly`: tasks related to gathering the necessary parts to assemble a working PC (or a sub-optimal solution if not all parts are available).
*`office_setup`: tasks related to decluttering an office. 
*`other_1`: various tasks related to pick-and-place operations.
*`other_2`: various tasks related to pick-and-place operations.

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

### Run

```
python3 dataset_creation.py
```

