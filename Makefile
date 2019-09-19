start_server:
	docker-compose up -d orm

stop_server:
	docker-compose stop orm

loaddata: start_server
	docker-compose exec orm python manage.py load_patient Patient.ndjson.txt
	docker-compose exec orm python manage.py load_encounter Encounter.ndjson.txt
	docker-compose exec orm python manage.py load_procedure Procedure.ndjson.txt
	docker-compose exec orm python manage.py load_observation Observation.ndjson.txt
	docker-compose exec orm python manage.py get_metrics
