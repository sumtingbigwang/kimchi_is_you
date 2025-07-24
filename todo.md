(!!) we need __eq__'s to hash shit properly. 

(!!) make objects into subclasses that have images as part of its class information. Have objects be drawn in respect to their sprite images. 

2. WIN ** 
    - WIN condition and what it does
    - WIN screen (Congratulations!) 

3. No player / loss ** 
    - After 2-3 seconds, pop out "Z to undo / R to reset" on top of screen

4. Reset / Undo function  ** 
    - Figure out how to revert the level dictionary back to its original state
    - If reset pressed, confirmation screen pops out
    - Store ALL object movement data in a big list with tuples (object, move)
    - Figure out how to reset chain pushes

5. Beauty / Good looking graphics
    - Import sprites from BABA IS YOU and link them to objects. 
    - Have objects be drawn as the sprites.
    - Finish the Kimchi Sprite (and mystery david kosbie / mike taylor sprites)
    - Draw gridlines option
    - Draw grid numbers option
    - Different background sizes for different levels
    - Decoration items
    ** Create system for movement trails (generate little cloud after player sprite)

**(2 or 3 levels-- then deem complete)
**(implement sprite graphics / level graphics)

5. Implement and map Space to the takeStep or "wait" function. 

6. Menu loader 
    - Separate title screen from menu/map page. 
    - Paused menu which prints the rules currently in play for the level (none for menu)
    - Map screen is actually a level. Implement the menu screen as a level class
        - Level design like level1???
        - final two levels create the 'KIMCHI' and 'FLAG' objects or something

7. Effects 
    (really, a lot of these are conditional "die" states.)
    - SINK
    - HOT / MELT
    - DEFEAT
    - MOVE / AUTO
    - WEAK
    - SHIFT 
    - LEVEL (purely for putting a BABA on the menu screen)
    - MORE  (** with backtracking / recursive fill similar to the MSPaint example)

8. Adjectives
    - ON
    - NOT 
    - AND (reads powered effects / subjects)
    - HAS (behaves like Is, is actually in the eq class)

10. Sound effects for everything
