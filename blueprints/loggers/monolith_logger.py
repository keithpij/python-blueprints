'''
Python Logging Blueprint for Multiple Loggers.
'''
import argparse
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

import logging_utils as lu


def create_logger_family():
    my_svc = logging.getLogger('my_svc')
    sales_predictions = logging.getLogger('my_svc.sales_predictions')
    sales_reports = logging.getLogger('my_svc.sales_reports')
    iot_telemetry = logging.getLogger('my_svc.iot_telemetry')
    data_access = logging.getLogger('my_svc.data_access')
    return my_svc, sales_predictions, sales_reports, iot_telemetry, data_access


def print_logger_relationships():
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


def create_stdout_logger(name, level):
    '''
    Creates a logger with no parent and a stdout handler.
    '''
    # Create and configure the logger.
    my_logger = logging.getLogger('my_service_name')
    my_logger.setLevel(logging.NOTSET)
    my_logger.parent = None
    my_logger.propagate = False

    # Create the handler and set the logging level.
    my_handler = logging.StreamHandler(sys.stdout)
    my_handler.setLevel(level)

    # Add the formatter to the handler.
    my_handler.setFormatter(create_formatter())

    # Add the handler to the logger.
    my_logger.addHandler(my_handler)

    return my_logger


def create_file_logger(log_file, level):
    '''
    Creates a logger with no parent and a stdout handler.
    '''
    # Create and configure the logger.
    logger = logging.getLogger('my_service_name')
    logger.setLevel(logging.NOTSET)
    logger.parent = None
    logger.propagate = False

    # Create the handler and set the logging level.
    handler = TimedRotatingFileHandler(log_file, when='midnight')
    handler.setLevel(level)

    # Create the formatter.
    format_string = '%(asctime)s — %(name)s — %(levelname)s — %(module)s:%(funcName)s:%(lineno)d — %(message)s'
    formatter = logging.Formatter(format_string)

    # Add the formatter to the handler.
    handler.setFormatter(formatter)

    # Add the handler to the logger.
    logger.addHandler(handler)

    return logger


def add_stdout_handler(service_logger, level=None):
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(create_formatter())
    if level is not None:
        stdout_handler.setLevel(level)
    service_logger.addHandler(stdout_handler)


def add_file_handler(service_logger, log_file, level=None):
    file_handler = TimedRotatingFileHandler(log_file, when='midnight')
    file_handler.setFormatter(create_formatter())
    if level is not None:
        file_handler.setLevel(level)
    service_logger.addHandler(file_handler)



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Send logs to the specified file using a file handler.')
    parser.add_argument('-fl', '--file_level', help='Set logging level for the file.')
    parser.add_argument('-s', '--stdout', help='Send logs to stdout using the stream handler.', action='store_true')
    parser.add_argument('-sl', '--stdout_level', help='Set logging level for stdout.')
    parser.add_argument('-m', '--multiple', help='Create multiple loggers.', action='store_true')
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
