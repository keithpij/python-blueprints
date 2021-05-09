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


class ServiceBus():

    def __init__(self, subscription, group):
        self.subscription = subscription
        self.group = group
        self.credential = EnvironmentCredential()

    def get_service_bus_client(self):
        return ServiceBusManagementClient(
            credential=self.credential,
            subscription_id=self.subscription.subscription_id)

    def create_namespace(self, namespace_name, sku_name):
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

        print("Create namespace:\n{}".format(namespace))


if __name__ == '__main__':
    # Setup all the CLI arguments for this module.
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create_namespace',
                        help='Create a Service Bus namespace.',
                        action='store_true')
    parser.add_argument('-s', '--sku',
                        help='SKU associated with the namespace.')

    # Parse what was passed in. This will also check the arguments for you and produce
    # a help message is something is wrong.
    args = parser.parse_args()
    if args.create_namespace:
        SUBSCRIPTION = Subscription()
        GROUP = ResourceGroup(SUBSCRIPTION,'eastus_service_bus_blueprint')
        SERVICE_BUS = ServiceBus(SUBSCRIPTION, GROUP)
        SERVICE_BUS.create_namespace('blueprints-namespace', args.sku)