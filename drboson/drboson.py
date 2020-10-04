from .DRBosonProducer import ClientProducer
import pathlib
import collections
from . import history
from . import messages
import json


class Run(object):
    def __init__(self, run_id="", project_id="", work_dir="", dataset_location=""):
        self.id = run_id
        self.project_id = project_id
        self.work_dir = pathlib.Path(work_dir)
        self.dataset_location = pathlib.Path(dataset_location)

        if self.work_dir.is_dir() is False:
            raise NotADirectoryError('drboson: Work directory is supposed to be a directory')

        # if self.dataset_location.is_dir() is False:
        #     raise NotADirectoryError('drboson: Data directory is supposed to be a directory')


class DRBoson:
    def __init__(self, run=Run(), producer=ClientProducer()):
        self.run = run
        self.producer = producer
        self.history = history.History(run, self.producer)

    def log(self, log, step=None, commit=True):
        if not isinstance(log, collections.Mapping):
            raise ValueError("drboson: log must be a dictionary")

        for key in log.keys():
            if not isinstance(key, str):
                raise KeyError('drboson: key values must be strings')

        self.history.add(log, step=step, commit=commit)

    def __prepare_message(self, message_type, payload):
        message = messages.make_communication_message(run_id=self.run.id,
                                                      project_id=self.run.project_id,
                                                      message_type=message_type,
                                                      payload=payload)
        return json.dumps(message)

    def save(self, filename):

        try:
            file_path = pathlib.Path(filename)
        except TypeError as e:
            raise Exception('drboson: Something went wrong. Report this to DRBoson')

        if not file_path.exists():
            raise FileNotFoundError(f'drboson: File {file_path} does not exist')

        if file_path.is_file() is False:
            raise TypeError(f'drboson: {file_path} is not a file')

        if self.run.work_dir not in file_path.absolute().parents:
            raise PermissionError(f'drboson: {file_path} is not in the work directory')

        message = self.__prepare_message(message_type='file', payload=str(file_path.absolute()))
        self.producer.produce(message)

    def started(self):
        message = self.__prepare_message(message_type='status', payload='running')
        self.producer.produce(message)

    def completed(self):
        message = self.__prepare_message(message_type='status', payload='completed')
        self.producer.produce(message)

    def failed(self):
        message = self.__prepare_message(message_type='status', payload='failed')
        self.producer.produce(message)
