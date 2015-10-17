import argparse
import imp
import json
import logging
import yaml
from app.semanticNetwork import SemanticNetwork

__author__ = 'federico'

logger = logging.getLogger("Fallas2")


def main():
    buildExampleNetwork2()

def buildExampleNetwork1():
    semanticNetwork = SemanticNetwork()
    semanticNetwork.add_object('Cow')
    semanticNetwork.add_object('Milk')
    semanticNetwork.add_relation('Cow', 'Milk', 'Produces')
    semanticNetwork.draw_network()

def buildExampleNetwork2():
    semanticNetwork = SemanticNetwork()
    semanticNetwork.add_object('Animal')
    semanticNetwork.add_object('Mammal')
    semanticNetwork.add_object('Bear')
    semanticNetwork.add_object('Water')
    semanticNetwork.add_object('Fish')
    semanticNetwork.add_object('Whale')
    semanticNetwork.add_object('Cat')
    semanticNetwork.add_object('Fur')
    semanticNetwork.add_object('Vertebra')
    semanticNetwork.add_relation('Animal', 'Mammal', 'is an')
    semanticNetwork.add_relation('Animal', 'Fish', 'is an')
    semanticNetwork.add_relation('Mammal', 'Vertebra', 'has')
    semanticNetwork.add_relation('Mammal', 'Cat', 'is a')
    semanticNetwork.add_relation('Mammal', 'Bear', 'is a')
    semanticNetwork.add_relation('Mammal', 'Whale', 'is a')
    semanticNetwork.add_relation('Water', 'Whale', 'lives in')
    semanticNetwork.add_relation('Water', 'Fish', 'lives in')
    semanticNetwork.add_relation('Fur', 'Bear', 'has')
    semanticNetwork.add_relation('Fur', 'Cat', 'has')
    semanticNetwork.draw_network()


if __name__ == '__main__':
    main()
