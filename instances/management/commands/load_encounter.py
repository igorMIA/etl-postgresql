import datetime
import json
from instances.management.commands.base_load_class import BaseLoadCommand
from instances.models import Encounter


class Command(BaseLoadCommand):
    MODEL_CLASS = Encounter
    FINAL_MESSAGE = 'loaded {} encounters - elapsed time {}'

    def _process_object(self, line):
        json_object = json.loads(line)
        return [{
            'source_id': json_object['id'],
            'patient_id_id': json_object['subject']['reference'].replace('Patient/', ''),
            'start_date': datetime.datetime.strptime(json_object['period']['start'], "%Y-%m-%dT%H:%M:%S%z"),
            'end_date': datetime.datetime.strptime(json_object['period']['end'], "%Y-%m-%dT%H:%M:%S%z"),
            'type_code': self._get_type_code(json_object, 'code'),
            'type_code_system': self._get_type_code(json_object, 'system')
        }]

    def _get_type_code(self, json_object, code):
        try:
            return json_object['type'][0]['coding'][0][code]
        except (IndexError, KeyError):
            return self.EMPTY_VALUE
