from models import EpsilonNFA, NFA, DFA
from conversion_utils import convert_epsilon_nfa_to_nfa, convert_nfa_to_dfa, minimize_dfa

def main():
    # Define an ε-NFA
    states = {'q0', 'q1', 'q2', 'q3'}
    alphabet = {'a', 'b'}
    transitions = {
        'q0': {'': {'q1', 'q2'}},
        'q1': {'a': {'q1'}, 'b': {'q1', 'q3'}},
        'q2': {'b': {'q3'}},
        'q3': {}
    }
    start_state = 'q0'
    accept_states = {'q3'}

    epsilon_nfa = EpsilonNFA(states, alphabet, transitions, start_state, accept_states)

    # Convert ε-NFA to NFA
    nfa = convert_epsilon_nfa_to_nfa(epsilon_nfa)

    # Convert NFA to DFA
    dfa = convert_nfa_to_dfa(nfa)

    # Minimize DFA
    minimized_dfa = minimize_dfa(dfa)

    # Output the results
    print("Minimized DFA:")
    print("States:", minimized_dfa.states)
    print("Alphabet:", minimized_dfa.alphabet)
    print("Start State:", minimized_dfa.start_state)
    print("Accept States:", minimized_dfa.accept_states)
    print("Transition Function:", minimized_dfa.transition_function)

if __name__ == "__main__":
    main()
