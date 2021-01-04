#!/usr/bin/env python3
from flask import Flask, abort, request,  redirect, url_for
from Video_DB import *
from time import sleep
from flask import render_template
app = Flask(__name__)


@app.route("/videos", methods=['GET'])
def returnsVideosJSON():
    return {"videos": listVideosDICT()}


@app.route("/videos/<id>", methods = ["GET"])
def returnSingleVideoJSON(id):
    try:
        v = getVideoDICT(id)
        return v
    except:
        abort(404)

@app.route("/videos", methods=['POST'])
def createNewVideo():
    j = request.get_json()
    ret = False
    try:
        ret = newVideo(j["user"],j["description"], j["url"])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)


@app.route("/videos/<int:id>/views", methods=['PUT', 'PATCH'])
def newView(id):
    try:
        return {"id":id, "views": newVideoView(id)}
    except:
        abort(404)

@app.route("/videos/<int:id>/questions", methods=['PUT', 'PATCH'])
def newQSum(id):
    try:
        return {"id":id, "num_questions": newQuestionSum(id)}
    except:
        abort(404)

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=3000, debug=True)