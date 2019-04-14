from random import randrange
import random
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

def main(request):
    request_json = request.get_json(silent=True)
    state = json.loads(request_json['gamestate']['board'])
    if not request_json:
        raise ValueError("JSON is not found")
    # column = pickAiSpot(board[:], 3)
    # out = {'move':column}
    # state = generateboard()
    num_turns = 20
    next_step = next_move(state)
    out = {}
    out['move'] = step(state, next_step,randrange(1,5))
    # print(state)
    # print(next_move(state))
    # if out['winner'] != 0:
    #     break
    return json.dumps(out)

def next_move(state):
    # move : 1,2,3,4 u d l r
    board = state['board']
    #p1 will be the greedy intelligient bot
    p1 = state['p1']
    pos = p1['pos']
    next_move=0
    #top left corner
    rand = random.random()
    if(pos[0]==0 and pos[1]==0):
        if(rand <= .5):
            return 4
        else:
            return 2
    #top right corner
    elif(pos[0]==0 and pos[1]==len(pos[0])-1):
        if(rand <= .5):
            return 3
        else:
            return 2
    #bottom left corner
    elif(pos[0]==len(pos)-1 and pos[1]==0):
        if(rand <= .5):
            return 4
        else:
            return 1
    #bottom right corner
    elif(pos[0]==len(pos)-1 and pos[1]==len(pos[0])-1):
        if(rand <= .5):
            return 3
        else:
            return 1
    #top row
    elif(pos[0]==0):
        return 2
    #bottom row
    elif(pos[0]==len(pos)-1):
        return 1
    #left column
    elif(pos[1]==0):
        return 4
    #right column
    elif(pos[1]==len(pos[0])-1):
        return 3
    else:
        if(rand <= .25):
            return 1
        elif(rand <=.5):
            return 2
        elif(rand <= .75):
            return 3
        else:
            return 4

if __name__ == '__main__':
    main()
