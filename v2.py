from imports import *

menu = ["EZPASS", "", "LOGIN", "RESET", "EXIT"]

def print_menu(stdscr, selected_row):
    stdscr.clear()
    for idx, row in enumerate(menu):
        if idx == selected_row:
            stdscr.addstr(idx, 0, row, curses.A_REVERSE)  # Highlight current row
        else:
            stdscr.addstr(idx, 0, row)
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0) #Set invis cursor for title of app
    print_menu(stdscr, 2) #print intial menu
    current_row = 2

    while True:
        key_pressed = stdscr.getch()
        
        if key_pressed == curses.KEY_UP and current_row > 2:
            current_row -= 1
        elif key_pressed == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1

        print_menu(stdscr, current_row)
        
        if key_pressed == curses.KEY_ENTER or key_pressed in [10, 13]:
            if current_row == 2:
                curses.curs_set(1)
                stdscr.addstr(2, 0, "USERNAME: ")
                stdscr.addstr(2, 0, "PASSWORD: ")
                curses.echo()
                username_attempt = stdscr.getstr(2, 10, 50)
                master_password_attempt = stdscr.getstr(3, 10, 50)
                curses.curs_set(0)
                stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)