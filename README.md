# FaceQuiz

You've just started at a new job, and if you're anything like me, it's going to be a huge struggle to learn everyone's name. Fear not! FaceQuiz helps you match faces to names from the comfort of Slack. Here's what it looks like: ![Image of Usage](http://i.imgur.com/Al2HGMY.png)  

You can add it to your Slack [here](https://facequiz.raphieps.com) but *beware*: this is a ridiculous, nowhere-near-production-ready hack. The main issue is that everything is stored in memory, so if the server dies, there goes FaceQuiz. I'm working on adding real database support, see todos below.

# Getting it Running
First register a [Slack application](https://api.slack.com/slack-apps), then run the following:

```shell
pip install -r requirements.txt # virtualenv, hopefully
export CLIENT_ID="client id from slack"
export CLIENT_SECRET="client secret from slack"
export SECRET_KEY="a secret key for flask"
export REDIRECT_URI="a redirect url you gave to slack, I did https://facequiz.raphieps.com/oauth"
python app.py
```

The app runs on port `5000`, but if you want to get fancy and forward from port 80, here's my nginx config:

```
server {
        listen 80;
        server_name facequiz.raphieps.com;
        location ~ ^/ {
                proxy_pass http://localhost:5000;
        }
}
```

# Todos

As alluded to, this is ridiculously crappy right now. Here's what I'd like to add soon:  
- [ ] An actual database, instead of janky global variables  
- [ ] A better interface - it's tiresome to keep typing `/facequiz`  
- [ ] Filtering for people without profile pictures  
- [ ] Ability to do something like `/facequiz #engineering` and get quizzed only on people in that channel  
- [ ] General code cleanup 
- [ ] Make a nice landing page 