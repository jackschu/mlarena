from django.shortcuts import render
from google.auth import app_engine
from google.cloud import storage
from googleapiclient.discovery import build
from google import auth
import google
import httplib2
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

# Create your views here.
PROJECT_ID = "mlarena"
REGION = "us-east1"

# Start a neew match in a random game based on leaderboards
def start_match(request):
    match = leaderboards_view.get_match_all_games()
    run_match(match)

# Run the given match
def run_match(match):
    match.state = 1
    # gamestate = run_cloudfunction("game" + str(match.game.id), {})
    # bot = 0
    # response = {'finished': False}
    # turn = 0
    # while not response['finished']:
    #     bot = bot % 2
    #     action = run_cloudfunction(_function_id("bot", match.bot_1.id if bot is 0 else match.bot_2.id), {
    #         'gamestate': gamestate
    #     })
    #     response = run_cloudfunction(_function_id("game", match.game.id), {
    #         'gmaestate': gamestate,
    #         'bot': bot,
    #         'action': action
    #     })
    #     gamestate = response['gamestate']
    #     frame = GameFrame()
    #     frame.frame_num = turn
    #     frame.state = gamestate
    #     turn = turn + 1
    #     bot = bot + 1
    # match_record = MatchRecord()
    # match_record.did_bot1_win = response.winner is 1
    # match.state = 2

def _function_id(id, type):
    return type + str(id)


def test_cloudfunction(request):
    file = "test"
    function_id = "testid2"
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, "main.zip")
    with open(file_path, 'rb') as fp:
        create_cloudfunction(fp, function_id, "game")

    return JsonResponse({'success': True})

def test_cloudfunction_run(request):
    function_id = "game15"
    params = {"frame": -1}
    return JsonResponse({
            'success': True,
            'result': run_cloudfunction(function_id, params)
        })


# Create a new cloud function with the given zip source archive, id (name), and type ("game"/"bot")
def create_cloudfunction(file, id, type):

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

# Run a Google Cloud Function with the given id with a dictionary of parameters
# Return: The result of the function
def run_cloudfunction(id, params):
    url = "https://" + REGION + "-" + PROJECT_ID + ".cloudfunctions.net/" + id
    r = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(params)) 
    return r.json() 