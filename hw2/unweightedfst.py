#!/usr/bin/python3
import string
import fst
from fst import FST
from fst import Transition
import unweightedM_w
from unweightedM_w import M_w
import callandvisualize
from callandvisualize import Lm
import cer
from cer import cer
import math

FST = FST()

def main():
    with open("train.new") as new, open("train.old") as old:
            content_new = new.read().splitlines()
            content_old = old.read().splitlines()
    new_alpha = set()
    old_alpha = set()
    for line_new, line_old in zip(content_new, content_old):
        for word_new, word_old in zip(line_new.strip(), line_old.strip()):
            for character_new, character_old in zip(list(word_new), list(word_old)):
                new_alpha.add(character_new)
                old_alpha.add(character_old)

    with open("test.old") as test_old, open("test.new") as test_new:
            shakespeare = test_old.read().splitlines()
            modern = test_new.read().splitlines()
    oldlines = set()
    newlines = set()
    for line_old, line_new in zip(shakespeare, modern):
        oldlines.add(line_old)
        newlines.add(line_new)

    unweightedT_m(new_alpha, old_alpha)
    #FST.visualize()

    COMP1 = fst.compose(Lm, FST)

    compared_strings = []
    for old_line, new_line in zip(oldlines, newlines):
        transducer = compose(COMP1, old_line)
        best_string = viterbi(transducer)
        compared_strings.append((new_line, best_string))
    print(cer(compared_strings))


def unweightedT_m(alpha_new, alpha_old):
    for new_char, old_char in zip(alpha_new, alpha_old):
        for old_char1 in alpha_old:
            FST.add_transition(Transition(1,(new_char, old_char1), 0))
            FST.add_transition(Transition(0,(new_char, old_char1), 0))
        FST.add_transition(Transition(0, ("ε", old_char), 0))
        FST.add_transition(Transition(0, (new_char, "ε"), 1))
    FST.add_transition(Transition(0, ("</s>", "</s>"), 2))
    FST.add_transition(Transition(1, ("</s>", "</s>"), 2))
    FST.set_start(0)
    FST.set_accept(2)
    return

def initialize_probabilities(alpha_new, alpha_old):
    for new_char in alpha_new:
        for old_char in alpha_old:
            if new_char == old_char:
                FST.reweight_transition(Transition(1, (new_char, old_char), 0), wt=100)
                FST.reweight_transition(Transition(0, (new_char, old_char), 0), wt=100)
    FST.normalize_cond()
    return

def compose(composed, line):
    w = M_w(line)
    return fst.compose(composed,w)


def sort(graph, final_state):
    ordered_all = []
    i = 0
    #print(final_state)
    while i <= final_state[1]:
        ordered = []
        for state in graph:
            #print(state)
            if state[1] == i:
                ordered.append(state)
        #print(ordered)
        if len(ordered) > 1:
            j = 0
            while j <= final_state[0][1]:
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
    best_weights[transducer.start] = 1
    for state in sorted_states:
        if state != transducer.start:
            best_weights[state] = "fakenewz"
        for incoming_transition, weight in transducer.transitions_to[state].items():
            if best_weights[incoming_transition.q] != "fakenewz":
                if best_weights[state] != "fakenewz":
                    if best_weights[incoming_transition.q] + math.log(weight) > best_weights[state]:
                        best_weights[state] = best_weights[incoming_transition.q] + math.log(weight)
                        best_transitions[state] = incoming_transition
                else:
                    best_weights[state] = best_weights[incoming_transition.q] + math.log(weight)
                    best_transitions[state] = incoming_transition
    
   # print(transducer.accept)
    transition_list = []
    cur_state = transducer.accept
    #print(cur_state)
    #print(sorted_states[0])
    #print(best_transitions)
    while cur_state != transducer.start:
        transition = best_transitions[cur_state]
        #print(transition)
        #print(transition.a)
        #print(transition.r)
        transition_list.append(transition.a)
        cur_state = transition.q
    character_changes = []
    for i in reversed(transition_list):
        characters = i[0][1]
        char = characters[0] 
        if char != "ε" and char != "</s>":
            character_changes.append(char)
    predicted_lines = ''.join(character_changes)
    return predicted_lines

    #not sure if I should be accessing 1 or 0 for char

  

if __name__ == "__main__":
    main()


