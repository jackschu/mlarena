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
from django.http import HttpResponse 
import json
import time
import os
import requests


# Create your views here.
PROJECT_ID = "mlarena"
REGION = "us-east1"

def test_cloudfunction(request):
    file = "test"
    function_id = "testid2"
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, "main.zip")
    with open(file_path, 'rb') as fp:
        create_cloudfunction(fp, function_id, "game")


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
            "url": "https://us-east1-mlarena.cloudfunctions.net/" + id
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

    return HttpResponse(operation_response)

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