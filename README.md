# Fallas 2

## Install global dependencies
    
    pip install virtualenv

## Setup virtualenv

    virtualenv env
    source env/bin/activate

## Install dependencies

    env/bin/pip install -r requirements.txt
    
## Run tests

    env/bin/py.test
    
## Run CLI
    
    cd app
    env/bin/python main.py -h
    env/bin/python main.py -r ./rules.py -i '{"animal": "dog"}' --method=forward -d
