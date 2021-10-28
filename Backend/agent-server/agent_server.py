from flask import Flask, request, jsonify
from flask_cors import CORS
from stable_baselines3 import PPO
import json

import agent_data_converter
import agent_model_driver
import assignment_gene_algo_driver

app = Flask(__name__)
CORS(app)

# This can take a quite noticeable amount of time
# that seems to grow as this environment gets more complex.
# Let's not take the hit per request.
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

    sortieToMissileRequest = agent_data_converter.PlanAssessmentToSortieMissileRequest(planAssessment)
    strikePackages = assignment_gene_algo_driver.allocateStrikePackages(50, 1000, sortieToMissileRequest, .99, .12)

    return {
       'planAssessment': planAssessment,
       'strikePackages': strikePackages,
    }
