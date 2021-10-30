from flask import Flask, request, jsonify
from flask_cors import CORS
from stable_baselines3 import PPO
import json

import agent_data_converter
import assignment_gene_algo_driver
import scheduling_gene_algo_driver
import simulate

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

    numJets, numPilots, numMissiles, desiredDamages = (
       agent_data_converter.GetScenarioEnvironmentInputs(operatingContext)
    )

    prediction = simulate.simulate(model, numMissiles, numJets, numPilots,
       desiredDamages[0], desiredDamages[1], desiredDamages[2],
       desiredDamages[3], desiredDamages[4], desiredDamages[5]
    )
    
    targetIds = []
    for entry in operatingContext['intendedTargetIdToDamage']['entries']:
       targetIds.append(entry['id'])
    planAssessment = agent_data_converter.GeneratePlanAssessment(prediction, targetIds)

    sortieToMissileRequest = agent_data_converter.GenerateSortieMissileRequest(planAssessment)
    strikePackages = assignment_gene_algo_driver.allocateStrikePackages(50, 100, sortieToMissileRequest, .99, .12)

    sortieToTargetIds, sortieToLengthHours = agent_data_converter.GenerateScheduleRequest(planAssessment)
    strikeSchedule = scheduling_gene_algo_driver.scheduleStrikePackages(50, 100, 7 * 24, sortieToLengthHours)

    assembledSortiesActions = agent_data_converter.AssembleSortieData(
       planAssessment, strikePackages, strikeSchedule,
       sortieToTargetIds, sortieToLengthHours, sortieToMissileRequest)
    return {
       'resultingActions': assembledSortiesActions,
       'resultingState': planAssessment['resultingState']
    }
