import pytest
from django.core.management import call_command
from instances.models import Patient


@pytest.mark.django_db
def test_import_commands():
    call_command('load_patient', 'tests/functional/input_files/patient_input')
    assert Patient.objects.all().count() == 4
