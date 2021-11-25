from flask import Flask, request, make_response, send_file
import io
import json
import manipulate_database as md

app = Flask(__name__)

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

@app.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['POST', 'DELETE'])

    data =json.loads(request.data.decode('utf-8'))
    nickname = data["nickname"]
    firstname = data["firstname"]
    surname = data["surname"]
    email = data["email"]
    dateOfBirth = data["dateOfBirth"]
    photo = open("resources/noname.png", 'rb')
    
    md.insert_into_account(nickname, firstname, surname, dateOfBirth, email, photo.read())
    return send_response("Poprawnie zarejestrowano użytkownika")

@app.route('/register', methods=['DELETE'])
def delete_user():
    data = json.loads(request.data.decode('utf-8'))
    email = data["email"]
    md.delete_user(email)
    return send_response("Poprawnie usunięto użytkownika")

@app.route('/register/check', methods=['GET', 'OPTIONS'])
def register_check():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['GET'])

    email = request.args["email"]
    isRegistred = md.is_user_registred(email)
    return send_response({"isRegistered": isRegistred})

@app.route('/account/change/name', methods=['PUT', 'OPTIONS'])
def change_name():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['PUT'])

    data = json.loads(request.data.decode('utf-8'))
    firstname = data["firstname"]
    surname = data["surname"]
    email = data["email"]
    
    md.change_name(firstname, surname, email)
    return send_response("Poprawnie zmieniono imię i nazwisko")

@app.route('/account/change/nickname', methods=['PUT', 'OPTIONS'])
def change_nickname():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['PUT'])

    data = json.loads(request.data.decode('utf-8'))
    nickname = data["nickname"]
    email = data["email"]
    
    md.change_nickname(nickname, email)
    return send_response("Poprawnie zmieniono nazwę użytkownika")

@app.route('/account/change/dateOfBirth', methods=['PUT', 'OPTIONS'])
def change_date_of_birth():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['PUT'])

    data = json.loads(request.data.decode('utf-8'))
    dateOfBirth = data["dateOfBirth"]
    email = data["email"]
    
    md.change_date_of_birth(dateOfBirth, email)
    return send_response("Poprawnie zmieniono datę urodzenia")

@app.route('/avatar', methods=['GET', 'OPTIONS'])
def get_avatar():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['GET', 'PUT'])
    email = request.args["email"]

    photo = md.get_photo(email)
    return send_response(send_file(io.BytesIO(photo), mimetype='image/png'))

@app.route('/avatar', methods=['PUT'])
def post_avatar():
    data = request.files["avatar"]
    email = request.form["email"]
    md.change_photo(data.read(), email)

    return send_response("Udało się zmienić avatar")

@app.route('/getInfo', methods=['GET', 'OPTIONS'])
def get_info():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['GET'])

    email = request.args["email"]
    info = md.get_user_info(email)
    return send_response(info)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)