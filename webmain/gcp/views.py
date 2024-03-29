from django.shortcuts import render
from google.auth import app_engine
from google.cloud import storage
from googleapiclient.discovery import build
from google import auth

import google
import httplib2
from games.models import GameFrame, Game, Match, MatchRecord
import google_auth_httplib2
import six
from . import auth
from django.http import HttpResponse, JsonResponse
import json
import time
import os
import requests
from leaderboards import views as leaderboards_view
from games.models import MatchRecord
from random import randrange

# Create your views here.
PROJECT_ID = "mlarena"
REGION = "us-east1"

# Start a neew match in a random game based on leaderboards
def start_match(request):
    match = leaderboards_view.get_match_all_games()
    return run_match(match)

# Run the given match
def run_match(match):
    match.state = 1
    bot = 0
    response = {'winner': 0}
    frame_num = 0
    init_state = {
        'frame': -1
    }
    response = run_cloudfunction(_function_id(match.game.id, "game"), init_state)
    gamestate = response['gamestate']
    record = MatchRecord()
    record.match = match
    record.save()
    frame = GameFrame()
    frame.frame_num = -1
    frame.state = json.dumps(response)
    frame.match_record = record
    frame.save()
    while response['winner'] == 0:
        bot = frame_num % 2
        action = run_cloudfunction(_function_id( match.bot1.id if bot is 0 else match.bot2.id,"bot"), {
            'gamestate': gamestate
        })
        response = run_cloudfunction(_function_id(match.game.id, "game"), {
            'frame':frame_num,
            'gamestate': gamestate,
            'bot': bot,
            'move': action['move'],
        })
        gamestate =response['gamestate']        
        frame_num+=1
        frame = GameFrame()
        frame.frame_num = frame_num
        frame.state = json.dumps(response)
        frame.match_record = record
        frame.save()
    
    record.winner_number = response['winner']

    record.save()
    match.state = 2
    return leaderboards_view.update_match_winner(match, record.winner_number)
    
def _function_id(id, type):
    return type + str(id)


def test_cloudfunction(request):
    file = "test"
    function_id = "jacktestid2"
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, "main.zip")
    with open(file_path, 'rb') as fp:
        print(fp)
        create_cloudfunction(fp, function_id, "game")

    return JsonResponse({'success': True})

def test_cloudfunction_run(request):
    function_id = "game17"
    params = {"frame": -1}
    return JsonResponse({
            'success': True,
            'result': run_cloudfunction(function_id, params)
        })


# Create a new cloud function with the given zip source archive, id (name), and type ("game"/"bot")
def create_cloudfunction(file, id, type):
    id = mod_id(id)
    print(file,id, type)
#    print(type(file),type(id), type(type)    )
    # Setup auth
    scopes = ('https://www.googleapis.com/auth/cloud-platform',)
    credentials = (
                    google.oauth2.service_account.Credentials.from_service_account_info(
                        auth.auth_key, scopes=scopes)
                )
    http = httplib2.Http()
    authed_http = google_auth_httplib2.AuthorizedHttp(
        credentials, http=http)

    # Build the client 
    cf_build = build('cloudfunctions', 'v1', http=authed_http)

    # Create the request data
    upload_url = upload_file(file, "projects/" + PROJECT_ID + "/locations/" + REGION, cf_build)
    cloudfunction = {
        "httpsTrigger": {
            "url": "https://" + REGION + "-" + PROJECT_ID + ".cloudfunctions.net/" + id
        },
        "sourceUploadUrl": upload_url, #upload_response['uploadUrl'],
        "availableMemoryMb": 256,
        "versionId": "1",
        "labels": {
            "type": type
        },
        "entryPoint": "main",
        "timeout": "60s", 
        "runtime": "python37", 
        "name": "projects/mlarena/locations/us-east1/functions/" + id,
    }

    # Create the cloud function
    response = cf_build.projects().locations().functions().create(location="projects/" + PROJECT_ID + "/locations/" + REGION, body=cloudfunction).execute(num_retries=0)
    operation_name = response["name"]

    # Wait for a response
    while True:
            operation_response = cf_build.operations().get(
                name=operation_name,
            ).execute(num_retries=0)
            if operation_response.get("done"):
                response = operation_response.get("response")
                error = operation_response.get("error")
                # Note, according to documentation always either response or error is
                # set when "done" == True
                if error:
                    raise Exception(str(error))
                return response
            time.sleep(1)

# Upload source files in zip format for a cloud function
# Returns: a signed link to the file
def upload_file(file, location, cf_build):
    # Generate the URL
    upload_response = cf_build.projects().locations().functions().generateUploadUrl(parent=location).execute()

    # Put the file at the URL 
    requests.put(
        url=upload_response['uploadUrl'],
        data=file.read(),
        headers={
            'Content-type': 'application/zip',
            'x-goog-content-length-range': '0,104857600',
        }
    )

    # Return the generated URL
    return upload_response['uploadUrl']

def mod_id(id):
    id =str(id)
    id += auth.name
    try:
        if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            id +='prod'
    except:
        pass
    return id
        

# Run a Google Cloud Function with the given id with a dictionary of parameters
# Return: The result of the function
def run_cloudfunction(id, params):
    id = mod_id(id)
    url = "https://" + REGION + "-" + PROJECT_ID + ".cloudfunctions.net/" + id
    r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(params)) 
    return r.json() 
