'''
A Basic Python Logging Blueprint.
'''
import argparse
import logging

import logging_utils as lu


def create_microservice_logger(level):
    '''
    Creates a logger with no parent and a stdout handler.
    '''
    # Create and configure the logger.
    basic_logger = logging.getLogger('my_service_name')
    basic_logger.setLevel(logging.NOTSET)
    basic_logger.parent = None
    basic_logger.propagate = False

    # Create the handler and set the logging level.
    stdout_handler = lu.create_stdout_handler(level)

    # Create and add the formatter to the handler.
    stdout_handler.setFormatter(lu.create_formatter())

    # Add the handler to the logger.
    basic_logger.addHandler(stdout_handler)

    return basic_logger


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logging_level',
                        help='Specify a logging level (NOTSET, DEBUG, INFO, WARNING, ERROR, or CRITICAL) for the basic logger.')
    parser.add_argument('-pl', '--print_levels',
                        help='Print all log levels and their numeric values.',
                        action='store_true')
    parser.add_argument('-ph', '--print_handlers',
                        help='Print all handlers within the logger that is created.',
                        action='store_true')
    args = parser.parse_args()

    if args.logging_level:
        LEVEL = lu.convert_logging_level(args.logging_level)
        print('The current level is : ' + str(LEVEL))
        LOGGER = create_microservice_logger(LEVEL)
        lu.log_sample_messages(LOGGER)
    if args.print_handlers:
        lu.print_handlers(LOGGER)
    if args.print_levels:
        lu.print_logging_levels()
