from confluent_kafka import Producer
import abc
import sys
import json


class DRBosonProducer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def produce(self, message):
        raise NotImplementedError

    @abc.abstractmethod
    def flush(self):
        raise NotImplementedError


class RemoteProducer(DRBosonProducer):
    def __init__(self, conf, topic):
        self.producer = Producer(conf)
        self.topic = topic

    @staticmethod
    def __delivery_callback(err, msg):
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write('%% Message delivered to %s [%d] @ %d\n' %
                             (msg.topic(), msg.partition(), msg.offset()))

    @staticmethod
    def __preprocess_message(message):
        return message

    def produce(self, message):
        preprocessed_message = RemoteProducer.__preprocess_message(message)

        try:
            self.producer.produce(self.topic, value=preprocessed_message, callback=RemoteProducer.__delivery_callback)
            self.producer.poll(1)
        except BufferError as e:
            self.producer.poll(10)
            self.producer.produce(self.topic, value=preprocessed_message, callback=RemoteProducer.__delivery_callback)

    def flush(self):
        self.producer.flush()


class ClientProducer(DRBosonProducer):

    @staticmethod
    def __file_message(payload):
        return f"[+] The file {payload} has been successfully saved!"

    @staticmethod
    def __log_message(payload):
        return f"[+] Log: {payload}"

    @staticmethod
    def __preprocess_message(message):
        message = json.loads(message)
        types = {
            'file': ClientProducer.__file_message,
            'log': ClientProducer.__log_message
        }
        message_type = message['type']

        return types[message_type](message['payload'])

    def produce(self, message):
        processed_message = ClientProducer.__preprocess_message(message)

        print(processed_message)

    def flush(self):
        pass
