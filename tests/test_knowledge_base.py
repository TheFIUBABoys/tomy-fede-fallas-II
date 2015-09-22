import pytest
from app.inference_engine.engine import KnowledgeBase
from app.inference_engine.rule import Rule

__author__ = 'tomas'


def test_knowledge_base_add_rule_adds_new_rule():
    def condition(subject):
        return subject.get('fruit', '') == 'strawberry'

    def consequence(subject):
        subject['color'] = 'red'

    rule = Rule('all strawberries are red', condition, consequence, ('fruit',))
    kb = KnowledgeBase()

    kb.add_rule(rule)

    assert len(kb.rules) == 1
    assert len(kb.rules_tree) == 1


def test_knowledge_base_add_rule_and_then_retrieve_it_returns_the_correct_one():
    def condition(subject):
        return subject.get('fruit', '') == 'strawberry'

    def consequence(subject):
        subject['color'] = 'red'

    rule = Rule('all strawberries are red', condition, consequence, ('fruit',))
    kb = KnowledgeBase()

    kb.add_rule(rule)

    assert kb.rules.get(rule.name) == rule
    assert kb.rules_tree.get(rule.fields)[0] == rule


def test_knowledge_base_add_rule_twice_should_raise_an_exception():
    def condition(subject):
        return subject.get('fruit', '') == 'strawberry'

    def consequence(subject):
        subject['color'] = 'red'

    rule = Rule('all strawberries are red', condition, consequence, ('fruit',))
    kb = KnowledgeBase()

    kb.add_rule(rule)
    with pytest.raises(KnowledgeBase.DuplicatedRuleException):
        kb.add_rule(rule)


def test_knowledge_base_add_two_rules_with_same_fields():
    def condition1(subject):
        return subject.get('fruit', '') == 'strawberry'

    def consequence1(subject):
        subject['color'] = 'red'

    def condition2(subject):
        return subject.get('fruit', '') == 'kiwi'

    def consequence2(subject):
        subject['color'] = 'brown'

    rule1 = Rule('all strawberries are red', condition1, consequence1, ('fruit',))
    rule2 = Rule('all kiwis are brown', condition1, consequence2, ('fruit',))
    kb = KnowledgeBase()

    kb.add_rule(rule1)
    kb.add_rule(rule2)

    assert len(kb.rules) == 2
    assert len(kb.rules_tree) == 1
    assert len(kb.rules_tree.get(('fruit',))) == 2

def test_forward_chaining():
    def condition1(subject):
        return subject.get('animal', '') == 'dog'

    def consequence1(subject):
        subject['legsQuantity'] = '4'

    def condition2(subject):
        return subject.get('legsQuantity', '') == '4'

    def consequence2(subject):
        subject['locomotion'] = 'quadrupedalism'

    rule1 = Rule('all dogs have 4 legs', condition1, consequence1, ('animal',))
    rule2 = Rule('Anything with 4 legs is a quadrupedalism', condition1, consequence2, ('legsQuantity',))
    kb = KnowledgeBase()

    kb.add_rule(rule1)
    kb.add_rule(rule2)
    kb.add_knowledge({'animal': 'dog'})

    assert kb.run_forward_chaining() == {'animal': 'dog', 'legsQuantity': '4', 'locomotion': 'quadrupedalism'}