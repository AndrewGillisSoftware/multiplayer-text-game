from computer_api.display import *
CURSOR = ">"

def set_cursor():
    set_display_at(0, DISPLAY_ROWS - 1, CURSOR)

def console_response(input):
    return "? SYNTAX ERROR"

def console_prompt():
    set_cursor()
    print_display()

    set_cursor()
    user_input = input(">")
    set_display_at(1, DISPLAY_ROWS - 1, user_input)
    print_display()
    shift_up_display(1)

    response = console_response(user_input)
    set_display_at(0, DISPLAY_ROWS - 1, response)
    print_display()
    shift_up_display(1)

while True:
    console_prompt()