import sys
import re

# List of syntax to token
token_exp = [
    (r'[ \t]+',                 None),
    (r'#[^\n]*',                None),
    (r'[\n]+[ \t]*\'\'\'[(?!(\'\'\'))\w\W]*\'\'\'',  None),
    (r'[\n]+[ \t]*\"\"\"[(?!(\"\"\"))\w\W]*\"\"\"',  None),

    # Integer and String
    (r'\"[^\"\n]*\"',           "STRING"),
    (r'\'[^\'\n]*\'',           "STRING"),
    (r'[\+\-]?[0-9]*\.[0-9]+',  "INT"),
    (r'[\+\-]?[1-9][0-9]+',     "INT"),
    (r'[\+\-]?[0-9]',           "INT"),

    # Delimiter
    (r'\n',                     "NEWLINE"),
    (r'\(',                     "KBKI"), 
    (r'\)',                     "KBKA"),
    (r'\[',                     "KSKI"), 
    (r'\]',                     "KSKA"),
    (r'\{',                     "KKKI"), 
    (r'\}',                     "KKKA"),
    (r'\;',                     "TITIKKOMA"), 
    (r'\:',                     "TITIKDUA"),

    # Operator
    (r'\+',                     "ADD"),
    (r'\-',                     "SUB"),
    (r'\*',                     "MUL"),
    (r'\*\*',                   "POW"),
    (r'/',                      "DIV"),
    (r'%',                      "MOD"),
    (r'\++',                    "INCR"),
    (r'\--',                    "DECR"),
    (r'\=',                     "AS"),
    (r'\+=',                    "SUMAS"),
    (r'-=',                     "SUBAS"),
    (r'\*=',                    "MULAS"),
    (r'/=',                     "DIVAS"),
    (r'%=',                     "MODAS"),
    (r'\*\*=',                  "POWAS"),
    # (r'\->',                    "ARROW"),
    (r'\==',                    "EQ"),
    (r'\===',                   "EQTYPE"),
    (r'!=',                     "NEQ"),
    (r'!==',                    "NEQTYPE"),
    (r'>',                      "G"),
    (r'<',                      "L"),
    (r'>=',                     "GEQ"),
    (r'<=',                     "LEQ"),
    (r'?',                      "TERNARY"),
    (r'\&&',                    "LAND"),
    (r'\||',                    "LOR"),
    (r'\!',                     "LNOT"),
    (r'&',                      "AND"),
    

    # Keyword
    (r'\bformat\b',             "FORMAT"),
    (r'\bif\b',                 "IF"),
    (r'\bthen\b',               "THEN"),
    (r'\belse\b',               "ELSE"),
    (r'\belif\b',               "ELIF"),
    (r'\bfor\b',                "FOR"),
    (r'\bwhile\b',              "WHILE"),
    (r'\brange\b',              "RANGE"),
    (r'\bbreak\b',              "BREAK"),
    (r'\bcontinue\b',           "CONTINUE"),
    (r'\bpass\b',               "PASS"),
    (r'\bFalse\b',              "FALSE"),
    (r'\bTrue\b',               "TRUE"),
    (r'\bNone\b',               "NONE"),
    (r'\bin\b',                 "IN"),
    (r'\bis\b',                 "IS"),
    (r'\bclass\b',              "CLASS"),
    (r'\bdef\b',                "DEF"),
    (r'\breturn\b',             "RETURN"),
    (r'\bfrom\b',               "FROM"),
    (r'\bimport\b',             "IMPORT"),
    (r'\braise\b',              "RAISE"),
    (r'\bwith\b',               "WITH"),
    (r'\bas\b',                 "AS"),
    (r'\bdict\b',               "TYPE"),
    (r'\bint\b',                "TYPE"),
    (r'\bstr\b',                "TYPE"),
    (r'\bfloat\b',              "TYPE"),
    (r'\bcomplex\b',            "TYPE"),
    (r'\blist\b',               "TYPE"),
    (r'\btuple\b',              "TYPE"),
    (r'\bset\b',                "TYPE"),
    (r'\,',                     "COMMA"),
    (r'\w+[.]\w+',              "KARTITIK"),
    (r'\.',                     "TITIK"),
    (r'\'\'\'[(?!(\'\'\'))\w\W]*\'\'\'',       "MULTILINE"),
    (r'\"\"\"[(?!(\"\"\"))\w\W]*\"\"\"',       "MULTILINE"),
    (r'[A-Za-z_][A-Za-z0-9_]*', "ID"),
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