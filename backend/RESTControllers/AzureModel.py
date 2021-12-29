from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid, json
from dotenv import load_dotenv
from flask import Flask, request, make_response, send_file, Blueprint, jsonify

from RESTControllers.ConfigREST import allowed_methods, send_response

load_dotenv()
ENDPOINT = os.getenv('ENDPOINT')
PREDICTION_KEY = os.getenv('PREDICTION_KEY')
PREDICTION_RESOURCE_ID = os.getenv('PREDICTION_RESOURCE_ID')
PREDICTION_EDIBLE_PROJECT_ID = os.getenv('PREDICTION_EDIBLE_PROJECT_ID')
PUBLISH_EDIBLE_ITERATION_NAME = os.getenv('PUBLISH_EDIBLE_ITERATION_NAME')
PREDICTION_SPECIES_PROJECT_ID = os.getenv('PREDICTION_SPECIES_PROJECT_ID')
PUBLISH_SPECIES_ITERATION_NAME = os.getenv('PUBLISH_SPECIES_ITERATION_NAME')

prediction_credentials = ApiKeyCredentials(
    in_headers={"Prediction-key": PREDICTION_KEY})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

azure_controller = Blueprint('AzureRESTController', __name__)


@azure_controller.route('/analyser/edible', methods=['POST', 'OPTIONS'])
def alyse_edible():
    if(request.method == 'OPTIONS'):
        return allowed_methods(['POST'])

    image = request.files["mushroom_image"]
    results = predictor.classify_image(
            PREDICTION_EDIBLE_PROJECT_ID, PUBLISH_EDIBLE_ITERATION_NAME, image.read())

    array_of_predictions = []
    for prediction in results.predictions:
        prediction_dto = {
            "tag_name": prediction.tag_name,
            "probability": "{0:.2f}%".format(prediction.probability * 100)
        }
        array_of_predictions.append(prediction_dto)

    return send_response(jsonify(array_of_predictions))

@azure_controller.route('/analyser/species', methods=['POST', 'OPTIONS'])
def alyse_species():
    if(request.method == 'OPTIONS'):
        return allowed_methods(['POST'])

    image = request.files["mushroom_image"]
    results = predictor.classify_image(
            PREDICTION_SPECIES_PROJECT_ID, PUBLISH_SPECIES_ITERATION_NAME, image.read())

    array_of_predictions = []
    for prediction in results.predictions:
        prediction_dto = {
            "tag_name": prediction.tag_name,
            "probability": "{0:.2f}%".format(prediction.probability * 100)
        }
        array_of_predictions.append(prediction_dto)

    return send_response(jsonify(array_of_predictions))
