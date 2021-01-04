#!/usr/bin/env python3
from flask import Flask, abort, request,  redirect, url_for
from QA_DB import *
from time import sleep
app = Flask(__name__)


@app.route("/QA/<id>", methods=['GET'])
def returnsQAJSON(id):
    return {"QA": listQADICT(id)}

@app.route("/QA/<id>/<q_id>", methods=['GET'])
def returnsQuestionJSON(id, q_id):
    return {"QA": listQuestionDICT(id, q_id)}

@app.route("/Answers/<id>", methods=['GET'])
def returnsAJSON(id):
    return {"Answers": listAnswersDICT(id)}

@app.route("/QA", methods=['POST'])
def createQuestion():
    sleep(0.1)
    j = request.get_json()
    ret = False
    try:
        ret = newQuestion(j["video_id"], j["user"], j["name"], j["time"], j["question"])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)

@app.route("/Answers", methods=['POST'])
def createAnswers():
    sleep(0.1)
    j = request.get_json()
    ret = False
    try:
        ret = newAnswer(j["user"], j["name"], j["answer"], j["question"])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=7000, debug=True)