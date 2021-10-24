# Environment setup

Assuming you have Python 3.8 and pip already installed, run the following:

```
python -m pip install --upgrade pip
# Installs known dependencies to run the server.
python -m pip install -r requirements.txt
```

# How to run the server

From Powershell:

```
$env:FLASK_APP = "agent_server.py"
python -m flask run
```