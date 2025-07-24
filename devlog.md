Jul 20
    (asked claude about this) list of shi to implement:
        model
            gameState
            - winCon (define win condition)
            - isWin (define sprite as winning)
            - getLevel
            - getPos (returns grid coordinates of any sprite)
            - getObjs (x,y) (returns all sprites on a grid point)

            rules
            - findPlayer
            - findWin
            - impRules

            objects
            - overlap
            - checkProps 
    
    - implementation of level
            loader
            - loadNext?? 
            MAP data or list data? 
            map: [
                    [[],[],[],[],[],[],[],[],[],[]]
                    [['B'],[],[],[],[],[],[],[],[],[]]
                    [[],[],[],[],[],[],[],[],[],[]]
                    [[],[],[],[],[],[],[],[],[],[]]
                    [['W'],['W'],[],[],[],[],[],[],[],[]]
            ]
            
            list: [('BABA',0,1) , (WALL,0,5),(WALL,1,5),...], for obj in list drawobj(obj)
            * go with map for now, find better implementation later

Jul 21
    - Implemented a load of shi
    - trying to figure out how to implement movement, and then pushing. The idea is to use the levels.data 3D list to read & write letters on the list, depending on whether they're players or not.
        - the issue is moving 1 instance vs many instances, and how to make it such that a unique instance (which can later be controlled in a group if all of it is player) can be moved individually. 
        - we shift from moving the sprite in the draw command to moving the sprite in the actual map.
        - also need to consider copying map for reset function. 

    - storing map -> cells -> objects as a class?
        map needs: 
            - rows
            - cols
            - method inside map to retrive row and call of objects to draw map
            - place objects inside map 
                map1.placeobject(objname,row,col), mutates map to reflect change
            - method to retrieve specific cell in map 
                map1.retrievecell(row,col) (returns list of all objects in cell)
                    - isempty, getobject(row,col)

            -movement is a method in the map class
                - moveobject: retrieve cell in direction of movement
                    
    - update: going with tyler's suggestion of storing level as dictionary entries, going with first form of implementation (sort of)
        need:
            - renewable level class
            - level has:
                - objects array, keys to dictionary
                - dictionary with values as list storing positions in tuples 
                - assoc. number to load

    pushing: 
    - isLegal: test if the target cell is a valid move
        - test if target cell out of bounds (implemented)
        - getObjects: get all objects on the target cell 
        - test if any object on the target cell has the effect 'STOP'; if so reject move 

    - moveObj: move objects and push any objects neighboring it
        - if target cell has a pushable object, try to move that object. 
            If movement returns false, reject move
        - if target cell's object moves, finally move the original. 


Jul 22
    - Implemented push and move mechanics for players. If an object has 'PUSH' in its effects array, it is pushable. It it has 'STOP' in its effects array, it is immovable. Otherwise, it just clips under the player / pushed block. 
        - Debug: player is PUSH and STOP (as of 4pm: fixed)
    
    - Feeling that access time is gonna pose a serious issue with more complex and larger levels due to the map and players being stored in lists. 
        - Need to make coordinate arrays and players into sets. Having positions stored in a list is okay-- the base game treats overlapping players / sprites as one sprite anyway, since they both sink / delete together. 
        - List mutilations need to be replaced with .pop and .add operations

        ** implemented sets, moving on to rules 
        
        ** Also split lookup functions and movement functions into different files. logic file is getting too large


    - Implementing rules:
        At start of game and every player input, search the board for rules in play. 

        Objects start with no rules attached-- only the words on the board gives the objects rules, done by storing strings in an object's "eff" set. 
            - consider: How do we update rules in objects? 

        So each word must have its own set of 'powered' data, unlike objects/sprites. Thus, we need to generate a new instance of the word in its class for every new instance of the word we want to put on the board.

        We implement this by introducing a 'wordDict' in levels which allows us to use list comprehension for words, and makes it easier to edit the level. However, each word now must also have its own key-value pair in the level dictionary. 

            -To make multiple instances of a word, create a set of coordinates where you want the word, and write the following: 

            [word]posSet = {(0,0), (2,4), (6,3)}
            wordDict = {eq/eff/obj(attributes):{pos} for pos in [word]posSet}

            this generates separate instances which findRules can check and modify individually. 

    -Update as of 5:29: pushing together and adding rules are working. Need to figure out how to remove words next upon a rule break (best way to do this is probably to keep & check on step a global list of rules, which we need to print anyway for the player). 

    -debug: sprites that are made players later are not drawn above objects. Need to fix by creating separate drawplayers() function that runs after drawobj. 

    -update 9:32: BABA IS FLAG / FLAG IS BABA now works. fundamental game mechanics should be done, important part now is to define other features:
            - like the WIN word, 
            - SINK/HOT/MELT/DEFEAT features,
            - implementing the 'game over' option. 
            - Also need reset / backtracking function.
            - Adjectives like ON or NOT or HAVE. 
            - States like AUTO or CHASE. 
            - Menu loader (maybe make the menu screen a level, ultra meta style?)
            - Separate drawWords, drawPlayers from drawObj function
            - Beauty / Good looking graphics
                (need to figure out how to import the BABA IS YOU sprites)
                (finish the kimchi sprite)
            

    (!!) Redo the move denominations. Instead of x and y, use Enums (UP = 1, DOWN = 2, etc...) to store moves as (OBJ, MOVE) so that the undo move saves can be a lot smaller
    
    (!!) make objects into subclasses that have images as part of its class information. 

Jul 23 
    -Project uploaded to github. 
    - Switching from claude to Cursor code editor for faster implementation of repeated stuff or quick bug fixes adjustments to existing functions 
    
    As of 11:26 pm:
        - added a readme with proper accreditation of code portions and todo list. 
        - mainly studying for quiz 5. I LOVE RECURSION AND TREES
        - (Cursor helped) fix drawing bug in drawObj where player sprites are hidden under objects with no collision. 
        - implemented a very rudimentary win screen, as well as a check-win function. 
        - The classes and object/sprite-as-instance system we have right now needs some serious reworking, as individual instances don't store their own direction data. If one instance of ROCK is pushed left, all of them face left. This is okay for static objects but for the "MOVE" effect this is diasterous. I'm working on this as soon as quiz is done, as well as the reset / undo feature. These two features are the two biggest roadblocks right now. 
