from argparse import ArgumentParser
from readgrammar import read_grammar, tokenization
from cfgtocnf import CFG_to_CNF
from cykparser import cykAlgorithm

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    argument_parser.add_argument("nama_file", type=str, help="Nama File yang hendak diparse.")

    args = argument_parser.parse_args()
    # print(tokenization(args.nama_file))
    # print(CFG_to_CNF(read_grammar("grammar.txt")))
    if cykAlgorithm(tokenization(args.nama_file), CFG_to_CNF(read_grammar("grammar.txt"))):
        print("ACCEPTED")
    else:
        print("SYNTAX ERROR")