Two Endpoints:

http://localhost:8000/api/data - get request to collect data

http://localhost:8000/api/summary - post request with response outage report in minutes

Operational steps:

	1. Change JSON file
	
	2. Run update_db.py
	
	3. Run sync_data.py
	
Data will be coherent and present in db and Pingdom.

To keep db up-to-date:
	1. Each appropriate interval run update_state.py to sync state 
	( implementation is inclined to perform for a shorter period between syncs if displaying last-time-down and time-to-recover is important metric to follow over casual updates of state).
	
To configure token:
	in /backend directory create .env file:
	
	TOKEN = {token}
	
Python version: 3.10.6
