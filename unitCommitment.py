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
	After the 1st solution, i realized that this function is not working as expected, we should prioritize the windturbines.

	Returns the key to sort the powerplants by its merit-order.
	"""
	if powerplant.type == 'windturbine':
		return powerplant.efficiency, powerplant.pmax
	else:
		fuelType = 'gas(euro/MWh)' if powerplant.type == 'gasfired' else 'kerosine(euro/MWh)'
		return powerplant.efficiency, getFuelValue(fuels=fuels, fuelType=fuelType) / powerplant.efficiency

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
	return sorted(payload.powerplants, key= lambda powerplant: meritOrderKey(powerplant, payload.fuels), reverse=True)

def solve(payload: dict) -> list:
	"""
	I thought about always siwtching on the windturbines while needed load > windturbin pmax*%wind and then switch on the powerplants in the merit order. But meritorder
	is not well-implemented, the solve function should switch on powerplant on its merit order until the load is reached, we don't need extra comparisons here.
	With the well-implemented meritorder, we can just switch on the powerplants in the merit order until the load is reached, because of the thermal efficiency,
	the load generated will be: efficiency * pmax for gas/kerosine powerplants and %wind * pmax for windturbines.
	After the 1st solution and improving merit orders functions, i had to update this function so it iterates only once over the powerplants list instead of
	iterating over it every iteration of the while loop. We can just iterate over the powerplants list once and switch on the powerplants in the merit order until the load is reached.
	After the 2nd solution, i had to improve the loop conditions so non swithced on powerplants are not considered in the generated load and their p value is zero. Also, i 
	was wrongly considering gasfired and turbojets production was efficiency*pmax instead of pmax, i had to fix this as well.

	Solves the unit commitment problem.
	"""
	response = []
	sortedPowerplants = meritOrder(payload)
	generatedLoad = 0
	powerplantIndex = 0
	
	while generatedLoad <= payload.load and powerplantIndex < len(sortedPowerplants):
		partialLoad = 0
		powerplant = sortedPowerplants[powerplantIndex]
		
		# We avoid switching on a powerplant if we don't need to
		if generatedLoad == payload.load:
			partialLoad = 0
		elif powerplant.type == "windturbine":
			partialLoad = powerplant.pmax * getFuelValue(fuels=payload.fuels, fuelType='wind(%)')
		else:
			partialLoad = powerplant.pmax
		
		# If we overpass the load, partialLod will not be pmax but the remaining load
		if generatedLoad + partialLoad > payload.load:
				partialLoad = payload.load - generatedLoad
		
		partialLoad = round(partialLoad * 10) / 10 # 0.1 Requirement
		generatedLoad += partialLoad
		
		# Append even if p is zero so we have the full responses list
		response.append(Response(powerplantName=powerplant.name, p=partialLoad))
		powerplantIndex += 1
	
	return response