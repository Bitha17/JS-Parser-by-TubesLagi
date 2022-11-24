import sys
import re

# Read grammar from grammar.txt
def read_grammar(filename):
    # Initiate file reading
    file = open(filename, "r")
    CFG = {}

    # Initiate 'line' to the first line of file
    line = file.readline()

    # Loop until file ends
    while line != "":
        variable, production = line.replace("\n","").split(" -> ")

        if variable not in CFG.keys():
            CFG[variable] = [production.split(" ")]
        else:
            CFG[variable].append(production.split(" "))
        
        # Advance to the next line
        line = file.readline()

    # Close file after process
    file.close()

    # Return the CFG obtained from grammar.txt
    return CFG

# Differentiating Terminals and Variables (used in grammar conversion)
def isTerminal(string):
    list_of_terminal = [
        "INCR",
        "DECR",
        "DEFAULT",
        "DELETE",
        "LET",
        "NULL",
        "SWITCH",
        "THROW",
        "TRY",
        "FINALLY",
        "EQUAL",
        "ISEQ",
        "KBKI",
        "KBKA",
        "SEMICOLON",
        "COLON",
        "ADD",
        "SUBTR",
        "MUL",
        "DIV",
        "LE",
        "L",
        "GE",
        "G",
        "NEQ",
        "SUBTREQ",
        "MULEQ",
        "SUMEQ",
        "DIVEQ",
        "AND",
        "OR",
        "NOT",
        "IF",
        "THEN",
        "ELSE",
        "ELIF",
        "WHILE",
        "RANGE",
        "FALSE",
        "TRUE",
        "NONE",
        "BREAK",
        "CASE",
        "CATCH",
        "CLASS",
        "CONTINUE",
        "FUNCTION",
        "FOR",
        "FROM",
        "FORMAT",
        "IMPORT",
        "IN",
        "IS",
        "RETURN",
        "PASS",
        "WITH",
        "COMMA",
        "DOT",
        "DOTBETWEEN",
        "PETIKSATU",
        "PETIKDUA",
        "KSKI",
        "KSKA",
        "KKKI",
        "KKKA",
        "NUM",
        "STRING",
        "MULTILINE",
        "VARIABLE",
        "NEWLINE",
        "TYPE",
        "ARROW",
        "COMMENT",
    ]
    
    return string in list_of_terminal

def isVar(string):
    return not isTerminal(string)