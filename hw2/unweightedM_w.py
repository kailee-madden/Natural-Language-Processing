#!/usr/bin/python3
import string
import fst
from fst import FST
from fst import Transition

def main():
    w = M_w("this is a test")
    w.visualize()

def M_w(input_string):
    fst = FST()
    i = 0
    fst.set_start(0)
    for word in input_string.split():
        fst.add_transition(Transition(i, (word, word), i+1))
        i+=1
    fst.set_accept(i)
    return fst

if __name__ == "__main__":
    main()