(!!)- highest priority, usually bug fixes
** - low priority / extra feature
----------------------------------------------------------------------------------------
(!!) When an object is SHUT, it is not pushable

1. Level Design
- Levels
    - 3 Forest of Fall
    - 3 The Lake
    - 3 The Factory 
- Levels unlock on a save file
- Final level has 'LEVEL': either solve the puzzle, or make LEVEL IS KIMCHI and solve the map level
- 12 Levels, S-shaped unlock pattern
- Levels unlock on a save file
- Final level has 'LEVEL': either solve the puzzle, or make LEVEL IS KIMCHI and solve the map level

2. More effects 
    - WEAK
    - SHIFT 
    - LEVEL (purely for putting a BABA on the menu screen)
    - MORE  (** with backtracking / recursive fill similar to the MSPaint example)

3. Adjectives and more features
    - ON (basic overlap feature.)
    - NOT (heard it's horrid to implement.) 
    - AND (reads powered effects / subjects)
    - HAS (behaves like Is, also in the eq class-- BABA HAS FLAG drops flag on death)
    - HIDE (doesn't draw the word, and also cuts collisions, but still makes a valid rule)
    ** MORE
    ** FACING (either 1 or all blocks in BABA's direction applicable.)
    ** FALL (gravity. Player sprites will drop to the highest-y, lowest on-screen block possible in their column.)
    ** Flashlight level: BLOCK NOT FACING BABA IS HIDE

** Proper win screen animation
** Level load transitions
    - 2 separate screens, balls on and off, both drawn last
** Proper win screen animation
** Level load transitions
** Create system for movement trails (generate little cloud after player sprite)
** WIN, HOT, MELT, and DEFEAT effect animations
** Start menu buttons highlighting
** Walkthrough option for each level.
    - Preprogammed steps; resets level, then BABA automatically walks through solution until win
    - Press R at any time to try again 