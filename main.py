import salt_utils
import socketio
import sys
import pymongo
import requests
import json

from salt_parser import Parser

sio = socketio.Client()   
#The dictionary containing the command words
data = {"Entry" : []}

try:
    configData = salt_utils.openF('config.json')
except:
    #If the client has still not been configured, the user is required to do so.
    print('The analyzer has still not been configured.')
    server = input('Please input the adress of the server.')
    db = input('Please input the adress of the database.')

    config = {
        "server": server,
        "database": db
    }

    with open('config.json', 'w') as outfile:
        json.dump(config, outfile)

#Connection to the database
dbClient = pymongo.MongoClient(configData['database'])
db = dbClient['Salt']
collection = db['extensions']

#Appends all the documents contained in the extensions collection to data
try:
    for commw in collection.find():
        data['Entry'].append(commw)
except:
    print('The Analyzer is currently unable to retrieve any command word')
    sys.exit()

#Login to the server and recuperation of a webtoken
server = configData['server']
username = input('Please input your Salt username: ')
password = input('Please input your Salt password: ')

try:   
    response = requests.post(server + '/admin/login', json={"username": username, "password": password})
    resJson = response.json()
except:
    input('Could not login to Salt\'s server')
    sys.exit()

try: 
    webtoken = resJson["token"]
except:
    input('Could not connect to your account')
    sys.exit()

@sio.on("connection")
def connect():
    print('Connected to the server')

@sio.on("parse", namespace='/analyzer') 
def parse(receiv):
    print(receiv['Command'])
    tr = Parser(receiv['Command'], data)
    tr = tr.treat()

    if(tr == False):
        pass
    elif(tr == -1):
        sio.emit('error', "Couldn't parse", namespace='/analyzer')
    else:
        #Creation of the object to be returned to the server
        robj = {}
        robj['ID'] = receiv['ID']
        robj['Command'] = tr
        result = json.dumps(robj)
        print(result)
        sio.emit('response', result, namespace='/analyzer')

sio.connect(server, headers={"auth": webtoken}, namespaces=['/analyzer'])
print(server)

sio.wait()