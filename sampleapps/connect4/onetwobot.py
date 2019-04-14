import json
from random import randrange
import flask
import requests

def main(request):    
    col =  randrange(0,2)
    out = {'move':col}
    return json.dumps(out)
