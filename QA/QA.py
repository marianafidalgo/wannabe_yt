#!/usr/bin/env python3
from flask import Flask, abort, request,  redirect, url_for
from QA_DB import *
from time import sleep
app = Flask(__name__)


@app.route("/logout")
def logout():
    print("log1")
    return redirect('http://127.0.0.1:7000/logout')


@app.route("/QA", methods=['GET'])
def returnsQAJSON():
    print(listQADICT())
    return {"QA": listQADICT()}

@app.route("/Answers/<id>", methods=['GET'])
def returnsAJSON(id):
    print(listAnswersDICT(id))
    return {"Answers": listAnswersDICT(id)}

@app.route("/API/videos/<int:id>/")
def returnSingleQJSON(id):
    try:
        v = getQDICT(id)
        return v
    except:
        abort(404)


@app.route("/QA", methods=['POST'])
def createQuestion():
    sleep(0.1)
    j = request.get_json()
    print (type(j))
    #if(getQuestion(j["url"]) is None):
    ret = False
    try:
        print(j["question"])
        ret = newQuestion(j["time"], j["question"])
    except:
        abort(400)
        #the arguments were incorrect
    if ret:
        return {"id": ret}
    else:
        abort(409)
    # else:
    #     print("Video already exists")
    #if there is an error return ERROR 409

@app.route("/Answers", methods=['POST'])
def createAnswers():
    sleep(0.1)
    j = request.get_json()
    print (j)
    #if(getQuestion(j["url"]) is None):
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
    # else:
    #     print("Video already exists")
    #if there is an error return ERROR 409

@app.route("/QA/<int:id>", methods=['PUT', 'PATCH'])
def newQSum(id):
    try:
        return {"id":id, "num_questions": newQuestionSum(id)}
    except:
        abort(404)

# @app.route("/")
# def index():
#     return app.send_static_file('videoListing.html')

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=7000, debug=True)