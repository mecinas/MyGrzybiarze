from flask import Flask, request, make_response, send_file


def allowed_methods(methods):
    origin = request.headers.get('Origin')
    if 'OPTIONS' not in methods:
        methods.append('OPTIONS')
    response = make_response('', 200)

    allowed_origins = ["http://localhost:3000"]
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin

    response.headers['Access-Control-Allow-Methods'] = ', '.join(methods)
    response.headers["Access-Control-Allow-Headers"] = 'Content-Type, auth_cookie'
    response.headers["Access-Control-Allow-Credentials"] = 'true'
    return response

def send_response(data):
    origin = request.headers.get('Origin')
    allowed_origins = ["http://localhost:3000"]
    response = make_response(data, 200)
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Credentials"] = 'true'
    return response