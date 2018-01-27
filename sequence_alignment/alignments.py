"""
Four functions are implemented in this file:

build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag)
compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
"""

######################################################
# Code for building the scoring matrix

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Takes as input a set of characters alphabet and three scores diag_score,
    off_diag_score, and dash_score. The function returns a dictionary of
    dictionaries whose entries are indexed by pairs of characters in alphabet
    plus '-'. The score for any entry indexed by one or more dashes is
    dash_score. The score for the remaining diagonal entries is diag_score.
    Finally, the score for the remaining off-diagonal entries is off_diag_score.
    """
    scoring_matrix = {'-': {'-': dash_score}}

    for letter1 in alphabet:
        if letter1 not in scoring_matrix:
            scoring_matrix[letter1] = {}
        scoring_matrix[letter1]['-'] = dash_score
        scoring_matrix['-'][letter1] = dash_score

        for letter2 in alphabet:
            if letter1 == letter2:
                scoring_matrix[letter1][letter2] = diag_score
            else:
                scoring_matrix[letter1][letter2] = off_diag_score

    return scoring_matrix

######################################################
# Code for computing the alignment matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common
    alphabet with the scoring matrix scores. The function computes and
    returns the alignment matrix for seq_x and seq_y. If global_flag is True,
    each entry of the matrix can be negative. If global_flag is False,
    then we will force each entry to be positive.
    """
    rows = len(seq_x)
    cols = len(seq_y)
    alignment_matrix = [[0 for dummy_j in range(cols+1)] for dummy_i in range(rows+1)]

    for idx_i in range(1, rows+1):
        score = alignment_matrix[idx_i-1][0] + scoring_matrix[seq_x[idx_i-1]]['-']
        if global_flag:
            alignment_matrix[idx_i][0] = score
        else:
            alignment_matrix[idx_i][0] = max(0, score)

    for idx_j in range(1, cols+1):
        score = alignment_matrix[0][idx_j-1] + scoring_matrix['-'][seq_y[idx_j-1]]
        if global_flag:
            alignment_matrix[0][idx_j] = score
        else:
            alignment_matrix[0][idx_j] = max(0, score)

    for idx_i in range(1, rows+1):
        for idx_j in range(1, cols+1):
            score_i_1_j_1 = alignment_matrix[idx_i-1][idx_j-1] + scoring_matrix[seq_x[idx_i-1]][seq_y[idx_j-1]]
            score_i_j_1 = alignment_matrix[idx_i][idx_j-1] + scoring_matrix['-'][seq_y[idx_j-1]]
            score_i_1_j = alignment_matrix[idx_i-1][idx_j] + scoring_matrix[seq_x[idx_i-1]]['-']
            if global_flag:
                alignment_matrix[idx_i][idx_j] = max([score_i_1_j_1, score_i_j_1, score_i_1_j])
            else:
                alignment_matrix[idx_i][idx_j] = max([max(0, score_i_1_j_1), max(0, score_i_j_1), max(0, score_i_1_j)])

    return alignment_matrix

######################################################
# Code for computing the global alignment

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as two sequences seq_x and seq_y whose elements share a common
    alphabet with scoring matrix. This function computes a global alignment
    of seq_x and seq_y using the global alignment matrix. The function
    returns a tuple of the form (score, align_x, align_y) where score is
    the score of the global alignment align_x and align_y. Note that
    align_x and align_y should have the same length and may include
    the padding character '-'.
    """
    idx_i = len(seq_x)
    idx_j = len(seq_y)
    score = alignment_matrix[idx_i][idx_j]
    align_x = ''
    align_y = ''

    while idx_i != 0 and idx_j != 0:
        if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i-1][idx_j-1] + scoring_matrix[seq_x[idx_i-1]][seq_y[idx_j-1]]:
            align_x = seq_x[idx_i-1] + align_x
            align_y = seq_y[idx_j-1] + align_y
            idx_i -= 1
            idx_j -= 1
        elif alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i-1][idx_j] + scoring_matrix[seq_x[idx_i-1]]['-']:
            align_x = seq_x[idx_i-1] + align_x
            align_y = '-' + align_y
            idx_i -= 1
        else:
            align_x = '-' + align_x
            align_y = seq_y[idx_j-1] + align_y
            idx_j -= 1

    while idx_i != 0:
        align_x = seq_x[idx_i-1] + align_x
        align_y = '-' + align_y
        idx_i -= 1

    while idx_j != 0:
        align_x = '-' + align_x
        align_y = seq_y[idx_j-1] + align_y
        idx_j -= 1

    return score, align_x, align_y

######################################################
# Code for computing the local alignment

def max_index(alignment_matrix):
    """
    Helper function that computes the index of the maximum in the
    alignment matrix.
    """
    max_i = 0
    max_j = 0
    for idx_i in range(len(alignment_matrix)):
        for idx_j in range(len(alignment_matrix[0])):
            if alignment_matrix[idx_i][idx_j] > alignment_matrix[max_i][max_j]:
                max_i = idx_i
                max_j = idx_j

    return max_i, max_j

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as two sequences seq_x and seq_y whose elements share a common
    alphabet with scoring matrix. This function computes a local alignment
    of seq_x and seq_y using the global alignment matrix. The function
    returns a tuple of the form (score, align_x, align_y) where score is
    the score of the optimal local alignment align_x and align_y. Note that
    align_x and align_y should have the same length and may include
    the padding character '-'.
    """
    idx_i, idx_j = max_index(alignment_matrix)
    score = alignment_matrix[idx_i][idx_j]
    align_x = ''
    align_y = ''
    max_score = score

    while max_score > 0:
        if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i-1][idx_j-1] + scoring_matrix[seq_x[idx_i-1]][seq_y[idx_j-1]]:
            align_x = seq_x[idx_i-1] + align_x
            align_y = seq_y[idx_j-1] + align_y
            max_score = alignment_matrix[idx_i-1][idx_j-1]
            idx_i -= 1
            idx_j -= 1
        elif alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i-1][idx_j] + scoring_matrix[seq_x[idx_i-1]]['-']:
            align_x = seq_x[idx_i-1] + align_x
            align_y = '-' + align_y
            max_score = alignment_matrix[idx_i-1][idx_j]
            idx_i -= 1
        else:
            align_x = '-' + align_x
            align_y = seq_y[idx_j-1] + align_y
            max_score = alignment_matrix[idx_i][idx_j-1]
            idx_j -= 1

    #while idx_i != 0 and alignment_matrix[idx_i][idx_j] != 0:
    #    align_x = seq_x[idx_i-1] + align_x
    #    align_y = '-' + align_y
    #    idx_i -= 1

    #while idx_j != 0 and alignment_matrix[idx_j][idx_j] != 0:
    #    align_x = '-' + align_x
    #    align_y = seq_y[idx_j-1] + align_y
    #    idx_j -= 1

    return score, align_x, align_y
