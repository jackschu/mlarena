import json
from random import randrange
import flask
import requests
def main(request):
    col =  randrange(0,7)
    out = {'move':col}
    return json.dumps(out)
