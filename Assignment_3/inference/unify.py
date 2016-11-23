import sys
import Assignment_3.inference.utils as utils
import Assignment_3.inference.parse as parse


class Unification(Exception):
    pass


def unify(x, y, theta):
    if theta is None:
        raise Unification(x, y, theta)
    elif x == y:
        return theta
    elif parse.var_sentence(x):
        return unify_var(x, y, theta)
    elif parse.var_sentence(y):
        return unify_var(y, x, theta)
    elif parse.is_sentence(x) and parse.is_sentence(y):
        return unify(x.operands, y.operands, unify(x.operator, y.operator, theta))
    elif utils.is_list(x) and utils.is_list(y) and (len(x) == len(y)):
        return unify(x[1:], y[1:], unify(x[0], y[0], theta))
    else:
        raise Unification


def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif x in theta:
        return unify(var, theta[x], theta)
    # assume no occur check occurs
    # elif occur_check(var, x):
    #     raise Unification
    else:
        theta[var] = x
        return theta


def substitute_theta(theta, clause):
    if utils.is_list(clause):
        arguments = [substitute_theta(theta, val) for val in clause]
        return arguments
    elif utils.is_tuple(clause):
        return tuple([substitute_theta(theta, val) for val in clause])
    elif not parse.is_sentence(clause):
        return clause
    elif utils.is_variable(clause.operator):
        return theta.get(clause, clause)
    else:
        arguments = [substitute_theta(theta, val) for val in clause.operands]
        return parse.Sentence(clause.operator, *arguments)
