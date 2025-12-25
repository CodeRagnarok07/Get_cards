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

def menu_interactivo(lista_opciones, buscador=False):
    """Muestra un menú interactivo con buscador opcional y retorna la opción seleccionada."""
    indice_seleccionado = 0
    query = ""
    MAX_VISIBLES = 15  # Número máximo de opciones a mostrar al mismo tiempo
    
    # Ocultar cursor
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        print(f"{Style.DIM}Usa las flechas (↑/↓) para moverte, escribe para filtrar y Enter para seleccionar{Style.RESET_ALL}\n")

        while True:
            # Filtrar opciones
            if buscador and query:
                opciones_filtradas = [o for o in lista_opciones if query.lower() in o.lower()]
            else:
                opciones_filtradas = lista_opciones

            if not opciones_filtradas:
                opciones_visuales = [f"{Fore.RED}No se encontraron resultados{Style.RESET_ALL}"]
                hay_resultados = False
                total_a_mostrar = 1
            else:
                hay_resultados = True
                if indice_seleccionado >= len(opciones_filtradas):
                    indice_seleccionado = len(opciones_filtradas) - 1
                
                # Calcular ventana de visualización (paginación)
                if len(opciones_filtradas) <= MAX_VISIBLES:
                    opciones_visuales = opciones_filtradas
                    inicio_ventana = 0
                else:
                    # Centrar el índice seleccionado si es posible
                    inicio_ventana = max(0, indice_seleccionado - MAX_VISIBLES // 2)
                    if inicio_ventana + MAX_VISIBLES > len(opciones_filtradas):
                        inicio_ventana = len(opciones_filtradas) - MAX_VISIBLES
                    
                    opciones_visuales = opciones_filtradas[inicio_ventana:inicio_ventana + MAX_VISIBLES]
                
                total_a_mostrar = len(opciones_visuales)

            # Dibujar buscador
            if buscador:
                sys.stdout.write(f"\r{Fore.YELLOW}Buscador: {Style.BRIGHT}{query}{Style.NORMAL}{Fore.WHITE}_   {Style.RESET_ALL}\033[K\n")

            # Dibujar opciones
            for i, opcion in enumerate(opciones_visuales):
                real_idx = i + (inicio_ventana if hay_resultados else 0)
                if hay_resultados and real_idx == indice_seleccionado:
                    sys.stdout.write(f"\r{Fore.CYAN}{Style.BRIGHT}  ➜  {opcion}{Style.RESET_ALL}\033[K\n")
                else:
                    sys.stdout.write(f"\r     {opcion}{Style.RESET_ALL}\033[K\n")
            
            # Indicador de más opciones
            if hay_resultados and len(opciones_filtradas) > MAX_VISIBLES:
                if inicio_ventana + MAX_VISIBLES < len(opciones_filtradas):
                     sys.stdout.write(f"\r     {Style.DIM}... y {len(opciones_filtradas) - (inicio_ventana + MAX_VISIBLES)} más ...{Style.RESET_ALL}\033[K\n")
                     total_a_mostrar += 1
            
            sys.stdout.flush()

            tecla = obtener_tecla()

            # Mover el cursor hacia arriba para redibujar
            cant_lineas = total_a_mostrar + (1 if buscador else 0)
            sys.stdout.write(f"\033[{cant_lineas}A")

            if tecla == '\x1b[A':  # Flecha Arriba
                if hay_resultados:
                    indice_seleccionado = (indice_seleccionado - 1) % len(opciones_filtradas)
            elif tecla == '\x1b[B':  # Flecha Abajo
                if hay_resultados:
                    indice_seleccionado = (indice_seleccionado + 1) % len(opciones_filtradas)
            elif tecla == '\r' or tecla == '\n':  # Enter
                if hay_resultados:
                    # Limpiar el área antes de salir
                    sys.stdout.write(f"\033[J") # Limpiar desde el cursor hasta el final
                    return opciones_filtradas[indice_seleccionado]
            elif buscador and (tecla == '\x7f' or tecla == '\x08'):  # Backspace
                query = query[:-1]
                indice_seleccionado = 0
                sys.stdout.write("\033[J") # Limpiar lo que sobra si la lista cambia
            elif tecla == '\x03':  # Ctrl+C
                sys.stdout.write(f"\033[{cant_lineas}B\n")
                sys.exit(0)
            elif buscador and len(tecla) == 1 and tecla.isprintable():
                query += tecla
                indice_seleccionado = 0
                sys.stdout.write("\033[J")
    finally:
        # Mostrar cursor de nuevo
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()



