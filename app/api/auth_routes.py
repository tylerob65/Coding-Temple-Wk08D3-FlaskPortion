from . import api
from ..models import Users
from flask import request
from ..apiauthhelper import basic_auth

@api.post('/signup')
def signUpAPI():
    data = request.json

    username = data['username']
    email = data['email']
    password = data['password']

    user = Users.query.filter_by(username=username).first()
    
    if user:
        return {
            'status': 'not ok',
            'message': 'Please choose a different username.'
        }, 400
    
    user = Users.query.filter_by(email=email).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'That email is already in use.'
        }, 400
    
    user = Users(username,email,password)
    user.saveToDB()

    return {
        'status': 'ok',
        'message': "You have successfully created an account."
    }, 201

@api.post('/signin')
@basic_auth.login_required
def loginAPI():
    return {
        'status': 'ok',
        'message': "You have successfully logged in.",
        'data': basic_auth.current_user().to_dict()
    }, 200

