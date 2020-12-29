#!/usr/bin/env python3
from flask import Flask, abort, request,  redirect, url_for
from logs_DB import *
import json
from time import sleep
app = Flask(__name__)

@app.route("/logs/DC", methods=['POST'])
def createDC():
    sleep(0.1)
    j = request.get_json()
    print (j)
    ret = False
    try:
        print(j["data_type"])
        content = json.dumps(j["content"])
        ret = newDC(j["data_type"], content, j["timestamp"], j["user"])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)

@app.route("/logs/Events", methods=['POST'])
def createEvent():
    sleep(0.1)
    j = request.get_json()
    print (j)
    ret = False
    try:
        print(j["timestamp"])
        ret = newEvent(j["timestamp"], j["url"])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)

@app.route("/logs/DataCreation", methods=['GET'])
def returnsDC():
    print(listDCDICT())
    return {"DataCreation": listDCDICT()}

@app.route("/logs/Events", methods=['GET'])
def returnsEvents():
    print("hereeee")
    print(listEventsDICT())
    return {"Events": listEventsDICT()}

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=6000, debug=True)