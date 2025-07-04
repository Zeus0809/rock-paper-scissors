# Rock Paper Scissors Battle Game

The game was vibe coded entirely with Claude 4 Sonnet through GitHub Copilot. These are the prompts used:

## Prompt 1:
It is a single screen 2D game. The user is not going to be involved in the game process itself, the game will play out on its own. When it starts, there would be small rock, paper, and scissors objects spawned in the game area (which could be just a black background, or something of your choice).

I want to be able to control the number of objects spawned for each object type. That should be a setting in the game, and it should set the number for all objects - meaning there should never be a case where you have more rocks than papers, more scissors than rocks, etc.

Each object type should be spawned from its own corner of the screen. E.g. scissors should start spawning from the bottom left, papers from the bottom right, and rocks from top right. The exact corners are up to you. Also, don't spawn all objects at once, have a tiny interval between spawns, so that objects start moving and dispersing randomly throughout the game area. That means every object should receive a momentum in a random direction at spawn time, but the speed should be the same.

After getting spawned, the objects should start slowly moving in random directions. If there is a collision, follow these rules:
1) if scissors hit a paper, paper disappears and scissors keep moving in the same direction at the same speed.
2) if paper hits a rock, rock disappears and paper keeps moving in the same direction at the same speed.
3) if rock hits scissors, scissors disappear and rock keeps moving in the same direction at the same speed.

When an object hits the bounds of the screen, it should properly reflect back at the opposite angle, like a pool ball when hitting a rail.

Size of objects: let's make it 1/20 of the size of game area. I should be able to change that, but not in the UI.

For each object type, there should be a count displayed at the top of the screen, saying how many instances of each object is left. It should update as objects get destroyed.

The game should stop as soon as there is only one object type left, for example, when all you see on the screen is rocks. That means rock wins, so there should be a message saying who the winner is. After that the user should be able to start the game over.

For object sprites, create a separate folder and I'll paste the images there. Suggest what image format I should look for and what image size for them to display well.

Any follow-up questions or considerations before I let you start?

## Prompt 2:
1. 1024x768 window
2. It should be a control in the UI on the screen. Place it in the top left corner next to object counts, follow UI/UX best practices. User should be able to increase/decrease the number of objects, make it a control with up and down arrows that change the number.
3. Spawn interval = 0.1 seconds
4. Object speed: they should move at 1 inch per second. Figure out how many pixels is one inch of screen, then convert that into pixels per frame.
5. There should be a 'New Game' button in the UI. Once pressed, it should restart the game with whatever the object number (the arrows control) was set to at the time.

Any other questions?

## Prompt 3:
When a collision happens, instead of eliminating the losing object, turn it into an instance of the winner object. Example: if a rock hit scissors, the scissors should turn into another rock, etc.

## Prompt 4:
I love it! Another change:

Add a 'Pause' button that pauses the game. When pressed, it should get replaced with a 'Resume' button that resumes the game.

## Prompt 5:
I don't like the way the object count increment buttons look. Make them actual up/down arrows and make them look nicer

## Prompt 6:
Also, make the game window resizable, and possible to turn to full screen.

## Prompt 7:
I'm getting an error when trying to run:
Traceback (most recent call last):
  File "/Users/illiakozlov/Desktop/rock-paper-scissors/game.py", line 489, in <module>
    game = Game()
  File "/Users/illiakozlov/Desktop/rock-paper-scissors/game.py", line 243, in __init__
    self.update_window_dependent_values()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/Users/illiakozlov/Desktop/rock-paper-scissors/game.py", line 264, in update_window_dependent_values
    for obj in self.objects:
               ^^^^^^^^^^^^
AttributeError: 'Game' object has no attribute 'objects'

## Prompt 8:
The New Game and Pause buttons overlap with the object count control. Let's rearrange the header items a little:

1) Put the New Game and Pause buttons in a column to the very right of the header.
2) Make the stats bigger and center them in the header.
3) Put the object count control on the left side, symmetrical to the column with the other buttons.
Make sure everything is symmetrical and nicely placed according to UI best practices. I don't want it to be ugly!

## Prompt 9:
Traceback (most recent call last):
  File "/Users/illiakozlov/Desktop/rock-paper-scissors/game.py", line 525, in <module>
    game = Game()
  File "/Users/illiakozlov/Desktop/rock-paper-scissors/game.py", line 251, in __init__
    self.update_window_dependent_values()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/Users/illiakozlov/Desktop/rock-paper-scissors/game.py", line 269, in update_window_dependent_values
    self.update_ui_positions()
    ~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/Users/illiakozlov/Desktop/rock-paper-scissors/game.py", line 283, in update_ui_positions
    self.new_game_button.rect.x = self.window_width - button_width - 20
    ^^^^^^^^^^^^^^^^^^^^
AttributeError: 'Game' object has no attribute 'new_game_button'

## Prompt 10:
The Pause button overlaps with the bottom header boundary. Make the header thicker to account for the button height.

## Prompt 11:


