from flask import Flask, request, make_response, send_file, Blueprint
from flask import jsonify
import json

from RESTControllers.configREST import allowed_methods, send_response
import manipulate_database as md

notification_controller = Blueprint('NotificationRESTController', __name__)


@notification_controller.route('/notification', methods=['POST', 'OPTIONS'])
def add_notification():
    if( request.method == 'OPTIONS'):
        return allowed_methods(['POST', 'DELETE', 'GET'])

    data = json.loads(request.data.decode('utf-8'))
    notification_type = data["notification_type"]
    message = data["message"]
    user_email = data["user_email"]
    request_url = data.get("request_url") #Może zwrócić None

    md.add_notification(notification_type, message, user_email, request_url)
    return send_response("Poprawnie zarejestrowano powiadomienie")

@notification_controller.route('/notification', methods=['DELETE'])
def delete_notification():
    data = json.loads(request.data.decode('utf-8'))
    notification_id = data["notification_id"]

    md.delete_notification(notification_id)
    return send_response("Poprawnie usunięto powiadomienie")

@notification_controller.route('/notification', methods=['GET'])
def get_notifications():
    user_email = request.args["user_email"]
    notification_list = md.get_user_notifications(user_email)

    return send_response(jsonify(notification_list))

