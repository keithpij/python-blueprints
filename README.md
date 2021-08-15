# python-blueprints
Reusable designs for creating Python services and apps

## Useful pyenv commands:
brew install pyenv
brew install pyenv-virtualenv

pyenv install --list
pyenv versions
pyenv global 3.8.5
pyenv local 3.8.5
pyenv global system
pyenv local system
pyenv which pip

pyenv virtualenv 3.8.5 onnx
cd onnx
pyenv local onnx

pyenv virtualenv 3.8.5 ray
pyenv shell ray

## To get a pylint config file with examples for all options.
pylint --generate-rcfile > pylintrc_sample
