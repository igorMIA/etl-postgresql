import time
from abc import ABC, abstractmethod
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError


class BaseLoadCommand(BaseCommand, ABC):
    COUNT = 0
    CHUNK_SIZE = 32
    EMPTY_VALUE = ''
    FINAL_MESSAGE = 'loaded {} instances - elapsed time {}'
    MODEL_CLASS = None

    help = 'Create new Instance instances from ndjson file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='path to json file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        try:
            start_time = time.time()

            with open(file_path, 'r') as f:
                tmp = []
                for line in f:
                    obj = self._process_object(line)
                    if obj:
                        tmp.extend(obj)
                    if len(tmp) == self.CHUNK_SIZE:
                        self._write_objects(tmp)
                        tmp = []
                if len(tmp) != self.CHUNK_SIZE:
                    self._write_objects(tmp)

            elapsed_time = time.time() - start_time
            print(self.FINAL_MESSAGE.format(self.COUNT, elapsed_time))
        except FileNotFoundError:
            raise CommandError('Cannot find file "%s"' % file_path)

    @abstractmethod
    def _process_object(self, line):
        pass

    def _write_objects(self, list_of_objects):
        objects = [self.MODEL_CLASS(**obj) for obj in list_of_objects]
        try:
            self.COUNT += len(self.MODEL_CLASS.objects.bulk_create(objects, ignore_conflicts=True,
                                                                   batch_size=self.CHUNK_SIZE))
        except IntegrityError:
            for obj in objects:
                try:
                    obj.save()
                    self.COUNT += 1
                except IntegrityError:
                    continue
