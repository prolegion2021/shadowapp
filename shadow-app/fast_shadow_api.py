import uvicorn as uvicorn
from fastapi import FastAPI, HTTPException
import re
import requests
import datetime
import env

app = FastAPI()
USER_AGENT = f'ShadowlerApp:{env.version} (by /u/{env.username})'
headers = {
    "User-Agent": USER_AGENT,
}

# Input validation and sanitization
def validate_username(username: str):
    if not re.match("^[A-Za-z0-9_-]{3,20}$", username):
        raise ValueError("Invalid username")
    return username

@app.get("/shadowban/{username}")
def reddit_user(username: str, full: int = 0):
    try:
        username = validate_username(username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        base_url = "https://old.reddit.com/user/"
        response = requests.get(base_url + username + "/about.json", headers=headers)
        if response.status_code == 404:
            return {"is_shadowbanned": True}
        if response.status_code == 200:
            data = response.json()
            if full == 1:
                return {
                    "is_shadowbanned": False,
                    "username": username,
                    "join_date": datetime.datetime.utcfromtimestamp(data['data']['created_utc']).strftime('%Y-%m-%d %H:%M:%S'),
                    "post_karma": data['data']['link_karma'],
                    "comment_karma": data['data']['comment_karma'],
                    "verified_mail": data['data']['has_verified_email']
                }
            else:
                return {"is_shadowbanned": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/")
def index():
    return {"message": "Hello World"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
