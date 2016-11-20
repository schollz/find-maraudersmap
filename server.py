import requests
import json
import time
import random
import hashlib
import os.path

# {
#   "users": {
#     "zack": [
#       {
#         "svm": null,
#         "location": "desk=36.00333=-78.93949=3",
#         "bayes": {
#           "afm=36.00336=-78.93946=3": 0.5955045187032928,
#           "elevator=36.00339=-78.93959=3": -1.1648174923452663,
#           "desk=36.00333=-78.93949=3": 0.950688524826225,
#           "laser=36.00334=-78.93947=3": -0.3813755511842516
#         },
#         "time": "2016-11-19 15:33:38.187513785 -0500 EST"
#       }
#     ]
#   },
#   "success": true,
#   "message": "Correctly found locations."
# }
# TO 
# {
#     "title": "Recent Uploads with geodata",
#     "link": "https:\/\/www.flickr.com\/photos\/",
#     "description": "",
#     "modified": "2016-11-19T20:01:45Z",
#     "generator": "https:\/\/www.flickr.com",
#     "items": [
#      {
#         "title": "Sofgfgfme",
#         "latitude" : "32.31740",
#         "longitude" : "-78.377410"
#      }
#     ]
# }



def getJSON(group):
    if os.path.isfile(group + ".json"):
        if time.time()-os.path.getmtime(group + ".json") < 3:
            return
    r = requests.get('https://ml.internalpositioning.com/location?group=' + group)
    data = r.json()
    payload = {}
    payload["title"] = "Some title"
    payload["link"] = "asldfkjaslfd"
    payload["description"] = "asldkfjaksldjf"
    payload["modified"] = "2016-11-19T20:01:45Z"
    payload["generator"] = "https:\/\/www.flickr.com"
    payload["items"] = []
    if 'users' not in data:
        return
    for user in data['users'].keys():
        try:
            foo = data['users'][user][0]['location']
            item = {}
            item['title'] = user
            item['description']= "Location: " + \
                foo.split('=')[0] + ", floor " + foo.split('=')[-1] + "<br>Last seen: " + \
                data['users'][user][0]['time'].split(".")[0] + \
                "<br><img src=\"/%s\" width=\"180\" height=\"240\" alt=\"\" \/>" % (user + ".jpg")
            rSeed = hash(data['users'][user][0]['time'])
            random.seed(rSeed)                
            item['latitude'] = str(float(foo.split('=')[1]) + random.random()/50000)
            item['longitude'] = str(float(foo.split('=')[2]) + random.random()/50000)
            payload['items'].append(item)
        except:
            pass
    print("got " + group)
    with open(group + ".json","w") as f:
        f.write(json.dumps(payload))
    return

from flask import Flask, request
app = Flask(__name__)

@app.route('/makejson')
def data():
    # here we want to get the value of user (i.e. ?user=some-value)
    group = request.args.get('group','')
    if len(group) == 0:
            return "must add group"
    getJSON(group)
    return "done"



if __name__ == "__main__":
    app.run(host="0.0.0.0")