from imports import *

import curses

def main(stdscr):
    curses.curs_set(1)  # Show the cursor for text input
    stdscr.clear()

    # Display menu options
    menu = ["Option 1", "Option 2", "Option 3", "Enter text"]
    current_row = 0

    # Function to display the menu
    def print_menu(stdscr, selected_row):
        stdscr.clear()
        for idx, row in enumerate(menu):
            if idx == selected_row:
                stdscr.addstr(idx, 0, row, curses.A_REVERSE)  # Highlight current row
            else:
                stdscr.addstr(idx, 0, row)
        stdscr.refresh()

    print_menu(stdscr, current_row)

    while True:
        key = stdscr.getch()

        # Navigate the menu
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1

        print_menu(stdscr, current_row)

        # If user presses Enter
        if key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == len(menu) - 1:  # If "Enter text" is selected
                stdscr.addstr(5, 0, "USERNAME: ")
                curses.echo()  # Enable echoing of characters to screen
                user_input = stdscr.getstr(len(menu) + 1, 10, 50)  # Get up to 20 characters
                stdscr.addstr(len(menu) + 2, 0, f"Your input: {user_input.decode('utf-8')}")
                stdscr.refresh()
                stdscr.getch()  # Wait for user to see the input before exiting
                break
            else:
                stdscr.addstr(len(menu), 0, f"You selected: {menu[current_row]}")
                stdscr.refresh()
                stdscr.getch()  # Pause to see the result
if __name__ == "__main__":
    curses.wrapper(main)
