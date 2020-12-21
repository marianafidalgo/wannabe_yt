#!/usr/bin/env python3
from flask import Flask, abort, request,  redirect, url_for
from Video_DB import *
from time import sleep
from flask import render_template
app = Flask(__name__)


@app.route("/logout")
def logout():
    print("log1")
    return redirect('http://127.0.0.1:7000/logout')


@app.route("/API/videos/", methods=['GET'])
def returnsVideosJSON():
    return {"videos": listVideosDICT()}


@app.route("/API/videos/<int:id>/")
def returnSingleVideoJSON(id):
    try:
        v = getVideoDICT(id)
        return v
    except:
        abort(404)


@app.route("/API/videos/<json>", methods=['POST'])
def createNewVideo(json):
    sleep(0.1)
    j = json
    print (type(j))
    if(getVideo(j["url"]) is None):
        ret = False
        try:
            print(j["description"])
            ret = newVideo(j["description"], j["url"])
        except:
            abort(400)
            #the arguments were incorrect
        if ret:
            return {"id": ret}
        else:
            abort(409)
    else:
        print("Video already exists")
    #if there is an erro return ERROR 409

@app.route("/API/videos/", methods=['POST'])
def sendQA():
    j = request.get_json()
    print (type(j))
    ret = False
    try:
        print(j["description"])
        ret = newVideo(j["description"], j["url"])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)


@app.route("/API/videos/<int:id>/views", methods=['PUT', 'PATCH'])
def newView(id):
    try:
        return {"id":id, "views": newVideoView(id)}
    except:
        abort(404)


@app.route("/")
def index():
    return render_template('videoListing.html')

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=8000, debug=True)