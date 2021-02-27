'''
Python Logging Blueprint
'''
import argparse
import logging
from logging.handlers import TimedRotatingFileHandler
import sys


format_string = '%(asctime)s — %(name)s — %(levelname)s — %(module)s:%(funcName)s:%(lineno)d — %(message)s'
formatter = logging.Formatter(format_string)


def create_logger_with_multiple_handlers():
    service_logger = logging.getLogger('my_service_name')
    service_logger.setLevel(logging.NOTSET)
    service_logger.parent = None
    service_logger.propagate = False
    log_file = "my_app.log"
    add_stdout_handler(service_logger, logging.INFO)
    add_file_handler(service_logger, log_file, logging.DEBUG)
    return service_logger


def create_stdout_logger(level):
    '''
    Creates a logger with no parent and a stdout handler.
    '''
    # Create and configure the logger.
    my_logger = logging.getLogger('my_service_name')
    my_logger.setLevel(logging.NOTSET)
    my_logger.parent = None
    my_logger.propagate = False

    # Create the handler and set the logging level.
    my_handler = logging.StreamHandler(sys.stdout)
    my_handler.setLevel(level)

    # Create the formatter.
    format_string = '%(asctime)s — %(name)s — %(levelname)s — %(module)s:%(funcName)s:%(lineno)d — %(message)s'
    my_formatter = logging.Formatter(format_string)

    # Add the formatter to the handler.
    my_handler.setFormatter(my_formatter)

    # Add the handler to the logger.
    my_logger.addHandler(my_handler)

    return my_logger


def create_file_logger(log_file, level):
    '''
    Creates a logger with no parent and a stdout handler.
    '''
    # Create and configure the logger.
    logger = logging.getLogger('my_service_name')
    logger.setLevel(logging.NOTSET)
    logger.parent = None
    logger.propagate = False

    # Create the handler and set the logging level.
    handler = TimedRotatingFileHandler(log_file, when='midnight')
    handler.setLevel(level)

    # Create the formatter.
    format_string = '%(asctime)s — %(name)s — %(levelname)s — %(module)s:%(funcName)s:%(lineno)d — %(message)s'
    formatter = logging.Formatter(format_string)

    # Add the formatter to the handler.
    handler.setFormatter(formatter)

    # Add the handler to the logger.
    logger.addHandler(handler)

    return logger


def add_stdout_handler(service_logger, level=None):
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    if level is not None:
        stdout_handler.setLevel(level)
    service_logger.addHandler(stdout_handler)


def add_file_handler(service_logger, log_file, level=None):
    file_handler = TimedRotatingFileHandler(log_file, when='midnight')
    file_handler.setFormatter(formatter)
    if level is not None:
        file_handler.setLevel(level)
    service_logger.addHandler(file_handler)


def print_logging_levels():
    print('\n')
    print('CRITICAL:', logging.CRITICAL)
    print('INFO:', logging.INFO)
    print('ERROR:', logging.ERROR)
    print('WARN:', logging.WARN)
    print('DEBUG:', logging.DEBUG)
    print('NOTSET:', logging.NOTSET)
    print('\n')


def log_sample_messages(logger):
    '''
    Sends a sample message for each logging level.
    '''
    logger.debug('This is a debug message.')
    logger.info('This is an info message')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    logger.critical('This is a critical message.')


def convert_level(level):
    '''
    Convert a string version of level to one of the constants.
    '''
    if level == '10' or level.lower() == 'debug':
        return logging.DEBUG
    elif level == '20' or level.lower() == 'info':
        return logging.INFO
    elif level == '30' or level.lower() == 'warn':
        return logging.WARN
    elif level == '40' or level.lower() == 'error':
        return logging.ERROR
    elif level == '50' or level.lower() == 'critical':
        return logging.WARN
    else:
        return logging.NOTSET
    

if __name__ == '__main__':
    print(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Send logs to the specified file using a file handler.')
    parser.add_argument('-fl', '--file_level', help='Set logging level for the file.')
    parser.add_argument('-s', '--stdout', help='Send logs to stdout using the stream handler.', action='store_true')
    parser.add_argument('-sl', '--stdout_level', help='Set logging level for stdout.')
    parser.add_argument('-pl', '--print_levels', help='Print all log levels and their numeric values.', action='store_true')
    args = parser.parse_args()

    if args.file:
        level = convert_level(args.file_level)
        logger = create_file_logger(args.file, level)
        log_sample_messages(logger)
    if args.stdout:
        level = convert_level(args.stdout_level)
        logger = create_stdout_logger(level)
        log_sample_messages(logger)
    if args.print_levels:
        print_logging_levels()
