from models import Response, Payload, Powerplant

def meritOrder(powerplants: list) -> list:
	"""
	Started ordering powerplants by efficiency, but it won't be enough to solve the unit commitment problem because we will need
	to consider the cost and the % wind of each powerplant as well. A gasfired pp with 0.2 efficiency and 10 euro/MWh will be in a higher position than
	a kerosine one with 0.3 efficiency and 50 euro/MWh, obviously you will preffer to switch on the gasfired one. The same goes for the windturbines, we will need
	to consider the pmax of each to decide which one to switch on first and maybe don't swithc on 2 powerplant when we can reach the load with only 1 switched on.
	So, we will need to add some conditions for the ordering.

	Sorts the powerplants by its merit-order.

	The merit-order is a way of ranking available sources of energy, especially electrical generation, based on ascending order of price (which may reflect 
	the order of their short-run marginal costs of production) and sometimes pollution, together with amount of energy that will be generated.
	"""
	return sorted(powerplants, key= lambda p: p.efficiency, reverse=True)

def solve(payload: dict) -> list:
	"""
	I thought about always siwtching on the windturbines while needed load > windturbin pmax*%wind and then switch on the powerplants in the merit order. But meritorder
	is not well-implemented, the solve function should switch on powerplant on its merit order until the load is reached, we don't need extra comparisons here.
	"""
	response = []
	sortedPowerplants = meritOrder(payload.powerplants)
	for powerplant in sortedPowerplants:
		response.append(Response(powerplantName=powerplant.name, p=0))
	return response