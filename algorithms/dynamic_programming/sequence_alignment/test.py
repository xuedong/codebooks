import alignments as alg
import utils

#alignment_matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 5, 4, 3, 2, 1, 0, 0, 0], [0, 0, 0, 2, 2, 5, 7, 6, 5, 4, 3, 2, 1], [0, 0, 0, 1, 4, 4, 6, 6, 5, 4, 3, 2, 1], [0, 0, 0, 0, 3, 6, 6, 5, 5, 4, 3, 2, 1], [0, 0, 0, 0, 2, 5, 5, 8, 7, 6, 5, 4, 3], [0, 0, 0, 0, 1, 4, 4, 7, 10, 9, 8, 7, 6], [0, 0, 0, 0, 0, 3, 3, 6, 9, 9, 8, 7, 6], [0, 0, 0, 0, 0, 2, 2, 5, 8, 11, 10, 9, 8], [0, 0, 0, 0, 0, 1, 1, 4, 7, 10, 13, 12, 11]]

#max_i, max_j = alignments.max_index(alignment_matrix, 11, 12)

#best = alignment_matrix[max_i][max_j]
#print(best)

human = utils.read_protein(utils.HUMAN_EYELESS_URL)
fly = utils.read_protein(utils.FRUITFLY_EYELESS_URL)
scoring_matrix = utils.read_scoring_matrix(utils.PAM50_URL)
#print(scoring_matrix)
print(human)
alignment_matrix = alg.compute_alignment_matrix(human, fly, scoring_matrix, False)
