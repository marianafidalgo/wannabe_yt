#!/usr/bin/env python3
from flask import Flask, abort, request, redirect, jsonify
import json
from flask import render_template
import requests
from datetime import datetime

app = Flask(__name__)

@app.before_request
def log_request_info():
    method = request.method
    if(method == 'POST'):
        data_type = request.content_type
        content = request.get_json()
        timestamp = str(datetime.now())
        data = {"data_type": data_type, "content": content, "timestamp": timestamp, "user": content["user"]}
        requests.post("http://127.0.0.1:6000/logs/DataCreation", json = data)
    else:
        timestamp = str(datetime.now())
        url = request.url
        data = {"timestamp": timestamp, "url": url}
        requests.post("http://127.0.0.1:6000/logs/Events", json = data)

# USER process

@app.route("/login")
def login():
    url = "http://127.0.0.1:5000"
    return redirect(url)

@app.route('/logout')
def logout():
    url = "http://127.0.0.1:5000/logout"
    return redirect(url)

@app.route("/stats", methods = ["GET"])
def stats():
    resp = requests.get("http://127.0.0.1:5000/stats")
    stats = {}
    if(resp.status_code == 200):
        stats = resp.json()
    return stats

@app.route("/stats/views/<user>", methods = ['PUT', 'PATCH'])
def num_views(user):
    resp = requests.put("http://127.0.0.1:5000/stats/views/" + user)
    num_v = {}
    if(resp.status_code == 200):
        num_v = resp.json()
    return num_v

@app.route("/stats/questions/<user>", methods = ['PUT', 'PATCH'])
def num_questions_(user):
    resp = requests.put("http://127.0.0.1:5000/stats/questions/" + user)
    num_q = {}
    if(resp.status_code == 200):
        num_q = resp.json()
    return num_q

@app.route("/stats/answers/<user>", methods = ['PUT', 'PATCH'])
def num_answers(user):
    resp = requests.put("http://127.0.0.1:5000/stats/answers/" + user)
    num_a = {}
    if(resp.status_code == 200):
        num_a = resp.json()
    return num_a

@app.route("/stats/videos_reg/<user>", methods = ['PUT', 'PATCH'])
def num_videos_reg(user):
    resp = requests.put("http://127.0.0.1:5000/stats/videos_reg/" + user)
    num_vd = {}
    if(resp.status_code == 200):
        num_vd = resp.json()
    return num_vd

# VIDEOS process

@app.route("/logged_In/<id>/<name>", methods = ["GET"])
def logged_In(id, name):
    resp = requests.get("http://127.0.0.1:5000/role/"+ id)
    user = {}
    if(resp.status_code == 200):
        user = resp.json()
    return render_template("videoListing.html", id = id, name = name, role = user["User"][0]["role"])

@app.route("/logged_In/<user>/videoPage.html/<id>/<name>", methods = ["GET"])
def logged_In_vid(user, id, name):
    return render_template("videoPage.html", user = user, name = name, id = id)

@app.route("/logged_In/<id>/logs/show", methods = ["GET"])
def go_to_logs(id):
    resp = requests.get("http://127.0.0.1:5000/role/"+ id)
    user = {}
    if(resp.status_code == 200):
        user = resp.json()
    return render_template("logs.html", role = user["User"][0]["role"])

@app.route("/logged_In/<id>/stats", methods = ["GET"])
def go_to_stats(id):
    resp = requests.get("http://127.0.0.1:5000/role/"+ id)
    user = {}
    if(resp.status_code == 200):
        user = resp.json()
    return render_template("stats.html", role = user["User"][0]["role"])

@app.route("/videos", methods = ["GET"])
def videos():
    resp = requests.get("http://127.0.0.1:8000/videos")
    videos = {}
    if(resp.status_code == 200):
        videos = resp.json()
    return videos

@app.route("/videos", methods = ["POST"])
def new_video():
    j = request.get_json()
    resp = requests.post("http://127.0.0.1:8000/videos", json = j)
    return str(resp.status_code)

@app.route("/videos/<id>", methods = ["GET"])
def video(id):
    resp = requests.get("http://127.0.0.1:8000/videos/" + id)
    video = {}
    if(resp.status_code == 200):
        video = resp.json()
    return video

@app.route("/videos/<id>/views", methods = ['PUT', 'PATCH'])
def video_views(id):
    resp = requests.put("http://127.0.0.1:8000/videos/" + id + "/views")
    num_vw = {}
    if(resp.status_code == 200):
        num_vw = resp.json()
    return num_vw

@app.route("/videos/<id>/questions", methods = ['PUT', 'PATCH'])
def num_questions(id,):
    resp = requests.put("http://127.0.0.1:8000/videos/" + id + "/questions")
    num_q = {}
    if(resp.status_code == 200):
        num_q = resp.json()
    return num_q

# QA process

@app.route("/QA", methods = ["POST"])
def new_question():
    j = request.get_json()
    resp = requests.post("http://127.0.0.1:7000/QA", json = j)
    return str(resp.status_code)

@app.route("/QA/<v_id>", methods = ["GET"])
def questions(v_id):
    resp = requests.get("http://127.0.0.1:7000/QA/"+ v_id)
    questions = {}
    if(resp.status_code == 200):
        questions = resp.json()
    return questions

@app.route("/QA/<v_id>/<q_id>", methods = ["GET"])
def question(v_id, q_id):
    resp = requests.get("http://127.0.0.1:7000/QA/"+ v_id + '/' + q_id)
    question = {}
    if(resp.status_code == 200):
        question = resp.json()
    return question

@app.route("/Answers", methods = ["POST"])
def new_answer():
    j = request.get_json()
    resp = requests.post("http://127.0.0.1:7000/Answers", json = j)
    return str(resp.status_code)

@app.route("/Answers/<id>", methods = ["GET"])
def answers_qid(id):
    resp = requests.get("http://127.0.0.1:7000/Answers/" + id)
    answers = {}
    if(resp.status_code == 200):
        answers = resp.json()
    return answers

# LOGS process

@app.route("/logs/DataCreation", methods = ["GET"])
def logs_dc():
    resp = requests.get("http://127.0.0.1:6000/logs/DataCreation")
    logs = {}
    if(resp.status_code == 200):
        logs = resp.json()
    return logs

@app.route("/logs/Events", methods = ["GET"])
def logs_events():
    resp = requests.get("http://127.0.0.1:6000/logs/Events")
    logs = {}
    if(resp.status_code == 200):
        logs = resp.json()
    return logs


@app.route("/")
def index():
    return render_template('appPage.html', loggedIn = False)

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=4000, debug=True)