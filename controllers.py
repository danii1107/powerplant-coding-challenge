from models import Payload, Powerplant, Fuel

def parsePayload(data: dict) -> Payload:
	"""
	Creates the powerplant objects from the given data.
	"""
	powerplants = []
	for powerplant in data.pop("powerplants"):
		powerplants.append(Powerplant(**powerplant))
	
	fuels = []
	for fuel in data.pop("fuels"):
		fuels.append(Fuel(**fuel))

	return Payload(**data, powerplants=powerplants, fuels=fuels)