from models import Response, Payload, Powerplant

def meritOrder(powerplants: list) -> list:
	"""
	Sorts the powerplants by its merit-order.

	The merit-order is a way of ranking available sources of energy, especially electrical generation, based on ascending order of price (which may reflect 
	the order of their short-run marginal costs of production) and sometimes pollution, together with amount of energy that will be generated.
	"""
	return sorted(powerplants, key= lambda p: p.efficiency, reverse=True)

def solve(payload: dict) -> list:
	"""
	Solves the unit commitment problem.
	"""
	response = []
	sortedPowerplants = meritOrder(payload.powerplants)
	for powerplant in sortedPowerplants:
		response.append(Response(powerplantName=powerplant.name, p=0))
	return response