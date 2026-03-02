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
    screen.mainloop()