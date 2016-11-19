import requests
import json
import time
import random
import hashlib

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


def getJSON():
	r = requests.get('https://ml.internalpositioning.com/location?group=hack')
	data = r.json()
	payload = {}
	payload["title"] = "Some title"
	payload["link"] = "asldfkjaslfd"
	payload["description"] = "asldkfjaksldjf"
	payload["modified"] = "2016-11-19T20:01:45Z"
	payload["generator"] = "https:\/\/www.flickr.com"
	payload["items"] = []
	for user in data['users'].keys():
		try:
			foo = data['users'][user][0]['location']
			item = {}
			item['title'] = user
			item['description']= "Location: " + \
				foo.split('=')[0] + "<br>Last seen: " + \
				data['users'][user][0]['time'].split(".")[0] + \
				"<br><img src=\"/%s\" width=\"180\" height=\"240\" alt=\"\" \/>" % (user + ".jpg")
			rSeed = hash(data['users'][user][0]['time'])
			random.seed(rSeed)				
			item['latitude'] = str(float(foo.split('=')[1]) + random.random()/50000)
			item['longitude'] = str(float(foo.split('=')[2]) + random.random()/50000)
			payload['items'].append(item)
		except:
			pass
	print(data)
	return payload

while True:
	time.sleep(3)
	with open("data.json","w") as f:
		f.write(json.dumps(getJSON()))

