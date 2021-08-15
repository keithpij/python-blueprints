'''
This module uses the Azure Service Bus management plane to manipulate queues.
To use the utilities in this module you must first install the Azure Service Bus management
library:
pip install azure-mgmt-servicebus
pip install azure-identity
'''
import argparse
import os

from azure.core.exceptions import HttpResponseError
from azure.identity import EnvironmentCredential
from azure.mgmt.servicebus import ServiceBusManagementClient

from blueprints.messaging.subscription import Subscription
from blueprints.messaging import utils


class Queue():
    '''
    This class encapsulates all the API calls for managing Service Bus queues.
    '''

    def __init__(self, subscription_id, group_name, namespace_name, queue_name):
        utils.load_env_vars()
        self.credential = EnvironmentCredential()
        self.subscription_id = subscription_id
        self.group_name = group_name
        self.namespace_name = namespace_name
        self.queue_name = queue_name
        self.location = None
        self.managed_by = None
        self.tags = None

    def get(self):
        '''
        Get a resource group.
        The get method of ServiceBusManagementClient.queues.get() returns an SBQueue object. The full documentation
        can be found at the link below.
        https://docs.microsoft.com/en-us/python/api/azure-mgmt-servicebus/azure.mgmt.servicebus.models.sbqueue?view=azure-python
        '''
        client = ServiceBusManagementClient(credential=self.credential,
                                          subscription_id=self.subscription_id)
        sb_queue = client.queues.get(self.group_name, self.namespace_name, self.queue_name)

        self.accessed_at = sb_queue.accessed_at
        self.auto_delete_on_idle = sb_queue.auto_delete_on_idle
        self.count_details = sb_queue.count_details
        self.queue_name = sb_queue.name
        self.message_count = sb_queue.message_count
        self.id = sb_queue.id
        self.status = sb_queue.status
        self.type = sb_queue.type
        self.updated_at = sb_queue.updated_at
        return sb_queue

    def create(self):
        '''
        Create a queue in the specified namespace.
        '''
        client = ServiceBusManagementClient(credential=self.credential,
                                          subscription_id=self.subscription_id)
        client.queues.create_or_update(self.group_name, self.namespace_name, self.queue_name,
                                        {'enable_partitioning': True})

    def delete(self):
        '''
        Delete queue
        '''
        client = ServiceBusManagementClient(credential=self.credential,
                                          subscription_id=self.subscription_id)
        client.queues.delete(self.group_name, self.namespace_name, self.queue_name)


if __name__ == '__main__':
    # Setup all the CLI arguments for this module.
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--group',
                        help='Group name.')
    parser.add_argument('-n', '--namespace',
                        help='Namespace name.')
    parser.add_argument('-q', '--queue',
                        help='Queue name.')

    parser.add_argument('-c', '--create_queue',
                        help='Create a queue.',
                        action='store_true')
    parser.add_argument('-i', '--print_queue_info',
                        help='Print queue information.',
                        action='store_true')
    parser.add_argument('-d', '--delete_queue',
                        help='Delete queue.',
                        action='store_true')

    parser.add_argument('-e', '--print_env_vars',
                        help='Print environment variables.',
                        action='store_true')

    # Parse what was passed in. 
    args = parser.parse_args()

    # Get the name of the logger.
    if args.print_env_vars:
        utils.print_environment_vars()

    if args.create_queue:
        SUBSCRIPTION = Subscription()
        QUEUE = Queue(SUBSCRIPTION.subscription_id, args.group, args.namespace, args.queue)
        QUEUE.create()
        print('{} has been created.'.format(args.queue))

    if args.print_queue_info:
        SUBSCRIPTION = Subscription()
        QUEUE = Queue(SUBSCRIPTION.subscription_id, args.group, args.namespace, args.queue)
        QUEUE.get()
        utils.print_object_info(QUEUE)

    if args.delete_queue:
        SUBSCRIPTION = Subscription()
        QUEUE = Queue(SUBSCRIPTION.subscription_id, args.group, args.namespace, args.queue)
        QUEUE.delete()
        print('{} has been deleted.'.format(args.queue))
