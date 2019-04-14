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
        pprint(state)
        if out['winner'] != 0:
            break
        

if __name__ == '__main__':
    main()
    
    
