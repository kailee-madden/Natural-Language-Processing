for character in string.printable:
    for character2 in string.printable:
        sub = (character, character2)
        s = Transition(1, sub, 0)
        s2 = Transition(0, sub, 0)
        fst.add_transition(s)
        fst.add_transition(s2)
    ins = ("ε", character)
    i = Transition(0, ins, 0)
    fst.add_transition(i)
    delete = (character, "ε")
    d = Transition(0, delete, 1)
    fst.add_transition(d)
fst.add_transition(Transition(0, ("</s>", "</s>"), 2))
fst.add_transition(Transition(1, ("</s>", "</s>"), 2))
fst.set_start(0)
fst.set_accept(2)


def unweightedT_m(new, old):
    fst = FST()
    with open(new) as f:
        content_new = f.read().splitlines()
    with open(old) as f:
        content_old = f.read().splitlines()
    content = content_new + content_old
    options = set()
    for line in content:
        for word in line.strip():
            for character in list(word):
                options.add(character)
    for character in options:
        for character2 in options:
            fst.add_transition(Transition(1, (character, character2), 0))
            fst.add_transition(Transition(0, (character, character2), 0))
        fst.add_transition(Transition(0, ("ε", character), 0))
        fst.add_transition(Transition(0, (character, "ε"), 1))
    fst.add_transition(Transition(0, ("</s>", "</s>"), 2))
    fst.add_transition(Transition(1, ("</s>", "</s>"), 2))
    fst.set_start(0)
    fst.set_accept(2)
    return fst


def unweightedT_m(new, old):
    fst = FST()
    with open(new) as new, open(old) as old:
        content_new = new.read().splitlines()
        content_old = old.read().splitlines()
    options = set()
    for line_new, line_old in zip(content_new, content_old):
        for word_new, word_old in line.strip():
            for character in list(word):
                options.add(character)
    for character in options:
        for character2 in options:
            fst.add_transition(Transition(1, (character, character2), 0))
            fst.add_transition(Transition(0, (character, character2), 0))
        fst.add_transition(Transition(0, ("ε", character), 0))
        fst.add_transition(Transition(0, (character, "ε"), 1))
    fst.add_transition(Transition(0, ("</s>", "</s>"), 2))
    fst.add_transition(Transition(1, ("</s>", "</s>"), 2))
    fst.set_start(0)
    fst.set_accept(2)
    return fst


def topological_sort(graph, key, path):
    path.append(key)
    for item in graph:
        if key == item[0][0][0][0]:
            key = item[1]
    if key not in path:
        topological_sort(graph, key, path)
    return path

def viterbi(transducer):
    best_weights = {}
    best_transitions = {}
    sorted_states = topological_sort(transducer.states, transducer.start, [])
    for state in sorted_states:
        #print(transducer.transitions_to)
        for incoming_transition in transducer.transitions_to:
            #print(transducer.transitions_to[incoming_transition])
            #print(incoming_transition)
            #self.transitions_to[t.r][t] = wt
            #print(transducer.transitions_to[incoming_transition[1]])
            #print(incoming_transition[1])
            #print(transducer.transitions_to[incoming_transition[1]][incoming_transition])
            if state not in best_weights:
                best_weights[state] = transducer.transitions_to[incoming_transition][1]
                best_transitions[state] = incoming_transition
            elif transducer.transitions_to[incoming_transition][1] > best_weights[state]:
                best_weights[state] = transducer.transitions_to[incoming_transition][1]
                best_transitions[state] = incoming_transition
            else:
                continue
    transition_list = []
    cur_state = sorted_states[len(sorted_states)-1]
    while cur_state != sorted_states[0]:
        transition = best_transitions[cur_state]
        transition_list.append(transition)
        cur_state = transition[1]
    character_changes = []
    for i in reversed(transition_list):
        characters = i[0][1]
        char = characters[0] 
        character_changes.append(char)
    predicted_lines = ''.join(character_changes)
    return predicted_lines

    #not sure if I should be accessing 1 or 0 for char


def topological_sort_util(graph, v, visited, stack):
    visited[v] = True
    #print(graph[v][0][0][0])
    for i in graph[v]:
        j = i[0][0][0]
        print(j)
        if visited[j] == False:
            topological_sort_util(graph, j, visited, stack)
    return stack.insert(0,v)

def topological_sort(graph, vertices):
    visited = [False]*vertices
    stack = []
    for i in range(vertices):
        #print(i)
        if visited[i] == False:
            topological_sort_util(graph, i, visited, stack)
    #print(stack)
    return stack






    def sort(graph, final_state):
    ordered_all = []
    i = 0
    while i < final_state[1]:
        ordered = []
        for state in graph:
            if state[1] == i:
                ordered.append(state)
        if len(ordered) > 1:
            j = 0
            for item in ordered:
                if j == item[0][1]:
                    ordered_all.append(item)
                j += 1
        else:
            ordered_all.append(state)
        i += 1

            
    #print(ordered_all)   
    return ordered_all
    
    
def viterbi(transducer):
    best_weights = {}
    best_transitions = {}
    sorted_states = sort(list(transducer.states), transducer.accept)
    for state in sorted_states:
        #print(state)
        for incoming_transition, weight in transducer.transitions_to[state].items(): 
            #print(incoming_transition.r)
            #print(weight)
            if state not in best_weights:
                best_weights[state] = weight
                best_transitions[state] = incoming_transition
            elif weight > best_weights[state]:
                best_weights[state] = weight
                best_transitions[state] = incoming_transition
            else:
                continue
    transition_list = []
    cur_state = #the accept state
    #print(cur_state)
    #print(sorted_states[0])
    while cur_state != #the start state:
        transition = best_transitions[cur_state]
        print(transition)
        print(transition.a)
        print(transition.r)
        transition_list.append(transition.a)
        cur_state = #the next state
        #figure out how to work backwards with the pointers
    character_changes = []
    for i in reversed(transition_list):
        characters = i[0][1]
        char = characters[0] 
        character_changes.append(char)
    predicted_lines = ''.join(character_changes)
    return predicted_lines

    #not sure if I should be accessing 1 or 0 for char