class EpsilonNFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  # {state: {symbol: set(states)}}
        self.start_state = start_state
        self.accept_states = accept_states

    # Additional methods will be added here


class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  # {state: {symbol: set(states)}}
        self.start_state = start_state
        self.accept_states = accept_states

    # Additional methods will be added here


class DFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function  # {state: {symbol: state}}
        self.start_state = start_state
        self.accept_states = accept_states

    # Additional methods will be added here
