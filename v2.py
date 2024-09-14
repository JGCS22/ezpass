from imports import *

def print_display(stdscr, display_menu, current_selection):
    stdscr.clear()
    for menu_item in display_menu:
        current_index = display_menu.index(menu_item)
        if current_index == current_selection:
            stdscr.addstr(current_index, 0, menu_item[0], curses.A_REVERSE)
        else:
            stdscr.addstr(current_index, 0, menu_item[0])
    stdscr.refresh()


def main(stdscr):
    display_menu = [["EZPASS", 0], ["", 0], ["LOGIN", 1], ["RESET", 1], ["BACK", 1]]
    current_selection = 2
    menu_state = 0

    username_attempt = ""
    master_password_attempt = ""

    curses.curs_set(0)
    print_display(stdscr, display_menu, current_selection)

    while True:
        if menu_state == 0:
            key_pressed = stdscr.getch()
            if key_pressed == curses.KEY_UP and current_selection > 2:
                current_selection -= 1
            elif key_pressed == curses.KEY_DOWN and current_selection < len(display_menu) - 1:
                current_selection += 1
                
            print_display(stdscr, display_menu, current_selection)

            if key_pressed == curses.KEY_ENTER or key_pressed in [10, 13]:
                if current_selection == 2:
                    

if __name__ == "__main__":
    curses.wrapper(main)