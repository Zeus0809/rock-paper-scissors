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


