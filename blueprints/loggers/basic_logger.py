'''
Basic Python Logging Blueprint.
This module requires the following environment variables to be set:
LOGGER_NAME, LOGGING_LEVEL, and FORMAT_STRING. Sample values are below:

export LOGGING_LEVEL = INFO
export LOGGER_NAME = my_service
export FORMAT_STRING = "%(asctime)s — %(name)s — %(levelname)s — %(module)s:%(funcName)s:%(lineno)d — %(message)s"

'''
import logging
import os
import sys


def get_logger():
    '''
    Return the logger that has been created with the name found in the LOGGER_NAME
    environment variable.
    '''
    return logging.getLogger(os.environ['LOGGER_NAME'])


def create_logger():
    '''
    Creates a logger with a StreamHandler that sends messages to stdout.
    '''
    # Create the logger and set the level.
    basic_logger = logging.getLogger(os.environ['LOGGER_NAME'])
    basic_logger.setLevel(os.environ['LOGGING_LEVEL'])
    basic_logger.parent = None
    basic_logger.propagate = False

    # Create the handler and add it to the logger.
    stdout_handler = logging.StreamHandler(sys.stdout)
    basic_logger.addHandler(stdout_handler)

    # Create and add the formatter to the handler.
    format_string = os.environ['FORMAT_STRING']
    my_formatter = logging.Formatter(format_string)
    stdout_handler.setFormatter(my_formatter)

    return basic_logger
