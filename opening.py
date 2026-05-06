import os
import time
import sys

def clear_screen():
    os.system('clear')

def loading_animation():
    animation = "|/-\\"
    for i in range(10):  # Adjust the range for a longer or shorter animation
        sys.stdout.write("\r\033[1;32mLoading... " + animation[i % len(animation)]) #ChatGPT was used in the making of this animation
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 20 + "\r")  # Clear the line

def display_title():
    clear_screen()
    print("""           ═════════════ >
          ╔═══╦═══╦═══╦═══╗
        ^ ║ X ║ O ║   ║ X ║ ║
        ║ ╠═══╬═══╬═══╬═══╣ ║
        ║ ║ O ║ X ║ O ║   ║ ║
        ║ ╠═══╬═══╬═══╬═══╣ ║
        ║ ║   ║ X ║ O ║ X ║ ║
        ║ ╠═══╬═══╬═══╬═══╣ ║
        ║ ║ O ║   ║ X ║ O ║ v
          ╚═══╩═══╩═══╩═══╝
           < ═════════════""")
    print("""
╔╦╗╦ ╦╦╔═╗╔╦╗  ╔╦╗╔═╗╔═╗  ╔═╗╔═╗╦ ╦╦═╗  
 ║ ║║║║╚═╗ ║    ║ ╠═╣║    ╠╣ ║ ║║ ║╠╦╝  
 ╩ ╚╩╝╩╚═╝ ╩    ╩ ╩ ╩╚═╝  ╚  ╚═╝╚═╝╩╚═ """)

def display_menu(queue):
    if queue == -1:
        queue = "Disabled"
    print("\033[1;92m          [1] \033[1;94mPlay Game")
    print("\033[1;92m          [2] \033[1;94mInfinite Mode" + f" ({queue}) ")
    print("\033[1;92m          [3] \033[1;94mHow to Play")
    print("\033[1;92m          [4] \033[1;94mQuit")
    print("\033[1;36m")

def handle_menu_choice(choice):
    os.system("clear")
    if choice == "1":
        loading_animation()  # Show loading animation after Play Game is selected
        print("\n\033[1;32mGame is starting!\033[0m")
        time.sleep(0.5)
    elif choice == "2":
        a = input("\n\033[1;33mBlank spaces until a piece gets removed (Default is 3, 0 to disable): \033[0m")
        a = str(a)
        while a.isnumeric() == False:
            print("Input invalid. Please try to type a valid input.")
            a = input("\n\033[1;33mBlank spaces until a piece gets removed (Default is 3, 0 to disable): \033[0m")
        a = int(a)
        while a < 0 or a > 16:
            print("Out of range, please input again")
            a = str(a)
            a = input("\n\033[1;33mBlank spaces until a piece gets removed (Default is 3, 0 to disable): \033[0m")
            while a.isnumeric() == False:
                print("Input invalid. Please try to type a valid input.")
                a = input("\n\033[1;33mBlank spaces until a piece gets removed (Default is 3, 0 to disable): \033[0m")
            a = int(a)
        if a == 0:
            return -1
        return a
    elif choice == "3":
        print("══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════")
        print('''Game Objective:
    1. The primary goal of Twist Tac Four is to align four of your pieces (either X or O) in a row, column, or diagonal on a 4x4 grid (After the Rotation). 
    2. The game can be played with one player against a computer-controlled opponent (The Robot).

How to Play:
    1. Starting the Game:
        - The opening screen shows a menu of options and the ability to customize the infinite option (how many spaces left until a random piece gets deleted)
        - When the player selects play game, the game will start
        - Player will always go first, and he will be O. The robot will always go second and will be X.
        - The game begins with an empty 4x4 grid.
    2. Taking Turns:
        - Player takes turns with the robot placing their pieces on the board (According to the provided map: 1-4, qwer, asd
        f, zxcv).
        - By placing a piece, the player also choose to rotate either the outer ring or the inner ring of the board. 
        - The outer ring rotates anti-clockwise, and the inner ring rotates clockwise.
    3. Winning the Game:
        - The game is won by the first player to align four of their pieces in a row, column, or diagonal.
        - If all spaces on the board are filled and no player has aligned four pieces, the game ends in a draw.
    4. Playing Against the Robot:
        - When playing against the computer, the Robot uses advanced algorithms to predict the best possible moves and 
        challenge the player.
    5. Infinite mode:
        - You can customized until how many spaces left will a random piece on the board gets deleted to add more fun!''')
        print("══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════")
        input("\033[1mPress Enter To Go Back")
    elif choice == "4":
        print("\n\033[1;31mWe hope you enjoy playing our game. Thank you and Goodbye!\033[0m")
        time.sleep(1)
        sys.exit()
    else:
        print("\n\033[1;31mInvalid choice. Please try again.\033[0m")
        time.sleep(1)

def screen():
    queue=3 #Default infinite mode
    choiceop = 0
    while choiceop != "1":
        display_title() #displays title
        display_menu(queue) #queue is inside to show the users customization
        choiceop = input("\033[1;36mSelect an option (1-4): \033[0m")
        a = handle_menu_choice(choiceop) #returns the infinite mode customization
        if a != None:
            queue = a #if handle_menu_choice does not return anything do not change the value of queue)
    return queue

if __name__ == "__main__":
    screen()
