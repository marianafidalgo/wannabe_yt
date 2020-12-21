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
    # print(fenix_blueprint.session.authorized)
    # print("Access token: "+ str(fenix_blueprint.session.access_token))
    # return render_template("appPage.html", loggedIn = fenix_blueprint.session.authorized)
    if fenix_blueprint.session.authorized == False:
        #if not logged in browser is redirected to login page (in this case FENIX handled the login)
        return redirect(url_for('fenix-example.login'))
    else:
        #if the user is authenticated then a request to FENIX is made
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
        #resp contains the response made to /api/fenix/vi/person (information about current user)
        data = resp.json()
        #send to DB
        print("hey bd")
        print(getUser(data["username"]))
        if(getUser(data["username"]) is None):
            ret = False
            try:
                if(data["username"] == "ist187077" or data["username"] == "ist187074"):
                    print("Hello admin")
                    ret = newUser(data["username"],data["name"], "admin")
                else:
                    print("Hello user")
                    ret = newUser(data["username"],data["name"], "user")
            except:
                abort(400)
        #send to proxy!!!
        #return redirect(url_for('user', id =data['username'], name=data['name']))
        url = "http://127.0.0.1:4000/logged_In/"+ data['username']+'/'+data['name']
        print(url)
        return redirect(url)


@app.route('/user/<id>/<name>',methods=['GET','POST'])
def user(id, name):
    paras = json.dumps({"id":id,"name":name})
    response = requests.post('http://127.0.0.1:4000/user_proxy',data=paras)
    print(response.status_code)
    if(response.status_code == 200 ):
        return redirect('http://127.0.0.1:4000/u_VQA')
    else:
        return "Error"



@app.route('/logout')
def logout():
    # this clears all server information about the access token of this connection
    res = str(session.items())
    print(res)
    session.clear()
    res = str(session.items())
    print(res)
    # when the browser is redirected to home page it is not logged in anymore
    return redirect("http://127.0.0.1:4000/")


@app.route('/private')
def private_page():
    #this page can only be accessed by a authenticated user

    # verification of the user is  logged in
    if fenix_blueprint.session.authorized == False:
        #if not logged in browser is redirected to login page (in this case FENIX handled the login)
        return redirect(url_for("fenix-example.login"))
    else:
        #if the user is authenticated then a request to FENIX is made
        resp = fenix_blueprint.session.get("/api/fenix/v1/person/")
        #resp contains the response made to /api/fenix/vi/person (information about current user)
        data = resp.json()
        print(resp.json())
        return render_template("privPage.html", username=data['username'], name=data['name'])



if __name__ == '__main__':
    app.run(debug=True)
