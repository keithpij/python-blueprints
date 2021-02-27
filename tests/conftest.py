'''
Fixtures to be used by unit tests.
'''
import pytest
import src.modeltools


@pytest.fixture(scope='session')
def model_definition():
    ''' Fixture that will return a model definition.'''
    definition = src.modeltools.ModelDefinition('sequential_model.json')
    return definition
