#!/usr/bin/env python3
from flask import Flask, abort, request, redirect, jsonify
import json
from flask import render_template
import requests

app = Flask(__name__)

user_id = ''
user_name = ''


@app.route("/login")
def login():
    url = "http://127.0.0.1:5000"
    print(url)
    return redirect(url)

@app.route('/logout')
def logout():
    url = "http://127.0.0.1:4000/"
    return redirect(url)

@app.route("/logged_In/<id>/<name>", methods = ["GET"])
def logged_In(id, name):
    return render_template("videoListing.html", id = id, name = name)

@app.route("/logged_In/<id_user>/videoPage.html/<name>/<id>", methods = ["GET"])
def logged_In_vid(id_user, name, id):
    return render_template("videoPage.html", user = id_user, name = name, id = id)

@app.route("/videos", methods = ["GET"])
def videos():
    resp = requests.get("http://127.0.0.1:8000/API/videos/")
    videos = {}
    if(resp.status_code == 200):
        videos = resp.json()
    return videos

@app.route("/videos", methods = ["POST"])
def new_video():
    j = request.get_json()
    resp = requests.post("http://127.0.0.1:8000/API/videos/", json = j)
    if(resp.status_code == 200):
        print(j)
    return j

@app.route("/videos/<id>/", methods = ["GET"])
def video(id):
    resp = requests.get("http://127.0.0.1:8000/API/videos/" + id)
    video = {}
    if(resp.status_code == 200):
        video = resp.json()
    return video

@app.route("/videos/<id>/views", methods = ['PUT', 'PATCH'])
def video_views(id):
    resp = requests.put("http://127.0.0.1:8000/API/videos/" + id + "/views")
    video = {}
    if(resp.status_code == 200):
        video = resp.json()
    return video

@app.route("/QA", methods = ["POST"])
def new_question():
    j = request.get_json()
    print(j)
    resp = requests.post("http://127.0.0.1:7000/QA/", json = j)
    if(resp.status_code == 200):
        print(j)
    return j

@app.route("/QA", methods = ["GET"])
def questions():
    resp = requests.get("http://127.0.0.1:7000/QA")
    questions = {}
    if(resp.status_code == 200):
        questions = resp.json()
    print(questions)
    return questions

@app.route("/Answers", methods = ["POST"])
def new_answer():
    j = request.get_json()
    print(j)
    resp = requests.post("http://127.0.0.1:7000/QA/", json = j)
    if(resp.status_code == 200):
        print(j)
    return j

@app.route("/Answers", methods = ["GET"])
def answers():
    resp = requests.get("http://127.0.0.1:7000/Answers")
    answers = {}
    if(resp.status_code == 200):
        answers = resp.json()
    print(answers)
    return answers

@app.route("/")
def index():
    return render_template('appPage.html', loggedIn = False)

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=4000, debug=True)