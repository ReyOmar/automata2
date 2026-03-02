import re

# ------------------------------------------------------------
# DFA para lenguaje de dibujo:
# - A<number> = avanzar
# - G<number> = girar
# - F         = cambiar de cuadrante (no cambia estado DFA)
#
# Este autómata registra estados/transiciones de cada cadena para
# que la interfaz pueda mostrar el recorrido (q0, q1, q2, ...).
# ------------------------------------------------------------
class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        # --------------------------------------------------------
        # Componentes formales del autómata.
        # --------------------------------------------------------
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

        # --------------------------------------------------------
        # Estado de ejecución de la última cadena procesada.
        # --------------------------------------------------------
        self.current_state = start_state
        self.current_index = 0
        self.total_line_commands = 0
        self.last_tokens = []
        self.last_states = [start_state]
        self.last_transitions = []

    def reset(self):
        # --------------------------------------------------------
        # Reinicia el contexto de evaluación para procesar una nueva
        # cadena desde el estado inicial.
        # --------------------------------------------------------
        self.current_state = self.start_state
        self.current_index = 0
        self.total_line_commands = 0
        self.last_states = [self.start_state]
        self.last_transitions = []

    def process_symbol(self, symbol):
        # --------------------------------------------------------
        # Procesa un símbolo individual y guarda la transición.
        # Reglas principales:
        # - Si es A#, avanza al siguiente estado dinámico.
        # - El último A# vuelve a q0 para "cerrar" la secuencia.
        # - Si es G# o F, conserva el estado actual.
        # --------------------------------------------------------
        if symbol not in self.alphabet:
            return False

        origin = self.current_state

        if symbol.startswith('A'):
            # Cada comando A (avanzar) genera progreso de estado q0 -> q1 -> q2...
            self.current_index += 1

            if self.total_line_commands > 0 and self.current_index == self.total_line_commands:
                # El último avance regresa al estado inicial para cerrar el recorrido.
                destination = self.start_state
            else:
                destination = f'q{self.current_index}'
                if destination not in self.states:
                    # Se agregan estados dinámicamente según la longitud del recorrido.
                    self.states.append(destination)

            self.current_state = destination
        else:
            # Comandos de giro y cambio de cuadrante no cambian de estado.
            destination = self.current_state

        # Se guarda la transición para visualización posterior.
        self.transitions[(origin, symbol)] = destination
        self.last_transitions.append((origin, symbol, destination))
        self.last_states.append(destination)
        return True

    def is_accepting(self):
        # Devuelve True si el estado actual está en los de aceptación.
        return self.current_state in self.accept_states

    def accepts(self, string):
        # --------------------------------------------------------
        # Valida cadena completa:
        # 1) Tokeniza la entrada.
        # 2) Verifica que no exista texto inválido fuera de tokens.
        # 3) Procesa cada token en orden.
        # 4) Actualiza estado final como estado de aceptación.
        # --------------------------------------------------------
        self.reset()
        tokens = self.tokenize(string)

        # Verifica que toda la entrada se haya tokenizado correctamente (sin ruido).
        compact_input = re.sub(r'\s+', '', string.upper())
        if ''.join(tokens) != compact_input:
            return False

        self.last_tokens = tokens
        # Cantidad de comandos de línea (A) usados para detectar el último avance.
        self.total_line_commands = sum(1 for token in tokens if token.startswith('A'))

        for token in tokens:
            if token not in self.alphabet:
                return False
            if not self.process_symbol(token):
                return False

        # El estado de aceptación final coincide con el estado alcanzado.
        self.accept_states = [self.current_state]
        return self.is_accepting()

    def tokenize(self, string):
        # Extrae tokens válidos (A#, G# y F) ignorando mayúsc/minúsc.
        string = string.upper()
        pattern = r'(A\d+|G\d+|F)'
        return re.findall(pattern, string)


# ALFABETO O LENGUAJE (símbolos permitidos)
alphabet = ['A' + str(i) for i in range(1, 1001)] + ['G90', 'G120', 'G180', 'G40'] + ['F']

states = ['q0']

# ESTADO INICIAL
start_state = 'q0'

accept_states = ['q0']

transitions = {}

# ------------------------------------------------------------
# Instancia global usada por la interfaz gráfica.
# ------------------------------------------------------------
dfa = DFA(states, alphabet, transitions, start_state, accept_states)