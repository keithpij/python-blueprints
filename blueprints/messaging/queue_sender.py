'''
Need to install azure-servicebus
pip install azure-servicebus
'''
import argparse

from azure.identity import EnvironmentCredential
from azure.servicebus import ServiceBusClient, ServiceBusMessage

from blueprints.messaging import utils


class SenderManager():
    '''
    Context Manager for the queue sender.
    '''
    def __init__(self, namespace_name, queue_name):
        self.namespace_name = namespace_name
        self.queue_name = queue_name
        self.servicebus_client = None
        self.sender = None

    def __enter__(self):
        utils.load_env_vars()
        credential = EnvironmentCredential()
        self.servicebus_client = ServiceBusClient(self.namespace_name, credential)
        self.sender = self.servicebus_client.get_queue_sender(queue_name=self.queue_name)
        return self.sender
      
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.sender.close()
        self.servicebus_client.close()


class QueueSender():
    '''
    Class to manage a queue sender.
    '''
    def __init__(self, namespace_name, queue_name):
        self.namespace_name = namespace_name
        self.queue_name = queue_name
        utils.load_env_vars()
        self.credential = EnvironmentCredential()

    def send(self, message):
        '''
        Send a single message to the queue.
        '''
        with SenderManager(self.namespace_name, self.queue_name) as sender:
            sender.send_messages(ServiceBusMessage(message))

    def send_list(self, message_list):
        '''
        This method will put one message on the queue for each entry in message_list.
        '''
        messages = [ServiceBusMessage(m) for m in message_list]
        with SenderManager(self.namespace_name, self.queue_name) as sender:
            sender.send_messages(messages)


def send_batch(namespace_name, queue_name, message_batch):
    batch_message = sender.create_message_batch()
    for _ in range(10):
        try:
            batch_message.add_message(ServiceBusMessage('Message inside a ServiceBusMessageBatch'))
        except ValueError:
            # ServiceBusMessageBatch object reaches max_size.
            # New ServiceBusMessageBatch object can be created here to send more data.
            break
    sender.send_messages(batch_message)


def create_batch(sender):
    batch_message = sender.create_message_batch()
    for _ in range(10):
        try:
            batch_message.add_message(ServiceBusMessage('Message inside a ServiceBusMessageBatch'))
        except ValueError:
            # ServiceBusMessageBatch object reaches max_size.
            # New ServiceBusMessageBatch object can be created here to send more data.
            break


def test_send_batch():
    pass


def test_send_list(namespace_name, queue_name):
    message_list = ['Message {} in list'.format(i) for i in range(10)]
    queue_sender = QueueSender(namespace_name, queue_name)
    queue_sender.send_list(message_list)
    print('Message list sucessfully sent to queue {}.'.format(queue_name))


def test_send():
    pass


class Point():
    '''
    Class to create an object that holds x and y coordinates.
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--namespace',
                        help='Namespace name.')
    parser.add_argument('-q', '--queue',
                        help='Queue name.')
    parser.add_argument('-m', '--message',
                        help='Message.')
    parser.add_argument('-l', '--message_list',
                        help='Send a message list test.',
                        action='store_true')
    # Parse what was passed in.
    args = parser.parse_args()

    if args.message:
        QUEUE_SENDER = QueueSender(args.namespace, args.queue)
        QUEUE_SENDER.send(args.message)
        print('Message: {} sucessfully sent to queue {}.'.format(args.message, args.queue))
    if args.message_list:
        test_send_list(args.namespace, args.queue)