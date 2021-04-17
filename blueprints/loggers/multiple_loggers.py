'''
Python Logging Blueprint for Multiple Loggers.
'''
import argparse
import logging

from blueprints.loggers import basic_logger
from blueprints.loggers import logging_utils as lu


def create_multiple_loggers(parent, children):
    """
    This function will create a parent logger with children loggers.
    The passed in parameters must be lists where the f
    """
    parent_logger = logging.getLogger(parent[0])
    parent_logger.setLevel(parent[1])
    for child in children:
        child_name = parent[0] + '.' + child[0]
        basic_logger.create_basic_logger(child_name, child[1])
    return parent_logger


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-pl', '--print_levels',
                        help='Print all log levels and their numeric values.',
                        action='store_true')
    parser.add_argument('-ph', '--print_handlers',
                        help='Print all handlers within the logger that is created.',
                        action='store_true')
    parser.add_argument('-pal', '--print_all_loggers',
                        help='Print all loggers.',
                        action='store_true')
    args = parser.parse_args()

    PARENT = ['my_svc', logging.INFO]
    CHILDREN = [['sales_predictions', logging.DEBUG], ['sales_reports', logging.INFO], ['iot_telemtry', logging.INFO], ['data_access', logging.INFO]]
    PARENT_LOGGER = create_multiple_loggers(PARENT, CHILDREN)
    lu.log_sample_messages(PARENT_LOGGER)

    if args.print_all_loggers:
        lu.print_all_loggers()

    if args.print_handlers:
        lu.print_handlers(PARENT_LOGGER)

    if args.print_levels:
        lu.print_logging_levels()
