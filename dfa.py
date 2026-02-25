import re

class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

        self.current_state = start_state
        self.current_index = 0
        self.last_tokens = []
        self.last_states = [start_state]
        self.last_transitions = []

    def reset(self):
        self.current_state = self.start_state
        self.current_index = 0
        self.last_states = [self.start_state]
        self.last_transitions = []
        self.transitions = {}

    def process_symbol(self, symbol):
        if symbol not in self.alphabet:
            return False

        origin = f'q{self.current_index}'
        self.current_index += 1
        destination = f'q{self.current_index}'

        self.current_state = destination
        if destination not in self.states:
            self.states.append(destination)

        self.transitions[(origin, symbol)] = destination
        self.last_transitions.append((origin, symbol, destination))
        self.last_states.append(destination)
        return True

    def is_accepting(self):
        return self.current_state in self.accept_states

    def accepts(self, string):
        self.reset()
        tokens = self.tokenize(string)

        compact_input = re.sub(r'\s+', '', string.upper())
        if ''.join(tokens) != compact_input:
            return False

        self.last_tokens = tokens

        for token in tokens:
            if token not in self.alphabet:
                return False
            if not self.process_symbol(token):
                return False

        self.accept_states = [self.current_state]
        return self.is_accepting()

    def tokenize(self, string):
        string = string.upper()
        pattern = r'(A\d+|G\d+|T\d+|F|RESET)'
        return re.findall(pattern, string)


# ESTADO INICIAL
start_state = 'q0'

# ESTE SERIA EL DE ESTADO
states = ['q0']

# ALFABETO O LENGIAJE (símbolos permitidos)
alphabet = ['A' + str(i) for i in range(1, 1001)] + ['G90', 'G120', 'G180', 'G40'] + ['T' + str(i) for i in range(1, 11)] + ['F', 'RESET']

# PARÁMETRO 3: TRANSICIONES (función de transición)
# Se generan dinámicamente durante la ejecución:
# q0 --s1--> q1 --s2--> q2 --s3--> ...
transitions = {}

# ESTADOS DE ACEPTACIÓN
# Se ajusta dinámicamente al estado final alcanzado en cada ejecución.
accept_states = ['q0']

dfa = DFA(states, alphabet, transitions, start_state, accept_states)