'''
This module contains utility functions that are used throughout the logging blueprints.

Utility list:
- convert_logging_level
- add_stdout_handler
- add_file_handler

'''
from collections import defaultdict
import json
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys


def get_logging_metadata(config_file_name):
    current_folder = os.path.dirname(__file__)
    logging_config_file = os.path.join(current_folder, config_file_name)
    logging_config = defaultdict(def_value)

    if os.path.isfile(logging_config_file):
        with open(logging_config_file, 'r') as file_handle:
            logging_config = json.load(file_handle)
    else:
        msg = logging_config_file + ' does not exist.'
        raise FileNotFoundError(msg)

    return logging_config


def def_value():
    '''
    This Function will return a default values for keys not present in a defaultdict.
    '''
    return "Not Present"


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


def log_sample_messages(logger_name):
    '''
    Sends a sample message for each logging level.
    '''
    logger = logging.getLogger(logger_name)
    logger.debug('This is a debug message.')
    logger.info('This is an info message')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    logger.critical('This is a critical message.')


def print_handlers():
    loggers = logging.getLogger()
    loggers = loggers + [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        handlers = logger.handlers
        for handler in handlers:
            print(handler)


def get_children(parent_logger):
    '''
    This function will return all children of the passed in logger.
    Do not set logger=None as the getChild method does not work on the root logger.
    '''
    children = []
    parent_name = parent_logger.name
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        if logger.name[0:len(parent_name)] == parent_name:
            children.append(logger)
    return children


def print_all_loggers():
    '''
    This function will print the root logger and all the loggers that have been created.
    '''
    # Get the root logger.
    root_logger = logging.getLogger()
    print_logger_info(root_logger)

    # This will return all the logger that were created by a service.
    # It does not get the root logger.
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        if logger.parent is logging.getLogger():
            print_logger_info(logger, '\t')

            children = get_children(logger)
            for child_logger in children:
                print_logger_info(child_logger, '\t\t')


def print_logger_info(logger, indent=''):
    logger_name = logger.name
    level_name = logging.getLevelName(logger.level)
    effective_level_name = logging.getLevelName(logger.getEffectiveLevel())
    print('{}{} - {}'.format(indent, logger_name, level_name))
    print('{}Effective Level: {}'.format(indent, effective_level_name))
    print('{}Propagate: {}\n'.format(indent, logger.propagate))


def print_logging_levels():
    print('\n')
    print('CRITICAL:', logging.CRITICAL)
    print('INFO:', logging.INFO)
    print('ERROR:', logging.ERROR)
    print('WARNING:', logging.WARNING)
    print('DEBUG:', logging.DEBUG)
    print('NOTSET:', logging.NOTSET)
    print('\n')
