__author__ = 'tomas'


class Rule:
    class RuleNotApplyException(Exception):
        pass

    def __init__(self, name, condition, consequence, fields=()):
        self.name = name
        self.condition = condition
        self.consequence = consequence
        self.fields = fields

    def evaluate(self, subject):
        self.validate_fields(subject)
        rule_applies = self.condition(subject)

        if rule_applies:
            self.consequence(subject)

        return rule_applies

    def validate_fields(self, subject):
        for field in self.fields:
            if subject.get(field) is None:
                raise Rule.RuleNotApplyException('Rule does not apply to subject')
