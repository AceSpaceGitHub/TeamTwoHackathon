# Backend server

At the moment, there is a single Python microservice that has one endpoint to drive solution generation.

## How to build/test

This assumes you have Python 3.8 installed on your machine.

```
cd Backend/agent-server

# Only need to do this in the beginning/when dependencies change.
python -m pip install -r requirements.txt

# To run the server - it will come up on localhost:50051
$env:FLASK_APP = "agent_server.py"
python -m flask run
```

Once the server is running, you can test it directly by `curl`'ing request files to it. The latest example of the expected request structure lives in this repo's `test-data` directory. Here's an example of how to use it via cmd terminal (PowerShell doesn't seem to like the `@` symbol...):

```
cd frontend/src/test-data
curl -X POST -H "Content-Type: application/json" -d @./getPlanAssessmentRequest.json localhost:5000/GetPlanAssessment > getPlanAssessmentResponse.json
```
