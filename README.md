# Frozen Summit

## Demo
Demo Video: https://youtu.be/e3ZWdW0g4ww

## GitHub Repository
GitHub Repo: https://github.com/TheFinaIFighter/falling-sky-project

## Description

Frozen Summit is a survival game created in Python using the Pygame library. The player controls a climber standing on a snowy mountain while avoiding falling icicles for as long as possible. As the game continues, the icicles begin to fall faster and more frequently, making survival increasingly difficult. The game also includes a slow-motion ability that temporarily slows the hazards before entering a short cooldown period.

The game uses several classes and functions to organize different systems. The Player class handles movement and drawing the player character, while the Hazard class controls the falling icicles and their randomized sizes and speeds. The Snow Particle and Burst Particle classes are used for visual effects such as falling snow and collision particles. The project also includes multiple game states, including a start screen, gameplay loop, and game over screen.

The gameplay is intentionally simple and easy to understand. The player moves left and right using the keyboard while avoiding falling icicles for as long as possible. Surviving longer increases the score and also increases the difficulty. The slow-motion ability gives the player a short moment to recover during more intense moments of gameplay.

If I continued working on this project, I would like to add sound effects, animated sprites, multiple hazard types, and a high score system. I would also like to improve the visual effects further with stronger weather effects such as snowfall intensity changes and screen shake during collisions.

## Controls

- Move Left: A or Left Arrow
- Move Right: D or Right Arrow
- Slow Motion Ability: SPACE
- Start Game: ENTER
- Restart After Game Over: R
- Quit From Game Over Screen: ESC

## Tutorials and Resources

The following tutorials and resources were helpful during the development of this project:

- Tech With Tim – Pygame Movement Tutorial  
  https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-tutorial-movement  
  Helped with implementing player movement and keyboard controls.

- Tech With Tim – Pygame Collision Tutorial  
  https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-collision  
  Helped explain collision detection and hitboxes using pygame.

- GeeksforGeeks – Collision Detection in Pygame  
  https://www.geeksforgeeks.org/python/collision-detection-in-pygame/  
  Useful reference for obstacle collision systems.

- DaFluffyPotato – Pygame Particle Tutorial  
  https://www.youtube.com/watch?v=F69-t33e8tk  
  Helpful for understanding basic particle effects and visual polish.

- Clear Code – Creating Particle Effects in Pygame  
  https://www.youtube.com/watch?v=yfcsB3SGsKY  
  Helped with understanding particle effect structure and visual effects logic.

- Tech With Tim – Scoring and Health Bars  
  https://www.youtube.com/watch?v=JLUqOmE9veI  
  Helpful for understanding score tracking.

- Creating a Scoring System in Pygame  
  https://www.codewithc.com/creating-a-scoring-system-in-pygame/  
  Used as a reference for updating and displaying score values over time.

- Pong Tutorial Using Pygame – Adding a Scoring System  
  https://www.101computing.net/pong-tutorial-using-pygame-adding-a-scoring-system/  
  Helpful example for creating an in-game score display system.

- Invent With Python – Game Loops and Game States  
  https://inventwithpython.com/pygame/  
  Helpful for understanding game loops, start screens, gameplay states, and game over screens.

- Pygame Documentation – pygame.Rect  
  https://www.pygame.org/docs/  
  Official documentation used as a reference.
