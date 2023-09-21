#!/usr/bin/python3

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
    from PyQt6.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import random
import math
import numpy as np

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1


class GeneSequencing:

    def __init__(self):
        pass

    # This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean
    # that tells you whether you should compute a banded alignment or full alignment, and _align_length_ tells you how
    # many base pairs to use in computing the alignment

    def align(self, seq1, seq2, banded, align_length):
        self.banded = banded
        self.MaxCharactersToAlign = align_length
        seq1 = seq1[:align_length]
        seq2 = seq2[:align_length]
        alignment1 = ""
        alignment2 = ""


        ###################################################################################################
        # your code should replace these three statements and populate the three variables:
        # score, alignment1 and alignment2

        if not self.banded:
            if len(seq1) < align_length:
                rows = len(seq1) + 1
            else:
                rows = align_length + 1
            if len(seq2) < align_length:
                cols = len(seq2) + 1
            else:
                cols = align_length + 1

            dynamicTable = np.zeros((rows, cols))
            prevTable = np.zeros((rows, cols))

            #Set prev and dynamic values for the blank row and column
            for row in range(rows):
                dynamicTable[row][0] = (row * 5)
            for col in range (cols):
                dynamicTable[0][col] = (col * 5)

            for row in range(1, rows):
                prevTable[row][0] = 2
            for col in range(1, cols):
                prevTable[0][col] = 1


            for row in range(1, rows):
                for col in range(1, cols):
                    minimumVal = math.inf
                    leftVal = dynamicTable[row][col - 1] + 5
                    upVal = dynamicTable[row - 1][col] + 5
                    if seq1[row - 1] == seq2[col - 1]:
                        diagonal = dynamicTable[row - 1][col - 1] - 3
                    else:
                        diagonal = dynamicTable[row - 1][col - 1] + 1

                    direction = ""

                    #Use arbitrary values to show whether we went left, up, or diagonal. 1 for left, 2 for up, 3 for diagonal
                    if leftVal < minimumVal:
                        minimumVal = leftVal
                        direction = 1
                    if upVal < minimumVal:
                        minimumVal = upVal
                        direction = 2
                    if diagonal < minimumVal:
                        minimumVal = diagonal
                        direction = 3

                    prevTable[row][col] = direction
                    dynamicTable[row][col] = minimumVal

            score = dynamicTable[rows - 1][cols - 1]
            prevRow = rows - 1
            prevCol = cols - 1
            seq1Index = prevRow - 1
            seq2Index = prevCol - 1

            while prevRow > 0 or prevCol > 0:
                if prevTable[prevRow][prevCol] == 1:
                    alignment1 = "-" + alignment1
                    alignment2 = seq2[seq2Index] + alignment2
                    prevCol = prevCol - 1
                    seq2Index = seq2Index - 1
                elif prevTable[prevRow][prevCol] == 2:
                    alignment1 = seq1[seq1Index] + alignment1
                    alignment2 = "-" + alignment2
                    prevRow = prevRow - 1
                    seq1Index = seq1Index - 1
                elif prevTable[prevRow][prevCol] == 3:
                    alignment1 = seq1[seq1Index] + alignment1
                    alignment2 = seq2[seq2Index] + alignment2
                    prevRow = prevRow - 1
                    prevCol = prevCol -1
                    seq1Index = seq1Index - 1
                    seq2Index = seq2Index - 1

        else:

            if len(seq1) < align_length:
                seq1Length = len(seq1)
            else:
                seq1Length = align_length

            if len(seq2) < align_length:
                seq2Length = len(seq2)
            else:
                seq2Length = align_length

            #Check if the two sequences can be compared using the banded algorithm, if not, no alignment is possible
            if abs(seq1Length - seq2Length) > 3:
                score = math.inf
                alignment1 = "No Alignment Possible"
                alignment2 = "No Alignment Possible"

            else:
                if seq1Length < seq2Length:
                    offset = seq2Length - seq1Length
                    if len(seq1) < align_length:
                        rows = len(seq1) + 1
                    else:
                        rows = align_length + 1
                else:
                    offset = 0
                    if len(seq2) < align_length:
                        rows = len(seq2) + 1
                    else:
                        rows = align_length + 1

                cols = 1 + (2 * MAXINDELS)
                dynamicTable = np.ones((rows, cols)) * math.inf
                prevTable = np.zeros((rows, cols))

                # Set dynamic values for the blank row and column
                for row in range(MAXINDELS + 1):
                    dynamicTable[row][0] = (row * 5)
                for col in range(MAXINDELS + 1):
                    dynamicTable[0][col] = col * 5

                for row in range(1, rows):
                    if row < MAXINDELS:
                        colRange = row + 4
                    elif rows - 1 - row + offset < MAXINDELS:
                        colRange = 4 + (rows - 1 - row + offset)
                    else:
                        colRange = 1 + (2 * MAXINDELS)
                    for col in range(colRange):
                        minimumVal = math.inf
                        if col - 1 < 0:
                            leftVal = math.inf
                        else:
                            leftVal = dynamicTable[row][col - 1] + 5
                        if row > 3:
                            if col < 6:
                                upVal = dynamicTable[row - 1][col + 1] + 5
                            else:
                                upVal = math.inf

                            if seq1[row - 1] == seq2[col - 1 + (row - 3)]:
                                diagonal = dynamicTable[row - 1][col] - 3
                            else:
                                diagonal = dynamicTable[row - 1][col] + 1
                        else:
                            upVal = dynamicTable[row - 1][col] + 5
                            if col > 0:
                                if seq1[row - 1] == seq2[col - 1]:
                                    diagonal = dynamicTable[row - 1][col - 1] - 3
                                else:
                                    diagonal = dynamicTable[row - 1][col - 1] + 1
                            else:
                                diagonal = math.inf

                        direction = ""

                        # Use arbitrary values to show whether we went left, up, or diagonal. 1 for left, 2 for up, 3 for diagonal
                        if leftVal < minimumVal:
                            minimumVal = leftVal
                            direction = 1
                        if upVal < minimumVal:
                            minimumVal = upVal
                            direction = 2
                        if diagonal < minimumVal:
                            minimumVal = diagonal
                            direction = 3

                        prevTable[row][col] = direction
                        dynamicTable[row][col] = minimumVal



                score = dynamicTable[rows - 1][MAXINDELS + offset]
                prevRow = rows - 1
                prevCol = MAXINDELS + offset
                seq1Index = len(seq1) - 1
                seq2Index = len(seq2) - 1

                while prevRow > 0 or prevCol > 0:
                    if prevTable[prevRow][prevCol] == 1:
                        alignment1 = "-" + alignment1
                        alignment2 = seq2[seq2Index] + alignment2
                        seq2Index = seq2Index - 1
                        if not (prevCol - 1 < 0):
                            prevCol = prevCol - 1
                    if prevRow > 3:
                        if prevTable[prevRow][prevCol] == 2:
                            alignment1 = seq1[seq1Index] + alignment1
                            alignment2 = "-" + alignment2
                            seq1Index = seq1Index - 1
                            prevRow = prevRow - 1
                            prevCol = prevCol + 1
                        elif prevTable[prevRow][prevCol] == 3:
                            prevRow = prevRow - 1
                            alignment1 = seq1[seq1Index] + alignment1
                            alignment2 = seq2[seq2Index] + alignment2
                            seq1Index = seq1Index - 1
                            seq2Index = seq2Index - 1
                    else:
                        if prevTable[prevRow][prevCol] == 2:
                            alignment1 = seq1[seq1Index] + alignment1
                            alignment2 = "-" + alignment2
                            prevRow = prevRow - 1
                            seq1Index = seq1Index - 1
                        elif col > 0:
                            if prevTable[prevRow][prevCol] == 3:
                                alignment1 = seq1[seq1Index] + alignment1
                                alignment2 = seq2[seq2Index] + alignment2
                                prevRow = prevRow - 1
                                prevCol = prevCol - 1
                                seq1Index = seq1Index - 1
                                seq2Index = seq2Index - 1

        #alignment1 = 'abc-easy  DEBUG:({} chars,align_len={}{})'.format(
        #    len(seq1), align_length, ',BANDED' if banded else '')
        #alignment2 = 'as-123--  DEBUG:({} chars,align_len={}{})'.format(
        #    len(seq2), align_length, ',BANDED' if banded else '')
        ###################################################################################################
        alignment1 = alignment1[:100]
        alignment2 = alignment2[:100]

        return {'align_cost': score, 'seqi_first100': alignment1, 'seqj_first100': alignment2}
