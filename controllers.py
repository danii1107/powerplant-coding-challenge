from models import Payload, Powerplant

def parsePayload(data: dict) -> Payload:
	"""
	Creates the powerplant objects from the given data.
	"""
	powerplants = []
	for powerplant in data.pop("powerplants"):
		powerplants.append(Powerplant(**powerplant))
	
	return Payload(**data, powerplants=powerplants)