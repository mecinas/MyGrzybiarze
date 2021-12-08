from flask import Flask, request, make_response, send_file, Blueprint
from flask import jsonify
import json

from RESTControllers.ConfigREST import allowed_methods, send_response
from ManipulateDatabase import FriendshipRepository as manipulate_friendship

friendship_controller = Blueprint('FriendshipRESTController', __name__)


@friendship_controller.route('/friendship', methods=['POST', 'OPTIONS'])
def add_friendship():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['POST', 'DELETE'])

    data = json.loads(request.data.decode('utf-8'))
    first_email = data["first_email"]
    sec_email = data["sec_email"]
    
    manipulate_friendship.add_friendship(first_email, sec_email)
    return send_response("Poprawnie zarejestrowano przyjaźń")

@friendship_controller.route('/friendship', methods=['DELETE'])
def delete_friendship():
    data = json.loads(request.data.decode('utf-8'))
    first_email = data["first_email"]
    sec_email = data["sec_email"]
    manipulate_friendship.delete_friendship(first_email, sec_email)

    return send_response("Poprawnie usunięto przyjaźń")

@friendship_controller.route('/friendship', methods=['GET', 'OPTIONS'])
def get_friends():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['GET'])

    user_email = request.args["user_email"]

    friend_list = manipulate_friendship.get_list_of_friends(user_email)
    return send_response(jsonify(friend_list))

@friendship_controller.route('/friendship/check', methods=['GET', 'OPTIONS'])
def register_check():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['GET'])

    first_email = request.args["first_email"]
    sec_email = request.args["sec_email"]

    are_friends = manipulate_friendship.are_users_friends(first_email, sec_email)

    return send_response({"areFriends": are_friends})