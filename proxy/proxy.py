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

@app.route("/logged_In/<id_user>/videoPage.html/<id>/", methods = ["GET"])
def logged_In_vid(id_user, id):
    return render_template("videoPage.html", id = id)

@app.route("/videos", methods = ["GET"])
def videos():
    resp = requests.get("http://127.0.0.1:8000/API/videos/")
    videos = {}
    if(resp.status_code == 200):
        videos = resp.json()
    return videos

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


@app.route("/")
def index():
    return render_template('appPage.html', loggedIn = False)

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=4000, debug=True)