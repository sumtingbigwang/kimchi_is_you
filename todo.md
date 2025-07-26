(!!)- highest priority 
** - low priority / extra feature
----------------------------------------------------------------------------------------
(!!) Fix players overlapping when 'STOP' or 'PUSH' is an effect
(!!) Collision is still bugged when making multiple players and resetting.
(!!) XX IS YOU rules also take one extra round to get registered. 

5. Beauty / Good looking graphics / Sound effects for everything
    - Import sprites from BABA IS YOU and link them to objects. 
    - Have objects be drawn as the sprites.
    - Have level backgrounds.
    - Finish the Kimchi Sprite (and mystery david kosbie / mike taylor sprites)
    - Pause menu
        - Draw gridlines option
        - Draw grid numbers option
    - Different background sizes for different levels
    - Decoration items
    - Proper win screen animation
    - Proper no player 'loss' animations
    ** Create system for movement trails (generate little cloud after player sprite)

(!) (implement 5 levels (3 tutorial, 3 hard ones) with base features-- then deem temporarily complete) 
    ^^We should be here by Monday. 
    
6. Implement and map Space to the takeStep or "wait" function. 

7. Menu loader 
    - Separate title screen from menu/map page. 
    - Paused menu which prints the rules currently in play for the level (none for menu)
    - Map screen is actually a level. Implement the menu screen as a level class
        - Level design like level1???
        - final two levels create the 'KIMCHI' and 'FLAG' objects or something

8. More effects 
    (really, a lot of these are conditional "die" states.)
    - SINK
    - HOT / MELT
    - DEFEAT
    - MOVE / AUTO
    - WEAK
    - SHIFT 
    - LEVEL (purely for putting a BABA on the menu screen)
    - MORE  (** with backtracking / recursive fill similar to the MSPaint example)

9. Adjectives and more features
    - ON (basic overlap feature.)
    - NOT (heard it's horrid to implement.) 
    - AND (reads powered effects / subjects)
    - HAS (behaves like Is, also in the eq class-- BABA HAS FLAG drops flag on death)
    - HIDE (doesn't draw the word, and also cuts collisions, but still makes a valid rule)
    ** MORE
    ** FACING (either 1 or all blocks in BABA's direction applicable.)
    ** FALL (gravity. Player sprites will drop to the highest-y, lowest on-screen block possible in their column.)
    ** Flashlight level: BLOCK NOT FACING BABA IS HIDE

10. Meta Level Loader and more levels 