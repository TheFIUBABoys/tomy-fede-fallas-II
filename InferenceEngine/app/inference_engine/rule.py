__author__ = 'tomas'


class Rule:
    class RuleNotApplyException(Exception):
        pass

    def __init__(self, name, condition, consequence, condition_object,fields=()):
        self.name = name
        self.condition = condition
        self.consequence = consequence
        self.condition_object = condition_object
        self.fields = fields

    def evaluate(self, subject):
        self.validate_fields(subject)
        rule_success = self.condition(subject)

        if rule_success:
            self.consequence(subject)

        return rule_success

    def validate_fields(self, subject):
        for field in self.fields:
            if subject.get(field) is None:
                raise Rule.RuleNotApplyException('Rule does not apply to subject')

    def has_consequence(self, test_consequence):
        current_consequence = {}
        self.consequence(current_consequence)

        return current_consequence == test_consequence