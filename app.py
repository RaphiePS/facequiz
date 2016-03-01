from flask import Flask, redirect, request, session, render_template, jsonify, Response
import json
import requests
import binascii
import os
import random

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]

# Global state lol
tokens = dict()
active_quizzes = dict()
users = dict()

def slackRequest(method, params={}):
    r = requests.post("https://slack.com/api/" + method, params=params)
    return r.json()

@app.route("/")
def index():
	# I'm so sorry
	return '<a href="https://slack.com/oauth/authorize?scope=commands,users:read&client_id=2323751764.23663576083"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x"></a> Talk to @raphael if this breaks!'

@app.route("/oauth")
def oauth():
    code = request.args.get("code")
    j = slackRequest("oauth.access", {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "state": binascii.b2a_hex(os.urandom(15))
    })
    print j
    if j["ok"] != True or "access_token" not in j:
        return "Error logging in :("
    tokens[j["team_id"]] = j["access_token"]
    return "All set up, now just try /facequiz in your Slack!"


@app.route("/facequiz", methods=["GET", "POST"])
def facequiz():
	team_id = request.form.get("team_id")
	text = request.form.get("text").strip()
	user_id = request.form.get("user_id")
	token = tokens[team_id]
	if user_id in active_quizzes:
		answer = active_quizzes[user_id]
		del active_quizzes[user_id]
		if text.lower() == answer.lower():
			return "Hooray, you got it - that's *%s*! Run `/facequiz` again for a new quiz!" % answer
		else:
			return "Whoops, that's actually *%s*. Run `/facequiz` again for a new quiz!" % answer
	if team_id not in users:
		users[team_id] = slackRequest("users.list", {
			"token": token
		})
	while True:
		pick = random.choice(users[team_id]["members"])
		if "first_name" in pick["profile"]:
			break
	active_quizzes[user_id] = pick["profile"]["first_name"].strip()
	res = json.dumps({
	    "text": "What's this person's first name? Respond with `/facequiz [name]`!",
	    "attachments": [
	        {
	            "fallback": "(Image of the person).",
	            "image_url": pick["profile"]["image_192"]
	        }
	    ]
	})
	return Response(res, mimetype="application/json")

if __name__ == "__main__":
	app.run("0.0.0.0", port=5000)