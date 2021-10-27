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

    for prediction in results:
        print('New Sortie - {}%'.format(prediction[0]))
        for sortie in prediction[1]:
            print(sortie)

    return jsonify(results)

app.run(port=5001)