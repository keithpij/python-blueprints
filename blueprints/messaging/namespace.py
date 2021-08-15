'''
This module contains the Namespace class which calls Azure APIs related to the management of 
Service Bus namespaces.
The online documention for the API calls used in this module can be found here:

https://azuresdkdocs.blob.core.windows.net/$web/python/azure-mgmt-servicebus/0.6.0/azure.mgmt.servicebus.operations.html

'''
import argparse
import os

from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.identity import EnvironmentCredential
from azure.mgmt.servicebus import ServiceBusManagementClient
from azure.mgmt.servicebus.models import SBNamespace
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from dotenv import load_dotenv

from blueprints.messaging.resource_group import Subscription
from blueprints.messaging.resource_group import ResourceGroup
from blueprints.messaging import utils


class Namespace():

    def __init__(self, subscription, group):
        self.subscription = subscription
        self.group = group
        self.credential = EnvironmentCredential()

    def get_service_bus_client(self):
        return ServiceBusManagementClient(
            credential=self.credential,
            subscription_id=self.subscription.subscription_id)

    def get(self, namespace_name):
        sb_client = self.get_service_bus_client()
        sb_namespace = sb_client.namespaces.get(self.group.group_name, namespace_name)
        return sb_namespace

    def create(self, namespace_name, sku_name):
        '''
        This method will create a service bus namespace.
        '''
        sb_client = ServiceBusManagementClient(credential=self.credential,
                                               subscription_id=self.subscription.subscription_id)

        kwargs = {}
        kwargs['location'] = self.group.location
        # SKU
        sku = {}
        sku['name'] = sku_name
        sku['tier'] = sku_name
        kwargs['sku'] = sku
        # Tags
        tags = {}
        tags['environment'] = self.group.environment
        tags['application'] = self.group.application
        kwargs['tags'] = tags

        parameters = SBNamespace(**kwargs)
        namespace = sb_client.namespaces.begin_create_or_update(
            self.group.group_name,
            namespace_name, parameters).result()

        #namespace = sb_client.namespaces.begin_create_or_update(
        #    self.group.group_name,
        #    namespace_name,
        #    {
        #    "sku": {
        #        "name": "Basic",
        #        "tier": "Basic"
        #    },
        #    "location": self.group.location,
        #    "tags": {
        #        "tag1": "value1",
        #        "tag2": "value2"
        #    }
        #    }
        #).result()


if __name__ == '__main__':
    # Setup all the CLI arguments for this module.
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--group',
                        help='Group name.')
    parser.add_argument('-n', '--namespace',
                        help='Namespace name.')
    parser.add_argument('-s', '--sku',
                        help='SKU associated with the namespace.')
    parser.add_argument('-c', '--create_namespace',
                        help='Create a Service Bus namespace.',
                        action='store_true')
    parser.add_argument('-i', '--print_namespace_info',
                        help='Print namespace information.',
                        action='store_true')

    # Parse what was passed in. This will also check the arguments for you and produce
    # a help message is something is wrong.
    args = parser.parse_args()
    if args.create_namespace:
        SUBSCRIPTION = Subscription()
        GROUP = ResourceGroup(SUBSCRIPTION,args.group)
        NAMESPACE = Namespace(SUBSCRIPTION, GROUP)
        NAMESPACE.create(args.namespace, args.sku)
        print("{} created".format(args.namespace))

    if args.print_namespace_info:
        SUBSCRIPTION = Subscription()
        GROUP = ResourceGroup(SUBSCRIPTION,args.group)
        NAMESPACE = Namespace(SUBSCRIPTION, GROUP)
        SB_NAMESPACE = NAMESPACE.get(args.namespace)
        utils.print_object_info(SB_NAMESPACE)