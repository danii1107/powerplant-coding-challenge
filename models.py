from pydantic import BaseModel, Field
from typing import List, Dict

class Powerplant(BaseModel):
	"""
	Represents a powerplant.
	
	Attributes:
		@name - powerplant's name
		@type - gasfired, turbojet or windturbine. 
		@efficiency - the efficiency at which they convert a MWh of fuel into a MWh of electrical energy. 1 for windturbine because it generates power at zero price.
		@pmin - the minimum amount of power the powerplant generates when switched on. 0 for windturbine
		@pmax - the maximum amount of power the powerplant can generate.
	"""
	name: str
	type: str
	efficiency: float
	pmin: int
	pmax: int

class Fuel(BaseModel):
	"""
	Represents a fuel or a % of wind.
	
	Attributes:
		@type - the type of the fuel (gas(euro/MWh), kerosine(euro/MWh) or wind(%))
		@price - the price of the fuel or the % of wind.
	"""
	type: str
	value: float

class Payload(BaseModel):
	"""
	Represents the full request data.
	
	Attributes:
		@load - the amount of energy that needs to be generated during one hour.
		@fuels - a dictionary which stores the type os fuel and its price for gas and kerosine. For wind, it stores the percentage of wind
		@powerplants - a list which describes the powerplants at disposal to generate the demanded load.
	"""
	load: int
	fuels: List[Fuel]
	powerplants: List[Powerplant]

class Response(BaseModel):
	"""
	Represents the response data.

	Attributes:
		@name - the name of the powerplant that has to generate the energy
		@p - the amount of energy that the powerplant has to generate
	"""
	powerplantName: str
	p: float

	def serialize(self) -> Dict[str, float]:
		"""
		Serialize the Response object to a dictionary.
		"""
		return {
			'powerplantName': self.powerplantName,
			'p': self.p
		}