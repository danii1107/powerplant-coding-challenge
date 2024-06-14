from models import Payload, Powerplant, Fuel

def parsePayload(data: dict) -> Payload:
	"""
	Creates the powerplant objects from the given data.
	"""
	powerplants = []
	
	try:
		for powerplant in data.pop("powerplants"):
			powerplants.append(Powerplant(**powerplant))
		
		fuels = []
		fuelsData = data.pop("fuels")
		for fuelName, fuelValue in fuelsData.items():
			fuels.append(Fuel(type=fuelName, value=fuelValue))

		return Payload(**data, powerplants=powerplants, fuels=fuels)
	except:
		return None