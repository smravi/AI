import sys

def is_variable(x):
    return is_string(x) and x[0].islower()


def is_numeric(x):
    return isinstance(x, int)


def is_str(x):
    return isinstance(x, str)


def is_string(x):
    return isinstance(x, str) and x[0].isalpha()


def is_list(x):
    return isinstance(x, list)

def is_tuple(x):
    return isinstance(x, tuple)


def is_predicate(x):
    x = x.strip()
    return is_string(x) and x[0].isupper()


def get_operator(x):
    x = x.strip()
    if is_numeric(x):
        return x
    else:
        return str(x)


def is_operator(x):
    x = x.strip()
    return is_string(x) and x in [AND, OR, NOT, IMPLIES]


def is_logic_constant(x):
    x = x.strip()
    return is_string(x) and x[0].isupper()


def not_implies_list(operator):
    return operator in [AND, OR, NOT]


NOT = '~'
AND = '&'
OR = '|'
IMPLIES = '=>'
OVERLOADED_IMPLIES = '>'
RECURSION_LIMIT = sys.getrecursionlimit()
