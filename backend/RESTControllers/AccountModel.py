from flask import Flask, request, make_response, send_file, Blueprint
import io
from flask import jsonify
import json

from RESTControllers.ConfigREST import allowed_methods, send_response
from ManipulateDatabase import AccountRepository as manipulate_account

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
    
    manipulate_account.insert_into_account(nickname, firstname, surname, dateOfBirth, email, photo.read())
    return send_response("Poprawnie zarejestrowano użytkownika")

@user_controller.route('/register', methods=['DELETE'])
def delete_user():
    data = json.loads(request.data.decode('utf-8'))
    email = data["email"]
    manipulate_account.delete_user(email)
    return send_response("Poprawnie usunięto użytkownika")

@user_controller.route('/register/check', methods=['GET', 'OPTIONS'])
def register_check():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['GET'])

    email = request.args["email"]
    isRegistred = manipulate_account.is_user_registred(email)

    return send_response({"isRegistered": isRegistred})

@user_controller.route('/user/single', methods=['GET', 'OPTIONS'])
def get_user():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['GET'])

    email = request.args["email"]
    user = manipulate_account.get_user(email)
    return send_response(user)

@user_controller.route('/user/list', methods=['GET', 'OPTIONS'])
def get_users():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['GET'])

    user_list = manipulate_account.get_users()
    converted_user_list = []
    for user in user_list:
        converted_user_list.append(json.dumps(user))
    return send_response(jsonify(converted_user_list))


@user_controller.route('/account/name', methods=['PUT', 'OPTIONS'])
def change_name():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['PUT'])

    data = json.loads(request.data.decode('utf-8'))
    firstname = data["firstname"]
    surname = data["surname"]
    email = data["email"]
    
    manipulate_account.change_name(firstname, surname, email)
    return send_response("Poprawnie zmieniono imię i nazwisko")

@user_controller.route('/account/nickname', methods=['PUT', 'OPTIONS'])
def change_nickname():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['PUT'])

    data = json.loads(request.data.decode('utf-8'))
    nickname = data["nickname"]
    email = data["email"]
    
    manipulate_account.change_nickname(nickname, email)
    return send_response("Poprawnie zmieniono nazwę użytkownika")

@user_controller.route('/account/dateOfBirth', methods=['PUT', 'OPTIONS'])
def change_date_of_birth():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['PUT'])

    data = json.loads(request.data.decode('utf-8'))
    date_of_birth = data["dateOfBirth"]
    email = data["email"]
    
    manipulate_account.change_date_of_birth(date_of_birth, email)
    return send_response("Poprawnie zmieniono datę urodzin użytkownika")
    
@user_controller.route('/account/avatar', methods=['OPTIONS','PUT'])
def post_avatar():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['PUT', 'GET'])

    avatar = request.files["avatar"]
    email = request.form["email"]
    manipulate_account.change_photo(avatar.read(), email)

    return send_response("Udało się zmienić avatar")

@user_controller.route('/account/avatar', methods=['GET'])
def get_avatar():
    email = request.args["email"]

    photo = manipulate_account.get_photo(email)
    return send_response(send_file(io.BytesIO(photo), mimetype='image/png'))
