import turtle

# ------------------------------------------------------------
# Módulo auxiliar de dibujo con Turtle.
# Recibe una lista de comandos ya tokenizados y los ejecuta en
# orden para generar la figura.
# ------------------------------------------------------------

def draw_figure(commands):
    # --------------------------------------------------------
    # Configuración inicial de ventana y puntero de dibujo.
    # --------------------------------------------------------
    screen = turtle.Screen()
    t = turtle.Turtle()
    t.speed(1)

    # --------------------------------------------------------
    # Ejecución de comandos:
    # - A# => avanzar distancia
    # - G# => girar a la derecha
    # --------------------------------------------------------
    for cmd in commands:
        if cmd.startswith('A'):
            dist = int(cmd[1:])
            t.forward(dist)
        elif cmd.startswith('G'):
            angle = int(cmd[1:])
            t.right(angle)

    # Mantiene la ventana abierta hasta cierre manual.
    screen.mainloop()