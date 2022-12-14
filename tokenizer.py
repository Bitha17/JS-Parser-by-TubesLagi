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
    (r'[\+\-]?[0-9]*\.[0-9]+',  "NUM"),
    (r'[\+\-]?[1-9][0-9]+',     "NUM"),
    (r'[\+\-]?[0-9]',           "NUM"),

    # Delimiter
    (r'\n',                     "NEWLINE"),
    (r'\(',                     "KBKI"), 
    (r'\)',                     "KBKA"),
    (r'\[',                     "KSKI"), 
    (r'\]',                     "KSKA"),
    (r'\{',                     "KKKI"), 
    (r'\}',                     "KKKA"),
    (r'\;',                     "SEMICOLON"), 
    (r'\:',                     "COLON"),
    (r'//',                     "COMMENT"),

    # Operator
    (r'\+\+',                   "INCR"),
    (r'\--',                    "DECR"),
    (r'\==',                    "ISEQ"),
    (r'\=',                     "EQUAL"),
    (r'\+=',                    "SUMEQ"),
    (r'-=',                     "SUBTREQ"),
    (r'\*=',                    "MULEQ"),
    (r'/=',                     "DIVEQ"),
    (r'\*\*=',                  "POWEQ"),
    (r'%=',                     "MODEQ"),
    (r'\->',                    "ARROW"),
    (r'\+',                     "ADD"),
    (r'\-',                     "SUBTR"),
    (r'\*',                     "MUL"),
    (r'/',                      "DIV"),
    (r'\*\*',                   "POW"),
    (r'%',                      "MOD"),
    (r'!=',                     "NEQ"),
    (r'>',                      "G"),
    (r'<',                      "L"),
    (r'>=',                     "GE"),
    (r'<=',                     "LE"),
    (r'&&',                     "AND"),
    (r'\|\|',                   "OR"),
    (r'!',                      "NOT"),
    

    # Keyword
    (r'\bconst\b',              "TYPE"),
    (r'\bcase\b',               "CASE"),
    (r'\bcatch\b',              "CATCH"),
    (r'\bdefault\b',            "DEFAULT"),
    (r'\blet\b',                "TYPE"),
    (r'\bnull\b',               "NULL"),
    (r'\bdelete\b',             "DELETE"),
    (r'\bfinally\b',            "FINALLY"),
    (r'\bswitch\b',             "SWITCH"),
    (r'\bthrow\b',              "THROW"),
    (r'\btry\b',                "TRY"),
    (r'\bvar\b',                "TYPE"),
    (r'\belse if\b',            "ELIF"),
    (r'\bif\b',                 "IF"),
    (r'\bthen\b',               "THEN"),
    (r'\belse\b',               "ELSE"),
    (r'\bfor\b',                "FOR"),
    (r'\bwhile\b',              "WHILE"),
    (r'\brange\b',              "RANGE"),
    (r'\bbreak\b',              "BREAK"),
    (r'\bcontinue\b',           "CONTINUE"),
    (r'\bpass\b',               "PASS"),
    (r'\bfalse\b',              "FALSE"),
    (r'\btrue\b',               "TRUE"),
    (r'\bnone\b',               "NONE"),
    (r'\bin\b',                 "IN"),
    (r'\bis\b',                 "IS"),
    (r'\bclass\b',              "CLASS"),
    (r'\bfunction\b',           "FUNCTION"),
    (r'\breturn\b',             "RETURN"),
    (r'\bfrom\b',               "FROM"),
    (r'\bimport\b',             "IMPORT"),
    (r'\bwith\b',               "WITH"),
    (r'\bas\b',                 "AS"),
    (r'\bdict\b',               "TYPE"),
    (r'\bnum\b',                "TYPE"),
    (r'\bstr\b',                "TYPE"),
    (r'\blist\b',               "TYPE"),
    (r'\bset\b',                "TYPE"),
    (r'\,',                     "COMMA"),
    (r'\w+[.]\w+',              "DOTBETWEEN"),
    (r'\bnull\b',               "NULL"),
    (r'\bdelete\b',             "DELETE"),
    (r'\.',                     "DOT"),
    (r'\'\'\'[(?!(\'\'\'))\w\W]*\'\'\'',       "MULTILINE"),
    (r'\"\"\"[(?!(\"\"\"))\w\W]*\"\"\"',       "MULTILINE"),
    (r'[A-Za-z_][A-Za-z0-9_]*', "VARIABLE"),
]

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

    return tokenResult