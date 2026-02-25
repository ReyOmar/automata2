import turtle
import re

def draw_figure(commands):
    screen = turtle.Screen()
    t = turtle.Turtle()
    t.speed(1)
    for cmd in commands:
        if cmd.startswith('A'):
            dist = int(cmd[1:])
            t.forward(dist)
        elif cmd.startswith('G'):
            angle = int(cmd[1:])
            t.right(angle)
        elif cmd.startswith('T'):
            size = int(cmd[1:])
            t.circle(size * 10)  # Escalar tamaño
    screen.mainloop()

# Ejemplo de uso
if __name__ == "__main__":
    # Cadena para cuadrado: A100 G90 A100 G90 A100 G90 A100 G90
    cadena_cuadrado = "A100G90A100G90A100G90A100G90"
    commands = re.findall(r'A\d+|G\d+|T\d+', cadena_cuadrado)
    draw_figure(commands)