'''
A Basic Python Logging Blueprint.
'''
import argparse
import logging

from blueprints.loggers import logging_utils as lu


def create_basic_logger(logger_name, logging_level, propagate_message=True):
    '''
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
    '''

    # Create and configure the logger.
    basic_logger = logging.getLogger(logger_name)
    basic_logger.setLevel(logging_level)
    #basic_logger.parent = None
    basic_logger.propagate = propagate_message

    # Create the handler and set the logging level.
    stdout_handler = lu.create_stdout_handler(logging_level)

    # Create and add the formatter to the handler.
    stdout_handler.setFormatter(lu.create_formatter())

    # Add the handler to the logger.
    basic_logger.addHandler(stdout_handler)

    return basic_logger


if __name__ == '__main__':
    # Setup all the CLI arguments for this module.
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--logger_name',
                        help='Specify the name of your logger.')
    parser.add_argument('-l', '--logging_level',
                        help='Specify a logging level (NOTSET, DEBUG, INFO, WARNING, ERROR, or CRITICAL) for the basic logger.')
    parser.add_argument('-pl', '--print_levels',
                        help='Print all log levels and their numeric values.',
                        action='store_true')
    parser.add_argument('-ph', '--print_handlers',
                        help='Print all handlers within the logger that is created.',
                        action='store_true')
    parser.add_argument('-pal', '--print_all_loggers',
                        help='Print all loggers.',
                        action='store_true')

    # Parse what was passed in. This will also check the arguments for you and produce
    # a help message is something is wrong.
    args = parser.parse_args()

    # Get the name of the logger.    
    if args.logger_name:
        NAME = args.logger_name
    else:
        NAME = __name__

    # get the level to be used for the logger's handler.
    if args.logging_level:
        LEVEL = lu.convert_logging_level(args.logging_level)
    else:
        LEVEL = logging.INFO

    print('The current level is : ' + str(LEVEL))
    LOGGER = create_microservice_logger(NAME, LEVEL, False)
    lu.log_sample_messages(LOGGER)

    # Print all handlers
    if args.print_handlers:
        lu.print_handlers(LOGGER)

    # Print logging levels.
    if args.print_levels:
        lu.print_logging_levels()

    # Print all loggers.
    if args.print_all_loggers:
        lu.print_all_loggers()
