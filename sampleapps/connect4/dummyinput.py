from random import randrange
from referee import main
import json

json_in = {
    'frame' : 0,
    'move' : ,
    }

winner = 0
while winner == 0:
    json_in = json.loads(main(json.dumps(json_in)))
    winner = int(json_in['winner'])
    json_in['frame'] += 1
    print(json_in['board'])
    input()
print(winner)
