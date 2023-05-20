import math
import tkinter as tk

from board import Board
import time
import random

ST=""
depth=-1
S=False

#GUI to get algorithm
def select_answer(answer):
	global ST # Use the global variable
	# Disable all buttons except the selected one
	button1.config(state=tk.DISABLED)
	button2.config(state=tk.DISABLED)

    # Store the selected answer in the global variable
	ST = answer

    # Destroy the Tkinter window
	window.destroy()

# Create a new Tkinter window
window = tk.Tk()
# Set the size and background of the window
window.configure(bg='black')
window.geometry("400x400")

# Get the dimensions of the screen
screen_width = 850
screen_height = 300

# Calculate the position of the window to center it on the screen
x = (screen_width - window.winfo_reqwidth()) / 2
y = (screen_height - window.winfo_reqheight()) / 2

# Set the position of the window to center it on the screen
window.geometry("+%d+%d" % (x, y))

# Create a label for the question
label = tk.Label(window, text="Choose the algorithm you want", bg="black", fg="white", font=("Arial", 18, "bold"))
label.pack(pady=30)

# Create buttons for each possible answer
button1 = tk.Button(window, text="Minimax Algorithm", bg="blue", fg="white", font=("Arial", 20), command=lambda: select_answer("Minimax Algorithm"))
button1.pack(pady=30)
button2 = tk.Button(window, text="Alpha_Bita Algorithm", bg="red", fg="white", font=("Arial", 20), command=lambda: select_answer("Alpha_Bita Algorithm"))
button2.pack(pady=20)

# Start the event loop of the Tkinter window
window.mainloop()


if ST=="Minimax Algorithm":
	S=False
elif ST=="Alpha_Bita Algorithm":
    S=True
#print(S)
######################################################################### 
#GUI to get the game level
def select_answer(answer):
	global ST # Use the global variable
    
	button1.config(state=tk.DISABLED)
	button2.config(state=tk.DISABLED)
	button3.config(state=tk.DISABLED)

    # Store the selected answer in the global variable
    
	ST = answer

    # Destroy the Tkinter window
    
	window.destroy()

# Create a new Tkinter window
window = tk.Tk()

# Set the size and background of the window
window.configure(bg='black')
window.geometry("400x400")

# Get the dimensions of the screen
screen_width = 850
screen_height = 300

# Calculate the position of the window to center it on the screen
x = (screen_width - window.winfo_reqwidth()) / 2
y = (screen_height - window.winfo_reqheight()) / 2

# Set the position of the window to center it on the screen
window.geometry("+%d+%d" % (x, y))

# Create a label for the question
label = tk.Label(window, text="Choose the level of the game", bg="black", fg="white", font=("Arial", 20, "bold"))
label.pack(pady=30)

# Create buttons for each possible answer
button1 = tk.Button(window, text="EASY", bg="blue", fg="white", font=("Arial", 20), command=lambda: select_answer("EASY"))
button1.pack(pady=20)
button2 = tk.Button(window, text="MEDIUM", bg="red", fg="white", font=("Arial", 20), command=lambda: select_answer("MEDIUM"))
button2.pack(pady=20)
button3 = tk.Button(window, text="HARD", bg="green", fg="white", font=("Arial", 20), command=lambda: select_answer("HARD"))
button3.pack(pady=20)
# Start the event loop of the Tkinter window
window.mainloop()

if ST=="EASY":
	depth=4
elif ST=="MEDIUM":
	depth=6
elif ST=="HARD":
	depth=8
#print(depth)
#########################################################################

# GAME LINK
# http://kevinshannon.com/connect4/


def main():
    board = Board()

    time.sleep(2)
    game_end = False
    while not game_end:
        (game_board, game_end) = board.get_game_grid()

        # FOR DEBUG PURPOSES

        # YOUR CODE GOES HERE

        # Insert here the action you want to perform based on the output of the algorithm
        # You can use the following function to select a column

        # print("Selected column: " + str(random_column))
        # board.print_grid(game_board)

        if S==True:
           col, minimax_score = board.minimax(game_board, depth, -math.inf, math.inf, True, True)
        elif S==False:
             col, minimax_score = board.minimax(game_board, depth, -math.inf, math.inf, True, False)

        # print(game_board)

        if board.is_valid_location(game_board, col):
            board.select_column(col)

            # pygame.time.wait(500)
            row = board.get_next_open_row(game_board, col)

            board.drop_piece(game_board, row, col, 1)
            board.print_grid(game_board)

        time.sleep(2)
        # board.print_grid(game_board)


if __name__ == "__main__":
    main()
