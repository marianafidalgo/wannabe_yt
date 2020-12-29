#!/usr/bin/env python3
from flask import Flask, abort, request,  redirect, url_for
from logs_DB import *
from time import sleep
app = Flask(__name__)

@app.route("/logs", methods=['POST'])
def createLog():
    sleep(0.1)
    j = request.get_json()
    print (type(j))
    ret = False
    try:
        print(j["content"])
        ret = newLog(j["data_type"], j["content"], j["timestamp"], j["user"])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)

@app.route("/logs/DataCreation", methods=['GET'])
def returnsLogs():
    print(listLogsDICT())
    return {"DataCreation": listLogsDICT()}

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=6000, debug=True)