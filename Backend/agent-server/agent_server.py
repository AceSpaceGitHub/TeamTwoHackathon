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
    operatingContext = request.json
    if (isinstance(operatingContext, str)):
       # Not sure if this is required.
       # Sometimes what you get from the frontend is string,
       # but it might be if you do like `request.get_json()` vs `request.json`
       # or something before this.
       operatingContext = json.loads(operatingContext)

    scenarioEnv = agent_data_converter.OperatingContextToScenarioEnvironment(operatingContext)

    prediction = agent_model_driver.GeneratePrediction(model, scenarioEnv)
    
    targetIds = []
    for entry in operatingContext['intendedTargetIdToDamage']['entries']:
       targetIds.append(entry['id'])
    planAssessment = agent_data_converter.PredictionToPlanAssessment(prediction, targetIds)

    #vehicleIds = []
    #for carrier in messageBody['friendlyForces']['carriers']:
    #    for squadron in carrier['squadrons']:
    #        for jetId in squadron['jetIds']:
    #            vehicleIds.append(jetId)
    #minJetsPerSortie = messageBody['minJetsPerSortie']
    #targetTimeConstraints = messageBody['targetTimeConstraints']['entries']
    #jetsToTargetIdx = agent_or_tools_driver.AllocateJetPairsToTargets(
    #   vehicleIds, minJetsPerSortie, targetTimeConstraints, targetIds, targetIdxSequence)

    return planAssessment
