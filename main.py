import tkinter as tk
from tkinter import messagebox, ttk
from dfa import dfa
import re
import math
from PIL import Image, ImageTk
import os

# Estado global
current_x = 125
current_y = 125
current_angle = 0
figure_count = 0
gif_animation_id = None
current_gif_frame = 0
gif_frames = []
gif_label = None

# Posiciones para 4 cuadrantes (plano cartesiano 2x2)
# Canvas 500x500 dividido en 4 cuadrantes iguales
positions = [
    (125, 125),   # Cuadrante 1: arriba-izquierda
    (375, 125),   # Cuadrante 2: arriba-derecha
    (125, 375),   # Cuadrante 3: abajo-izquierda
    (375, 375)    # Cuadrante 4: abajo-derecha
]

def draw_command(canvas, cmd, state_text=None):
    global current_x, current_y, current_angle, figure_count
    
    # Mostrar el estado ANTES de ejecutar el comando
    if state_text:
        # Dibujar un pequeño círculo para marcar la posición del estado
        canvas.create_oval(current_x - 3, current_y - 3, current_x + 3, current_y + 3, fill="red", outline="red")
        
        # Extraer el número del estado (q0, q1, q2, etc.)
        state_num = int(state_text[1:]) if len(state_text) > 1 else 0
        
        # Distribuir los estados alrededor del punto para evitar superposición
        positions_offset = [
            (-15, -15),  # arriba-izquierda
            (15, -15),   # arriba-derecha
            (15, 15),    # abajo-derecha
            (-15, 15),   # abajo-izquierda
        ]
        offset = positions_offset[state_num % 4]
        
        # Mostrar el texto del estado en tamaño más pequeño
        canvas.create_text(current_x + offset[0], current_y + offset[1], text=state_text, fill="red", font=("Arial", 8, "bold"), anchor="center")
    
    if cmd.startswith('A'):
        dist = int(cmd[1:])
        rad = math.radians(current_angle)
        dx = dist * 0.1 * math.sin(rad)
        dy = -dist * 0.1 * math.cos(rad)
        nx = current_x + dx
        ny = current_y + dy
        canvas.create_line(current_x, current_y, nx, ny, fill="black", width=2)
        current_x, current_y = nx, ny
    elif cmd.startswith('G'):
        degrees = int(cmd[1:])
        current_angle = (current_angle + degrees) % 360
    elif cmd.startswith('T'):
        size = int(cmd[1:])
        radius = size * 2
        canvas.create_oval(current_x - radius, current_y - radius, current_x + radius, current_y + radius, outline="black", width=2)
    elif cmd == 'F':
        # Mover a la siguiente posición en el grid (4 cuadrantes)
        if figure_count < len(positions) - 1:
            figure_count += 1
            current_x, current_y = positions[figure_count]
            current_angle = 0
        else:
            messagebox.showwarning("Aviso", "No hay más cuadrantes disponibles.")
    elif cmd == 'RESET':
        canvas.delete("all")
        figure_count = 0
        current_x, current_y, current_angle = positions[0]
        # Redibujar las líneas divisoras
        canvas.create_line(250, 0, 250, 500, fill="lightgray", width=1, dash=(4, 4))
        canvas.create_line(0, 250, 500, 250, fill="lightgray", width=1, dash=(4, 4))
        canvas.create_text(125, 15, text="I", fill="lightgray", font=("Arial", 10, "bold"))
        canvas.create_text(375, 15, text="II", fill="lightgray", font=("Arial", 10, "bold"))
        canvas.create_text(125, 485, text="III", fill="lightgray", font=("Arial", 10, "bold"))
        canvas.create_text(375, 485, text="IV", fill="lightgray", font=("Arial", 10, "bold"))
def load_gif_frames():
    """Cargar los frames del GIF"""
    global gif_frames
    gif_path = "icons8-python.gif"
    if os.path.exists(gif_path):
        try:
            gif = Image.open(gif_path)
            gif_frames = []
            for frame_idx in range(gif.n_frames):
                gif.seek(frame_idx)
                frame = gif.convert("RGBA")
                # Redimensionar el GIF a 50x50 con alta calidad
                frame = frame.resize((50, 50), Image.Resampling.BICUBIC)
                gif_frames.append(ImageTk.PhotoImage(frame))
        except Exception as e:
            print(f"Error cargando GIF: {e}")

def animate_gif():
    """Animar el GIF en el canvas"""
    global gif_animation_id, current_gif_frame, gif_label
    
    if not gif_frames or gif_label is None:
        return
    
    # Mostrar frame actual
    gif_label.config(image=gif_frames[current_gif_frame])
    gif_label.image = gif_frames[current_gif_frame]
    
    # Siguiente frame
    current_gif_frame = (current_gif_frame + 1) % len(gif_frames)
    
    # Programar siguiente animación (50ms por frame - más rápido)
    gif_animation_id = root.after(50, animate_gif)

def show_loading_gif():
    """Mostrar el GIF de carga en el centro del canvas"""
    global gif_label, current_gif_frame
    
    if not gif_frames:
        return
    
    current_gif_frame = 0
    gif_label = tk.Label(root, bg="white")
    gif_label.place(x=225, y=270, width=50, height=50)
    animate_gif()

def hide_loading_gif():
    """Ocultar el GIF de carga"""
    global gif_animation_id, gif_label
    
    if gif_animation_id:
        root.after_cancel(gif_animation_id)
        gif_animation_id = None
    
    if gif_label:
        gif_label.place_forget()
        gif_label = None
def show_transition_table():
    """Mostrar la tabla de transición del autómata (solo transiciones A)"""
    # Crear ventana para la tabla
    table_window = tk.Toplevel(root)
    table_window.title("Tabla de Transición - Movimientos")
    table_window.geometry("500x250")
    
    # Crear marco para la tabla
    frame = ttk.Frame(table_window)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Crear Treeview
    columns = ['Estado', 'Símbolo', 'Estado_Siguiente']
    tree = ttk.Treeview(frame, columns=columns, height=15)
    
    # Definir encabezados
    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('Estado', anchor=tk.CENTER, width=120)
    tree.column('Símbolo', anchor=tk.CENTER, width=150)
    tree.column('Estado_Siguiente', anchor=tk.CENTER, width=130)
    
    tree.heading('#0', text='', anchor=tk.CENTER)
    tree.heading('Estado', text='Estado', anchor=tk.CENTER)
    tree.heading('Símbolo', text='Símbolo (A)', anchor=tk.CENTER)
    tree.heading('Estado_Siguiente', text='→ Siguiente', anchor=tk.CENTER)
    
    # Filtrar solo transiciones con símbolos A (avanzar)
    transitions_dict = dfa.transitions
    transition_list = sorted(
        [key for key in transitions_dict.keys() if str(key[1]).startswith('A')],
        key=lambda x: (int(str(x[0])[1:]), int(str(x[1])[1:]))
    )
    
    # Insertar transiciones filtradas
    for idx, (state, symbol) in enumerate(transition_list):
        next_state = transitions_dict[(state, symbol)]
        tree.insert('', tk.END, values=(state, symbol, next_state))
    
    # Agregar scrollbar
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Información adicional
    info_frame = ttk.Frame(table_window)
    info_frame.pack(fill=tk.X, padx=10, pady=5)
    
    info_text = f"Transiciones de Movimiento (A) | Inicial: {dfa.start_state} | Final: {dfa.current_state}"
    info_label = ttk.Label(info_frame, text=info_text, foreground="blue", font=("Arial", 9))
    info_label.pack()

def draw_commands_step_by_step(canvas, commands, index=0, states_list=None):
    if index == 0:
        # Mostrar GIF al comenzar
        show_loading_gif()
    
    if index >= len(commands):
        # Ocultar GIF al terminar
        hide_loading_gif()
        entry.delete(0, tk.END)  # Limpiar caja después de todos
        # Mostrar tabla de transición después de 500ms
        root.after(500, show_transition_table)
        return
    cmd = commands[index]
    # Usar q1, q2, q3... para los comandos (index+1)
    state_text = states_list[index] if states_list and index < len(states_list) else None
    draw_command(canvas, cmd, state_text)
    # Dibujar siguiente después de 1000ms
    root.after(700, draw_commands_step_by_step, canvas, commands, index + 1, states_list)

def process_input(event=None):
    global current_x, current_y, current_angle
    input_text = entry.get().strip()
    if not input_text:
        return
    tokens = dfa.tokenize(input_text)
    
    # Validar que se hayan encontrado tokens
    if not tokens:
        messagebox.showerror("Error", "Esto no pertenece al autómata.")
        return
    
    # Validar que todos los tokens sean válidos
    invalid_tokens = [token for token in tokens if token not in dfa.alphabet]
    if invalid_tokens:
        messagebox.showerror("Error", "Esto no pertenece al autómata.")
        return
    
    # Validar que la secuencia sea aceptada por el autómata
    if not dfa.accepts(input_text):
        messagebox.showerror("Error", "Esto no pertenece al autómata.")
        return
    
    # Filtrar solo comandos de navegación (F, RESET)
    drawing_tokens = [token for token in tokens if token not in ['F', 'RESET']]
    
    # Si solo hay comandos de navegación, ejecutarlos sin dibujar
    if not drawing_tokens:
        for token in tokens:
            draw_command(canvas, token)
        entry.delete(0, tk.END)
        return
    
    # Mostrar q0 como punto inicial (pequeño círculo rojo)
    canvas.create_oval(current_x - 3, current_y - 3, current_x + 3, current_y + 3, fill="red", outline="red")
    canvas.create_text(current_x - 15, current_y - 15, text="q0", fill="red", font=("Arial", 8, "bold"), anchor="center")
    
    # Usar estados reales del recorrido secuencial del DFA (solo comandos de dibujo)
    states_list = [
        next_state for (_, symbol, next_state) in dfa.last_transitions
        if symbol not in ['F', 'RESET']
    ]
    
    # Luego de 500ms, comenzar a dibujar los comandos
    root.after(500, draw_commands_step_by_step, canvas, drawing_tokens, 0, states_list)

root = tk.Tk()
root.title("Dibujador de Figuras con Autómata")

entry = tk.Entry(root, width=50)
entry.pack(pady=10)
entry.bind("<Return>", process_input)
entry.focus()  # Foco en la caja

canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack()

# Dibujar líneas divisoras del plano cartesiano (4 cuadrantes)
canvas.create_line(250, 0, 250, 500, fill="lightgray", width=1, dash=(4, 4))  # Línea vertical
canvas.create_line(0, 250, 500, 250, fill="lightgray", width=1, dash=(4, 4))  # Línea horizontal

# Etiquetar los cuadrantes
canvas.create_text(125, 15, text="I", fill="lightgray", font=("Arial", 10, "bold"))
canvas.create_text(375, 15, text="II", fill="lightgray", font=("Arial", 10, "bold"))
canvas.create_text(125, 485, text="III", fill="lightgray", font=("Arial", 10, "bold"))
canvas.create_text(375, 485, text="IV", fill="lightgray", font=("Arial", 10, "bold"))

# Cargar frames del GIF
load_gif_frames()

root.mainloop()