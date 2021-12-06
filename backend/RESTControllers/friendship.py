from flask import Flask, request, make_response, send_file, Blueprint
import io
from flask import jsonify
import json

from RESTControllers.configREST import allowed_methods, send_response
import manipulate_database as md

friendship_controller = Blueprint('FriendshipRESTController', __name__)


@friendship_controller.route('/friendship', methods=['POST', 'OPTIONS'])
def add_friendship():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['POST', 'DELETE'])

    data = json.loads(request.data.decode('utf-8'))
    first_email = data["first_email"]
    sec_email = data["sec_email"]
    
    md.add_friendship(first_email, sec_email)
    return send_response("Poprawnie zarejestrowano przyjaźń")

@friendship_controller.route('/friendship', methods=['DELETE'])
def delete_friendship():
    data = json.loads(request.data.decode('utf-8'))
    first_email = data["first_email"]
    sec_email = data["sec_email"]
    md.delete_friendship(first_email, sec_email)

    return send_response("Poprawnie usunięto przyjaźń")

@friendship_controller.route('/friendship', methods=['GET', 'OPTIONS'])
def get_friends():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['GET'])

    user_email = request.args["user_email"]

    friend_list = md.get_list_of_friends(user_email)
    return send_response(jsonify(friend_list))

@friendship_controller.route('/friendship/check', methods=['GET', 'OPTIONS'])
def register_check():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['GET'])

    first_email = request.args["first_email"]
    sec_email = request.args["sec_email"]

    are_friends = md.are_users_friends(first_email, sec_email)

    return send_response({"areFriends": are_friends})