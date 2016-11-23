import sys

import Assignment_3.inference.utils as utils
import re


class Sentence:
    def __init__(self, operator, *operands):
        if isinstance(operator, str) or (utils.is_numeric(operator) and not operands):
            self.operator = utils.get_operator(operator)
            self.operands = [parse_sentence(operand) for operand in operands]

    def __eq__(self, param):
        return (param is self) or (
            isinstance(param, Sentence) and self.operator == param.operator and self.operands == param.operands)

    def __hash__(self):
        return hash(self.operator) ^ hash(tuple(self.operands))

    def __call__(self, *operands):
        if utils.is_string(self.operator) and not self.operands:
            return Sentence(self.operator, *operands)

    def __invert__(self):
        return Sentence(utils.NOT, self)

    def __and__(self, param):
        return Sentence(utils.AND, self, param)

    def __or__(self, param):
        return Sentence(utils.OR, self, param)

    def __gt__(self, param):
        return Sentence(utils.OVERLOADED_IMPLIES, self, param)

    def __repr__(self):
        "Show something like 'P' or 'P(x, y)', or '~P' or '(P | Q | R)'"
        if len(self.operands) == 0:  # Constant or proposition with arity 0
            return str(self.operator)
        elif utils.is_string(self.operator):  # Functional or Propositional operator
            return '%s(%s)' % (self.operator, ', '.join(map(repr, self.operands)))
        elif len(self.operands) == 1:  # Prefix operator
            return self.operator + repr(self.operands[0])
        else:  # Infix operator
            return '(%s)' % (' ' + self.operator + ' ').join(map(repr, self.operands))

def is_sentence(x):
    return isinstance(x, Sentence)

def parse_sentence(operand):
    if isinstance(operand, Sentence):
        return operand
    if utils.is_numeric(operand):
        return Sentence(operand)
    # support operator overloading
    operand = operand.replace('=>', '>')
    operand = re.sub(r'([0-9a-zA-Z_.]+)', r'Sentence("\g<1>")', operand)
    result = eval(operand)
    return result

def var_sentence(x):
    return is_sentence(x) and utils.is_variable(x.operator) and not x.operands
#ex = parse_sentence('((B(x,y)&~C(x,y))=>A(x))')
#print(ex)
