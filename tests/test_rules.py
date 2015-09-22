import pytest
from app.inference_engine.rule import Rule

__author__ = 'tomas'


def test_rule_evaluate_returns_true_when_rule_pass():
    def condition(subject):
        return subject['fruit'] == 'strawberry'
    
    def consequence(subject):
        subject['color'] = 'red'

    rule = Rule('all strawberries are red', condition, consequence, {'fruit': 'strawberry'}, ('fruit',))

    assert rule.evaluate({'fruit': 'strawberry'})


def test_rule_evaluate_returns_false_when_rule_dont_pass():
    def condition(subject):
        return subject['fruit'] == 'strawberry' 
    
    def consequence(subject):
        subject['color'] = 'red'

    rule = Rule('all strawberries are red', condition, consequence, {'fruit': 'strawberry'}, ('fruit',))

    assert not rule.evaluate({'fruit': 'lime'})


def test_rule_evaluate_applies_consequence_when_true():
    def condition(subject):
        return subject['fruit'] == 'strawberry'
    
    def consequence(subject):
        subject['color'] = 'red'

    s = {'fruit': 'strawberry'}

    rule = Rule('all strawberries are red', condition, consequence, {'fruit': 'strawberry'}, ('fruit',))
    rule.evaluate(s)

    assert s.get('color') == 'red'


def test_rule_evaluate_does_not_apply_consequence_when_false():
    def condition(subject):
        return subject['fruit'] == 'strawberry'
    
    def consequence(subject):
        subject['color'] = 'red'

    s = {'fruit': 'lime'}

    rule = Rule('all strawberries are red', condition, consequence, {'fruit': 'strawberry'}, ('fruit',))
    rule.evaluate(s)

    assert s.get('color') is None


def test_rule_evaluate_raise_error_when_applied_to_subject_without_rule_field():
    def condition(subject):
        return subject['fruit'] == 'strawberry'
    
    def consequence(subject):
        subject['color'] = 'red'

    s = {}

    rule = Rule('all strawberries are red', condition, consequence, {'fruit': 'strawberry'}, ('fruit',))

    with pytest.raises(Rule.RuleNotApplyException):
        rule.evaluate(s)

def test_rule_has_consequence_when_true():
    def condition(subject):
        return subject['fruit'] == 'strawberry'
    
    def consequence(subject):
        subject['color'] = 'red'

    rule = Rule('all strawberries are red', condition, consequence, {'fruit': 'strawberry'}, ('fruit',))

    assert rule.has_consequence({'color': 'red'})

def test_rule_has_consequence_when_false_same_field():
    def condition(subject):
        return subject['fruit'] == 'strawberry'
    
    def consequence(subject):
        subject['color'] = 'red'

    rule = Rule('all strawberries are red', condition, consequence, {'fruit': 'strawberry'}, ('fruit',))

    assert rule.has_consequence({'color' : 'blue'}) is False

def test_rule_has_consequence_when_false_different_field():
    def condition(subject):
        return subject['fruit'] == 'strawberry'
    
    def consequence(subject):
        subject['color'] = 'red'

    rule = Rule('all strawberries are red', condition, consequence, {'fruit': 'strawberry'}, ('fruit',))

    assert rule.has_consequence(condition) is False