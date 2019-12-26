#!/usr/bin/env python
import urllib.parse
import requests
import sys


# Custom exception
class MyException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


# Get an authentication token
def get_auth_token(url, user, password):
    endpoint = url + '/jwt/token'
    response = requests.get(endpoint, auth=(user, password))
    if response.status_code == 403:
        raise MyException('Error getting token. status_code was: {}'.format(response.status_code))
    else:
        response = response.json()
        token_string = response['token']

    return token_string


def slides_in_collection(token, url, coll_id):
    endpoint = url + '/listofimages/' + str(coll_id) + '?_format=json'
    # print(endpoint)
    headers = {"Authorization": "Bearer " + token}
    response = requests.get(endpoint, headers=headers).json()
    if not response:
        eprint('slides_in_collection', response)
        exit(1)

    return response


def maps_for_slide(token, url, slide_id):
    endpoint = url + '/maps/' + str(slide_id) + '?_format=json'
    # print(endpoint)
    headers = {"Authorization": "Bearer " + token}
    response = requests.get(endpoint, headers=headers).json()

    return response


# Get the slide unique identifier
def get_slide_unique_id(token, url, collection, studyid, clinicaltrialsubjectid, imageid):
    # COLLECTION/STUDY/SUBJECT/IMAGE
    coll_encoded = urllib.parse.quote(collection)

    # NEW WAY
    endpoint = url + "/idlookup/" + coll_encoded + "/" + studyid + "/" + clinicaltrialsubjectid + "/" + imageid
    # OLD WAY
    # endpoint = url + "/idlookup/" + studyid + "/" + clinicaltrialsubjectid + "/" + imageid + "/" + coll_encoded
    # print('endpoint', endpoint)

    headers = {"Authorization": "Bearer " + token}
    response = requests.get(endpoint, headers=headers).json()
    if response:
        # pdb["uuid"] = response[0]['uuid'][0]['value']
        _id = response[0]['nid'][0]['value']
        # print('slide id', _id)
    else:
        eprint('Error getting ID.', response)
        eprint('endpoint', endpoint)
        exit(1)

    return str(_id)


# Print to std err
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
