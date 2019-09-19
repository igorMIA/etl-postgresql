start_server:
	docker-compose up -d orm

stop_server:
	docker-compose stop orm
	docker-compose stop db

loaddata: start_server
	docker-compose exec orm python manage.py load_patient input_files/Patient.ndjson.txt
	docker-compose exec orm python manage.py load_encounter input_files/Encounter.ndjson.txt
	docker-compose exec orm python manage.py load_procedure input_files/Procedure.ndjson.txt
	docker-compose exec orm python manage.py load_observation input_files/Observation.ndjson.txt
	docker-compose exec orm python manage.py get_metrics

run_tests:
	docker-compose up --build tests
