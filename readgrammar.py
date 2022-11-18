import sys
import re

# List of syntax to token
token_exp = [

]

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

# Converting characters in a program into a sequence of lexical tokens
def lexer(text, token_exp):
    abs_pos = 0     # Absolute position in text
    rel_pos = 1     # Position in relative to line
    line_num = 1    # Current line number

    tokens = []

    while abs_pos < len(text):
        if text[abs_pos] == '\n':   # Reading new Line
            rel_pos = 1     # Reset relative position to 1
            line_num += 1   # Update current line number

        flag = None         # Reset flag value

        for expression in token_exp:    # Iterating through sets of patterns and tags in list of token expression
            pattern, tag = expression
            regex = re.compile(pattern)
            flag = regex.match(text, abs_pos)

            if flag:
                if tag:
                    token = tag
                    tokens.append(token)
                break

        if not flag:
            # belum yakin ini bener ga... kl di punya ka gede dkk ini buat illegal character
            print(f"\nSyntax Error\n\nTerjadi kesalahan ekspresi pada line {line_num}: {text[abs_pos]}")
            sys.exit(1)     # Exiting program if illegal character found
        else:
            abs_pos = flag.end(0)
        rel_pos += 1
    
    return tokens

def tokenization(text):
    file = open(text)
    char = file.read()
    file.close()

    tokens = lexer(char,token_exp)
    tokenResult = []

    for token in tokens:
        tokenResult.append(token)

    return " ".join(tokenResult)