'''
Python Logging Blueprint for Multiple Loggers.
'''
import argparse
import logging

import logging_utils as lu


def create_monolith_logger(parent_name, children_names, level):
    parent_logger = logging.getLogger(parent_name)
    parent_logger.setLevel(level)
    for child_name in children_names:
        child_logger = logging.getLogger(parent_name + '.' + child_name)
        child_logger.setLevel(logging.NOTSET)
    return parent_logger


def print_logger_relationships(parent_logger=None):
    '''
    If None is used in the getLogger function then the root logger will be returned.
    '''
    root_logger = logging.getLogger(None)
    print(root_logger.getChild())
    my_svc, sales_predictions, sales_reports, iot_telemetry, data_access = create_logger_family()
    print(my_svc.parent.name)
    print(type(logging.getLogger('root')))

    if my_svc.parent is logging.getLogger(None):
        print('The parent of my_svc is root.')
    if sales_predictions.parent is logging.getLogger('my_svc'):
        print('The parent of sales_predictions is my_svc.')
    if sales_reports.parent is logging.getLogger('my_svc'):
        print('The parent of sales_reports is my_svc.')
    if iot_telemetry.parent is logging.getLogger('my_svc'):
        print('The parent of iot_telemetry is my_svc.')
    if data_access.parent is logging.getLogger('my_svc'):
        print('The parent of data_access is my_svc.')


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
        PARENT_NAME = 'my_svc'
        CHILDREN_NAMES = ['sales_predictions', 'sales_reports', 'iot_telemtry', 'data_access']
        LOGGER = create_monolith_logger(PARENT_NAME, CHILDREN_NAMES, LEVEL)
        lu.log_sample_messages(LOGGER)

    if args.print_handlers:
        lu.print_handlers(LOGGER)

    if args.print_levels:
        lu.print_logging_levels()
