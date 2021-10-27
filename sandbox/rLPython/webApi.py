from flask import Flask, request, jsonify
from simulate import simulate

app = Flask(__name__)

app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/v1/resources/scenario', methods=['GET'])
def api_id():
    content = request.json
    print(content)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    results = simulate()
    predictionResults = []

    for prediction in results:
        actions = []
        for sortie in prediction[1]:
            sortieResult = {"Actions":sortie[0], "Missiles": sortie[1][0], "ExpectedHits": sortie[1][1], "CurrentHits": sortie[1][2], "Assets": sortie[1][3]}
            actions.append(sortieResult)
        
        predictionResult = {"SuccessRate": prediction[0], "Actions": actions}
        predictionResults.append(predictionResult)
    

    jsonResults = {"Results": predictionResults}

    return jsonify(jsonResults)

app.run(port=5001)