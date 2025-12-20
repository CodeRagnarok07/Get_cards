import sys
import tty
import termios
from colorama import init, Fore, Style

# Inicializar colorama para soporte de colores ANSI
init(autoreset=True)



def obtener_tecla():
    """Lee una sola tecla del usuario sin esperar a Enter."""
    fd = sys.stdin.fileno()
    original_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':  # Secuencia de escape (flechas, etc.)
            ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, original_settings)
    return ch

def menu_interactivo(lista_opciones):
    """Muestra un menú interactivo y retorna la opción seleccionada."""
    indice_seleccionado = 0
    
    # Ocultar cursor
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        print(f"{Style.DIM}Usa las flechas (↑/↓) para moverte y Enter para seleccionar{Style.RESET_ALL}\n")

        while True:
            # Dibujar opciones
            for i, opcion in enumerate(lista_opciones):
                if i == indice_seleccionado:
                    sys.stdout.write(f"{Fore.CYAN}{Style.BRIGHT}  ➜  {opcion}{Style.RESET_ALL}\n")
                else:
                    sys.stdout.write(f"     {opcion}\n")
            sys.stdout.flush()

            tecla = obtener_tecla()

            # Mover el cursor hacia arriba para redibujar el menú en la siguiente iteración
            sys.stdout.write(f"\033[{len(lista_opciones)}A")
            sys.stdout.flush()

            if tecla == '\x1b[A':  # Flecha Arriba
                indice_seleccionado = (indice_seleccionado - 1) % len(lista_opciones)
            elif tecla == '\x1b[B':  # Flecha Abajo
                indice_seleccionado = (indice_seleccionado + 1) % len(lista_opciones)
            elif tecla == '\r' or tecla == '\n':  # Enter
                # Mover cursor al final del menú antes de salir
                sys.stdout.write(f"\033[{len(lista_opciones)}B")
                sys.stdout.flush()
                return lista_opciones[indice_seleccionado]
            elif tecla == '\x03':  # Ctrl+C (KeyboardInterrupt)
                sys.stdout.write(f"\033[{len(lista_opciones)}B")
                sys.stdout.flush()
                sys.exit(0)
    finally:
        # Mostrar cursor de nuevo
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

