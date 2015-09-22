__author__ = 'tomas'

from app.inference_engine.rule import Rule

class KnowledgeBase:
	class DuplicatedRuleException(Exception):
	    pass

	class DuplicatedKnowledgeException(Exception):
	    pass

	def __init__(self):
	    self.rules_tree = {}
	    self.rules = {}
	    self.knowledge = {}

	def add_knowledge(self, new_knowledge):
		if (self.knowledge.get(new_knowledge.keys()[0]) is None):
			self.knowledge.update(new_knowledge);
		else:
			raise KnowledgeBase.DuplicatedKnowledgeException

	def add_rule(self, rule):
	    if self.rules.get(rule.name) is None:
	        self.rules[rule.name] = rule
	    else:
	        raise KnowledgeBase.DuplicatedRuleException

	    if self.rules_tree.get(rule.fields) is None:
	        self.rules_tree[rule.fields] = [rule]
	    else:
	        self.rules_tree[rule.fields].append(rule)

	def run_forward_chaining(self):
		forward_chaining_knowledge = self.knowledge.copy()
		rules_to_check = self.rules.copy()	# Copy rules that will be triggered

		restart = True
		while restart:
			restart = False

			for ruleName in rules_to_check.keys():
				currentRule = rules_to_check[ruleName]

				try:
					if (currentRule.evaluate(forward_chaining_knowledge)):	# Check if rule is applicable
						rules_to_check.pop(ruleName, None)
						restart = True	# Restart from beginning removing the triggered rule
						break
				except Rule.RuleNotApplyException:
					pass

		return forward_chaining_knowledge;

	def run_backward_chaining(self, hipotesis):
		if (self.knowledge.get(hipotesis.keys()[0]) is not None):	# If aldready exists at knowledge Knowledge Base
			return self.knowledge.get(hipotesis.keys()[0]) == hipotesis.values()[0]	# And has the correct value, return true

		for ruleName in self.rules:
			currentRule = self.rules[ruleName]
		
			if (currentRule.has_consequence(hipotesis)):	# If the rule has the consecuence of the hipotesis
				result = self.run_backward_chaining( currentRule.condition )	# Repeat for the condition of the rule
				if result:
					return True

		return False


