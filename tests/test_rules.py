import pytest
from app.inference_engine.rule import Rule

__author__ = 'tomas'


def test_rule_evaluate_returns_true_when_rule_pass():
    def consequence(subject):
        subject['color'] = 'red'

    rule = Rule('all strawberries are red', {'fruit' : 'strawberry'}, consequence, ('fruit',))

    assert rule.evaluate({'fruit': 'strawberry'})


def test_rule_evaluate_returns_false_when_rule_dont_pass():
    def consequence(subject):
        subject['color'] = 'red'

    rule = Rule('all strawberries are red', {'fruit' : 'strawberry'}, consequence, ('fruit',))

    assert not rule.evaluate({'fruit': 'lime'})


def test_rule_evaluate_applies_consequence_when_true():
    def consequence(subject):
        subject['color'] = 'red'

    subject = {'fruit': 'strawberry'}

    rule = Rule('all strawberries are red', {'fruit' : 'strawberry'}, consequence, ('fruit',))
    rule.evaluate(subject)

    assert subject.get('color') == 'red'


def test_rule_evaluate_does_not_apply_consequence_when_false():
    def consequence(subject):
        subject['color'] = 'red'

    subject = {'fruit': 'lime'}

    rule = Rule('all strawberries are red', {'fruit' : 'strawberry'}, consequence, ('fruit',))
    rule.evaluate(subject)

    assert subject.get('color') is None


def test_rule_evaluate_raise_error_when_applied_to_subject_without_rule_field():
    def consequence(subject):
        subject['color'] = 'red'

    subject = {}

    rule = Rule('all strawberries are red', {'fruit' : 'strawberry'}, consequence, ('fruit',))

    with pytest.raises(Rule.RuleNotApplyException):
        rule.evaluate(subject)

def test_rule_has_consequence_when_true():
    def consequence(subject):
        subject['color'] = 'red'

    subject = {}

    rule = Rule('all strawberries are red', {'fruit' : 'strawberry'}, consequence, ('fruit',))

    assert rule.has_consequence({'color' : 'red'})

def test_rule_has_consequence_when_false_same_field():
    def consequence(subject):
        subject['color'] = 'red'

    subject = {}

    rule = Rule('all strawberries are red', {'fruit' : 'strawberry'}, consequence, ('fruit',))

    assert rule.has_consequence({'color' : 'blue'}) is False

def test_rule_has_consequence_when_false_different_field():
    def consequence(subject):
        subject['color'] = 'red'

    subject = {}

    rule = Rule('all strawberries are red', {'fruit' : 'strawberry'}, consequence, ('fruit',))

    assert rule.has_consequence({'fruit' : 'strawberry'}) is False