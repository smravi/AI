import sys
import Assignment_3.inference.parse as parse
import Assignment_3.inference.utils as utils
import itertools

counter = itertools.count()

def string_check_cnf(clause):
    if utils.is_str(clause):
        return parse.parse_sentence(clause)
    else:
        return clause

def get_cnf_sentence(clause):
    # clause = parse.parse_sentence(clause)
    if clause:
        clause = string_check_cnf(clause)
        clause = horn_form(clause)
        clause = negate(clause)
        std_dict, clause = standardize(clause)
        clause = conjunction_of_disjunction(clause)
    return clause


def standardize(clause, std_map=None):
    if std_map is None:
        std_map = dict()
    if utils.is_variable(clause.operator):
        if clause in std_map:
            return (std_map, std_map[clause])
        else:
            new_variable = 'p_{}'.format(next(counter))
            std_map[clause] = parse.Sentence(new_variable)
            return (std_map, std_map[clause])
    else:
        arguments = [standardize(operand, std_map)[1] for operand in clause.operands]
        sentence = parse.Sentence(clause.operator, *arguments)
        return (std_map, sentence)


def horn_form(clause):

    if contains_operand(clause):
        # if the clause contaisns operands then change the form
        operands = [horn_form(operand) for operand in clause.operands]
        if clause.operator == utils.OVERLOADED_IMPLIES:
            # return ~a | b
            return (operands[-1] | ~operands[0])
        else:
            if utils.not_implies_list(clause.operator):
                return parse.Sentence(clause.operator, *operands)
    else:
        # if its a operator there is nothing to do just return
        return clause


def negate(clause):
    if not contains_operand(clause):
        return clause
    elif clause.operator is utils.NOT:
        term = clause.operands[0]
        if term.operator is utils.NOT:
            return negate(term.operands[0])
        if term.operator is utils.AND:
            arguments = [negate(~operand) for operand in term.operands]
            return normalize_operator(utils.OR, arguments)
        if term.operator is utils.OR:
            arguments = [negate(~operand) for operand in term.operands]
            return normalize_operator(utils.AND, arguments)
        return clause
    else:
        arguments = [negate(operand) for operand in clause.operands]
        return parse.Sentence(clause.operator, *arguments)


# associate
def normalize_operator(operator, operands):
    operands = atomize_terms(operator, operands)
    if len(operands) > 1:
        return parse.Sentence(operator, *operands)
    else:
        return operands[0]


# disassociate
def atomize_terms(operator, operands):
    op_list = []
    atomize(operands, operator, op_list)
    return op_list


def atomize(operands, operator, op_list):
    for operand in operands:
        if operand.operator == operator:
            atomize(operand.operands, operand.operator, op_list)
        else:
            op_list.append(operand)


def CnfError(Exception):
    pass


def check_for_length(operand_list):
    # this case will not happen
    # if len(operand_list) == 0:
    #     raise CnfError(operand_list)
    if len(operand_list) == 1:
        return operand_list[0]


def conjunction_of_disjunction(clause):
    if clause.operator == utils.AND:
        arguments = [conjunction_of_disjunction(operand) for operand in clause.operands]
        return normalize_operator(utils.AND, arguments)
    elif clause.operator == utils.OR:
        clause = normalize_operator(utils.OR, clause.operands)

        if clause.operator != utils.OR:
            return conjunction_of_disjunction(clause)
        value = check_for_length(clause.operands)
        if value:
            return conjunction_of_disjunction(value)
        first_term = None
        for operand in clause.operands:
            if operand.operator == utils.AND:
                first_term = operand
        if first_term:
            # check if this works
            remain_terms = []
            for operand in clause.operands:
                if operand is not first_term:
                    remain_terms.append(operand)
            remain_clause = normalize_operator(utils.OR, remain_terms)
            and_arguments = []
            for terms in first_term.operands:
                and_arguments.append(conjunction_of_disjunction(terms | remain_clause))
            return normalize_operator(utils.AND, and_arguments)
        else:
            return clause
    else:
        return clause


# disjuncts
def convert_with_or(clause):
    return atomize_terms(utils.OR, [clause])


# conjuncts
def convert_with_and(clause):
    return atomize_terms(utils.AND, [clause])


def contains_operand(clause):
    return (not utils.is_string(clause.operator) and bool(clause.operands))


#print(get_cnf_sentence('(~(B(x,y) & ~C(x,y)) => A(x))'))
#print(get_cnf_sentence('~(Parent(x,y) & Ancestor(y,z)) | Ancestor(x,z)'))
#print(get_cnf_sentence('(P(x) & Q(y)) | (R(x) & S(t))'))
#print(convert_with_and(get_cnf_sentence('(P(x)&(Q(x)&(R(x)|S(x))))')))
#print(convert_with_and(get_cnf_sentence('(P(x)=>((P(y)=>P(D)) & ~(Q(x,y)=>P(y))))')))