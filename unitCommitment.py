from models import Response, Payload, Fuel, Powerplant

def getFuelValue(fuels: list[Fuel], fuelType: str) -> float:
	"""
	After creating the Fuel model so we don't process the full payload in meritOrder function, we can get the fuel value from the fuels list.

	Returns the value of the fuel from the fuels list.
	"""
	for fuel in fuels:
		if fuel.type == fuelType:
			if fuelType == 'wind(%)':
				return fuel.value / 100
			return fuel.value
	return 0

def meritOrderKey(powerplant: Powerplant, fuels: list[Fuel]):
	"""
	As we need extra condtions for ordering the powerplants list, we can't do it with a simple lambda function.
	We need to get the payload here, so we can get the fuels and the wind(%) from it. Definetely, it is useful to have a Fuel model.

	Returns the key to sort the powerplants by its merit-order.
	"""
	if powerplant.type == 'windturbine':
		return powerplant.pmax
	else:
		fuelType = 'gas(euro/MWh)' if powerplant.type == 'gasfired' else 'kerosine(euro/MWh)'
		return getFuelValue(fuels=fuels, fuelType=fuelType) / powerplant.efficiency

def meritOrder(payload: Payload) -> list:
	"""
	Started ordering powerplants by efficiency, but it won't be enough to solve the unit commitment problem because we will need
	to consider the cost and the % wind of each powerplant as well. A gasfired pp with 0.2 efficiency and 10 euro/MWh will be in a higher position than
	a kerosine one with 0.3 efficiency and 50 euro/MWh, obviously you will preffer to switch on the gasfired one. The same goes for the windturbines, we will need
	to consider the pmax of each to decide which one to switch on first and maybe don't swithc on 2 powerplant when we can reach the load with only 1.
	So, we will need to add some conditions for the ordering: pmax for windturbines, price / efficiency for gasfired and kerosine powerplants.

	Sorts the powerplants by its merit-order.

	The merit-order is a way of ranking available sources of energy, especially electrical generation, based on ascending order of price (which may reflect 
	the order of their short-run marginal costs of production) and sometimes pollution, together with amount of energy that will be generated.
	
	Thermal efficiency is the ratio of the net work output to the heat input. 
	If gas is at 6 euro/MWh and if the efficiency of the powerplant is  50% (i.e. 2 units of gas will generate one unit of electricity),
	the cost of generating 1 MWh is 12 euro. Same for kerosine. For %wind, 25% wind during an hour, a wind-turbine with a Pmax of 4 MW will generate 1MWh of energy.
	"""
	return sorted(payload.powerplants, key= lambda powerplant: meritOrderKey(powerplant, payload.fuels))
	

def solve(payload: dict) -> list:
	"""
	I thought about always siwtching on the windturbines while needed load > windturbin pmax*%wind and then switch on the powerplants in the merit order. But meritorder
	is not well-implemented, the solve function should switch on powerplant on its merit order until the load is reached, we don't need extra comparisons here.
	With the well-implemented meritorder, we can just switch on the powerplants in the merit order until the load is reached, because of the thermal efficiency,
	the load generated will be: efficiency * pmax for gas/kerosine powerplants and %wind * pmax for windturbines.
	
	Solves the unit commitment problem.
	"""
	response = []
	sortedPowerplants = meritOrder(payload)
	generatedLoad = 0
	while generatedLoad < payload.load:
		for powerplant in sortedPowerplants:
			if powerplant.type == 'windturbine':
				partialLoad = powerplant.pmax * getFuelValue(fuels=payload.fuels, fuelType='wind(%)')
				generatedLoad += partialLoad
				response.append(Response(powerplantName=powerplant.name, p=partialLoad))
			else:
				partialLoad = powerplant.pmax * powerplant.efficiency
				generatedLoad +=  partialLoad
				response.append(Response(powerplantName=powerplant.name, p=partialLoad))
	return response