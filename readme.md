# IMPORTANT!

In the game code, there are several sys.path.insert import commands that are key to making sure functions can access functions in other directories. Before you run the game, please change these commands to the respective file paths on YOUR computer so that the game can load properly. Thank you!

### Introduction
KIMCHI IS YOU is a python remake of an existing puzzle game, BABA IS YOU. 

The origin of the name 'Kimchi' originates from Carnegie Mellon 15-112 Prof. Michael Taylor's pink pet axolotl, whose name is actually Kimchee. To fit Kimchee's name text within the 6-character game limit, liberties were taken to shorten the name of the protagonist-- who is also a pink axolotl-- to Kimchi. Sorry Mike! Players move around a pixellated world shaped by words around them, forming ingenious solutions for seemingly impossible puzzles by changing the rules of the game.

## The Game
In case you missed the tutorial levels:
- W/A/S/D and Arrow keys allow you to move the player-- If there is one! 
- This is a mouse free game. To confirm an option, press ENTER; to go back or pause, press ESCAPE.
- While in a level (might mean more places than it seems!), press Z to undo a move or R to reset the entire level.

The game consists of 22 levels, with 9 tutorial levels and 4 worlds of 2-4 levels each that attempt to gradually demonstrate the 10 core mechanics/words integrated into the game. Each world is intended to scale up in difficulty, with the final level in the world designed to be the hardest, or to have put together the most features. Be warned-- the final world (located at the top of the map screen) is a collection of some of the hardest levels in BABA IS YOU, and will take a while to figure out. You can find walkthroughs for each level by searching up the level name (provided in the pause and map menus) and 'BABA IS YOU,' as most of these levels are direct copies of their counterparts in game. 

At first, level 22 may seem unreachable. I recommend you play around a bit more with level 21 after beating it to see what new META mechanics you might be able to use! Although a fraction of what Hempuli's original had to offer, I hope this short project was fun for you to play! 

### Background
Baba Is You is a puzzle video game created by Arvi 'Hempuli' Teikari, a Finnish independent developer. Inspired by the Japanese box-pushing puzzle game Sokoban (lit. 'warehouse manager'), the game centers around the manipulation of "rules"—represented in the play area by movable tiles with words written on them—in order to allow the player character to reach a specified goal. Rules later in the game get increasingly complex, and the game gets mind-numbingly hard-- but also incredibly rewarding -- to push through as more and more rules must be rearranged to reach the solution. If you haven't yet, [I strongly recommend you check out the original game here.](https://store.steampowered.com/app/736260/Baba_Is_You/)

As part of a game jam, Hempuli coded the preliminary version of the game with PUSH/STOP/DEFEAT/HOT/MELT and UNDO functionality in 72 hours on multimedia fusion 2. I wanted to challenge myself by seeing if I could do that and possibly a bit more with a week of time and a new knowledge of Python code! 

As a 15-112 student, I was given ~1 week to code a term project that demonstrated computational complexity while also being "boldly creative." Despite having last played BABA IS YOU nearly 6 years ago, I could think of no better term project to deliver. Just like how this seemingly simple block-pushing game can turn shockingly complex, the coding process for this game has also quickly evolved from a simple-looking task into a challenging, tedious, but rewarding matter. KIMCHI IS YOU turned out to be a deceptively complex game that was both a challenge and a labor of love to code up, and I'm incredibly proud to present it in a finished state.

**The hope is that, by the end of this project, I will have created a memorable, complete, and intellectually stimulating experience for my players that goes beyond the average 15-112 term project. Something you would actually install in your free time as a game!**

### Technicals
This project was coded in Python 3.12. The project runs through the file 'main.py'. Cmu_graphics is the graphics engine, and has been provided with the project. Pillow (pip install pillow) is also required to crop sprites for animations. 
Aside from the aformentioned two libraries, no additional libraries need to be installed provided that 'main.py' is run in the same folder as the accompanied cmu_graphics folder.

### Credits
cmu_graphics developed by Carnegie Mellon University. 
Music, art, sprites and level designs by Arvi "Hempuli" Teikari. 
This project is created for educational purposes only, and is not intended for commercialization or monetization.
