#!/usr/bin/env python3
from flask import Flask
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import json
from flask import jsonify, url_for, abort
from flask import session

from user_DB import *

import requests

#necessary so that our server does not need https
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Click details do get the Client Id and Client Secret and fill the next constructor
app = Flask(__name__)
app.secret_key = "supersekrit"  # Replace this with your own secret!
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
fenix_blueprint = OAuth2ConsumerBlueprint(
    "fenix-example", __name__,
    # this value should be retrived from the FENIX OAuth page
    client_id="1695915081466092",
    # this value should be retrived from the FENIX OAuth page
    client_secret="vmumAkyvslJjcTB7J0hoeqvrBqi9drd7JOsxBbkPtozV20XeGtHYeMFMISZnYz3IKW0oRxmFCE0LLSfLf0BVzQ==",
    # do not change next lines
    base_url="https://fenix.tecnico.ulisboa.pt/",
    token_url="https://fenix.tecnico.ulisboa.pt/oauth/access_token",
    authorization_url="https://fenix.tecnico.ulisboa.pt/oauth/userdialog",
)

app.register_blueprint(fenix_blueprint)



@app.route('/')
def home_page():
    # The access token is generated everytime the user authenticates into FENIX
    if fenix_blueprint.session.authorized == False:
        #if not logged in browser is redirected to login page
        return redirect(url_for('fenix-example.login'))
    else:
        #if the user is authenticated then a request to FENIX is made
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
        #resp contains the response made to /api/fenix/vi/person (information about current user)
        data = resp.json()
        #send to DB
       # try:
        if(getUser(data["username"]) is None):
            ret = False
            try:
                if(data["username"] == "ist187077" or data["username"] == "ist187074"):
                    ret = newUser(data["username"],data["name"], "admin")
                else:
                    ret = newUser(data["username"],data["name"], "user")
            except:
                abort(400)
        #send to proxy!!!
        url = "http://127.0.0.1:4000/logged_In/"+ data['username']+'/'+data['name']
        return redirect(url)
        # except:
        #     None

@app.route('/user/<id>/<name>',methods=['GET','POST'])
def user(id, name):
    paras = json.dumps({"id":id,"name":name})
    response = requests.post('http://127.0.0.1:4000/user_proxy',data=paras)
    if(response.status_code == 200 ):
        return redirect('http://127.0.0.1:4000/u_VQA')
    else:
        return "Error"

@app.route('/logout')
def logout():
    try:
        del fenix_blueprint.token
    except:
        pass
    return redirect("http://127.0.0.1:4000/")

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
    try:
        return {"user":user, "videos_reg": newVideoReg(user)}
    except:
        abort(404)

@app.route("/role/<id>", methods=['GET'])
def returnRole(id):
    return {"User": listUDICT(id)}


@app.route("/stats", methods=['GET'])
def returnsStats():
    return {"Users": listUsersDICT()}


if __name__ == '__main__':
    app.run(debug=True)
