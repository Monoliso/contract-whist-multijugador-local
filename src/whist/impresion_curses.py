import time
import curses

def print_menu(ventana_v, selected_row_idx, seleccion):
    h, w = ventana_v.getmaxyx()
    for idx, row in enumerate(seleccion):
        x = w//2 - len(row)//2
        y = h//2 - len(seleccion)//2 + idx
        if idx == selected_row_idx:
            ventana_v.attron(curses.color_pair(1))
            ventana_v.addstr(y, x, row)
            ventana_v.attroff(curses.color_pair(2))
        else:
          ventana_v.addstr(y, x, row)
    ventana_v.refresh()

def imprimir_seleccion_modo(stdscr, altura_p: int, largo_p: int) -> None:
    
    nombre_juego = "Contract Whist"
    seleccion = ["1. Ingresar a una partida", "2. Crear una sala"]
    tamaño_nombre = 3, 18
    tamaño_seleccion = 8, 50
    coordx_nombre = largo_p//2 - len(nombre_juego)//2
    coordy_nombre = altura_p//5
    coordx_seleccion = largo_p//2 - tamaño_seleccion[1]//2
    coordy_seleccion = altura_p//2
    condicion_seleccion = True

    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
    nombre_v = curses.newwin(tamaño_nombre[0], tamaño_nombre[1], coordy_nombre, coordx_nombre)
    nombre_v.bkgd(' ', curses.color_pair(2))
    nombre_v.border()
    nombre_v.addstr(1, 2, nombre_juego, curses.A_UNDERLINE | curses.A_BOLD)

    seleccion_v = curses.newwin(tamaño_seleccion[0], tamaño_seleccion[1], coordy_seleccion, coordx_seleccion)
    seleccion_v.border()

    current_row = 0
    while condicion_seleccion:
        key = seleccion_v.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(seleccion)-1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            seleccion_v.getch()
    		# if user selected last row, exit the program
            if current_row == len(seleccion)-1:
                break
        
        print_menu(seleccion_v, current_row, seleccion)

    # nombre_v.getch()
    # stdscr.addstr("xd")
    # stdscr.getch()
    # ventana.bkgdset(' ', curses.color_pair(1))

    # ventana.attroff(curses.color_pair(1))
    # stdscr. refresh()
    # time. sleep(3)

def main(stdscr):

    curses.curs_set(False)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    stdscr.bkgd(' ', curses.color_pair(1)) # Ojo, este método no se refresca automáticamente
    altura_p, largo_p = stdscr.getmaxyx()
    imprimir_seleccion_modo(stdscr, altura_p, largo_p)
    

curses.wrapper(main)