from django.db import models


class Patient(models.Model):
    source_id = models.TextField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.TextField(null=True, blank=True)
    race_code = models.TextField(null=True, blank=True)
    race_code_system = models.TextField(null=True, blank=True)
    ethnicity_code = models.TextField(null=True, blank=True)
    ethnicity_code_system = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)


class Encounter(models.Model):
    source_id = models.TextField(unique=True)
    patient_id = models.ForeignKey('Patient', on_delete=models.CASCADE, to_field='source_id')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    type_code = models.TextField(null=True, blank=True)
    type_code_system = models.TextField(null=True, blank=True)


class Procedure(models.Model):
    source_id = models.TextField()
    patient_id = models.ForeignKey('Patient', on_delete=models.CASCADE, to_field='source_id')
    encounter_id = models.ForeignKey('Encounter', on_delete=models.CASCADE, null=True, blank=True, to_field='source_id')
    procedure_date = models.DateTimeField()
    type_code = models.TextField()
    type_code_system = models.TextField()


class Observation(models.Model):
    source_id = models.TextField()
    patient_id = models.ForeignKey('Patient', on_delete=models.CASCADE, to_field='source_id')
    encounter_id = models.ForeignKey('Encounter', on_delete=models.CASCADE, null=True, blank=True, to_field='source_id')
    observation_date = models.DateTimeField()
    type_code = models.TextField()
    type_code_system = models.TextField()
    value = models.DecimalField(max_digits=19, decimal_places=10)
    unit_code = models.TextField(null=True, blank=True)
    unit_code_system = models.TextField(null=True, blank=True)
