# Pacman_Qlearning
This script is based on the python script written by Parsons.
## What is it about?

The main idea of this script is the implement of Q-learning method in Pacman game in UC Berkeley CS188 Intro to AI. http://ai.berkeley.edu/reinforcement.html

The script contains a Q-learning agent player class of Pacman game. 
**Note: this is not a solution for the coursework in UC Berkeley CS188.**

## How does it work?
1. Download the reinforcement pack of Pacman game from:
https://s3-us-west-2.amazonaws.com/cs188websitecontent/projects/release/reinforcement/v1/001/reinforcement.zip

2. Unzip the package and place mlLearningAgents.py inside the directory.

3. Run the training command in the directory.
  ***i.e.*** for 2000 runs of training and 10 runs of playing in a small grid, run:
  
          python pacman.py -p QLearnAgent -x 2000 -n 2010 -l smallGrid

