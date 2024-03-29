import json
#modified from:
# MIT License

# Copyright (c) 2017 jam1garner

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#                     Description:
#                  ==================
# A Connect 4 AI that uses heuristic board definitions to evaluate
# a subsection of the game tree in order to decide which move is
# most likely to lead to a win. Made in less than an hour for a
# challenge/bet. Enjoy and hope you can learn something from it! 

from copy import deepcopy
import time

# Dictionaries to map iteration direction to end of range
xends = {-1 : -1, 1 : 7}
yends = {-1 : -1, 1 : 6}

# Checks if a board state is a win for a player
def isWin(board, x, y, player):
    directionPairs = [(1,0),(0,1),(1,1),(-1,1)]
    for dx,dy in directionPairs:
        firstDirection = 0
        if dx == 0:
            xiter = [x for _ in range(7)]
        else:
            xiter = range(x + dx, xends[dx], dx)
        if dy == 0:
            yiter = [y for _ in range(7)]
        else:
            yiter = range(y + dy, yends[dy], dy)
        for xi,yj in zip(xiter,yiter):
            if board[yj][xi] == player:
                firstDirection+=1
            else:
                break
        secondDirection = 0
        if dx == 0:
            xiter = [x for _ in range(7)]
        else:
            xiter = range(x - dx, xends[-dx], -dx)
        if dy == 0:
            yiter = [y for _ in range(7)]
        else:
            yiter = range(y - dy, yends[-dy], -dy)
        for xi,yj in zip(xiter,yiter):
            if board[yj][xi] == player:
                secondDirection+=1
            else:
                break
        if secondDirection+firstDirection >= 3:
            return 1
    return 0

# Return the distance from the bottom, this is used
# for knowing where the next piece will go
def distanceFromBottom(board, column):
    d = 0
    for i in range(5, -1, -1):
        if board[i][column] != 0:
            d += 1
        else:
            break
    return d

# Hueristically rate a board state this is
# somewhat arbitrary but it is weighted based on:
# * Whether each spot is a win
# * The distance from bottom that spot is
# * Defense > Offense (Weighted 4x as heavily)
# These values were tweaked iteratively based
# on tests against ~20 real world players, nothing
# scientific but is designed to do decently well
# based on human tendency.
def rateBoard(board):
    numberOfWinsX = 0
    for row in range(6):
        for column in range(7):
            if board[row][column] == 0:
                d = distanceFromBottom(board, column)
                numberOfWinsX += isWin(board, column, row, 1) * (0.8 ** (5 - row - d))
    numberOfWinsO = 0
    for row in range(6):
        for column in range(7):
            if board[row][column] == 0:
                d = distanceFromBottom(board, column)
                numberOfWinsO += isWin(board, column, row, 2) * 4 * (0.8 ** (5 - row - d))
    return numberOfWinsX - numberOfWinsO

# Try all paths for a certain depth from a certain board
# state recursively, using the average hueristic rating 
# evaluation in order to pick one based on said average 
def recursivelyPickAiSpot(board, iterations, turn):
    if turn == 1:
        turn = 2
    else:
        turn = 1
    if iterations <= 0:
        return rateBoard(board)
    avg = 0
    for column in range(7):
        boardCopy = deepcopy(board)
        r,c = 5 - distanceFromBottom(board, column),column
        if turn == 2 and isWin(boardCopy, c, r, 2):
            return -4
        elif turn == 1 and isWin(boardCopy, c, r, 1):
            return 1
        boardCopy[r][c] = turn
        avg += recursivelyPickAiSpot(boardCopy, iterations - 1, turn)
    avg /= 7
    return avg

# Pick the place to play, if a winning play exists pick it
# if there is a way to block an ensured loss pick it
# otherwise use the recursive column picking in order
# to decide which play is best
def pickAiSpot(board, iterations):
    for column in range(7):
        r,c = 5 - distanceFromBottom(board, column),column
        if board[r][c] == 0 and isWin(board, c, r, 1):
            return column
    for column in range(7):
        r,c = 5 - distanceFromBottom(board,column),column
        if board[r][c] == 0 and isWin(board, c, r, 2):
            return column
    plays = [0 for i in range(7)]
    for column in range(7):
        boardCopy = [row[:] for row in board]
        r,c = 5 - distanceFromBottom(board, column),column
        if r < 0:
            plays[column] = -100000
        else:
            boardCopy[r][c] = 1
            plays[column] =  recursivelyPickAiSpot(boardCopy, iterations - 1, 2)

    for column in range(7):
        boardCopy = [row[:] for row in board]
        r,c = 5 - distanceFromBottom(board, column),column
        if r > 0:
            boardCopy[r][c] = 1
            if isWin(boardCopy, c, r - 1, 2):
                plays[column] = -10000

    p = plays.copy()
    p.sort()
    return plays.index(p[-1])


# User interface, kinda rough and doesn't verify
# user input so it isn't great but it does the job
# so long as the user doesn't try and cheat!
def main(request):
    request_json = request.get_json(silent=True)
    board = json.loads(request_json['gamestate']['board'])
    if not request_json:
        raise ValueError("JSON is not found")
    
    column = pickAiSpot(board[:], 3)
    out = {'move':column}
    return json.dumps(out)
