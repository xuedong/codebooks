"""
Helper functions
"""

DESKTOP = True

import math
import random
from urllib.request import urlopen

if DESKTOP:
    import matplotlib.pyplot as plt
    import alignments as alg
else:
    import simpleplot
    import userXX_XXXXXXX as xxxxxxx
    

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# Helper functions

#def read_scoring_matrix(filename):
#    scoring_dict = {}
#    scoring_file = urlopen(filename)
#    ykeys = scoring_file.readline()
#    ykeychars = ykeys.split()
#    for line in scoring_file.readlines():
#        vals = line.split()
#        xkey = vals.pop(0)
#        scoring_dict[xkey] = {}
#        for ykey, val in zip(ykeychars, vals):
#            scoring_dict[xkey][ykey] = int(val)
#    return scoring_dict


def read_scoring_matrix(filename):
    """
    Helper function to read a scoring matrix from a file.
    Returns the scoring matrix as a dictionary.
    """
    matrix_file = open(filename, 'r')
    scoring_matrix = dict()
    # Read the first line and create a list
    column_values = matrix_file.readline().split()
    # Read the other lines
    for line in matrix_file.readlines():
        scores = line.split()
        row_value = scores.pop(0)
        scoring_matrix[row_value] = dict()
        for column_value, score in zip(column_values, scores):
            scoring_matrix[row_value][column_value] = int(score)
    matrix_file.close()

    return scoring_matrix


#def read_protein(filename):
#    protein_file = urlopen(filename)
#    protein_seq = protein_file.read()
#    protein_seq = protein_seq.rstrip()
#    return protein_seq


def read_protein(filename):
    """
    Helper function to read protein sequence from a file.
    Returns the sequence as a string.
    """
    protein_file = open(filename, 'r')
    protein_sequence = protein_file.read().rstrip()
    protein_file.close()
    
    return protein_sequence


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urlopen(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print("Loaded a dictionary with " + len(word_list) + " words")
    return word_list




