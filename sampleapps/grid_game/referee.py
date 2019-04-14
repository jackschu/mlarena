from random import randrange
from pprint import pprint

def generateboard():
    n = 5
    board = [[randrange(0,5) for l in range(n)] for x in range(n)]
    board[0][0] = 0
    board[n-1][n-1] = 0

    p1 = {'pos':[0,0], 'score': 0}
    p2 = {'pos':[0,0], 'score': 0}
    gamestate = {'board':board, 'p1': p1, 'p2':p2}
    return gamestate

def apply_move(board, p, move):
    dp = 0
    n=5
    if move == 1:
        dp = [0,1]
    elif move == 2:
        dp = [0,-1]
    elif move == 3:
        dp = [-1,0]
    elif move == 4:
        dp = [1,0]
    p['pos'][0] += dp[0]
    p['pos'][1] += dp[1]
    if p['pos'][0] > n-1 or p['pos'][0] < 0 \
       or p['pos'][1] > n-1 or p['pos'][1] < 0:
        return -1
    p['score'] += board[p['pos'][0]][p['pos'][1]]
    board[p['pos'][0]][p['pos'][1]] = 0
    return 0



def step(state, move1, move2):

    # move : 1,2,3,4 u d l r
    res = apply_move(state['board'], state['p1'], move1)
    if res < 0:
        return {'winner':2, 'state':state}
    res = apply_move(state['board'], state['p2'], move2)
    if res < 0:
        return {'winner':1, 'state':state}
    return {'winner':0, 'state':state}

def main():
    state = generateboard()
    num_turns = 20
    for i in range(20):
        out = step(state, randrange(1,5),randrange(1,5))
        # pprint(state)
        print(next_move(state))
        if out['winner'] != 0:
            break

def next_move(state):
    # move : 1,2,3,4 u d l r
    board = state['board']
    #p1 will be the greedy intelligient bot
    p1 = state['p1']
    pos = p1['pos']
    #4 cases: top or bottom row, or left or right column
    next_move=0
    #top left corner
    if(pos[0]==0 and pos[1]==0):
        return 4 if board[0][1]>board[1][0] else 2
    #top right corner
    elif(pos[0]==0 and pos[1]==len(pos[0])-1):
        return 3 if board[0][len(pos[0])-2] > board[1][len(pos[0])-1] else 2
    #bottom left corner
    elif(pos[0]==len(pos)-1 and pos[1]==0):
        return 1 if board[len(pos)-2][0] > board[len(pos)-1][1] else 4
    #bottom right corner
    elif(pos[0]==len(pos)-1 and pos[1]==len(pos[0])-1):
        return 3 if board[len(pos)-2][len(pos)-1] > board[len(pos)-1][len(pos)-2] else 1
    #left column
    elif(pos[0]==0):
        return 2
    #right column
    elif(pos[0]==len(pos)-1):
        return 1
    #top row
    elif(pos[1]==0):
        return 4
    #bottom row
    elif(pos[1]==len(pos[0])-1):
        return 3
    else:
        x = pos[0]
        y = pos[1]
        next_move = max(board[x-1][y], board[x][y-1], board[x+1][y], board[x][y+1])
        if(board[x-1][y]==max):
            return 3
        elif(board[x+1][y]==max):
            return 4
        elif(board[x][y-1]==max):
            return 2
        elif(board[x][y+1]==max):
            return 1

if __name__ == '__main__':
    main()
