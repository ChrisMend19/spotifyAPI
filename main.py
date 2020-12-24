import requests
import base64, json
from secrets import *

# curl -H "Authorization: Basic ZjM...zE=" -d grant_type=authorization_code -d code=MQCbtKe...44KN -d redirect_uri=https%3A%2F%2Fwww.foo.com%2Fauth https://accounts.spotify.com/api/token

authURL   = "https://accounts.spotify.com/api/token"

authHeader =  {}
authData = {}

# base64 Encode Cilient ID and Cilient Secret
def getAccessToken(clientID, clientSecret):
    message = f"{clientID}:{clientSecret}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    authHeader['Authorization'] = "Basic " + base64_message
    authData['grant_type'] = "client_credentials"

    res = requests.post(authURL, headers = authHeader, data = authData)
    responseObject = res.json()
    # print(json.dumps(responseObject, indent=2))
    accessToken = responseObject['access_token']
    return accessToken

def getPlaylistTracks(token, playlistID):
    playlistEndPoint = f"https://api.spotify.com/v1/playlists/{playlistID}"

    getHeader = {
        "Authorization": "Bearer " + token 
    }
    
    res = requests.get(playlistEndPoint, headers = getHeader)
    playlistObject = res.json()
    return playlistObject

def getPlaylist(token,userID):
    #user_id = "	https://api.spotify.com/v1/me" # attempt to get profile from login
    #playlistEndPoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    #https://open.spotify.com/user/21ihblz4jyinya46jfpuetmia?si=iVAZQKbOTFW-6okxEBdNKA
    playlistEndPoint = f"https://api.spotify.com/v1/users/{userID}/playlists"
    getHeader = {
        "Authorization": "Bearer " + token 
    }
    
    res = requests.get(playlistEndPoint, headers = getHeader)
    playlistObject = res.json()
    return playlistObject

def getSearched(token, name, typeOf):
    # types include album , artist, playlist, track, show and episode. 
    # name is name of item according to type
    playlistEndPoint = f"https://api.spotify.com/v1/search?q={name}&type={typeOf}&market=us"

    getHeader = {
        "Authorization": "Bearer " + token 
    }
    
    res = requests.get(playlistEndPoint, headers = getHeader)
    playlistObject = res.json()
    return playlistObject

# API requests
token = getAccessToken(clientID, clientSecret)

myUserID = "21ihblz4jyinya46jfpuetmia" # works
playlistMe = getPlaylist(token, myUserID)

playlistID = "28en0wPucGgZRIYaBMcohP?si=neKH65YAQ464wtBFiYXegg" # works
tracklist = getPlaylistTracks(token,playlistID)

searched = getSearched(token, "polo g", "album") # works
#print(searched)
#print(json.dumps(searched, indent=2))
#with open('songlist.json','w') as f:
#    json.dump(searched,f)

for t in tracklist['tracks']['items']:
    songName = t['track']['name']
    #print(songName)

for p in playlistMe['items']:
    playListName = p['name']
    #print(playListName)

for s in searched['albums']['items']:
    print(s['name'])