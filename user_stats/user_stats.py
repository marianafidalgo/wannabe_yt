#!/usr/bin/env python3
from flask import Flask, abort, request,  redirect, url_for
from user_stats_DB import *
import json
from time import sleep
app = Flask(__name__)

@app.route("/stats/user/<user>", methods=['POST'])
def newU(user):
    ret = False
    try:
        ret = newUser(user)
    except:
        abort(400)
        #the arguments were incorrect

@app.route("/stats/views/<user>", methods=['PUT', 'PATCH'])
def newV(user):
    try:
        return {"user":user, "views": newVideoView(user)}
    except:
        abort(404)

@app.route("/stats/questions/<user>", methods=['PUT', 'PATCH'])
def newQ(user):
    try:
        return {"user":user, "num_questions": newQuestion(user)}
    except:
        abort(404)

@app.route("/stats/answers/<user>", methods=['PUT', 'PATCH'])
def newA(user):
    try:
        return {"user":user, "views": newAnswer(user)}
    except:
        abort(404)

@app.route("/stats/videos_reg/<user>", methods=['PUT', 'PATCH'])
def newVideo(user):
    print(user)
    try:
        return {"user":user, "videos_reg": newVideoReg(user)}
    except:
        abort(404)


@app.route("/stats", methods=['GET'])
def returnsStats():
    print(listStatsDICT())
    return {"Stats": listStatsDICT()}


if __name__ == "__main__":
   app.run(host='127.0.0.1', port=9000, debug=True)