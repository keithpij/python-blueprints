'''
Python Logging Blueprint for Multiple Loggers.
'''
import argparse
import logging

from blueprints.loggers import basic_logger
from blueprints.loggers import logging_utils as lu


def create_multiple_loggers():
    """
    This function will create a parent logger with children loggers.
    The passed in parameters must be lists where the f

    Creates a logger with a StreamHandler that sends messages to stdout. The logging level of
    the logger itself is set to NOTSET. The logging level of the handler is set to the value
    passed in via the logging_level parameter.

    The logging level must numeric. Typically it is one of the contants found in the logging
    module (ex. logging.INFO) but it can be any number. As an example, setting it to
    logging.CRITICAL + 1 will turn off the handler.

    Setting propagate_message to True will cause messages to be sent to parent loggers where
    the messages will be sent to the parents handlers regardless of the level of the logger.
    When this parameter is false the logger will behave like a root logger.

    IMPORTANT: If the logger is set to NOTSET then the logger will propagate to the parent
    regardless of how the propagate property is set.

    """
    logging_config = lu.get_logging_metadata('logging_config.json')

    # Create the parent logger.
    parent_name = logging_config['parent']['name']
    parent_level = lu.convert_logging_level(logging_config['parent']['level'])
    basic_logger.create_basic_logger(parent_name, parent_level)
    #parent_logger = logging.getLogger(parent_name)
    #parent_logger.setLevel(parent_level)

    # Create the child loggers. Note that the parent name is added as a prefix to the child names.
    # This is a requirement of the logging module. It establishes a parent/child relationship within
    # the logger.
    for child in logging_config['children']:
        child_name = parent_name + '.' + child['name']
        child_level = lu.convert_logging_level(child['level'])
        basic_logger.create_basic_logger(child_name, child_level)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-pl', '--print_levels',
                        help='Print all log levels and their numeric values.',
                        action='store_true')
    parser.add_argument('-ph', '--print_handlers',
                        help='Print all handlers within all loggers.',
                        action='store_true')
    parser.add_argument('-pal', '--print_all_loggers',
                        help='Print all loggers.',
                        action='store_true')
    parser.add_argument('-s', '--sample_logger',
                        help='Logger to use for sending sample messages.')
    args = parser.parse_args()

    # Create the parent logger.
    create_multiple_loggers()

    if args.print_all_loggers:
        lu.print_all_loggers()

    if args.print_handlers:
        lu.print_handlers()

    if args.print_levels:
        lu.print_logging_levels()

    # Send sample messages to the specified logger.
    if args.sample_logger:
        lu.log_sample_messages(args.sample_logger)
