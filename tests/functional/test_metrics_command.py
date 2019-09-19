import time
import pytest
from django.core.management import call_command
from instances.models import Patient, Encounter, Procedure


CONSOLE_STDOUT = """
The number of patients by gender:
female: 10
male: 6
The top 10 types of procedures:
type55: 55
type50: 50
type23: 46
type33: 33
type29: 29
type10: 20
type17: 17
type15: 15
type12: 12
type7: 7
The most and least popular days of the week when encounters occurred:
Thursday: 27
Friday: 24
Tuesday: 20
Sunday: 18
Monday: 13
Saturday: 12
Wednesday: 9
"""


@pytest.mark.django_db
def test_metrics_command(capfd):
    patient = Patient.objects.create(source_id='test', gender='male')
    for x in range(10):
        Patient.objects.create(source_id=x, gender='female')
    for x in range(10, 15):
        Patient.objects.create(source_id=x, gender='male')

    procedure_count = [10, 15, 23, 2, 55, 7, 10, 3, 12, 50, 23, 17, 29, 2, 4, 33]
    for count in procedure_count:
        for x in range(count):
            Procedure.objects.create(
                source_id=time.time(),
                patient_id=patient,
                procedure_date='2017-01-24 10:36:38',
                type_code='type{}'.format(count),
                type_code_system='http://snomed.info/sct'
            )

    date_count = {
        16: '2008-08-21 21:50:07',
        14: '2008-08-22 21:50:07',
        12: '2008-08-23 21:50:07',
        18: '2008-08-24 21:50:07',
        13: '2008-08-25 21:50:07',
        20: '2008-08-26 21:50:07',
        9: '2008-08-27 21:50:07',
        11: '2008-08-28 21:50:07',
        10: '2008-08-29 21:50:07',
    }
    for count, date in date_count.items():
        for x in range(count):
            Encounter.objects.create(
                source_id=time.time(),
                patient_id=patient,
                start_date=date_count[count],
                end_date='2017-01-24 10:36:38',
            )

    call_command('get_metrics')
    out, err = capfd.readouterr()
    assert CONSOLE_STDOUT.replace('\n', '') == out.replace('\n', '')
