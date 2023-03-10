import json
import re
from flask import Flask, jsonify, request, render_template
import requests
import datetime
from waitress import serve
# from flask_cors import CORS, cross_origin

gurl = {'url': "https://www.reddit.com/r/DesignPorn/comments/10gmp90/saint_pete_beach_public_library/", 'xpath': "//*[@id='upvote-button-t3_10gmp90']"}
username = 'TrainingPick3936'
version = 'v1.0.0'
app = Flask(__name__)
USER_AGENT = f'ShadowlerApp:{version} (by /u/{username})'
headers = {
    "User-Agent": USER_AGENT,
}

def validate_username(username):
    if not re.match("^[A-Za-z0-9_-]{3,20}$", username):
        raise ValueError("Invalid username")
    return username


@app.route('/shadowban/<username>', methods=['GET'])
def reddit_user(username):
    if request.method != 'GET':
        return None, 405
    try:
        username = validate_username(username)
    except ValueError as e:
        return jsonify(error=str(e)), 400
    try:
        base_url = "https://old.reddit.com/user/"
        response = requests.get(base_url + username + "/about.json", headers=headers)
        full = request.args.get("full")
        if response.status_code == 404:
            return jsonify(is_shadowbanned=True)
        if response.status_code == 200:
            data = response.json()
            if full == str(1):
                return jsonify(is_shadowbanned=False,
                               username=username,
                               join_date=datetime.datetime.utcfromtimestamp(data['data']['created_utc']).strftime('%Y-%m-%d %H:%M:%S'),
                               post_karma=data['data']['link_karma'],
                               comment_karma=data['data']['comment_karma'],
                               verified_mail=data['data']['has_verified_email'])
            else:
                return jsonify(is_shadowbanned=False)
    except Exception as e:
        return jsonify(error="Internal Server Error"), 500

@app.route('/')
def index():
    return render_template('index.html')


# create route for /script Response format text
@app.route('/script', methods=['GET'])
def script():
    # jsonResp = {'url': "https://old.reddit.com/"}
    # print(jsonify(jsonResp))
    return jsonify(gurl)

# @app.route('/script_update/<url>', methods=['POST'])
# def create_url(url):
#     # update key value in dictionary
#     gurl['url'] = url
#     return "DOne"
# create route for post request update url in gurl
@app.route('/script_update', methods=['POST'])
def create_url():
    # update key value in dictionary
    gurl['url'] = request.form['url']
    gurl['xpath'] = request.form['xpath']
    return jsonify(gurl)
# example post request update url and xpath in gurl
# {
#     "url": "https://old.reddit.com/",
#     "xpath": "//*[@id='upvote-button-t3_10gmp90']"
# }


if __name__ == '__main__':
    print("Starting Prod API 2000 server...")
    # CORS(app)
    serve(app, host="0.0.0.0", port=5000)
    # app.run(debug=False)