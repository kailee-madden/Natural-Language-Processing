#!/usr/bin/python3
import fst
from fst import make_ngram

Lm = make_ngram(open("train.new"), 2)

def main():
    Lm.visualize()

if __name__ == "__main__":
    main()
