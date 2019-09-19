# Generated by Django 2.2.4 on 2019-09-18 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Encounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.TextField(unique=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('type_code', models.TextField(blank=True, null=True)),
                ('type_code_system', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.TextField(unique=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('gender', models.TextField(blank=True, null=True)),
                ('race_code', models.TextField(blank=True, null=True)),
                ('race_code_system', models.TextField(blank=True, null=True)),
                ('ethnicity_code', models.TextField(blank=True, null=True)),
                ('ethnicity_code_system', models.TextField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.TextField()),
                ('procedure_date', models.DateTimeField()),
                ('type_code', models.TextField()),
                ('type_code_system', models.TextField()),
                ('encounter_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='instances.Encounter', to_field='source_id')),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instances.Patient', to_field='source_id')),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.TextField()),
                ('observation_date', models.DateTimeField()),
                ('type_code', models.TextField()),
                ('type_code_system', models.TextField()),
                ('value', models.DecimalField(decimal_places=10, max_digits=19)),
                ('unit_code', models.TextField(blank=True, null=True)),
                ('unit_code_system', models.TextField(blank=True, null=True)),
                ('encounter_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='instances.Encounter', to_field='source_id')),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instances.Patient', to_field='source_id')),
            ],
        ),
        migrations.AddField(
            model_name='encounter',
            name='patient_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instances.Patient', to_field='source_id'),
        ),
    ]