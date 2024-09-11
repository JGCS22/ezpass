import curses


def print_menu(stdscr, selected_row_idx, menu):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def main(stdscr):
    # Turn off cursor blinking
    menu = ["LOGIN", "RESET", "EXIT"]
    curses.curs_set(0)

    # Enable arrow keys and mouse events
    stdscr.keypad(1)

    # Set up color pair for selected menu item
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row = 0
    print_menu(stdscr, current_row, menu)

    while True:
        key = stdscr.getch()

        # Handle key input
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu[current_row] == "LOGIN":
                menu.clear()
                menu = ["USERNAME", "PASSWORD"]
            if current_row == len(menu) - 1:  # Exit option
                break
            stdscr.addstr(0, 0, f"You selected {menu[current_row]}")
            stdscr.refresh()
        
        print_menu(stdscr, current_row, menu)

# Start curses application
curses.wrapper(main)