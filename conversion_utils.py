from models import EpsilonNFA, NFA, DFA


def epsilon_closure(state, transitions):
    """
    Compute the epsilon closure for a given state.
    """
    closure = {state}
    stack = [state]

    while stack:
        current = stack.pop()
        for next_state in transitions.get(current, {}).get('', []):
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)

    return closure

def convert_epsilon_nfa_to_nfa(epsilon_nfa):
    """
    Convert ε-NFA to NFA.
    """
    nfa_transitions = {}
    for state in epsilon_nfa.states:
        closure = epsilon_closure(state, epsilon_nfa.transitions)
        nfa_transitions[state] = {}

        for symbol in epsilon_nfa.alphabet:
            if symbol == '':
                continue
            destinations = set()
            for closure_state in closure:
                for next_state in epsilon_nfa.transitions.get(closure_state, {}).get(symbol, []):
                    destinations.update(epsilon_closure(next_state, epsilon_nfa.transitions))
            nfa_transitions[state][symbol] = destinations

    nfa_states = epsilon_nfa.states
    nfa_start_state = epsilon_closure(epsilon_nfa.start_state, epsilon_nfa.transitions)
    nfa_accept_states = set()
    for accept_state in epsilon_nfa.accept_states:
        for state in epsilon_nfa.states:
            if accept_state in epsilon_closure(state, epsilon_nfa.transitions):
                nfa_accept_states.add(state)

    return NFA(nfa_states, epsilon_nfa.alphabet, nfa_transitions, nfa_start_state, nfa_accept_states)


def convert_nfa_to_dfa(nfa):
    """
    Convert NFA to DFA using the subset construction algorithm.
    """
    initial_state = frozenset(epsilon_closure(nfa.start_state, nfa.transitions))
    dfa_states = set([initial_state])
    unmarked_states = [initial_state]
    dfa_transitions = {}
    dfa_accept_states = set()

    while unmarked_states:
        current = unmarked_states.pop()
        dfa_transitions[current] = {}

        for symbol in nfa.alphabet:
            if symbol == '':
                continue
            next_state = frozenset.union(*[nfa.transitions[state].get(symbol, set()) for state in current])
            dfa_transitions[current][symbol] = next_state

            if next_state not in dfa_states:
                dfa_states.add(next_state)
                unmarked_states.append(next_state)

    # Determining accept states for the DFA
    for state in dfa_states:
        if nfa.accept_states.intersection(state):
            dfa_accept_states.add(state)

    return DFA(dfa_states, nfa.alphabet, dfa_transitions, initial_state, dfa_accept_states)


def minimize_dfa(dfa):
    """
    Minimize a DFA using the partition refinement method.
    """
    # Initialize partitions: Accept states and non-accept states
    P = {frozenset(dfa.accept_states), frozenset(dfa.states - dfa.accept_states)}

    # Function to find the set in P that contains state
    def find_set(state, partition):
        for subset in partition:
            if state in subset:
                return subset
        return None

    # Refining partitions
    while True:
        newP = set()
        for Y in P:
            splits = {}
            for state in Y:
                key = tuple(find_set(dfa.transition_function[state].get(symbol), P) for symbol in dfa.alphabet)
                if key in splits:
                    splits[key].add(state)
                else:
                    splits[key] = {state}
            newP.update(frozenset(s) for s in splits.values())

        if newP == P:
            break
        P = newP

    # Building the minimized DFA
    new_states = {frozenset(subset): i for i, subset in enumerate(P)}
    new_transitions = {}
    for subset, new_state in new_states.items():
        representative = next(iter(subset))
        new_transitions[new_state] = {symbol: new_states[frozenset(find_set(dfa.transition_function[representative][symbol], P))] for symbol in dfa.alphabet}

    new_start_state = new_states[frozenset(find_set(dfa.start_state, P))]
    new_accept_states = {new_states[frozenset(subset)] for subset in P if subset & dfa.accept_states}

    return DFA(new_states.values(), dfa.alphabet, new_transitions, new_start_state, new_accept_states)

