import json
from instances.management.commands.base_load_class import BaseLoadCommand
from instances.models import Patient


class Command(BaseLoadCommand):
    MODEL_CLASS = Patient
    FINAL_MESSAGE = 'loaded {} patients - elapsed time {}'

    def _process_object(self, line):
        json_object = json.loads(line)
        try:
            return [{
                'source_id': json_object['id'],
                'birth_date': json_object.get('birthDate', self.EMPTY_VALUE),
                'gender': json_object.get('gender', self.EMPTY_VALUE),
                'country': json_object.get('address', self.EMPTY_VALUE)[0].get('country', self.EMPTY_VALUE)
                if json_object.get('address', self.EMPTY_VALUE) else self.EMPTY_VALUE,
                'race_code': self._get_extension_value(
                    json_object,
                    'http://hl7.org/fhir/us/core/StructureDefinition/us-core-race',
                    'code'
                ),
                'race_code_system': self._get_extension_value(
                    json_object,
                    'http://hl7.org/fhir/us/core/StructureDefinition/us-core-race',
                    'system'
                ),
                'ethnicity_code': self._get_extension_value(
                    json_object,
                    'http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity',
                    'code'
                ),
                'ethnicity_code_system': self._get_extension_value(
                    json_object,
                    'http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity',
                    'system'
                )
            }]
        except ValueError:
            return None

    def _get_extension_value(self, json_object, url, value):
        extensions = json_object.get('extension')
        if extensions:
            for extension in extensions:
                if extension['url'] == url:
                    try:
                        return extension['valueCodeableConcept']['coding'][0][value]
                    except KeyError:
                        return self.EMPTY_VALUE
        return self.EMPTY_VALUE

