from flask import Flask, request, make_response, send_file, Blueprint
import io
from flask import jsonify
import json

from RESTControllers.configREST import allowed_methods, send_response
import manipulate_database as md

user_controller = Blueprint('UserRESTController', __name__)


@user_controller.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['POST', 'DELETE'])

    data = json.loads(request.data.decode('utf-8'))
    nickname = data["nickname"]
    firstname = data["firstname"]
    surname = data["surname"]
    email = data["email"]
    dateOfBirth = data["dateOfBirth"]
    photo = open("resources/noname.png", 'rb')
    
    md.insert_into_account(nickname, firstname, surname, dateOfBirth, email, photo.read())
    return send_response("Poprawnie zarejestrowano użytkownika")

@user_controller.route('/register', methods=['DELETE'])
def delete_user():
    data = json.loads(request.data.decode('utf-8'))
    email = data["email"]
    md.delete_user(email)
    return send_response("Poprawnie usunięto użytkownika")

@user_controller.route('/register/check', methods=['GET', 'OPTIONS'])
def register_check():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['GET'])

    email = request.args["email"]
    isRegistred = md.is_user_registred(email)

    return send_response({"isRegistered": isRegistred})

@user_controller.route('/user/single', methods=['GET', 'OPTIONS'])
def get_user():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['GET'])

    email = request.args["email"]
    user = md.get_user(email)
    return send_response(user)

@user_controller.route('/user/list', methods=['GET', 'OPTIONS'])
def get_users():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['GET'])

    user_list = md.get_users()
    return send_response(jsonify(user_list))


@user_controller.route('/account/change/name', methods=['PUT', 'OPTIONS'])
def change_name():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['PUT'])

    data = json.loads(request.data.decode('utf-8'))
    firstname = data["firstname"]
    surname = data["surname"]
    email = data["email"]
    
    md.change_name(firstname, surname, email)
    return send_response("Poprawnie zmieniono imię i nazwisko")

@user_controller.route('/account/change/nickname', methods=['PUT', 'OPTIONS'])
def change_nickname():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['PUT'])

    data = json.loads(request.data.decode('utf-8'))
    nickname = data["nickname"]
    email = data["email"]
    
    md.change_nickname(nickname, email)
    return send_response("Poprawnie zmieniono nazwę użytkownika")

@user_controller.route('/account/change/dateOfBirth', methods=['PUT', 'OPTIONS'])
def change_date_of_birth():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['PUT'])

    data = json.loads(request.data.decode('utf-8'))
    date_of_birth = data["dateOfBirth"]
    email = data["email"]
    
    md.change_date_of_birth(date_of_birth, email)
    return send_response("Poprawnie zmieniono datę urodzin użytkownika")
    
@user_controller.route('/account/change/avatar', methods=['PUT'])
def post_avatar():
    data = request.files["avatar"]
    email = request.form["email"]
    md.change_photo(data.read(), email)

    return send_response("Udało się zmienić avatar")

@user_controller.route('/avatar', methods=['GET', 'OPTIONS'])
def get_avatar():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['GET', 'PUT'])
    email = request.args["email"]

    photo = md.get_photo(email)
    return send_response(send_file(io.BytesIO(photo), mimetype='image/png'))
