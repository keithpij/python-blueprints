import os
import pprint

from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


def load_env_vars():
    '''
    This function encapsulates load_dotenv for the entire module.
    It will create the environment variables described in the .env file.
    '''
    load_dotenv()


def print_environment_vars():
    azure_client_id = os.environ.get('AZURE_CLIENT_ID', None)
    azure_client_secret = os.environ.get('AZURE_CLIENT_SECRET', None)
    azure_tenet_id = os.environ.get('AZURE_TENANT_ID', None)
    subscription_id = os.environ.get('SUBSCRIPTION_ID', None)
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


def print_object_info(object):
    print('\n')
    pprint.pprint(object.__dict__)
    print('\n')


