'''
Python Logging Blueprint for Multiple Loggers.
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


def add_stdout_handler(service_logger, level):
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(level)
    service_logger.addHandler(stdout_handler)


def add_file_handler(service_logger, log_file, level):
    file_handler = TimedRotatingFileHandler(log_file, when='midnight')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    service_logger.addHandler(file_handler)


def log_sample_messages(logger):
    '''
    Sends a sample message for each logging level.
    '''
    logger.debug('This is a debug message.')
    logger.info('This is an info message')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    logger.critical('This is a critical message.')


if __name__ == '__main__':
    print(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Send logs to the specified file using a file handler.')
    parser.add_argument('-fl', '--file_level', help='Set logging level for the file.')
    parser.add_argument('-s', '--stdout', help='Send logs to stdout using the stream handler.', action='store_true')
    parser.add_argument('-sl', '--stdout_level', help='Set logging level for stdout.')
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
    if args.multiple:
        print_logger_relationships()
