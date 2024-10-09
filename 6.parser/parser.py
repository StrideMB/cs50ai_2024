import nltk
import sys

from nltk.tokenize import RegexpTokenizer

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP | S Conj NP | S Conj NP VP | S Conj NP VP PP
NP -> N | Det N | Det AP N | NP PP | AP NP | NP Adv | Det N Adv | Det AP N Adv
VP -> V | V NP | V NP PP | V PP | VP Adv | VP PP | VP Adv PP
PP -> P NP | P S
AP -> Adj | Adj AP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    #words = []
    #for word in nltk.word_tokenize(sentence):
    #    if any(char.isalpha() for char in word):
    #        words.append(word.lower())
    sentence = sentence.lower()
    regex = RegexpTokenizer(r'\w+')
    return regex.tokenize(sentence)
    #return words
    # raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    '''np_chunks = []

    def find_np_chunks(tree, np_chunks):
        if not hasattr(tree, "label"):
            return
        if tree.label() == "NP" and not any(child.label() == "NP" for child in tree):
            np_chunks.append(tree)
        else:
            for child in tree:
                find_np_chunks(child, np_chunks)

    find_np_chunks(tree, np_chunks)
    return np_chunks'''

    NP_chunks = []

    # tree.subtrees() finds all trees at all levels,
    # i.e. it is already recursive
    for subtree in tree.subtrees():

        # can ignore VP because in case of V NP, that NP
        # will show up in the tree.subtrees() on its own
        if subtree.label() == 'NP':
            if not check_subtree(subtree):
                NP_chunks.append(subtree)

    return NP_chunks
    # raise NotImplementedError

def check_subtree(subtree: nltk.tree.tree.Tree) -> bool:
    """
    Function check if there are any NP tags
    one level deeper in a subtree
    """
    for node in subtree.subtrees():
        if subtree == node:
            continue

        if node.label() == 'NP':
            return True

    return False

if __name__ == "__main__":
    main()
