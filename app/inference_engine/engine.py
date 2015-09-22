from abc import abstractmethod
import logging
from app.inference_engine.rule import Rule

__author__ = 'tomas'


class KnowledgeBase:
    class DuplicatedKnowledgeException(Exception):
        pass

    def __init__(self):

        self.knowledge = {}

    def add_knowledge(self, new_knowledge):
        if self.knowledge.get(new_knowledge.keys()[0]) is None:
            self.knowledge.update(new_knowledge)
            logging.debug('Added new knowledge: {}'.format(new_knowledge))
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
            logging.debug('Added new rule: {}'.format(rule))
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

        logging.debug('Starting forward chaining algorithm')
        while len(applying_rules) > 0:
            logging.debug('There are {} rules to apply. Using the first one'.format(len(applying_rules)))
            first_rule = list(applying_rules)[0]

            logging.debug('Evaluating rule {}'.format(first_rule.name))
            result = first_rule.evaluate(self.knowledge_base.get_subject())
            logging.debug('Matches: {}'.format(result))

            applied_rules.add(first_rule)

            applying_rules = set(self.rule_set.get_applying_rules(self.knowledge_base.get_subject())).difference(
                applied_rules)

        return True


class BackwardChainingInferenceEngine(InferenceEngine):

    def __init__(self, knowledge_base=None, rule_set=None):
        InferenceEngine.__init__(self, knowledge_base, rule_set)
        self.hypothesis = {}

    def set_hypothesis(self, hypothesis):
        self.hypothesis = hypothesis

    def run_engine(self):
        # If already exists at knowledge Knowledge Base
        if self.knowledge_base.knowledge.get(self.hypothesis.keys()[0]) is not None:
            # And has the correct value, return true
            return self.knowledge_base.knowledge.get(self.hypothesis.keys()[0]) == self.hypothesis.values()[0]

        for ruleName in self.rule_set.rules:
            current_rule = self.rule_set.rules[ruleName]

            # If the rule has the consequence of the hypothesis
            if current_rule.has_consequence(self.hypothesis):
                self.hypothesis = current_rule.condition_object
                # Repeat for the condition of the rule
                result = self.run_engine()
                if result:
                    return True

        return False
