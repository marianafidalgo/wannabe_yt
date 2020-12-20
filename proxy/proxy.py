#!/usr/bin/env python3
from flask import Flask, abort, request,  redirect, jsonify
from flask import json
from flask import render_template

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
    url = "http://127.0.0.1:5000/logout"
    return redirect(url)

@app.route("/logged_In/<id>/<name>")
def logged_In(id, name):
    print(id)
    print(name)
    return render_template("videoListing.html", id = id, name = name)

# @app.route("/user_proxy", methods=['GET', 'POST'])
# def user_proxy():
#     resp = request.get_json(force=True)
#     global user_id
#     global user_name
#     user_id = resp['id']
#     print(user_id)
#     user_name = resp['name']
#     print(user_name)
#     #ver quem é a pessoa e guardar ?
#     return resp

# @app.route("/u_VQA", methods=['GET', 'POST'])
# def u_VQA():
#     print("name" + user_name)
#     url = "http://127.0.0.1:8000?" + user_name
#     print(url)
#     return redirect(url)

# @app.route("/logout")
# def logout():
#     return redirect('http://127.0.0.1:5000/logout')

@app.route("/")
def index():
    return render_template('appPage.html', loggedIn = False)

if __name__ == "__main__":
   app.run(host='127.0.0.1', port=4000, debug=True)