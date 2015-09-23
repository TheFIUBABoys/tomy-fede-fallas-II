import argparse
import imp
import json
import logging
import yaml
from app.inference_engine.engine import RuleSet, KnowledgeBase, ForwardChainingInferenceEngine, \
    BackwardChainingInferenceEngine

__author__ = 'tomas'

logger = logging.getLogger("Fallas2")


def forward_chaining_method(rules, init_knowledge):
    rules_set = RuleSet()
    map(rules_set.add_rule, rules)

    knowledge_base = KnowledgeBase()
    knowledge_base.add_knowledge(yaml.safe_load(init_knowledge))

    inference_engine = ForwardChainingInferenceEngine(knowledge_base, rules_set)
    inference_engine.run_engine()

    logger.info('Final Knowledge')
    logger.info(knowledge_base.knowledge)


def backward_chaining_method(rules, init_knowledge, hypothesis):
    rules_set = RuleSet()
    map(rules_set.add_rule, rules)

    knowledge_base = KnowledgeBase()
    knowledge_base.add_knowledge(yaml.safe_load(init_knowledge))

    inference_engine = BackwardChainingInferenceEngine(knowledge_base, rules_set)
    inference_engine.set_hypothesis(yaml.safe_load(hypothesis))
    result = inference_engine.run_engine()

    logger.info('Result: {}'.format(result))


def validate_parameters(args):
    if args.init_knowledge is None:
        logger.error('No knowledge provided')
        exit(2)

    if args.method == 'backward' and args.hypothesis is None:
        logger.error('No hypothesis provided')
        exit(3)


def setup_logger(args):
    log_formater = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')

    if args.output is not None:
        file_handler = logging.FileHandler(args.output)
        file_handler.setFormatter(log_formater)
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formater)
    logger.addHandler(console_handler)

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


def main():
    parser = argparse.ArgumentParser(description='Interactive Inference Engine example')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                        help="Enable step by step description for the chosen method")
    parser.add_argument('-m', '--method', type=str, dest='method', choices=['forward', 'backward'],
                        help="Choose the chaining method of your preferences")
    parser.add_argument('-i', '--init-knowledge', type=str, dest='init_knowledge',
                        help="A JSON document with the initial knowledge")
    parser.add_argument('-y', '--hypothesis', type=str, dest='hypothesis',
                        help="A JSON document with the hypothesis for backward chaining")
    parser.add_argument('-r', '--rules-script', type=str, dest='rules_script', default='./rules.py',
                        help="A python import script containing the set of rules to use. Check the example for usage")
    parser.add_argument('-o', '--output', type=str, dest='output',
                        help="Logger output path")
    args = parser.parse_args()

    setup_logger(args)

    rules = imp.load_source('rules', args.rules_script).rules
    if rules is None:
        logger.error('No rules provided')
        exit(1)

    validate_parameters(args)

    if args.method == 'forward':
        forward_chaining_method(rules, args.init_knowledge)
    elif args.method == 'backward':
        backward_chaining_method(rules, args.init_knowledge, args.hypothesis)
    else:
        logging.error('Unsupported chaining method: {}'.format(args.method))


if __name__ == '__main__':
    main()
