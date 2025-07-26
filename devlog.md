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
    - Project uploaded to github. Hi Mike!
    - Switching from claude to Cursor code editor for faster implementation of repeated stuff or quick bug fixes adjustments to existing functions 
    
    As of 11:26 pm:
        - added a readme with proper accreditation of code portions and todo list. 
        - mainly studying for quiz 5. I LOVE RECURSION AND TREES
        - (Cursor helped) fix drawing bug in drawObj where player sprites are hidden under objects with no collision. 
        - implemented a very rudimentary win screen, as well as a check-win function. 
        - The classes and object/sprite-as-instance system we have right now needs some serious reworking, as individual instances don't store their own direction data. If one instance of ROCK is pushed left, all of them face left. This is okay for static objects but for the "MOVE" effect this is diasterous. I'm working on this as soon as quiz is done, as well as the reset / undo feature. These two features are the two biggest roadblocks right now. 

Jul 24
    **Okay. a F--K ton happened between today and yesterday.**

        As of 11:01pm (total ~7 hours worked on this damn thing today)

        I began working this morning shortly after the quiz, and realized that the reset level / undo move features would be incredibly tedous/inefficient/downright impossible to implement without completely reworking how map, sprite, and player data was handled. Also, I needed to be able to apply rules and player-control sprites as a group, but have each individual sprite retain its own direction data. This too was impossible with the object subclass: coordinate points dictionary sytem. Thus, for the sake of implementing more ambitious features, I decided to redo the foundations and rewrite how data was stored entirely. Thankfully, I could re-use some of the object classes.

        Figuring out what class organization and system to use only took about 30 minutes. Figuring out how to have the program recognize objects and draw stuff again took 2 hours. Then restoring movement took 4 more; it was insanely buggy. Stuff didn't want to push, stuff would push but not draw, stuff wouldn't recurse on VERY SPECIFIC occasions and caused the game to break, or BABA would use the force and start hurling blocks off the map when a word was moved. I only (nearly) got back to where I was yesterday under the new datatype at 9:30PM. 

        I'm pretty sure YOU + STOP still doesn't stop players from overlapping, a feature lost from yesterday. I'm putting that on a debug list for tomorrow. Kudos to Cursor for helping me debug. See comments/credits in the code.

        Update list: 
        - Reworked the entire collision detection, map data storage, sprite/object/word data stoage system.
        
        - Particular objects (e.g. KIMCHI, BABA, KEKE, WALL, FLAG) are no longer particular subclasses. All non-word objects on the map are an instance of the obj class, initialized as follows: 

                def __init__(self, name, attribute):

                    #object base information (determines what object e.g. baba, keke, kimchi the object instance is)
                    self.name = name 
                    self.attribute = attribute 
                    self.drawInfo = objDrawDict[self.attribute]
                    self.initialstate = self.attribute 
            
            self.attribute is what gives a particular object its appearance. It's a string containing the name of the object ('keke', 'baba') whose sprite info can be found in objDrawDict, leading to the new drawinfo file where all sprites and animations can be neatly stored. 

            All "XX IS XX" rule searches now also search for attribute instead of a specific class of object. Holy crap, this makes dealing with rule changes SO much easier. Effectively, this makes every sprite a reskin of the same thing, which is great since we can very easily change the appearance of the sprite, along with its ruleset. It's as simple as setting item.attribute = 'attribute'. No more list / set merger BS. 


        - Move undo (Z) and level reset (R) functions implemented, as well as reset, win, and 'loss' screens.
            Arguably the greatest innovation of the day: 

                    #movement info
                    self.pos = None
                    self.posHist = []
                    self.effectsList = []
                    
                    #drawing info
                    self.direction = 'right'
                    self.type = 'obj'

                def MoveObject(self, direction):
                    self.posHist.append(self.pos)
                    x, y = self.pos
                    dx, dy = moveDict[direction]
                    self.direction = direction
                    self.pos = (x + dx, y + dy)

                def undoMove(self):
                    self.pos = self.posHist.pop()
                
                def resetPos(self):
                    if self.posHist:
                        self.pos = self.posHist[0]
                        self.posHist = []
            
            This is what makes undos and level resets possible. These move/reset methods are stored in EVERY class-- objects and all types of words. Undoing a move or item change is as simple as calling a method. It's beautiful. 

            Move histories are also stored globally in tuples of (object, move) or (object, oldType, newType) in a move history folder: 

                def refresh(app,level):
                    #cache all moves made this turn, put it in a stack that can be executed on one button press.
                    if app.turnMoves: #don't want to store empty stacks
                        app.level.moveHistory += [app.turnMoves] #'your mom could be a stack' --seunghyeok lee
                    #now reset turn moves for the next action done. 
                    app.turnMoves = []
            
            You can see that moves are stored in app.turnMoves first-- "stacks", or nested lists, to execute with one button press. Otherwise, a chain push of 6 items would only reset item by item by item on repeated key presses, and we don't want players to get stuck in a half-reset state. 

            Credits to my friend Seunghyeok Lee for that idea. 
    
        More to go tomorrow with the implementation of the deletion function that takes sprites off the map. I'll probably also try, if it's convenient, to implement an "add" function that puts sprites ON the map instead. 

Jul 25
    Decided to work on graphics and implementation of sprites first instead of implementing delete / defeat / sink functionalities. 
    Working menu is probably next, then we'll get some levels, implement sounds, and be in a good spot for Monday. 
    
    - Fleshed out and updated reset function, including a draw bug where winning a level and resetting causes items to be drawn in their pre-reset state. 
    - Added direction reset functions (resetting a move now makes the object face the way they did before). 
    - Added new sprite-loading files (loadimages.py, drawinfo.py) and implemented new functions for sprite drawing. Visually, objects are split into these types:
        - Walls have neighbor checks that affect their appearance. 
        - Sprites are commonly player-used objects that have more extensive animations. 
        - Objects are everything else inbetween, less well animated but still important. 
        - Object2s are more extensively animated objects (belts, robots) that will have functions affecting player movement.
        - Words have a powered (glowing) and non-powered (dark) state to indicate whether a rule is in play or not. 
    sprites are taken from 5 central spritesheets, cropped / greenscreened using pillow, and made into a CMU_Graphics compatible package. Most of the day (~2pm to 11pm) was spent figuring out how, where and when to draw things. 
    Found new bugs in the movement system from the datatype switch on July 24, though, so we'll need to debug those first thing tomorrow. Might take even more time...
        

    
