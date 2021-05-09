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
from azure.identity import DefaultAzureCredential
from azure.identity import EnvironmentCredential
from azure.mgmt.servicebus import ServiceBusManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from dotenv import load_dotenv


class Subscription():

    def __init__(self, subscription_id=None):
        if subscription_id is None:
            load_dotenv()
            subscription_id = os.environ.get("SUBSCRIPTION_ID", None)
        self.subscription_id = subscription_id

    def get_resource_groups(self):
        '''
        Create a resource group in the specified location.
        '''
        load_dotenv()
        credential = EnvironmentCredential()
        resource_management_client = ResourceManagementClient(credential=credential,
                                                subscription_id=self.subscription_id)

        return resource_management_client.resource_groups.list()


class ResourceGroup():
    '''
    This class encapsulates all the API calls for managing Azure resource groups
    '''

    def __init__(self, subscription_id, group_name, location='eastus', environment='dev', application='blueprints'):
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
        load_dotenv()
        client = ResourceManagementClient(credential=self.credential,
                                          subscription_id=self.subscription_id)
        group = client.get(self.group_name)
        self.location = group.location
        self.managed_by = group.managed_by
        self.tags = group.tags
        self.environment = tags['environment']
        self.application = tags['application']

    def create(self, location, environment, project):
        '''
        Create a resource group in the specified location.
        '''
        load_dotenv()
        resource_management_client = ResourceManagementClient(credential=self.credential,
                                                subscription_id=self.subscription_id)
        kwargs = dict()
        kwargs['location'] = location
        # Tags
        tags = dict()
        tags['environment'] = environment
        tags['project'] = project
        kwargs['tags'] = tags

        resource_management_client.resource_groups.create_or_update(self.group_name, **kwargs)

    def get_resources(self):
        resource_client = ResourceManagementClient(credential=self.credential,
                                                subscription_id=self.subscription_id)

        return resource_client.resources.list_by_resource_group(self.group_name,
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


def print_resource_groups(groups):
    column_width = 40
    print('\n')
    print('Resource Group'.ljust(column_width) + 'Location')
    print('-' * (column_width * 2))
    for group in list(groups):
        print(f'{group.name:<{column_width}}{group.location}')
    print('\n')


def print_environment_vars():
    azure_client_id = os.environ.get("AZURE_CLIENT_ID", None)
    azure_client_secret = os.environ.get("AZURE_CLIENT_SECRET", None)
    azure_tenet_id = os.environ.get("AZURE_TENANT_ID", None)
    subscription_id = os.environ.get("SUBSCRIPTION_ID", None)
    print('\n')
    print('AZURE_CLIENT_ID: {}'.format(azure_client_id))
    print('AZURE_CLIENT_SECRET: {}'.format(azure_client_secret))
    print('AZURE_TENET_ID: {}'.format(azure_tenet_id))
    print('SUBSCRIPTION_ID: {}'.format(subscription_id))
    print('\n')


def get_default_azure_credential():
    '''
    This method will use the DefaultAzureCredential class to setup an Azure credential.
    '''
    kwargs = {}
    kwargs['authority'] = None
    kwargs['exclude_cli_credential'] = True
    kwargs['exclude_environment_credential'] = False
    kwargs['exclude_managed_identity_credential'] = True
    kwargs['exclude_visual_studio_code_credential'] = True
    kwargs['exclude_shared_token_cache_credentia'] = True
    kwargs['exclude_interactive_browser_credential'] = True
    kwargs['interactive_browser_tenant_id'] = None
    kwargs['managed_identity_client_id'] = None
    kwargs['shared_cache_username'] = None
    kwargs['shared_cache_tenant_id'] = None
    kwargs['visual_studio_code_tenant_id'] = None

    credential = DefaultAzureCredential(**kwargs)
    return credential


if __name__ == '__main__':
    # Setup all the CLI arguments for this module.
    parser = argparse.ArgumentParser()
    parser.add_argument('-pr', '--print_resources_in_group',
                        help='Print all resources in a group.')
    parser.add_argument('-prg', '--print_resource_groups',
                        help='Print all resource groups in a subscription.',
                        action='store_true')
    parser.add_argument('-penv', '--print_env_vars',
                        help='Print environment variables.',
                        action='store_true')

    # Parse what was passed in. This will also check the arguments for you and produce
    # a help message is something is wrong.
    args = parser.parse_args()

    # Get the name of the logger.
    if args.print_env_vars:
        print_environment_vars()

    if args.print_resource_groups:
        SUBSCRIPTION = Subscription()
        GROUPS = SUBSCRIPTION.get_resource_groups()
        print_resource_groups(GROUPS)

    if args.print_resources_in_group:
        SUBSCRIPTION = Subscription()
        GROUP = ResourceGroup(SUBSCRIPTION.subscription_id, args.print_resources_in_group)
        RESOURCES = GROUP.get_resources_in_group()
        print_resources(RESOURCES)


    #get_service_bus_management_client()
    #create_resource_group('eastus_service_bus_blueprint', 'eastus')
