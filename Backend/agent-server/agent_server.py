from flask import Flask, request, jsonify
from flask_cors import CORS
import json

import agent_model_driver

app = Flask(__name__)
CORS(app)

@app.route('/GetPlanAssessment', methods=['POST'])
def get_plan_assessment():
    messageBody = json.loads(request.get_json()['body'])
    #scenarioEnv = agent_data_converter.OperatingPictureToScenarioEnvironment(request)

    targetIds = []
    for entry in messageBody['targetIdToDamage']['entries']:
       targetIds.append(entry['id'])
    #prediction = agent_model_driver.GeneratePrediction(self.model, scenarioEnv)

    #planAssessment = agent_data_converter.PredictionToPlanAssessment(prediction, targetIds)
    return jsonify(targetIds)
