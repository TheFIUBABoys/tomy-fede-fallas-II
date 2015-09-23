from app.inference_engine.rule import Rule

__author__ = 'tomas'


def condition1(subject):
    return subject['animal'] == 'dog'


def consequence1(subject):
    subject['legsQuantity'] = '4'


rule1 = Rule('All dogs have 4 legs', condition1, consequence1, {'animal': 'dog'}, ('animal',))


def condition2(subject):
    return subject['animal'] == 'spider'


def consequence2(subject):
    subject['legsQuantity'] = '8'


rule2 = Rule('All spiders have 8 legs', condition2, consequence2, {'animal': 'spider'}, ('animal',))


def condition3(subject):
    return subject['animal'] == 'ostrich'


def consequence3(subject):
    subject['legsQuantity'] = '2'


rule3 = Rule('All ostriches have 2 legs', condition3, consequence3, {'animal': 'ostrich'}, ('animal',))


def condition4(subject):
    return subject['legsQuantity'] == '4'


def consequence4(subject):
    subject['locomotion'] = 'quadruped'


rule4 = Rule('Anything with 4 legs is a quadruped', condition4, consequence4, {'legsQuantity': '4'},
             ('legsQuantity',))


def condition5(subject):
    return subject['legsQuantity'] == '2'


def consequence5(subject):
    subject['locomotion'] = 'biped'


rule5 = Rule('Anything with 2 legs is a biped', condition5, consequence5, {'legsQuantity': '2'},
             ('legsQuantity',))



def condition6(subject):
    return subject['legsQuantity'] == '8'


def consequence6(subject):
    subject['locomotion'] = 'octoped'


rule6 = Rule('Anything with 8 legs is a octoped', condition6, consequence6, {'legsQuantity': '8'},
             ('legsQuantity',))


def condition7(subject):
    return subject['animal'] == 'dog'


def consequence7(subject):
    subject['class'] = 'mammal'


rule7 = Rule('All dogs are mammals', condition7, consequence7, {'animal': 'dog'}, ('animal',))


def condition8(subject):
    return subject['animal'] == 'spider'


def consequence8(subject):
    subject['class'] = 'insect'


rule8 = Rule('All spiders are insects', condition8, consequence8, {'animal': 'spider'}, ('animal',))


def condition9(subject):
    return subject['animal'] == 'ostrich'


def consequence9(subject):
    subject['class'] = 'bird'


rule9 = Rule('All ostriches are birds', condition9, consequence9, {'animal': 'ostrich'}, ('animal',))


def condition10(subject):
    return subject['class'] == 'mammal'


def consequence10(subject):
    subject['skin'] = 'hair'


rule10 = Rule('All mammal have hair', condition10, consequence10, {'class': 'mammal'}, ('class',))


def condition11(subject):
    return subject['class'] == 'insect'


def consequence11(subject):
    subject['skin'] = 'chitin'


rule11 = Rule('All insects have chitin', condition11, consequence11, {'class': 'insect'}, ('class',))


def condition12(subject):
    return subject['class'] == 'bird'


def consequence12(subject):
    subject['skin'] = 'feathers'


rule12 = Rule('All birds have feathers', condition12, consequence12, {'class': 'bird'}, ('class',))


rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12]
