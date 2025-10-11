# Evolving Enemies
## Using a Genetic Algorithm to control Enemy behavior in Video Games

This code uses the concepts of Genetic Algorithms such as Selection, Crossover and Mutation to control and evolve Enemy behavior. 

The entire behavior of the enemy is coded in the structure of a chromosome.

<p align="center">
  <img width="650" height="300" src="https://github.com/NeonInc/Adaptive-Gameplay/blob/master/Images/Chromosome_Attributes.png">
</p>

Genes 0 - 5 are in binary format with 0 being the respective option disabled and 1 being being the respective option enabled.
Gene 6 is in decimal format to record the fitness value of the chromosome.

### Dependencies (pip install)
```
pygame
pygame-menu==1.96.1
```
### Usage

```
python3 evolving_enemies.py
```
#### Main Menu

The Main Menu allows the players to navigate to Play Menu and the Help and About Menus. The Help Menu details the game controls while About Menu lists game information.

<p align="center">
  <img width="640" height="480" src="https://github.com/NeonInc/Adaptive-Gameplay/blob/master/Images/Main_Menu.png">
</p>

#### Play Menu

In the Play Menu, players can change game difficulty and the mutation rate of the Genetic Algorithm. Changing game difficulty adjusts parameters such as player firing rate and enemy firing rate. Increasing the mutation rate will cause more genes to be mutated and thus, causing more diversification in the population. With a higher mutation rate, players will see more variations across the episodes.

<p align="center">
  <img width="640" height="480" src="https://github.com/NeonInc/Adaptive-Gameplay/blob/master/Images/Play_Menu.png">
</p>

#### In-Game Screenshot

In-Game screenshot of Evolving Enemies

<p align="center">
  <img width="640" height="480" src="https://github.com/NeonInc/Adaptive-Gameplay/blob/master/Images/Game_Screenshot.png">
</p>
