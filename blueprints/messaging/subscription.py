'''
This module uses the Azure management plane to query subscription information.
To use the utilities in this module you must first install:
pip install azure-mgmt-servicebus
pip install azure-identity

'''
import argparse
import os

from azure.core.exceptions import HttpResponseError
from azure.identity import EnvironmentCredential
from azure.mgmt.resource import ResourceManagementClient

from blueprints.messaging import utils


class Subscription():

    def __init__(self, subscription_id=None):
        utils.load_env_vars()
        if subscription_id is None:
            subscription_id = os.environ.get("SUBSCRIPTION_ID", None)
        self.subscription_id = subscription_id
        self.credential = EnvironmentCredential()

    def get_resource_groups(self):
        '''
        Create a resource group in the specified location.
        '''
        client = ResourceManagementClient(credential=self.credential,
                                          subscription_id=self.subscription_id)

        return client.resource_groups.list()


def print_resource_groups(groups):
    column_width = 40
    print('\n')
    print('Resource Group'.ljust(column_width) + 'Location')
    print('-' * (column_width * 2))
    for group in list(groups):
        print(f'{group.name:<{column_width}}{group.location}')
    print('\n')


def setup_args_parser():
    '''
    Setup all the CLI arguments for this module.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--print_resource_groups',
                        help='Print all resource groups in a subscription.',
                        action='store_true')
    parser.add_argument('-e', '--print_env_vars',
                        help='Print environment variables.',
                        action='store_true')
    return parser


def main(parser):
    '''
    Parse what was passed in. This will also check the arguments for you and produce
    a help message if something is wrong.
    '''
    args = parser.parse_args()

    if args.print_env_vars:
        utils.print_environment_vars()

    if args.print_resource_groups:
        subscription = Subscription()
        groups = subscription.get_resource_groups()
        print_resource_groups(groups)


if __name__ == '__main__':
    PARSER = setup_args_parser()
    main(PARSER)
