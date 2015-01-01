export DEBUG=True
export DATABASE_URL=postgres://localhost:5432/ships

initdb:
	python initdb.py

start:
	honcho start
