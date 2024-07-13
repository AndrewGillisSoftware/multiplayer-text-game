import os

EMPTY_CHARACTER = "."
DISPLAY_ROWS, DISPLAY_COLS = (18,64)

# Correctly initialize the display matrix with separate lists for each row
display = [[EMPTY_CHARACTER] * DISPLAY_COLS for _ in range(DISPLAY_ROWS)]

def print_display():
    cls()
    for row in display:
        for character in row:
            print(str(character) + "", end="")
        print()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def set_display_at(posx, posy, string):
    for i in range(len(string)):
        display[posy][posx + i] = string[i]

def shift_up_display(shift_number):
    if shift_number >= DISPLAY_ROWS:
        # If x is greater than or equal to the number of rows, clear the entire display
        for i in range(DISPLAY_ROWS):
            display[i] = [EMPTY_CHARACTER] * DISPLAY_COLS
    else:
        # Shift the display up by x rows
        for i in range(shift_number, DISPLAY_ROWS):
            display[i - shift_number] = display[i]
        # Clear the last x rows
        for i in range(DISPLAY_ROWS - shift_number, DISPLAY_ROWS):
            display[i] = [EMPTY_CHARACTER] * DISPLAY_COLS

