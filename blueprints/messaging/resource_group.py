'''
This module uses the Azure Service Bus management plane to manipulate namespaces,
queues, and topics.
To use the utilities in this module you must first install the Azure Service Bus management
library:
pip install azure-mgmt-servicebus
pip install azure-identity
'''
import argparse
import os

from azure.core.exceptions import HttpResponseError
from azure.identity import EnvironmentCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from dotenv import load_dotenv

from blueprints.messaging.subscription import Subscription
from blueprints.messaging import utils


class ResourceGroup():
    '''
    This class encapsulates all the API calls for managing Azure resource groups
    '''

    def __init__(self, subscription_id, group_name, location='eastus', environment='dev', application='blueprints'):
        utils.load_env_vars()
        self.subscription_id = subscription_id
        self.group_name = group_name
        self.location = location
        self.managed_by = None
        self.tags = None
        self.environment = environment
        self.application = application
        self.credential = EnvironmentCredential()

    def get(self):
        '''
        Get a resource group.
        '''
        client = ResourceManagementClient(credential=self.credential,
                                          subscription_id=self.subscription_id)
        group = client.resource_groups.get(self.group_name)
        self.location = group.location
        self.managed_by = group.managed_by
        self.tags = group.tags
        return group

    def create(self, location, environment, project):
        '''
        Create a resource group in the specified location.
        '''
        load_dotenv()
        client = ResourceManagementClient(credential=self.credential,
                                          subscription_id=self.subscription_id)
        kwargs = dict()
        kwargs['location'] = location
        # Tags
        tags = dict()
        tags['environment'] = environment
        tags['project'] = project
        kwargs['tags'] = tags
        client.resource_groups.create_or_update(self.group_name, **kwargs)

    def delete(self):
        '''
        Delete Group
        '''
        client = ResourceManagementClient(credential=self.credential,
                                          subscription_id=self.subscription_id)
        client.resource_groups.begin_delete(self.group_name).result()

    def get_resources(self):
        client = ResourceManagementClient(credential=self.credential,
                                          subscription_id=self.subscription_id)

        return client.resources.list_by_resource_group(self.group_name,
                                                       expand='createdTime,changedTime')


def print_resources(resources):
    column_width = 35
    print('Resource'.ljust(column_width)
        + 'Type'.ljust(column_width)
        + 'Create Date'.ljust(column_width)
        + 'Change Date'.ljust(column_width))
    print('-' * (column_width * 4))

    for resource in list(resources):
        print(f'{resource.name:<{column_width}}' \
            f'{resource.type:<{column_width}}' \
            f'{str(resource.created_time):<{column_width}}' \
            f'{str(resource.changed_time):<{column_width}}')


def print_group_info(group):
    print('\n')
    print('Group Name: {}'.format(group.name))
    print('Location: {}'.format(group.location))
    print('Tags: {}'.format(group.tags))
    print('ID: {}'.format(group.id))
    print('Type: {}'.format(group.type))
    print('Managed by: {}'.format(group.managed_by))
    print('\n')


if __name__ == '__main__':
    # Setup all the CLI arguments for this module.
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list_resources_in_group',
                        help='Print all resources in a group.')
    parser.add_argument('-i', '--print_resource_group_info',
                        help='Print all resource group information.')
    parser.add_argument('-d', '--delete_resource_group',
                        help='Delete resource group.')
    parser.add_argument('-e', '--print_env_vars',
                        help='Print environment variables.',
                        action='store_true')

    # Parse what was passed in. This will also check the arguments for you and produce
    # a help message if something is wrong.
    args = parser.parse_args()

    # Get the name of the logger.
    if args.print_env_vars:
        utils.print_environment_vars()

    if args.print_resource_group_info:
        SUBSCRIPTION = Subscription()
        GROUP = ResourceGroup(SUBSCRIPTION.subscription_id, args.print_resource_group_info)
        GROUP_INFO = GROUP.get()
        print_group_info(GROUP_INFO)

    if args.list_resources_in_group:
        SUBSCRIPTION = Subscription()
        GROUP = ResourceGroup(SUBSCRIPTION.subscription_id, args.list_resources_in_group)
        RESOURCES = GROUP.get_resources()
        print_resources(RESOURCES)

    if args.delete_resource_group:
        SUBSCRIPTION = Subscription()
        GROUP = ResourceGroup(SUBSCRIPTION.subscription_id, args.delete_resource_group)
        GROUP.delete()
        print('{} has been deleted.'.format(args.delete_resource_group))


    #get_service_bus_management_client()
    #create_resource_group('eastus_service_bus_blueprint', 'eastus')
