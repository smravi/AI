import sys
import Assignment_3.inference.parse as parse
import Assignment_3.inference.utils as utils
import Assignment_3.inference.unify as unify
import Assignment_3.inference.cnf as cnf
import itertools
from collections import namedtuple
import time
count = itertools.count(0, 1)

Resolvent = namedtuple('Resolvent', 'substitute clause')
count = itertools.count(0, 1)

def preprocess(clauses):
    pre_clauses = clauses[:]
    new = set()
    for i_clause in range(len(clauses)):
        for j_clause in range(i_clause + 1, len(clauses)):
            fol_res = fol_resolve(clauses[i_clause], clauses[j_clause])
            if fol_res is not False:
                subst_values, resolvents = fol_res
                print(('resolvant: {}').format(resolvents))
                if len(resolvents) > 0 and subst_values:
                    print(('* subst :{}').format(subst_values))
                    print(('*before :{}').format(resolvents))
                    resolvents = unify.substitute_theta(subst_values, resolvents)
                    print(('*after :{}').format(resolvents))
                    print('------------------------------------------------')
                    for res in resolvents:
                        res.operands = list(set(res.operands))
                    new = new.union(set(resolvents))
                    if len(new) > 0 and not new.issubset(clauses):
                        pre_clauses.extend(resolvents)
    return pre_clauses


def get_predicates(clause, predicate_dict=None):
    if predicate_dict is None: predicate_dict = {}
    if not isinstance(clause, parse.Sentence):
        return {}
    elif utils.is_predicate(clause.operator):
        if not clause.operator in predicate_dict:
            predicate_dict[clause.operator] = [clause]
        else:
            predicate_dict[clause.operator].append(clause)
    elif clause.operator == '~':
        if not clause.operands[0].operator in predicate_dict:
            predicate_dict[clause.operands[0].operator] = [clause]
        else:
            predicate_dict[clause.operands[0].operator].append(clause)
    else:
        for c in clause.operands:
            get_predicates(c, predicate_dict)
    return predicate_dict


def is_not(literal):
    if literal.operator == '~':
        return True
    for arg in literal.operands:
        is_not(arg)
    return False


def find_resolvent(ci, cj):
    # TODO have to make sure only one resolvant happens at one time. Check if that is taken care.
    ci_predicate = get_predicates(ci)
    cj_predicate = get_predicates(cj)
    resolvent = []
    visited = set()
    # only one should initial_resolve
    for key in ci_predicate.keys():
        if key in cj_predicate:
            for ci_literal in ci_predicate[key]:
                for cj_literal in cj_predicate[key]:
                    if (is_not(ci_literal) and not is_not(cj_literal) or (
                                not is_not(ci_literal) and is_not(cj_literal))):
                        if not (ci_literal in visited and cj_literal in visited):
                            resolvent.append((ci_literal, cj_literal))
                            visited.add(ci_literal)
                            visited.add(cj_literal)

    return resolvent


class Solved(Exception):
    pass


def resolve_and_substitute(subst_values, substitute_clause):
    new = set()
    if subst_values:
        print(('* subst :{}').format(subst_values))
        print(('*before :{}').format(substitute_clause))
        substitute_clause = unify.substitute_theta(subst_values, substitute_clause)
        print(('*after :{}').format(substitute_clause))
        print('------------------------------------------------')
        new = set(substitute_clause)
    return substitute_clause, new

def checkTimeOut(timeout):
    if time.time() > timeout:
        return True

def recur_resolve(clauses, goal, substall, recur_depth, timeout):
    print(('search: {}').format(goal))
    if recur_depth > (utils.RECURSION_LIMIT - 50):
        return False
    setClause = set(clauses)
    for sentence in clauses:
        if checkTimeOut(timeout):
            return False
        print(('trying: {}------{}').format(goal, sentence))
        resolve_list = fol_resolve(sentence, goal[0])
        #this case if for handling for more than one resolvent in a clause
        for resolvents in resolve_list:
            print(('resolvant: {}').format(resolvents.clause))
            if len(resolvents.clause) == 0:
                print('###############')
                print(('* subst :{}').format(resolvents.substitute))
                return True
            else:
                new_clause_subst, new = resolve_and_substitute(resolvents.substitute, resolvents.clause)
                if len(new) > 0 and new.issubset(setClause):
                    continue
                dic, sent_clause = cnf.standardize(new_clause_subst[0])
                isResolved = recur_resolve(clauses + goal, [sent_clause], (resolvents.substitute, substall), recur_depth + 1, timeout)
                print('BACKTRACKING .......')
                if isResolved:
                    return True
    return False

def fol_resolve(ci, cj):
    resolve_list = []
    resolvents = find_resolvent(ci, cj)
    if len(resolvents) > 0:
        remove_set = set()
        for a, b in resolvents:
            if is_not(a):
                lit1 = a.operands[0]
                lit2 = b
            else:
                lit1 = a
                lit2 = b.operands[0]
            try:
                subst = {}
                unify.unify(lit1, lit2, subst)
            except unify.Unification:
                pass
            else:
                # if unified:
                print(next(count))
                print('removed', a, b)
                remove_set.add(a)
                remove_set.add(b)
        if len(remove_set) > 0:
            print('Clause')
            print(('{} ------ {}').format(ci, cj))

            ci_or = cnf.convert_with_or(ci)
            cj_or = cnf.convert_with_or(cj)
            ci_left = remove_terms(a, ci_or)
            cj_left = remove_terms(b, cj_or)
            new_clause = list(set(ci_left + cj_left))
            new_clause_expr = []
            if len(new_clause) > 0:
                new_clause_expr.append(cnf.normalize_operator(utils.OR, new_clause))
            resolve_list.append(Resolvent(subst, new_clause_expr))

    return resolve_list


def remove_terms(term, clause):
    result = []
    if isinstance(clause, str):
        result = clause.replace(term, '')
    else:
        for operand in clause:
            if term != operand:
                result.append(operand)
    return result


def fol_resolution_corrected(KB, alpha):
    sentences = KB
    try:
        return recur_resolve(sentences, cnf.convert_with_and(cnf.get_cnf_sentence(~alpha)), None, 0, time.time() + 30)
    except Solved:
        pass
    else:
        return False

# s = ['Mother(Liz,Charley)', 'Father(Charley,Billy)', '~Mother(x,y) | Parent(x,y)',
#      '~Father(x,y) | Parent(x,y)', '~Parent(x,y) | Ancestor(x,y)', '~(Parent(x,y) & Ancestor(y,z)) | Ancestor(x,z)']
# s = ['Dog(D)', 'Owns(Jack, D)',
#      '~Dog(y) | ~ Owns(x,y) |AnimalLover(x)', '~AnimalLover(w) | ~Animal(y) | ~Kills(w,y)',
#      'Kills(Jack,Tuna) | Kills(Curiosity,Tuna)', 'Cat(Tuna)', '~Cat(z) | Animal(z)']
s = ['A(x) => H(x)', 'D(x,y) => ~H(y)', '((B(x,y) & C(x,y)) => A(x))', 'B(John,Alice)', 'B(John,Bob)',
'(D(x,y) & Q(y)) => C(x,y)', 'D(John,Alice)', 'Q(Bob)', 'D(John,Bob)', 'F(x) => G(x)', 'G(x) => H(x)',
'H(x) => F(x)', 'R(x) => H(x)', 'R(Tom)']

inputkb = []
for item in s:
    inputkb.extend(cnf.convert_with_and(cnf.get_cnf_sentence(item)))

for i in inputkb:
    print(i)
print(len(inputkb))
print('*********************************')

resolved = fol_resolution_corrected(inputkb, parse.parse_sentence('H(John)'))
print(resolved)


