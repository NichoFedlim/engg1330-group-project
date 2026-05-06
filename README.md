# engg1330-group-project
ENGG1330 Group Project - Twist Tac Four Game

***** Game Title: Twist Tac Four *****

1. Description
Twist Tac Four is a strategic board game that challenges problem-solving skills of a player to outmaneuver an AI opponent. 
The game features a unique rotating board mechanism, adding a dynamic twist to traditional gameplay. 
This added layer of complexity makes the game both challenging and engaging for players of all ages.
Players take turns placing their pieces on a 4x4 grid, aiming to align four pieces in a row. 
The board's outer and inner rings will always be rotated to disrupt opponents' strategies and create new opportunities.

2. Key Features
The game's AI, powered by a sophisticated algorithm, predicts player moves and calculates the best possible counteractions. 
The AI employs a game tree structure, evaluating moves with preserving and aggressive strategies to ensure optimal play.
- Dynamic Rotating Board: Rotate sections of the board to gain an advantage or thwart opponents.
- Advanced AI Opponent: Utilizing a tree-based prediction system, the AI (Robot) adaptively counters player strategies.
- Challenging Gameplay: Balancing offensive and defensive tactics to achieve victory.

3. Objective
The primary goal of Twist Tac Four is to align four of your pieces (either X or O) in a row, column, or diagonal on a 4x4 grid (After the Rotation). 
The game can be played with one player against a computer-controlled opponent (The Robot).

4. Game Components
- Game Board: A 4x4 grid where the player place or type their pieces.
- Pieces: Each player has a set of pieces, either X or O.
- Rotation Mechanism: The board is divided into an outer ring and an inner ring, both of which can be rotated to change the positions of the pieces.

5. How to Play
    1. Starting the Game:
        - In the terminal, type "python game.py"
        - The opening screen shows a menu of options and the ability to customize the infinite option (how many spaces left until a random piece gets deleted)
        - When the player selects play game, the game will start
        - Player will always go first, and he will be O. The robot will always go second and will be X.
        - The game begins with an empty 4x4 grid.
    2. Taking Turns:
        - Player takes turns with the robot placing their pieces on the board (According to the provided map: 1-4, qwer, asdf, zxcv).
        - By placing a piece, the player also choose to rotate either the outer ring or the inner ring of the board. 
        - The outer ring rotates anti-clockwise, and the inner ring rotates clockwise.
    3. Winning the Game:
        - The game is won by the first player to align four of their pieces in a row, column, or diagonal.
        - If all spaces on the board are filled and no player has aligned four pieces, the game ends in a draw.
    4. Playing Against the Robot:
        - When playing against the computer, the Robot uses advanced algorithms to predict the best possible moves and challenge the player.
    5. Infinite mode:
        - You can customized until how many spaces left will a random piece on the board gets deleted to add more fun!

6. Game Mechanics
- Rotation: The rotation mechanism adds a strategic element to the game. Player must think ahead not only about where to place their pieces but also how rotating the board will affect the game state.
- Prediction: The Robot uses a game tree to foresee possible moves and outcomes, ensuring it makes optimal decisions.

7. Simplified Summary of the Logic of the Code
The main program consists of three key components: GameBoard, Robot, and Tree. 
The GameBoard manages the game state, including the positions of chess pieces and whose turn it is. 
It has methods to rotate the board, display it, determine whose turn, check for available spaces, and identify winning patterns. 
The Robot acts as the AI player, using the Tree to predict possible moves. 
The Tree generates a game tree based on the current board state, assigning values to each node to determine the best move. 
It considers both conservative and aggressive strategies to predict future moves up to four steps ahead. 
The game mechanics include a rotation mechanism that affects piece positions and a winning mechanism that checks for patterns to determine the winner. 
The Robot uses these predictions to make the best possible move, ensuring a challenging game for the player.

8. Strategy Tips
- Plan Ahead: Consider both your moves and potential rotations to maximize your chances of winning.
- Block Opponents: Always be aware of your opponent's potential to align four pieces and block their moves.
- Use Rotations Wisely: Rotating the board can disrupt your opponent's strategy and create new opportunities for you.

Twist Tac Four is a game of skill, strategy, and foresight. 
It offers an engaging experience that combines elements of classic board games with modern AI technology, providing endless strategic possibilities.
Whether playing against a friend or the computer, it offers a dynamic and challenging experience that keeps player engaged and entertained. 
Enjoy the game and may the best strategist win! 

#Demo Video: https://youtu.be/XhFQoipspb8
#Trailer Video: https://youtu.be/yIUieJZs9JE
