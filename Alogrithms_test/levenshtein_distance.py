from constants import *

"""
Calculate the Levenshtein distance of two words

Create a matrix that is 2 rows and 2 columns greater than
the words' lengths to allow for the matrix initialisation.
The matrix is then populated based on the formula 
(https://medium.com/@ethannam/understanding-the-
levenshtein-distance-equation-for-beginners-c4285a5604f0)
The distance of the two words will be the element at the 
largest [row][column] index of the matrix.
"""

def levenshtein_distance(a_word: str, b_word: str) -> int:
    if type(a_word) != str or type(b_word) != str:
        return Result.NOT_FOUND
    
    row, col = len(a_word)+2, len(b_word) + 2
    matrix=[[0 for _ in range(col)] for _ in range(row) ]
  
    for y in range(1, row):        
         matrix[y][1] = y-1
         if y >= 2:
             matrix[y][0]=a_word[y-2]

    for x in range(1,col):
         matrix[1][x] = x -1
         if x >= 2:
            matrix[0][x]=b_word[x-2]

    for i in range (2, row):
        for j in range(2, col):
                matrix[i][j] = min(
                                    matrix[i-1][j] + 1,
                                    matrix[i][j-1] +1,
                                    matrix[i-1][j-1] + 1 if matrix[0][j] != matrix[i][0] else matrix[i-1][j-1]
                                  )
                
    return matrix[row-1][col-1]


