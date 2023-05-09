"""
This file is autogenerated
"""

from src.afn import Thompson
import argparse

# Inputs
parser = argparse.ArgumentParser(description='Generated lexical analyzer')
parser.add_argument('filename', type=open, help='File to read and tokenize')
args = parser.parse_args()
print(args)

# Internal variables
postfixs = {'WHITESPACE': ' \t|\n|+', 'ID': 'AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|01|2|3|4|5|6|7|8|9||*д', 'NUMBER': "01|2|3|4|5|6|7|8|9|+.01|2|3|4|5|6|7|8|9|+д?дE'+''-'|?01|2|3|4|5|6|7|8|9|+д?д", 'PLUS': "'+'", 'MINUS': "'-'", 'TIMES': "'*'", 'DIV': "'/'", 'LPAREN': "'('", 'RPAREN': "')'"}
alphabets = {'WHITESPACE': ['\t', '\n', ' '], 'ID': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'], 'NUMBER': ['+', '-', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'E'], 'PLUS': ['+'], 'MINUS': ['-'], 'TIMES': ['*'], 'DIV': ['/'], 'LPAREN': ['('], 'RPAREN': [')']}

# Create AFNs
anfs = {}
for token in postfixs.keys():
    thompson = Thompson(postfixs[token], alphabets[token])
    thompson.construct()
    anfs[token] = thompson


def tokenize(queue):
    word = []
    _token = list(anfs.keys())[0]
    while len(queue) > 0:
        match = False
        word.append(queue.pop(0))
        string = ''.join(word)
        for token, afn in anfs.items():
            if afn.simulate(string) == "Si":
                _token = token
                match = True
        if (not match) or len(queue) == 0:
            if len(word) == 1:
                print("UNDEFINED SYMBOL ", word.pop())
                break
            if len(queue) != 0:
                queue.insert(0, word.pop())
            string = ''.join(word)
            word = []
            print(f"<{string}, {_token}>")
            # token = _token


# Read file
with open(args.filename.name) as file:
    for line in file:
        queue = list(line)
        tokenize(queue)
