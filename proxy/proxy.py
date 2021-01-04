#!/usr/bin/env python3
from flask import Flask, abort, request, redirect, jsonify
import json
from flask import render_template
import requests
from datetime import datetime
import urllib.request

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
    try:
        code = urllib.request.urlopen(url).getcode()
        if code == 200:
            print('Login site exists')
            return redirect(url)
    except:
        print('Login does not exist')
        return "fail"


@app.route('/logout')
def logout():
    url = "http://127.0.0.1:5000/logout"
    return redirect(url)

@app.route("/stats", methods = ["GET"])
def stats():
    try:
        resp = requests.get("http://127.0.0.1:5000/stats")
        stats = {}
        if(resp.status_code == 200):
            stats = resp.json()
            return stats
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500

@app.route("/stats/views/<user>", methods = ['PUT', 'PATCH'])
def num_views(user):
    try:
        resp = requests.put("http://127.0.0.1:5000/stats/views/" + user)
        num_v = {}
        if(resp.status_code == 200):
            num_v = resp.json()
            return num_v
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500

@app.route("/stats/questions/<user>", methods = ['PUT', 'PATCH'])
def num_questions_(user):
    try:
        resp = requests.put("http://127.0.0.1:5000/stats/questions/" + user)
        num_q = {}
        if(resp.status_code == 200):
            num_q = resp.json()
            return num_q
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500

@app.route("/stats/answers/<user>", methods = ['PUT', 'PATCH'])
def num_answers(user):
    try:
        resp = requests.put("http://127.0.0.1:5000/stats/answers/" + user)
        num_a = {}
        if(resp.status_code == 200):
            num_a = resp.json()
            return num_a
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500

@app.route("/stats/videos_reg/<user>", methods = ['PUT', 'PATCH'])
def num_videos_reg(user):
    try:
        resp = requests.put("http://127.0.0.1:5000/stats/videos_reg/" + user)
        num_vd = {}
        if(resp.status_code == 200):
            num_vd = resp.json()
            return num_vd
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500

# VIDEOS process

@app.route("/logged_In/<id>/<name>", methods = ["GET"])
def logged_In(id, name):
    try:
        resp = requests.get("http://127.0.0.1:5000/role/"+ id)
        user = {}
        if(resp.status_code == 200):
            user = resp.json()
            return render_template("videoListing.html", id = id, name = name, role = user["User"]["role"])
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500

@app.route("/logged_In/<user>/videoPage.html/<id>/<name>")
def logged_In_vid(user, id, name):
    try:
        return render_template("videoPage.html", user = user, name = name, id = id)
    except:
        print('Web site does not exist')
        return "fail"

@app.route("/logged_In/<id>/logs/show", methods = ["GET"])
def go_to_logs(id):
    try:
        resp = requests.get("http://127.0.0.1:5000/role/"+ id)
        user = {}
        if(resp.status_code == 200):
            user = resp.json()
            return render_template("logs.html", role = user["User"]["role"])
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500

@app.route("/logged_In/<id>/stats", methods = ["GET"])
def go_to_stats(id):
    try:
        resp = requests.get("http://127.0.0.1:5000/role/"+ id)
        user = {}
        if(resp.status_code == 200):
            user = resp.json()
            return render_template("stats.html", role = user["User"]["role"])
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500

@app.route("/videos", methods = ["GET"])
def videos():
    try:
        resp = requests.get("http://127.0.0.1:8000/videos")
        videos = {}
        if(resp.status_code == 200):
            videos = resp.json()
            return videos
        else:
            abort(resp.status_code)
    except:
        try:
            resp = requests.get("http://127.0.0.1:3000/videos")
            videos = {}
            if(resp.status_code == 200):
                videos = resp.json()
                return videos
            else:
                abort(resp.status_code)
        except:
            return jsonify("failure"), 500

@app.route("/videos", methods = ["POST"])
def new_video():
    try:
        j = request.get_json()
        resp = requests.post("http://127.0.0.1:8000/videos", json = j)
        if(resp.status_code == 200):
            videos = resp.json()
            return str(resp.status_code)
        else:
            abort(resp.status_code)
    except:
        try:
            j = request.get_json()
            resp = requests.post("http://127.0.0.1:3000/videos", json = j)
            if(resp.status_code == 200):
                videos = resp.json()
                return str(resp.status_code)
            else:
                abort(resp.status_code)
        except:
            return jsonify("failure"), 500

@app.route("/videos/<id>", methods = ["GET"])
def video(id):
    try:
        resp = requests.get("http://127.0.0.1:8000/videos/" + id)
        video = {}
        if(resp.status_code == 200):
            video = resp.json()
            return video
        else:
            abort(resp.status_code)
    except:
        try:
            resp = requests.get("http://127.0.0.1:3000/videos/" + id)
            video = {}
            if(resp.status_code == 200):
                video = resp.json()
                return video
            else:
                abort(resp.status_code)
        except:
            return jsonify("failure"), 500

@app.route("/videos/<id>/views", methods = ['PUT', 'PATCH'])
def video_views(id):
    try:
        resp = requests.put("http://127.0.0.1:8000/videos/" + id + "/views")
        num_vw = {}
        if(resp.status_code == 200):
            num_vw = resp.json()
            return num_vw
        else:
            abort(resp.status_code)
    except:
        try:
            resp = requests.put("http://127.0.0.1:3000/videos/" + id + "/views")
            num_vw = {}
            if(resp.status_code == 200):
                num_vw = resp.json()
                return num_vw
            else:
                abort(resp.status_code)
        except:
            return jsonify("failure"), 500

@app.route("/videos/<id>/questions", methods = ['PUT', 'PATCH'])
def num_questions(id,):
    try:
        resp = requests.put("http://127.0.0.1:8000/videos/" + id + "/questions")
        num_q = {}
        if(resp.status_code == 200):
            num_q = resp.json()
            return num_q
        else:
            abort(resp.status_code)
    except:
        try:
            resp = requests.put("http://127.0.0.1:3000/videos/" + id + "/questions")
            num_q = {}
            if(resp.status_code == 200):
                num_q = resp.json()
                return num_q
            else:
                abort(resp.status_code)
        except:
            return jsonify("failure"), 500

# QA process

@app.route("/QA", methods = ["POST"])
def new_question():
    try:
        j = request.get_json()
        resp = requests.post("http://127.0.0.1:7000/QA", json = j)
        if(resp.status_code == 200):
            return str(resp.status_code)
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500

@app.route("/QA/<v_id>", methods = ["GET"])
def questions(v_id):
    try:
        resp = requests.get("http://127.0.0.1:7000/QA/"+ v_id)
        questions = {}
        if(resp.status_code == 200):
            questions = resp.json()
            return questions
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500

@app.route("/QA/<v_id>/<q_id>", methods = ["GET"])
def question(v_id, q_id):
    try:
        resp = requests.get("http://127.0.0.1:7000/QA/"+ v_id + '/' + q_id)
        question = {}
        if(resp.status_code == 200):
            question = resp.json()
            return question
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500

@app.route("/Answers", methods = ["POST"])
def new_answer():
    try:
        j = request.get_json()
        resp = requests.post("http://127.0.0.1:7000/Answers", json = j)
        if(resp.status_code == 200):
            return str(resp.status_code)
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500

@app.route("/Answers/<id>", methods = ["GET"])
def answers_qid(id):
    try:
        resp = requests.get("http://127.0.0.1:7000/Answers/" + id)
        answers = {}
        if(resp.status_code == 200):
            answers = resp.json()
            return answers
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500

# LOGS process

@app.route("/logs/DataCreation", methods = ["GET"])
def logs_dc():
    try:
        resp = requests.get("http://127.0.0.1:6000/logs/DataCreation")
        logs = {}
        if(resp.status_code == 200):
            logs = resp.json()
            return logs
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500

@app.route("/logs/Events", methods = ["GET"])
def logs_events():
    try:
        resp = requests.get("http://127.0.0.1:6000/logs/Events")
        logs = {}
        if(resp.status_code == 200):
            logs = resp.json()
            return logs
        else:
            abort(resp.status_code)
    except:
        return jsonify("failure"), 500


@app.route("/")
def index():
    return render_template('appPage.html', loggedIn = False)

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=4000, debug=True)