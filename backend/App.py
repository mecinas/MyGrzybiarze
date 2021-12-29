from flask import Flask, request, make_response, send_file

from RESTControllers.AccountModel import user_controller
from RESTControllers.FriendshipModel import friendship_controller
from RESTControllers.NotificationModel import notification_controller
from RESTControllers.AzureModel import azure_controller

app = Flask(__name__)
app.register_blueprint(user_controller)
app.register_blueprint(friendship_controller)
app.register_blueprint(notification_controller)
app.register_blueprint(azure_controller)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)