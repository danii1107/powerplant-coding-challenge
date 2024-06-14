import os
from flask import Flask, request, jsonify
from controllers import parsePayload
from unitCommitment import solve

app = Flask(__name__)

# This API only supports POST method so we don't need any other pages than the main one
@app.route("/productionplan", methods=["POST"])
def productionPlan():
	"""
	Implements the api allowing users to make requests to it.
	The api will parse the given data and process the request to
		return a solution
	"""
	try:
		data = request.get_json()
		payload = parsePayload(data)
		if payload is None:
			return jsonify({'error': 'Payload failure'}), 400	
		responses = solve(payload)
		if responses.__len__ == 0:
			return jsonify({'error': 'We can not reach a solution with the given data'}), 200
		serializedResponses = [r.serialize() for r in responses]
		if serializedResponses[0]['name'] == 'error':
			return jsonify(serializedResponses), 500	
		return jsonify(serializedResponses), 200
	except Exception as e:
		# If its not a POST return Bad request
		return jsonify({'error': str(e)}), 400	

if __name__ == "__main__":
	# Checks if debug env variable exists and uses it, otherwise debug will be false
	if 'DEBUG' in os.environ:
		debug = os.environ.get("DEBUG")
	else:
		debug = False

	# Runs the api	
	app.run(debug=debug, port=8888)