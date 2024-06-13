import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# This API only supports POST method so we don't need any other pages than the main one
@app.route("/", methods=["POST"])
def index():
	"""
	Implements the api allowing users to make requests to it.
	The api will parse the given data and process the request to
		return a solution
	"""
	try:
		# Provisional implementation
		data = request.get_json()
		return jsonify(data), 200
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
	app.run(debug=debug)