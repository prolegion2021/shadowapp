# ShadowlerApp
## A Python script that uses the PRAW library to interact with the Reddit API, and the Flask library to create a web application that checks whether a Reddit user is shadowbanned.

### API Endpoint:
http://localhost:5000/ - for local usage
```Bash
http://localhost:5000/shadowban/{username}
```
### Method:
```Bash
GET
```
### Description:
This endpoint returns whether the provided username is shadowbanned on Reddit.

#### Request Parameters:
username (string): the username of the Reddit user to check for shadowban.
full (int): if set to 1, returns additional information about the user (join date, post karma, comment karma, and whether they have a verified email). Default is 0.
### Response:
#### 200 OK: If the request is successful.
#### 400 Bad Request: If the provided username is invalid.
#### 401 Unauthorized: If invalid Reddit client ID or secret is provided.
#### 405 Method Not Allowed: If a non-GET request is made to the endpoint.
#### 500 Internal Server Error: If an error occurs while processing the request.
### Response Format:

#### If the user is not shadowbanned:

```Bash
{
    "is_shadowbanned": false,
    "username": {username},
    "join_date": {join_date},
    "post_karma": {post_karma},
    "comment_karma": {comment_karma},
    "verified_mail": {verified_mail}
}
```
#### If the user is shadowbanned:

```Bash
{
    "is_shadowbanned": true
}
```
Note: The values in curly braces {} will be replaced by the actual values for the user.

### Example Request:

#### GET /shadowban/exampleuser?full=1

#### Example Response:
```Bash
{
    "is_shadowbanned": false,
    "username": "exampleuser",
    "join_date": "2022-03-01 12:30:45",
    "post_karma": 1000,
    "comment_karma": 2000,
    "verified_mail": true
}
```
Usage:
### Install the necessary dependencies by running 
#### pip install -r requirements.txt.

### Set the following environment variables:

#### CLIENT_ID: Reddit app client ID

#### CLIENT_SECRET: Reddit app client secret

#### username: Reddit username(for reddit script user-agent)

#### Run the script with python app.py.
#### Run the script with python unit_test_app.py.

### Additional Information

The script uses basic logging to log messages to the console.

The script includes input validation and sanitization to ensure that the provided username is valid.

The script uses the NotFound exception from the prawcore library to check whether a user is shadowbanned.

If you have any issues please open a issue on GitHub.
