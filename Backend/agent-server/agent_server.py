from flask import Flask, request, jsonify
from flask_cors import CORS
from stable_baselines3 import PPO
import json

import agent_data_converter
import agent_model_driver
import agent_or_tools_driver

app = Flask(__name__)
CORS(app)

model = PPO.load("ScenarioEnvironment")

@app.route('/GetPlanAssessment', methods=['POST'])
def get_plan_assessment():
    messageBody = request.json['body']
    if (isinstance(messageBody, str)):
       # Not sure if this is required.
       # Sometimes what you get from the frontend is string,
       # but it might be if you do like `request.get_json()` vs `request.json`
       # or something before this.
       messageBody = json.loads(messageBody)

    scenarioEnv = agent_data_converter.OperatingContextToScenarioEnvironment(messageBody)

    #targetIds = []
    #for entry in messageBody['targetIdToDamage']['entries']:
    #   targetIds.append(entry['id'])
    prediction = agent_model_driver.GeneratePrediction(model, scenarioEnv)

    # Subject to change. Not sure the final structure of the prediction
    # and/or if original conversion will be needed.
    # Currently assuming pairs of [actionType, targetIdx].
    #prediction = [[0, 1], [1, 1], [1, 4], [1, 4], [1, 0]]
    #targetIdxSequence = []
    #for action in prediction:
    #   targetIdxSequence.append(action[1])
    #planAssessment = agent_data_converter.PredictionToPlanAssessment(prediction, targetIds)

    #vehicleIds = []
    #for carrier in messageBody['friendlyForces']['carriers']:
    #    for squadron in carrier['squadrons']:
    #        for jetId in squadron['jetIds']:
    #            vehicleIds.append(jetId)
    #minJetsPerSortie = messageBody['minJetsPerSortie']
    #targetTimeConstraints = messageBody['targetTimeConstraints']['entries']
    #jetsToTargetIdx = agent_or_tools_driver.AllocateJetPairsToTargets(
    #   vehicleIds, minJetsPerSortie, targetTimeConstraints, targetIds, targetIdxSequence)

    # This is just to give it something to return for now.
    # Client isn't hooked up to actually use this yet.
    return jsonify([])
