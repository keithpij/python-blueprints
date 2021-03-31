'''
This module uses the Azure Service Bus management plane to manipulate namespaces,
queues, and topics.
To use the utilities in this module you must first install the Azure Service Bus management
library:
pip install azure-mgmt-servicebus
pip install azure-identity

'''
from azure.identity import DefaultAzureCredential
from azure.mgmt.servicebus import ServiceBusManagmentClient


SUBSCRIPTION_ID = '43ab820b-e14b-4a28-ad48-b5add7ed9aed'

def get_client():
    client = ServiceBusManagmentClient(credential=DefaultAzureCredential(),
                                       subscription_id=SUBSCRIPTION_ID)
    return client


if __name__ == '__main__':
    get_client()
    print('Successfully created the management client.')