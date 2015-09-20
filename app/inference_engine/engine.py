__author__ = 'tomas'

class KnowledgeBase:
    class DuplicatedRuleException(Exception):
        pass

    def __init__(self):
        self.rules_tree = {}
        self.rules = {}
        self.knowledge = {}

    def add_rule(self, rule):
        if self.rules.get(rule.name) is None:
            self.rules[rule.name] = rule
        else:
            raise KnowledgeBase.DuplicatedRuleException

        if self.rules_tree.get(rule.fields) is None:
            self.rules_tree[rule.fields] = [rule]
        else:
            self.rules_tree[rule.fields].append(rule)
