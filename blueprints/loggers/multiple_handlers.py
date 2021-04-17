'''
Python Logging Blueprint for Multiple Loggers.
'''
import argparse
import logging
from logging.handlers import TimedRotatingFileHandler

import logging_utils as lu


def create_multi_handler_logger(stdout_level, file_level, log_file='debug_level.log'):
    '''
    This function will set up a logger with two handlers. One handler for sending
    messages to stdout and another handler for sending messages to a file.
    '''
    # Create the logger.
    # Note - if the level of the logger is set to NOTSET then the handlers get to decide their
    # logging level.
    debug_logger = logging.getLogger('my_service_name')
    debug_logger.setLevel(logging.NOTSET)
    debug_logger.parent = None
    debug_logger.propagate = False

    # Create the formatter
    my_formatter = lu.create_formatter()

    # Create the handler and set the logging level.
    stdout_handler = lu.create_stdout_handler(stdout_level)

    # Create and add the formatter to the handler.
    stdout_handler.setFormatter(my_formatter)

    # Add the handler to the logger.
    debug_logger.addHandler(stdout_handler)

    # Setup the file handler to send messages to a file.
    file_handler = lu.create_file_handler(file_level, log_file)
    debug_logger.addHandler(file_handler)

    return debug_logger



if __name__ == '__main__':
    print(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument('-fl', '--file_level', help='Set logging level for the file handler.')
    parser.add_argument('-sl', '--stdout_level', help='Set logging level for stdout handler.')
    parser.add_argument('-pl', '--print_levels',
                        help='Print all log levels and their numeric values.',
                        action='store_true')
    parser.add_argument('-ph', '--print_handlers',
                        help='Print all handlers within the logger that is created.',
                        action='store_true')
    args = parser.parse_args()

    if args.file_level:
        FILE_LEVEL = lu.convert_logging_level(args.file_level)
    else:
        FILE_LEVEL = logging.NOTSET

    if args.stdout_level:
        STDOUT_LEVEL = lu.convert_logging_level(args.stdout_level)
    else:
        STDOUT_LEVEL = logging.NOTSET

    print('The current file_level is : ' + str(FILE_LEVEL))
    print('The current stdout_level is : ' + str(STDOUT_LEVEL))
    LOGGER = create_multi_handler_logger(STDOUT_LEVEL, FILE_LEVEL)
    lu.log_sample_messages(LOGGER)

    if args.print_handlers:
        lu.print_handlers(LOGGER)
    if args.print_levels:
        lu.print_logging_levels()
