import json
from instances.management.commands.base_load_class import BaseLoadCommand
from instances.models import Procedure


class Command(BaseLoadCommand):
    MODEL_CLASS = Procedure
    FINAL_MESSAGE = 'loaded {} procedures - elapsed time {}'

    def _process_object(self, line):
        json_object = json.loads(line)
        try:
            return [{
                'source_id': json_object['id'],
                'patient_id_id': json_object['subject']['reference'].replace('Patient/', ''),
                'encounter_id_id': json_object['context'].get('reference', self.EMPTY_VALUE).replace('Encounter/', '')
                if json_object.get('context') else self.EMPTY_VALUE,
                'procedure_date': self._get_procedure_date(json_object),
                'type_code': json_object['code']['coding'][0]['code'],
                'type_code_system': json_object['code']['coding'][0]['system']
            }]
        except (ValueError, KeyError, IndexError):
            return None

    @staticmethod
    def _get_procedure_date(json_object):
        if json_object.get('performedDateTime'):
            return json_object['performedDateTime']
        return json_object['performedPeriod']['start']
