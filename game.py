import copy
import queue
import random
import time
import os
import opening #Imports from opening.py
total_step = 4 # Total number of steps for the robot's decision tree depth

class GameBoard: # Class representing the game board
    def __init__(self):
        self.gameBoard=[[" "," "," "," "],[" "," "," "," "],[" "," "," "," "],[" "," "," "," "]] # Initialize the game board as a 4x4 grid
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
        a = "X"
        if(self.turn): #If self.turn is false, it is robots turn, if not then it's the player's turn 
            a = "0"
        if(self.gameBoard[next_move[1]][next_move[0]]!=" "): #Error if user tries to input in non blank spaces
            return False
        self.gameBoard[next_move[1]][next_move[0]] = a #Placing pieces on the board
        self.turn = not self.turn #Switching turns
        return True
    
    def win(self,pattern): # Check if a specific pattern results in a win
        a = self.gameBoard[pattern[0][1]][pattern[0][0]]
        if(a!="0" and a!="X"): # If the first cell in the pattern is empty, it's not a win
            return [False,"X"]
        for i in range(3): # Check if all cells in the pattern contain the same piece
            if(a != self.gameBoard[pattern[i+1][1]][pattern[i+1][0]]):
                return [False,"X"]
        return [True,a]
    def noSpace(self): #Check if the board is full, if so = draw
        no_space = True
        for i in self.gameBoard:
            for j in i:
                if j == " ":
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
        for i in range(len(pattern_list)):
            if(self.win(pattern_list[i])[0] and self.win(pattern_list[i])[1]=="X"):
                if(won==True and winner=="0"):
                    return "Draw"
                won=True
                winner="X"
            if(self.win(pattern_list[i])[0] and self.win(pattern_list[i])[1]=="0"):
                if(won==True and winner=="X"):
                    return "Draw"
                won=True
                winner="0"
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
        chess_type = " "
        current_chess_type = self.gameBoard[outer_rotate_list[0][1]][outer_rotate_list[0][0]]
        for i in range(len(outer_rotate_list)-1):
            if(current_chess_type!=" " and current_chess_type == self.gameBoard[outer_rotate_list[i+1][1]][outer_rotate_list[i+1][0]]):
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
        if(self.gameBoard[outer_rotate_list[0][1]][outer_rotate_list[0][0]]==current_chess_type and current_chess_type!=" "):
            length+=first_length
            if(max_length<length):
                    max_length=length
                    chess_type = current_chess_type
        if(max_length==4):
            if(chess_type=="0"):
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
            if(self.win(pattern_list[i])[0] and self.win(pattern_list[i])[1]=="0"):
                return 0.9
            if(self.win(pattern_list[i])[0] and self.win(pattern_list[i])[1]=="X"):
                return -0.9
        num_X = 0
        num_0 = 0
        for i in range(len(inner_rotate_list)):
            if(self.gameBoard[inner_rotate_list[i][1]][inner_rotate_list[i][0]]=="X"):
                num_X+=1
            if(self.gameBoard[inner_rotate_list[i][1]][inner_rotate_list[i][0]]=="0"):
                num_0+=1
        if(num_0>3):
            return 0.2
        elif(num_X>3):
            return -0.2
        return 0
    
    def blank(self): #Count number of blank spaces
        num = 0
        for i in range(4):
            for j in range(4):
                if(self.gameBoard[i][j]==" "):
                    num+=1
        return num #Randomly replaces a piece on the board
    
    def randomRemove(self): # Randomly remove a piece from the board
        a = True
        while(a): #Loops until a non blank space is deleted
            #Randomizing the coordinate where a piece gets deleted
            i = random.randint(0,3)
            j = random.randint(0,3)
            if(self.gameBoard[i][j]!=" "): #Check if the coordinate selected is blank or not
                self.gameBoard[i][j]=" " #Deleting the piece
                a = False #Stopping the loop
        return

