import copy
import queue
import random
import time
import os
import opening #Imports from opening.py
from typing import Union

total_step = 4 # Total number of steps for the robot's decision tree depth
PLAYER_MARKER = "O"
ROBOT_MARKER = "X"
EMPTY_CELL = " "


class GameBoard: # Class representing the game board
    def __init__(self):
        self.gameBoard=[[EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],[EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],[EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],[EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL]] # Initialize the game board as a 4x4 grid
        self.turn = True #Player's or robot's turn (True for player, False for robot)
    
    def rotateBoard(self): 
        #Dividing outer and inner parts of the board
        outer_rotate_list = [[0,0],[1,0],[2,0],[3,0],[3,1],[3,2],[3,3],[2,3],[1,3],[0,3],[0,2],[0,1]] 
        inner_rotate_list = [[1,1],[1,2],[2,2],[2,1]]
        temp = copy.copy(self.gameBoard[outer_rotate_list[0][1]][outer_rotate_list[0][0]])
        #Rotating outer grid anticlockwise
        for i in range(1,len(outer_rotate_list)):
            self.gameBoard[outer_rotate_list[i-1][1]][outer_rotate_list[i-1][0]] = copy.copy(self.gameBoard[outer_rotate_list[i][1]][outer_rotate_list[i][0]])
        self.gameBoard[outer_rotate_list[len(outer_rotate_list)-1][1]][outer_rotate_list[len(outer_rotate_list)-1][0]]=temp
        #Rotating inner grid clockwise
        temp = copy.copy(self.gameBoard[inner_rotate_list[0][1]][inner_rotate_list[0][0]])
        for i in range(1,len(inner_rotate_list)):
            self.gameBoard[inner_rotate_list[i-1][1]][inner_rotate_list[i-1][0]] = copy.copy(self.gameBoard[inner_rotate_list[i][1]][inner_rotate_list[i][0]])
        self.gameBoard[inner_rotate_list[len(inner_rotate_list)-1][1]][inner_rotate_list[len(inner_rotate_list)-1][0]]=temp

    def drawBoard(self): # Draw the game board in the console
        actionBoard = [["1", "2", "3", "4"], ['q', 'w', 'e', 'r'], ['a', 's', 'd', 'f'],['z', 'x', 'c', 'v']] # Action board showing user input options
        print("╔═══╦═══╦═══╦═══╗", end=' ')
        print("║", end=' ')
        print("╔═══╦═══╦═══╦═══╗")
        for i in range(4):
            for j in range(4): # Draw the game board
                print("║",end="")
                print(" ",end='')
                print(self.gameBoard[i][j],end="", flush=True) #Prints the elements inside the board (the X and O's)
                print(" ",end='')
            print("║", end=' ')
            print("║", end=' ')
            for j in range(4): # Draw the action board
                print("║",end="")
                print(" ",end="")
                print(actionBoard[i][j],end="", flush=True) #Prints what inputs the user should type corresponding to the grid
                print(" ",end="")
            print("║")
            if i < 3:
                print("╠═══╬═══╬═══╬═══╣ ║ ╠═══╬═══╬═══╬═══╣")
            else: 
                print("╚═══╩═══╩═══╩═══╝ ║ ╚═══╩═══╩═══╩═══╝")
    #Execute the next move
    def nextMove(self,next_move):
        #global turn
        a = ROBOT_MARKER
        if(self.turn): #If self.turn is false, it is robots turn, if not then it's the player's turn 
            a = PLAYER_MARKER
        if(self.gameBoard[next_move[1]][next_move[0]] != EMPTY_CELL): #Error if user tries to input in non blank spaces
            return False
        self.gameBoard[next_move[1]][next_move[0]] = a #Placing pieces on the board
        self.turn = not self.turn #Switching turns
        return True
    
    def win(self,pattern): # Check if a specific pattern results in a win
        a = self.gameBoard[pattern[0][1]][pattern[0][0]]
        if(a != PLAYER_MARKER and a != ROBOT_MARKER): # If the first cell in the pattern is empty, it's not a win
            return [False, ROBOT_MARKER]
        for i in range(3): # Check if all cells in the pattern contain the same piece
            if(a != self.gameBoard[pattern[i+1][1]][pattern[i+1][0]]):
                return [False, ROBOT_MARKER]
        return [True, a]
    def noSpace(self): #Check if the board is full, if so = draw
        no_space = True
        for i in self.gameBoard:
            for j in i:
                if j == EMPTY_CELL:
                    no_space = False
        return no_space
    def checkWin(self): #Check if someone has won
        pattern_list = []
        for i in range(4): # Define patterns for rows, columns, and diagonals
            pattern_list.append([])
            for j in range(4):
                pattern_list[i].append([i,j])
        for i in range(4):
            pattern_list.append([])
            for j in range(4):
                pattern_list[i+4].append([j,i])
        pattern_list.append([[0,0],[1,1],[2,2],[3,3]])
        pattern_list.append([[3,0],[2,1],[1,2],[0,3]])
        won = False
        ready_to_win = False
        winner = None
        for i in range(len(pattern_list)):
            if(self.win(pattern_list[i])[0] and self.win(pattern_list[i])[1] == ROBOT_MARKER):
                if(won==True and winner == PLAYER_MARKER):
                    return "Draw"
                won=True
                winner=ROBOT_MARKER
            if(self.win(pattern_list[i])[0] and self.win(pattern_list[i])[1] == PLAYER_MARKER):
                if(won==True and winner == ROBOT_MARKER):
                    return "Draw"
                won=True
                winner=PLAYER_MARKER
        if(won):
            return winner
        else:
            if(self.noSpace()):
                return "Draw"
            else:
                return "NotYet"
    
    def checkReadyToWin(self):
        outer_rotate_list = [[0,0],[1,0],[2,0],[3,0],[3,1],[3,2],[3,3],[2,3],[1,3],[0,3],[0,2],[0,1]]
        inner_rotate_list = [[1,1],[1,2],[2,2],[2,1]]
        max_length = 1
        length = 1
        first_length = 1
        first = True
        chess_type = EMPTY_CELL
        current_chess_type = self.gameBoard[outer_rotate_list[0][1]][outer_rotate_list[0][0]]
        for i in range(len(outer_rotate_list)-1):
            if(current_chess_type != EMPTY_CELL and current_chess_type == self.gameBoard[outer_rotate_list[i+1][1]][outer_rotate_list[i+1][0]]):
                length+=1
                if(first):
                    first_length+=1
                if(max_length<length):
                    max_length=length
                    chess_type = current_chess_type
            else:
                first=False
                current_chess_type = self.gameBoard[outer_rotate_list[i+1][1]][outer_rotate_list[i+1][0]]
                length=1
        if(self.gameBoard[outer_rotate_list[0][1]][outer_rotate_list[0][0]] == current_chess_type and current_chess_type != EMPTY_CELL):
            length += first_length
            if(max_length < length):
                    max_length = length
                    chess_type = current_chess_type
        if(max_length==4):
            if(chess_type == PLAYER_MARKER):
                return 0.9
            else:
                return -0.9
        pattern_list = []
        pattern_list.append([[0,0],[1,1],[2,2],[3,3]])
        pattern_list.append([[3,0],[2,1],[1,2],[0,3]])
        pattern_list.append([[1,1],[3,1],[1,2],[0,3]])
        pattern_list.append([[0,0],[1,1],[2,1],[2,3]])
        pattern_list.append([[3,0],[2,1],[2,2],[0,2]])
        pattern_list.append([[1,0],[1,2],[2,2],[3,3]])
        pattern_list.append([[1,0],[2,1],[1,2],[2,3]])
        pattern_list.append([[2,0],[1,1],[2,2],[1,3]])
        pattern_list.append([[0,1],[1,2],[2,1],[3,2]])
        pattern_list.append([[0,2],[1,1],[2,2],[3,1]])
        for i in range(len(pattern_list)):
            if(self.win(pattern_list[i])[0] and self.win(pattern_list[i])[1] == PLAYER_MARKER):
                return 0.9
            if(self.win(pattern_list[i])[0] and self.win(pattern_list[i])[1] == ROBOT_MARKER):
                return -0.9
        num_X = 0
        num_0 = 0
        for i in range(len(inner_rotate_list)):
            if(self.gameBoard[inner_rotate_list[i][1]][inner_rotate_list[i][0]] == ROBOT_MARKER):
                num_X += 1
            if(self.gameBoard[inner_rotate_list[i][1]][inner_rotate_list[i][0]] == PLAYER_MARKER):
                num_0 += 1
        if(num_0 > 3):
            return 0.2
        elif(num_X > 3):
            return -0.2
        return 0
    
    def blank(self): #Count number of blank spaces
        num = 0
        for i in range(4):
            for j in range(4):
                if(self.gameBoard[i][j] == EMPTY_CELL):
                    num += 1
        return num #Randomly replaces a piece on the board
    
    def randomRemove(self): # Randomly remove a piece from the board
        a = True
        while(a): #Loops until a non blank space is deleted
            #Randomizing the coordinate where a piece gets deleted
            i = random.randint(0,3)
            j = random.randint(0,3)
            if(self.gameBoard[i][j] != EMPTY_CELL): #Check if the coordinate selected is blank or not
                self.gameBoard[i][j] = EMPTY_CELL #Deleting the piece
                a = False #Stopping the loop
        return

# =========================================================================================
class Robot:
    def __init__(self):
        self.game_tree = Tree() #Initialize the robot's decision tree

    def getNextStep(self,board): # Get the next move from the decision tree
        return self.game_tree.getNextStep(board,copy.copy(total_step)).position

# =========================================================================================
percentage = 0 # Helper variable for tracking progress of the robot
class Tree: # Tree class for managing the decision-making process
    def __init__(self):

        self.preserving_value = 0
        self.aggressive_value = 0
        self.position = []
    
    def buildTree(self,board,step,position: Union[str, list] = "NA"): # Build the tree for the robot's decision-making
        global total_step
        son = []
        stage = board.checkWin()
        self.position = position
        
        # Progress calculation for loading
        global percentage
        global game_board
        percentage +=1
        base = 1
        blank = game_board.blank()
        for i in range(total_step): #Counting the steps to make the progress bar
            base = base*blank
            blank-=1
            if blank == 0:
                break # Prevents base from becoming zero
        if base != 0:
            loading_percentage = int(percentage / base * 100)
            if loading_percentage > 100:
                loading_percentage = 100  # Cap the percentage at 100%
            print(f"loading: {loading_percentage}%", end='\r')
        else:
            print("Error: Division by zero", end='\r')
        #Game results for every possible moves (0 for nothing, 1 if player has the advantage, -1 if robot does)
        if(stage == "Draw"):
            self.preserving_value = self.aggressive_value = 0
        elif(stage == PLAYER_MARKER):
            self.preserving_value = self.aggressive_value = 1
        elif(stage == ROBOT_MARKER):
            self.preserving_value = self.aggressive_value = -1
        else: #Explore possible moves
            for i in range(4):
                for j in range(4):
                    temp_board = copy.deepcopy(board)
                    if(temp_board.gameBoard[i][j] == EMPTY_CELL and step != 0):

                        temp_board.nextMove([j,i])
                        temp_board.rotateBoard()
                        temp_tree = Tree()
                        temp_tree.buildTree(copy.deepcopy(temp_board),copy.copy(step)-1,[copy.copy(j),copy.copy(i)])
                        son.append(temp_tree)
                        #self.board.gameBoard[i][j]==" "
        
        # Progress calculation for loading
        self.SetPreservingValue(step,son,board)
        self.SetAggressiveValue(step,son,board)

        #print("bottom")
        return son

    def getNextStep(self,board,step,position="NA"): # Get the next move from the decision tree
        return self.findGreatestValue(step,self.buildTree(board,step,position),board)
    def whoseTurn(self,board): # Check whose turn it is based on the board state
        o = 0
        x = 0
        for i in range(4):
            for j in range(4):
                if(board.gameBoard[j][i] == ROBOT_MARKER):
                    x += 1
                elif(board.gameBoard[j][i] == PLAYER_MARKER):
                    o += 1
        if(o == x):
            return PLAYER_MARKER
        else:
            return ROBOT_MARKER
    # Find the best move based on the decision tree's values
    def findGreatestValue(self,step,son,board):
        #preserving value
        global total_step
        possible_choice = []
        best_choice = []
        if(len(son) == 0):
            return Tree()
        # Find the move with the best preserving value
        if(self.whoseTurn(board) == PLAYER_MARKER):
            max_min = son[0].preserving_value
            for i in range(len(son)):
                if(max_min < son[i].preserving_value):
                    max_min = son[i].preserving_value
        else:
            max_min = son[0].preserving_value
            for i in range(len(son)):
                if(max_min > son[i].preserving_value):
                    max_min = son[i].preserving_value
        for i in range(len(son)):
            if(son[i].preserving_value == max_min):
                possible_choice.append(copy.copy(son[i]))
        # Find the move with the best aggressive value
        max_min = possible_choice[0].aggressive_value
        for i in range(len(possible_choice)):
            if((total_step-step)%2 == 0):
                if(max_min < possible_choice[i].aggressive_value):
                    max_min = possible_choice[i].aggressive_value
            else:
                if(max_min > possible_choice[i].aggressive_value):
                    max_min = possible_choice[i].aggressive_value
        for i in range(len(possible_choice)):
            if(max_min == possible_choice[i].aggressive_value):
                best_choice.append(possible_choice[i])
        # Randomly pick one of the best choices
        return best_choice[random.randint(0,len(best_choice)-1)]

    # Set the preserving value for this node in the tree
    def SetPreservingValue(self,step,son,board):
        #print("to bottom of tree")
        if(board.blank() == 14):
            if(board.gameBoard[1][1] == ROBOT_MARKER or board.gameBoard[2][1] == ROBOT_MARKER or board.gameBoard[1][2] == ROBOT_MARKER or board.gameBoard[2][2] == ROBOT_MARKER):
                self.preserving_value = -0.5
                return
        if(step == 0):
            self.preserving_value = board.checkReadyToWin()
            return
        if(len(son) == 0):
            return
        if(self.whoseTurn(board) == PLAYER_MARKER):
            #print(son,step)
            max_min = son[0].preserving_value
            for i in range(len(son)):
                if(max_min < son[i].preserving_value):
                    max_min = son[i].preserving_value
        else:
            max_min = son[0].preserving_value
            for i in range(len(son)):
                if(max_min > son[i].preserving_value):
                    max_min = son[i].preserving_value
        self.preserving_value = copy.copy(max_min)

    # Set the aggressive value for this node in the tree
    def SetAggressiveValue(self,step,son,board):
        if(step == 0):
            self.aggressive_value = board.checkReadyToWin()
            return
        for i in range(len(son)):
            self.aggressive_value += son[i].aggressive_value

def sleep(): # Sleep function placeholder
    print("sleep")
def endGameCheck(): #check if the game has finished/ended
    global finished
    if(game_board.checkWin() == PLAYER_MARKER): #If player wins
        print("You Win!!! Congratulations")
        game_board.drawBoard()
        finished = True
    elif(game_board.checkWin() == "NotYet"): #When theres no 4 in a row yet
        print("Next Turn")
    elif(game_board.checkWin() == ROBOT_MARKER):
        print("You Lose, better luck next time.") #If "X" wins i.e. the robot
        finished = True
    elif(game_board.checkWin() == "Draw"): #If board is full or 2 lines are made at the same time
        print("Wow, It's a Draw")
        finished = True

# ========================================================================================================================
def main(): 
    # Initialize the game by calling the classes
    global game_board, robot, record, finished, infinimode
    game_board = GameBoard()
    robot = Robot()
    record = queue.Queue()

    # Making a variable "finished"
    finished = False
    opening.clear_screen()
    infinimode = opening.screen() #running the opening screen and customizing the infinite mode

    playAgain = "yes"
    while playAgain.lower() == "yes": #Loop if user wants to play again
        while(not finished): #Main loop of the game
            opening.clear_screen()
            game_board.drawBoard()
            #print("|1|2|3|4|\n|q|w|e|r|\n|a|s|d|f|\n|z|x|c|v|")
            # Get player's move
            in_a = input("Input the corresponding index: ")
            while in_a not in ["1", "2", "3", "4", 'q', 'w', 'e', 'r', 'a', 's', 'd', 'f', 'z', 'x', 'c', 'v']: #Catching inputs which are invalid
                print("Input not in board. Please input a valid position.")
                in_a = input("Input the corresponding index: ")
            a_list = [['1','2','3','4'],['q','w','e','r'],['a','s','d','f'],['z','x','c','v']]
            a = []

            # Map input to coordinates
            for i, row in enumerate(a_list):
                for j, element in enumerate(row):
                    if element == in_a:
                        a = [j,i]
            # Place the player's piece
            while(not game_board.nextMove(copy.copy(a))):
                in_a = input("Input the corresponding index (please put chess piece to empty spaces): ")
                for i, row in enumerate(a_list):
                    for j, element in enumerate(row):
                        if element == in_a:
                            a = [j,i]
            #User's turn
            record.put(copy.copy(a))
            opening.clear_screen()
            game_board.drawBoard()
            print("Before Rotation")
            time.sleep(2)
            opening.clear_screen()
            game_board.rotateBoard() #Calling rotateboard
            game_board.drawBoard() #Print board
            print("After Rotation")
            endGameCheck() #Check if the game is done (finished true or not)
            if(finished==True):
                break
            
            # Check if a random piece needs to be removed
            if(game_board.blank()<infinimode): #If the number of blanks are less than the mode
                game_board.randomRemove() #Removing random piece
                print("Randomly removing 1 chess piece")
                time.sleep(2.5)
                opening.clear_screen()
                game_board.drawBoard()
            
            # Robot's turn
            print("Robot is thinking")
            a=robot.getNextStep(copy.copy(game_board))
            percentage = 0
            record.put(copy.copy(a))
            opening.clear_screen()
            game_board.nextMove(copy.copy(a))
            game_board.drawBoard()
            print("Before Rotation")
            time.sleep(2)
            opening.clear_screen()
            game_board.rotateBoard()
            game_board.drawBoard()
            print("After Rotation")
            endGameCheck()
            if(finished==True):
                break
            time.sleep(1)
            
            # Check if a random piece needs to be removed
            if(game_board.blank()<infinimode):
                opening.clear_screen()
                print("Randomly removing 1 piece...")
                game_board.randomRemove()
                game_board.drawBoard()
                time.sleep(1)
        
        # Ask if the player wants to play again
        playAgain = input("Do you want to play again? (Yes/No): ")
        if playAgain.lower() == "yes":
            infinimode = opening.screen()
            game_board = GameBoard() #Restarting the board
            finished = False #Changing finished value from True to False

    print("Thanks For Playing!")

if __name__ == "__main__":
    main()