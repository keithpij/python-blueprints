import argparse
import os

from blueprints.loggers import basic_logger


def log_sample_messages():
    '''
    Sends a sample message for each logging level.
    '''
    queue_name = 'orders'
    message_data = {'customerId': 42, 'productId': 12345, 'quantity': 5}
    attempt = 2

    logger = basic_logger.get_logger()
    logger.debug('Message recieved from queue: %s, message data: %s', queue_name, message_data)
    logger.info('Message received from queue: %s', queue_name)
    logger.warning('Old message format detected. Queue: %s, Message data: %s', queue_name, message_data)
    logger.error('Could not connect to queue. Attempt: %i', attempt, stack_info=True)
    logger.critical('Error processing message from queue: %s, message_data: %s.',
                     queue_name, message_data, stack_info=True)


if __name__ == '__main__':
    # Setup all the CLI arguments for this module.
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--logger_name',
                        help='Specify the name of your logger.')
    parser.add_argument('-l', '--logging_level',
                        help='Specify a logging level (NOTSET, DEBUG, INFO, WARNING, ERROR, or CRITICAL) for the basic logger.')

    # Parse what was passed in.
    args = parser.parse_args()

    # Get the name of the logger.
    if args.logger_name:
        os.environ['LOGGER_NAME'] = args.logger_name
    else:
        os.environ['LOGGER_NAME'] = __name__

    # Get the level to be used for the logger's handler.
    if args.logging_level:
        os.environ['LOGGING_LEVEL'] = args.logging_level
    else:
        os.environ['LOGGING_LEVEL'] = 'INFO'

    os.environ['FORMAT_STRING'] = '%(asctime)s — %(name)s — %(levelname)s — %(module)s:%(funcName)s:%(lineno)d — %(message)s'
    print('Logger name: ' + os.environ['LOGGER_NAME'])
    print('Logging level: ' + os.environ['LOGGING_LEVEL'])
    print('Format: ' + os.environ['FORMAT_STRING'])
    basic_logger.create_logger()
    log_sample_messages()
