import json
from instances.management.commands.base_load_class import BaseLoadCommand
from instances.models import Observation


class Command(BaseLoadCommand):
    MODEL_CLASS = Observation
    FINAL_MESSAGE = 'loaded {} observations - elapsed time {}'

    def _process_object(self, line):
        json_object = json.loads(line)
        if json_object.get('component'):
            return self._process_objects(json_object)
        try:
            return [{
                'source_id': json_object['id'],
                'patient_id_id': json_object['subject']['reference'].replace('Patient/', ''),
                'encounter_id_id': json_object['context'].get('reference', self.EMPTY_VALUE).replace('Encounter/', '')
                if json_object.get('context') else self.EMPTY_VALUE,
                'observation_date': json_object['effectiveDateTime'],
                'type_code': json_object['code']['coding'][0]['code'],
                'type_code_system': json_object['code']['coding'][0]['system'],
                'value': json_object['valueQuantity']['value'],
                'unit_code': json_object['valueQuantity'].get('unit', self.EMPTY_VALUE)
                if json_object.get('valueQuantity') else self.EMPTY_VALUE,
                'unit_code_system': json_object['valueQuantity'].get('system', self.EMPTY_VALUE)
                if json_object.get('valueQuantity') else self.EMPTY_VALUE,
            }]
        except (ValueError, KeyError, IndexError):
            return None

    def _process_objects(self, json_object):
        output = []
        base = {
            'source_id': json_object['id'],
            'patient_id_id': json_object['subject']['reference'].replace('Patient/', ''),
            'encounter_id_id': json_object['context'].get('reference', self.EMPTY_VALUE).replace('Encounter/', '')
            if json_object.get('context') else self.EMPTY_VALUE,
            'observation_date': json_object['effectiveDateTime'],
        }

        for component in json_object.get('component'):
            try:
                output.append(
                    {
                        **base,
                        'type_code': component['code']['coding'][0]['code'],
                        'type_code_system': component['code']['coding'][0]['system'],
                        'value': component['valueQuantity']['value'],
                        'unit_code': component['valueQuantity'].get('unit', self.EMPTY_VALUE)
                        if component.get('valueQuantity') else self.EMPTY_VALUE,
                        'unit_code_system': component['valueQuantity'].get('system', self.EMPTY_VALUE)
                        if component.get('valueQuantity') else self.EMPTY_VALUE,
                    }
                )
            except (IndexError, KeyError):
                pass
        return output
