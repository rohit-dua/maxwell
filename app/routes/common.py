from app import app, request
from app.models import User, db
import json
import bcrypt
import jwt
from datetime import datetime
from dateutil.parser import parse
from functools import wraps


def validateToken(token):
    validationObj = dict(success=False, message='',username=None)
    try:
        decodedObj = jwt.decode(token, app.configini['DEFAULT']['secret'], algorithms=['HS256'])
    except:
        validationObj[u'success'] = False
        validationObj[u'message'] = "Invalid access token"
        return validationObj
    if (datetime.now() - parse(decodedObj[u'createdAt'])).days >= 1:
        validationObj[u'success'] = False
        validationObj[u'message'] = "Token timed out. Generate new token"
        return validationObj
    validationObj[u'success'] = True
    validationObj[u'username'] = decodedObj[u'username']
    return validationObj


def checkAuth(func):
    """Checks whether token is logged in or raises error 401."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        if request.method == 'POST':
            jsonObj = request.get_json()
            token = jsonObj['token'] if 'token' in jsonObj.keys() else None
        if token == None:
            token = request.args.get('token')
        if token == None:
            return json.dumps({"status": "fail", "message": "missing token"}), 401
        validation = validateToken(token)
        if validation['success'] == False:
            return json.dumps({"status": "fail", "message": validation[u'message']}), 401
        user = User.query.filter_by(username=validation[u'username']).first()
        if user == None:
            return json.dumps({"status": "fail", "message": "no user found"}), 401
        userData = dict(username=validation[u'username'])
        userData['userId'] = user.id
        g = func.__globals__        # not thread safe!
        g['userData'] = userData
        return func(*args, **kwargs)
    return wrapper



@app.route('/')
@app.route('/index')
def index():
    return json.dumps({"status": "success"})


@app.errorhandler(404)
def notFound404(e):
    statusCode = 404
    return json.dumps({"status": "fail", "code": statusCode}), statusCode


@app.route('/fetchAccessToken',methods = ['POST'])
def login():
    """Fetch api access token for registered username/password"""
    req_data = request.get_json()
    username = req_data['username']
    password = req_data['password'] or ''
    password = password.encode('UTF_8')
    user = User.query.filter_by(username=username).first()
    if user == None:
        return json.dumps({"status": "fail", "message": "invalid username or password"}), 401
    if not bcrypt.checkpw(password, user.password.encode('UTF_8')):
        return json.dumps({"status": "fail", "message": "invalid username or password"}), 401
    token = jwt.encode({'username': username,
        'createdAt': str(datetime.now())}, app.configini['DEFAULT']['secret'], algorithm='HS256')
    return json.dumps({"status": "success", "token": token})


@app.route('/register',methods = ['POST'])
def register():
    """Register the user. (input: username/password)"""
    req_data = request.get_json()
    username = req_data['username']
    password = req_data['password']
    if username == None or password == None:
        return json.dumps({"status": "fail", "message": "username and password required"}), 400
    password = password.encode('UTF_8')
    user = User.query.filter_by(username=username).first()
    if user != None:
        return json.dumps({"status": "fail", "message": "username exists"}), 401
    newUser = User(username, bcrypt.hashpw(password, bcrypt.gensalt()))
    db.session.add(newUser)
    db.session.commit()
    return json.dumps({"status": "success", "message": "registered"}), 200
