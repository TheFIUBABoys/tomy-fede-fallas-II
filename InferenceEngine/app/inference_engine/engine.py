from abc import abstractmethod
import logging
from app.inference_engine.rule import Rule

__author__ = 'tomas'

logger = logging.getLogger("Fallas2")


class KnowledgeBase:
    class DuplicatedKnowledgeException(Exception):
        pass

    def __init__(self):

        self.knowledge = {}

    def add_knowledge(self, new_knowledge):
        if self.knowledge.get(new_knowledge.keys()[0]) is None:
            self.knowledge.update(new_knowledge)
            logger.debug('Added new knowledge: {}'.format(new_knowledge))
        else:
            raise KnowledgeBase.DuplicatedKnowledgeException

    def get_subject(self):
        return self.knowledge


class RuleSet:
    class DuplicatedRuleException(Exception):
        pass

    def __init__(self):
        self.rules = {}
        self.rules_tree = {}

    def add_rule(self, rule):
        if self.rules.get(rule.name) is None:
            self.rules[rule.name] = rule
            logger.debug('Added new rule: "{}"'.format(rule.name))
        else:
            raise RuleSet.DuplicatedRuleException

        if self.rules_tree.get(rule.fields) is None:
            self.rules_tree[rule.fields] = [rule]
        else:
            self.rules_tree[rule.fields].append(rule)

    def get_applying_rules(self, subject):
        def rule_applies(rule):
            try:
                rule.validate_fields(subject)
                return True
            except Rule.RuleNotApplyException:
                return False

        return filter(rule_applies, self.rules.values())


class InferenceEngine:
    def __init__(self, knowledge_base=None, rule_set=None):

        if knowledge_base is None:
            self.knowledge_base = KnowledgeBase()
        else:
            self.knowledge_base = knowledge_base

        if rule_set is None:
            self.rule_set = RuleSet()
        else:
            self.rule_set = rule_set

    @abstractmethod
    def run_engine(self):
        pass


class ForwardChainingInferenceEngine(InferenceEngine):
    def run_engine(self):
        applying_rules = set(self.rule_set.get_applying_rules(self.knowledge_base.get_subject()))
        applied_rules = set()

        iterations = 1

        logger.info('STARTING forward chaining algorithm')
        logger.debug('Initial Knowledge: {}\n'.format(self.knowledge_base.get_subject()))
        while len(applying_rules) > 0:
            logger.debug('ITERATION {}'.format(iterations))
            logger.debug('There are {} rules to apply. Using the first one'.format(len(applying_rules)))
            first_rule = list(applying_rules)[0]

            logger.debug('Evaluating rule {} : {}'.format(first_rule.name, first_rule.condition_object))
            result = first_rule.evaluate(self.knowledge_base.get_subject())
            logger.debug('Result: {}'.format(result))
            logger.debug('Partial Knowledge: {}\n'.format(self.knowledge_base.get_subject()))

            applied_rules.add(first_rule)

            applying_rules = set(self.rule_set.get_applying_rules(self.knowledge_base.get_subject())).difference(
                applied_rules)
            iterations += 1

        logger.info('Forward chaining algorithm took {} iterations'.format(iterations - 1))
        return True


class BackwardChainingInferenceEngine(InferenceEngine):
    def __init__(self, knowledge_base=None, rule_set=None):
        InferenceEngine.__init__(self, knowledge_base, rule_set)
        self.hypothesis = {}

    def set_hypothesis(self, hypothesis):
        self.hypothesis = hypothesis

    def can_prove_hypothesis(self):
        if self.knowledge_base.knowledge.get(self.hypothesis.keys()[0]) is not None:
            return self.knowledge_base.knowledge.get(self.hypothesis.keys()[0]) == self.hypothesis.values()[0]
        return False

    def run_engine(self):
        logger.info('STARTING backward chaining algorithm')
        logger.debug('Initial Knowledge: {}\n'.format(self.knowledge_base.get_subject()))

        result = self.engine_iteration()

        logger.info('Backward chaining algorithm finish with result {}'.format(result))
        return result

    def engine_iteration(self):
        logger.info('Backward chaining algorithm current hypothesis {}'.format(self.hypothesis))

        can_prove = self.can_prove_hypothesis()
        if can_prove:
            logger.debug('The current Knowledge base CAN prove the hypothesis\n')
            return True
        else:
            logger.debug('The current Knowledge base CAN\'T prove the hypothesis\n')

        for ruleName in self.rule_set.rules:
            current_rule = self.rule_set.rules[ruleName]

            # If the rule has the consequence of the hypothesis
            logger.debug('Evaluating rule {} : {}'.format(current_rule.name, current_rule.condition_object))
            if current_rule.has_consequence(self.hypothesis):
                self.hypothesis = current_rule.condition_object
                # Repeat for the condition of the rule
                logger.debug('Current rule has relevant consequence\n')
                result = self.engine_iteration()
                if result:
                    return True
            else:
                logger.debug('Current rule has not relevant consequence\n')

        return False
