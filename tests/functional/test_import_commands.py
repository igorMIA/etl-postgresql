import pytest
from django.core.management import call_command, CommandError
from instances.models import Patient, Encounter, Procedure, Observation


@pytest.mark.django_db
def test_import_patient():
    expected_dict = {
        'source_id': '3b0420d8-8d7d-4add-b20b-2c9bbb9e6962',
        'birth_date':  '1960-12-18',
        'gender': 'female',
        'race_code': '2106-3',
        'race_code_system': 'http://hl7.org/fhir/v3/Race',
        'ethnicity_code': '2186-5',
        'ethnicity_code_system': 'http://hl7.org/fhir/v3/Ethnicity',
        'country': 'US'
    }
    call_command('load_patient', 'tests/functional/input_files/patient_input')
    for key, value in expected_dict.items():
        assert value == str(getattr(Patient.objects.all()[0], key))
    assert Patient.objects.all().count() == 1


@pytest.mark.django_db
def test_import_encounter():
    patient = Patient.objects.create(source_id='e2309dce-a235-4624-af3c-ad209843fe93')

    expected_dict = {
        'source_id': '273275b7-dd3e-4bcb-b893-35f5248438b2',
        'patient_id':  str(patient),
        'start_date': '2008-08-21 21:50:07',
        'end_date': '2008-08-21 21:50:07',
        'type_code': '270427003',
        'type_code_system': 'http://snomed.info/sct'
    }
    call_command('load_encounter', 'tests/functional/input_files/encounter_input')
    for key, value in expected_dict.items():
        assert value == str(getattr(Encounter.objects.all()[0], key))
    assert Encounter.objects.all().count() == 3


@pytest.mark.django_db
def test_import_procedure():
    patient = Patient.objects.create(source_id='e2309dce-a235-4624-af3c-ad209843fe93')
    encounter = Encounter.objects.create(
        source_id='fb1f4ee4-d1cc-4a25-b2f0-c874cec957d9',
        patient_id=patient,
        start_date='2008-08-21 21:50:07',
        end_date='2008-08-21 21:50:07'
    )

    expected_dict = {
        'source_id': '180382',
        'patient_id':  str(patient),
        'encounter_id': str(encounter),
        'procedure_date': '2017-01-24 10:36:38',
        'type_code': '428191000124101',
        'type_code_system': 'http://snomed.info/sct'
    }
    call_command('load_procedure', 'tests/functional/input_files/procedure_input')
    for key, value in expected_dict.items():
        assert value == str(getattr(Procedure.objects.all()[0], key))
    assert Procedure.objects.all().count() == 2


@pytest.mark.django_db
def test_import_observation():
    patient = Patient.objects.create(source_id='e2309dce-a235-4624-af3c-ad209843fe93')
    encounter = Encounter.objects.create(
        source_id='fb1f4ee4-d1cc-4a25-b2f0-c874cec957d9',
        patient_id=patient,
        start_date='2008-08-21 21:50:07',
        end_date='2008-08-21 21:50:07'
    )

    expected_dict = {
        'source_id': '0f08874b-355b-4d6a-b230-0f2881decf87',
        'patient_id':  str(patient),
        'encounter_id': str(encounter),
        'observation_date': '2007-08-21 06:59:32',
        'type_code': '2571-8',
        'type_code_system': 'http://loinc.org',
        'value': '144.0000000000',
        'unit_code': 'mg/dL',
        'unit_code_system': 'http://unitsofmeasure.org/'
    }
    call_command('load_observation', 'tests/functional/input_files/observation_input')
    for key, value in expected_dict.items():
        assert value == str(getattr(Observation.objects.all()[0], key))
    assert Observation.objects.all().count() == 4


def test_run_command_without_file():
    with pytest.raises(CommandError):
        call_command('load_observation')


@pytest.mark.django_db
def test_run_command_with_bad_json():
    call_command('load_observation', 'tests/functional/input_files/broken_input')
    assert 0 == Observation.objects.all().count()
