import json
import flask
import requests
xends = {-1 : -1, 1 : 7}
yends = {-1 : -1, 1 : 6}

def dist_from_bot(board, col):
    out = 0
    for i in range(0,6):
        if board[i][col] == 0:
            return out
        out+=1
        
    return -1
        

def checkwin(board, x ,y , player):
    dirs = [(1,0),(0,1),(1,1),(-1,1)]

    for dx,dy in dirs:
            forward = 0
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
                    forward+=1
                else:
                    break
            backward = 0
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
                    backward+=1
                else:
                    break
            if backward+forward >= 3:
                return player
    return 0

    
def start_board():
    board = [[0 for i in range(7)] for j in range(6)]
    return board

def main(request):
    winner = 0
    request_json = request.get_json(silent=True)
    #request_json = json.loads(request)
    if not request_json:
        raise ValueError("JSON is not found")
    
    if  'frame' in request_json:
        frame = int(request_json['frame'])
        first = frame  == -1
        if frame == 41:
            winner= 3
            request_json['winner'] = 3
            request_json['gamestate']['board'] = json.dumps(board)
            return json.dumps(request_json)
        if first:
            board = start_board()            
            print('frist')
            if not 'gamestate' in request_json:
                request_json['gamestate'] = {}
            request_json['winner'] = 0
            request_json['gamestate']['board'] = json.dumps(board)
            return json.dumps(request_json)
        elif 'board' in request_json['gamestate']:
            board = json.loads(request_json['gamestate']['board'])
        
        else:
            raise ValueError("Board is not found")
    player = frame%2+1    
    if 'move' in request_json:
        try:
            move = int(request_json['move'])
        except:
            if first:
                request_json['gamestate']['board'] = json.dumps(board)
            winner = 1 if player ==2 else 2
    else:
        raise ValueError("Move is not found")


    if move < 0  or move >= 7:
        if first:
            request_json['gamestate']['board'] = json.dumps(board)
        winner = 1 if player ==2 else 2
        request_json['winner'] = winner
        return json.dumps(request_json)
    dist = dist_from_bot(board,move)
    if dist< 0:
        winner = 1 if player ==2 else 2
        if first:
            request_json['gamestate']['board'] = json.dumps(board)
        request_json['winner'] = winner
        return json.dumps(request_json)
    
    board[dist][move] = player
    winner = checkwin(board, move, dist, player)

    request_json['gamestate']['board'] = json.dumps(board)
    request_json['winner'] = winner

    return json.dumps(request_json)
