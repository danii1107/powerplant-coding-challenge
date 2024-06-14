# powerplant-coding-challenge

1. Activate virtual enviroment:  `python3 -m venv venv && source venv/bin/activte`
2. Export the enviroment variables: `source .env`
3. Install all the dependencies: `pip3 install -r requirements.txt`
4. Run server: `python3 app.py`

### Useful commands

- `curl -X POST -H "Content-Type: application/json" -d @example_payloads/payload3.json http://localhost:8888/productionplan`

### Progress solutions

- 1st solution: [{"p":243.8,"powerplantName":"gasfiredbig1"},{"p":243.8,"powerplantName":"gasfiredbig2"},{"p":21.599999999999998,"powerplantName":"windpark2"},{"p":77.7,"powerplantName":"gasfiredsomewhatsmaller"},{"p":90.0,"powerplantName":"windpark1"},{"p":4.8,"powerplantName":"tj1"},{"p":243.8,"powerplantName":"gasfiredbig1"},{"p":243.8,"powerplantName":"gasfiredbig2"},{"p":21.599999999999998,"powerplantName":"windpark2"},{"p":77.7,"powerplantName":"gasfiredsomewhatsmaller"},{"p":90.0,"powerplantName":"windpark1"},{"p":4.8,"powerplantName":"tj1"}]

- 2nd solution: [{"name":"windpark1","p":90.0},{"name":"windpark2","p":21.599999999999998},{"name":"gasfiredbig1","p":243.8},{"name":"gasfiredbig2","p":243.8},{"name":"gasfiredsomewhatsmaller","p":77.7},{"name":"tj1","p":4.8}]
