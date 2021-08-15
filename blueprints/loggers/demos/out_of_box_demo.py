'''
Out of the box demo of Python's logging library.
'''
import logging


def demo():
    '''
    This is an out of the box demo of Python's logging library.
    It uses the default logger which is ready to use once the logger
    has been imported. You should not use the default logger in production
    code unless you are building a library.
    '''
    queue_name = 'orders'
    message_data = {'customerId': 42, 'productId': 12345, 'quantity': 5}
    attempt = 2

    logging.debug('Message recieved from queue: %s, message data: %s', queue_name, message_data)
    logging.info('Message received from queue: %s', queue_name)
    logging.warning('Old message format detected. Queue: %s, Message data: %s', queue_name, message_data)
    logging.error('Could not connect to queue. Attempt: %i', attempt)
    logging.critical('Error processing message from queue: %s, message_data: %s.',
                     queue_name, message_data)
    #logging.error('Could not connect to queue. Attempt: %i', attempt, stack_info=True)
    #logging.critical('Error processing message from queue: %s, message_data: %s.',
    #                 queue_name, message_data, stack_info=True)

if __name__ == '__main__':
    #logging.getLogger().setLevel(logging.DEBUG)
    demo()
