import pytest
from app.inference_engine.engine import KnowledgeBase, RuleSet, ForwardChainingInferenceEngine, \
    BackwardChainingInferenceEngine
from app.inference_engine.rule import Rule

__author__ = 'tomas'


def test_knowledge_base_add_rule_adds_new_rule():
    def condition(subject):
        return subject['fruit'] == 'strawberry'

    def consequence(subject):
        subject['color'] = 'red'

    rule = Rule('all strawberries are red', condition, consequence, {'fruit': 'strawberry'}, ('fruit',))
    rs = RuleSet()

    rs.add_rule(rule)

    assert len(rs.rules) == 1
    assert len(rs.rules_tree) == 1


def test_knowledge_base_add_rule_and_then_retrieve_it_returns_the_correct_one():
    def condition(subject):
        return subject['fruit'] == 'strawberry'

    def consequence(subject):
        subject['color'] = 'red'

    rule = Rule('all strawberries are red', condition, consequence, {'fruit': 'strawberry'}, ('fruit',))
    rs = RuleSet()

    rs.add_rule(rule)

    assert rs.rules.get(rule.name) == rule
    assert rs.rules_tree.get(rule.fields)[0] == rule


def test_knowledge_base_add_rule_twice_should_raise_an_exception():
    def condition(subject):
        return subject['fruit'] == 'strawberry'

    def consequence(subject):
        subject['color'] = 'red'

    rule = Rule('all strawberries are red', condition, consequence, {'fruit': 'strawberry'}, ('fruit',))
    rs = RuleSet()

    rs.add_rule(rule)
    with pytest.raises(RuleSet.DuplicatedRuleException):
        rs.add_rule(rule)


def test_knowledge_base_add_two_rules_with_same_fields():
    def condition1(subject):
        return subject['fruit'] == 'strawberry'

    def condition2(subject):
        return subject['fruit'] == 'kiwi'

    def consequence1(subject):
        subject['color'] = 'red'

    def consequence2(subject):
        subject['color'] = 'brown'

    rule1 = Rule('all strawberries are red', condition1, consequence1, {'fruit': 'strawberry'}, ('fruit',))
    rule2 = Rule('all kiwis are brown', condition2, consequence2, {'fruit': 'kiwi'}, ('fruit',))
    rs = RuleSet()

    rs.add_rule(rule1)
    rs.add_rule(rule2)

    assert len(rs.rules) == 2
    assert len(rs.rules_tree) == 1
    assert len(rs.rules_tree.get(('fruit',))) == 2


def test_forward_chaining():
    def condition1(subject):
        return subject['animal'] == 'dog'

    def condition2(subject):
        return subject['legsQuantity'] == '4'

    def consequence1(subject):
        subject['legsQuantity'] = '4'

    def consequence2(subject):
        subject['locomotion'] = 'quadruped'

    rule1 = Rule('all dogs have 4 legs', condition1, consequence1, {'animal': 'dog'}, ('animal',))
    rule2 = Rule('Anything with 4 legs is a quadruped', condition2, consequence2, {'legsQuantity': '4'},
                 ('legsQuantity',))

    rs = RuleSet()
    rs.add_rule(rule1)
    rs.add_rule(rule2)

    kb = KnowledgeBase()
    kb.add_knowledge({'animal': 'dog'})

    ie = ForwardChainingInferenceEngine(kb, rs)
    ie.run_engine()

    assert ie.knowledge_base.knowledge == {'animal': 'dog', 'legsQuantity': '4', 'locomotion': 'quadruped'}


def test_backward_chaining_when_true():
    def condition1(subject):
        return subject['animal'] == 'dog'

    def condition2(subject):
        return subject['legsQuantity'] == '4'

    def consequence1(subject):
        subject['legsQuantity'] = '4'

    def consequence2(subject):
        subject['locomotion'] = 'quadruped'

    rule1 = Rule('all dogs have 4 legs', condition1, consequence1, {'animal': 'dog'}, ('animal',))
    rule2 = Rule('Anything with 4 legs is a quadruped', condition2, consequence2, {'legsQuantity': '4'},
                 ('legsQuantity',))
    rs = RuleSet()
    rs.add_rule(rule1)
    rs.add_rule(rule2)

    kb = KnowledgeBase()
    kb.add_knowledge({'animal': 'dog'})

    ie = BackwardChainingInferenceEngine(kb, rs)
    ie.set_hypothesis({'locomotion': 'quadruped'})

    assert ie.run_engine()


def test_backward_chaining_wrong_hipotesis_when_false():
    def condition1(subject):
        return subject['animal'] == 'dog'

    def condition2(subject):
        return subject['legsQuantity'] == '4'

    def consequence1(subject):
        subject['legsQuantity'] = '4'

    def consequence2(subject):
        subject['locomotion'] = 'quadruped'

    rule1 = Rule('all dogs have 4 legs', condition1, consequence1, {'animal': 'dog'}, ('animal',))
    rule2 = Rule('Anything with 4 legs is a quadruped', condition2, consequence2, {'legsQuantity': '4'},
                 ('legsQuantity',))
    rs = RuleSet()
    rs.add_rule(rule1)
    rs.add_rule(rule2)

    kb = KnowledgeBase()
    kb.add_knowledge({'animal': 'dog'})

    ie = BackwardChainingInferenceEngine(kb, rs)
    ie.set_hypothesis({'locomotion': 'bipedal'})

    assert ie.run_engine() is False


def test_backward_chaining_missing_rule_when_false():
    def condition1(subject):
        return subject['animal'] == 'dog'

    def condition2(subject):
        return subject['legsQuantity'] == '4'

    def consequence1(subject):
        subject['legsQuantity'] = '4'

    def consequence2(subject):
        subject['locomotion'] = 'quadruped'

    rule2 = Rule('Anything with 4 legs is a quadruped', condition2, consequence2, {'legsQuantity': '4'},
                 ('legsQuantity',))
    rs = RuleSet()
    rs.add_rule(rule2)

    kb = KnowledgeBase()
    kb.add_knowledge({'animal': 'dog'})

    ie = BackwardChainingInferenceEngine(kb, rs)
    ie.set_hypothesis({'locomotion': 'quadruped'})

    assert ie.run_engine() is False
