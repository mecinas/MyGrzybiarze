from flask import Flask, request, make_response, send_file
import io
import json

from RESTControllers.user import user_controller
import manipulate_database as md

app = Flask(__name__)
app.register_blueprint(user_controller)




"""
def check_auth(username, password):
    return username == AUTH_LOGIN and password == AUTH_PASS

@app.before_request
def before_request():
    auth = request.authorization
    if not (auth and check_auth(auth.username, auth.password)):
        return 'Unauthorized', 401

@app.after_request
def after_request_func(response):
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
"""
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)