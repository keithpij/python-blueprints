'''
This module contains utility functions that are used throughout the logging blueprints.

Utility list:
- convert_logging_level
- add_stdout_handler
- add_file_handler

'''
import logging
from logging.handlers import TimedRotatingFileHandler
import sys


def convert_logging_level(level):
    '''
    Convert a string version of level to one of the logging constants.
    '''
    if level == '10' or level.lower() == 'debug':
        return logging.DEBUG
    if level == '20' or level.lower() == 'info':
        return logging.INFO
    if level == '30' or level.lower() == 'warn':
        return logging.WARN
    if level == '30' or level.lower() == 'warning':
        return logging.WARN
    if level == '40' or level.lower() == 'error':
        return logging.ERROR
    if level == '50' or level.lower() == 'critical':
        return logging.CRITICAL
    if level.lower() == 'off':
        return logging.CRITICAL + 1

    return logging.NOTSET


def create_file_handler(level, log_file):
    '''
    Will create a file handler with the log_file parameter as the local file.
    '''
    file_handler = TimedRotatingFileHandler(log_file, when='midnight')
    file_handler.setFormatter(create_formatter())
    file_handler.setLevel(level)
    return file_handler


def create_formatter():
    format_string = '%(asctime)s — %(name)s — %(levelname)s — %(module)s:%(funcName)s:%(lineno)d — %(message)s'
    formatter = logging.Formatter(format_string)
    return formatter


def create_stdout_handler(level):
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(create_formatter())
    stdout_handler.setLevel(level)
    return stdout_handler


def log_sample_messages(logger):
    '''
    Sends a sample message for each logging level.
    '''
    logger.debug('This is a debug message.')
    logger.info('This is an info message')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    logger.critical('This is a critical message.')


def print_handlers(logger):
    handlers = logger.handlers
    for handler in handlers:
        print(handler)


def print_descendants(logger=None):
    '''
    This function will print all descendants of the passed in logger.
    Setting logger=None will cause this function to start at the root since logging.getLogger(None)
    returns the root logger.
    '''
    root_logger = logging.getLogger(logger)
    print(root_logger)
    for child_logger in root_logger.getChild(logger.name):
        print(child_logger)


def print_all_loggers():
    '''
    This function will print the root logger and all the loggers that have been created.
    '''
    loggers = [logging.getLogger()]  # get the root logger
    loggers = loggers + [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        print(logger)
        print(logger.parent)
        print('\n')


def print_logging_levels():
    print('\n')
    print('CRITICAL:', logging.CRITICAL)
    print('INFO:', logging.INFO)
    print('ERROR:', logging.ERROR)
    print('WARNING:', logging.WARNING)
    print('DEBUG:', logging.DEBUG)
    print('NOTSET:', logging.NOTSET)
    print('\n')
