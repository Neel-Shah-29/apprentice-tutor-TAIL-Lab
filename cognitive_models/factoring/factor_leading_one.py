import math
from functools import reduce
from random import randint
from pprint import pprint
from random import random

from py_rete import Fact
from py_rete import Production
from py_rete import ReteNetwork
from py_rete import V
from py_rete import Filter

from models import KnowledgeComponent

# from cognitive_models.base import check_sai
# from cognitive_models.base import get_hint
from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

import sympy as sp
import re
def quadratic_factorization(expression):
    x = sp.symbols('x')

    # Convert the expression to SymPy format
    expression = expression.replace("^", "**")  # Replace "^" with "**" for exponentiation
    expression = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', expression)  # Add "*" for multiplication between coefficient and variable

    # Parse the expression and factor it
    factored_expression = sp.factor(expression)

    return str(factored_expression.args[0]).replace("*",""), str(factored_expression.args[1]).replace("*","")

def factors(n):
    fset = set(reduce(list.__add__,
               ([i, n//i] for i in range(1, int(abs(n)**0.5) + 1)
                if n % i == 0)))

    other_signs = set([-1 * f for f in fset])
    fset = fset.union(other_signs)

    return fset

def factor_leading_one_problem():
    n1 = 1

    print(type(random))

    n2 = randint(1, 5)
    if random() > 0.5:
        n2 *= -1

    n3 = 1

    n4 = randint(1, 5)
    if random() > 0.5:
        n4 *= -1

    problem = "x^2"

    b_value = n1*n4+n2*n3
    if b_value == 0:
        return factor_leading_one_problem()

    if b_value > 0:
        problem += "+"

    problem += "{}x".format(b_value)

    c_value = n2 * n4
    if c_value > 0:
        problem += "+"

    problem += "{}".format(c_value)

    return problem

def factor_leading_one_model():
    net = ReteNetwork()

    # compute value of b 
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="b_value", disabled=False)) 
    def update_b_value(init_value):
        mid = init_value.split('x')[1]
        if "-" in mid:
            b = '-' + mid.split('-')[-1]
        else:
            b = mid.split('+')[1]
        return [Fact(selection="b_value", action="input change", input=b)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="c_value", disabled=False))
    def update_c_value(init_value):
        c = init_value.split('x')[-1].replace('+', '')
        return [Fact(selection="c_value", action="input change", input=c)]

    @Production(Fact(field="c_value", value=V('product_c'),
                     disabled=True) &
                Fact(field="b_value", value=V('sum_b'),
                     disabled=True) &
                Fact(field=V('selection1'), row=1, column=1,
                     disabled=False) &
                Fact(field=V('selection2'), row=1, column=2,
                     disabled=False))
    def update_factors_row1(product_c, sum_b, selection1, selection2):
        product_c = int(product_c)
        all_factors = [(abs((product_c/f + f) - int(sum_b)), f)
                       for f in factors(product_c)]
        all_factors.sort()
        sais = [Fact(selection=selection1, action="input change",
                     input='{}'.format(f)) for _, f in all_factors]
        sais += [Fact(selection=selection2, action="input change",
                      input='{}'.format(f)) for _, f in all_factors]
        return sais

    @Production(Fact(field="c_value", value=V('product_c'),
                     disabled=True) &
                Fact(field="b_value", value=V('sum_b'),
                     disabled=True) &
                Fact(field=V('selection1'), row=V('row'), column=1,
                     disabled=False) &
                Fact(row=V('prev_row'), column=1, disabled=True) &
                Filter(lambda row, prev_row: prev_row + 1 == row) &
                Fact(field=V('selection2'), row=V('row'), column=2,
                     disabled=False) &
                Fact(row=V('prev_row'), column=2, disabled=True) &
                ~Fact(column=4, disabled=True) &
                Fact(row=V('prev_row'), column=3, value=V('prev_sum'),
                     disabled=True) &
                Filter(lambda prev_sum, sum_b: prev_sum != sum_b))
    def update_factors_other_rows(product_c, sum_b, selection1, selection2):
        product_c = int(product_c)
        all_factors = [(abs((product_c/f + f) - int(sum_b)), f)
                       for f in factors(product_c)]
        all_factors.sort()

        sais = [Fact(selection=selection1, action="input change",
                     input='{}'.format(f)) for _, f in all_factors]
        sais += [Fact(selection=selection2, action="input change",
                      input='{}'.format(f)) for _, f in all_factors]
        return sais

    @Production(Fact(field="c_value", value=V('product_c'),
                     disabled=True) &
                Fact(field=V('selection'), row=V('row'), column=1,
                     disabled=False) &
                Fact(row=V('row'), column=2, value=V('other_factor'),
                     disabled=True))
    def update_factor_1_other(product_c, other_factor, selection):
        f = int(int(product_c) / int(other_factor))
        return [Fact(selection=selection, action="input change",
                     input='{}'.format(f))]

    @Production(Fact(field="c_value", value=V('product_c'),
                     disabled=True) &
                Fact(row=V('row'), column=1, value=V('other_factor'),
                     disabled=True) &
                Fact(field=V('selection'), row=V('row'), column=2,
                     disabled=False))
    def update_factor_2_other(product_c, other_factor, selection):
        f = int(int(product_c) / int(other_factor))
        return [Fact(selection=selection, action="input change",
                     input='{}'.format(f))]

    @Production(Fact(row=V('row'), column=1, value=V('first_factor'),
                     disabled=True) &
                Fact(row=V('row'), column=2, value=V('second_factor'),
                     disabled=True) &
                Fact(field=V('selection'), row=V('row'), column=3,
                     disabled=False))
    def sum_factors(first_factor, second_factor, selection):
        s = int(int(first_factor) + int(second_factor))
        return [Fact(selection=selection, action="input change",
                     input='{}'.format(s))]

    @Production(Fact(field="b_value", value=V('b'), disabled=True) &
                Fact(row=V('row'), column=3, value=V('b'), disabled=True) &
                Fact(field=V('selection'), row=V('row'), column=4,
                     disabled=False))
    def update_sum_equals_b(selection):
        return [Fact(selection=selection, action="input change",
                     input="checked")]

    @Production(Fact(row=V('row'), column=4, disabled=True) &
                Fact(row=V('row'), column=1, disabled=True,
                     value=V('factor1')) &
                Fact(row=V('row'), column=2, disabled=True,
                     value=V('factor2')) &
                Fact(field='first_expression', disabled=False) &
                Fact(field='second_expression', disabled=False))
    def create_first_expression(factor1, factor2):
        resp = []
        factor1 = int(factor1)
        factor2 = int(factor2)

        if factor1 < 0:
            resp.append(Fact(selection="first_expression",
                        action="input change",
                        input="(x-{})".format(abs(factor1))))
            resp.append(Fact(selection="second_expression",
                        action="input change",
                        input="(x-{})".format(abs(factor1))))
        else:
            resp.append(Fact(selection="first_expression",
                        action="input change",
                        input="(x+{})".format(abs(factor1))))
            resp.append(Fact(selection="second_expression",
                        action="input change",
                        input="(x+{})".format(abs(factor1))))

        if factor2 < 0:
            resp.append(Fact(selection="first_expression",
                        action="input change",
                        input="(x-{})".format(abs(factor2))))
            resp.append(Fact(selection="second_expression",
                        action="input change",
                        input="(x-{})".format(abs(factor2))))
        else:
            resp.append(Fact(selection="first_expression",
                        action="input change",
                        input="(x+{})".format(abs(factor2))))
            resp.append(Fact(selection="second_expression",
                        action="input change",
                        input="(x+{})".format(abs(factor2))))

        return resp

    @Production(Fact(row=V('row'), column=4, disabled=True) &
                Fact(row=V('row'), column=1, disabled=True,
                     value=V('factor1')) &
                Fact(row=V('row'), column=2, disabled=True,
                     value=V('factor2')) &
                Fact(field="first_expression", disabled=False) &
                Fact(field="second_expression", disabled=True,
                     value=V('second_exp')))
    def create_second_expression_first(factor1, factor2, second_exp):
        factor1 = int(factor1)
        factor2 = int(factor2)

        if '-' in second_exp:
            other = int('-' + second_exp.split('-')[-1].replace(')', ''))
        else:
            other = int(second_exp.split('+')[-1].replace(')', ''))

        if other == factor1 and factor2 < 0:
            return [Fact(selection="first_expression",
                    action="input change",
                    input="(x-{})".format(abs(factor2)))]
        if other == factor1:
            return [Fact(selection="first_expression",
                    action="input change",
                    input="(x+{})".format(abs(factor2)))]
        if other == factor2 and factor1 < 0:
            return [Fact(selection="first_expression",
                    action="input change",
                    input="(x-{})".format(abs(factor1)))]
        if other == factor2:
            return [Fact(selection="first_expression",
                    action="input change",
                    input="(x+{})".format(abs(factor1)))]

    @Production(Fact(row=V('row'), column=4, disabled=True) &
                Fact(row=V('row'), column=1, disabled=True,
                     value=V('factor1')) &
                Fact(row=V('row'), column=2, disabled=True,
                     value=V('factor2')) &
                Fact(field="first_expression", disabled=True,
                     value=V('first_exp')) &
                Fact(field="second_expression", disabled=False))
    def create_second_expression_second(factor1, factor2, first_exp):
        factor1 = int(factor1)
        factor2 = int(factor2)

        if '-' in first_exp:
            other = int('-' + first_exp.split('-')[-1].replace(')', ''))
        else:
            other = int(first_exp.split('+')[-1].replace(')', ''))

        if other == factor1 and factor2 < 0:
            return [Fact(selection="second_expression",
                    action="input change",
                    input="(x-{})".format(abs(factor2)))]
        if other == factor1:
            return [Fact(selection="second_expression",
                    action="input change",
                    input="(x+{})".format(abs(factor2)))]
        if other == factor2 and factor1 < 0:
            return [Fact(selection="second_expression",
                    action="input change",
                    input="(x-{})".format(abs(factor1)))]
        if other == factor2:
            return [Fact(selection="second_expression",
                    action="input change",
                    input="(x+{})".format(abs(factor1)))]

    @Production(Fact(field="final_answer", disabled=False) &
                Fact(field="first_expression", disabled=True,
                     value=V('first_exp')) &
                Fact(field="second_expression", disabled=True,
                     value=V('second_exp')) &
                Fact(field="initial_problem", value=V('init_value')))
    def update_final_answer(first_exp, second_exp, init_value):
        final_1, final_2 = quadratic_factorization(init_value)
        return [Fact(selection="final_answer", action="input change",
                     input="({})({})".format(final_1, final_2)),
                Fact(selection="final_answer", action="input change",
                     input="({})({})".format(final_2, final_1))]

    @Production(Fact(field="final_answer", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click",
                     input="")]

    net.add_production(update_b_value)
    net.add_production(update_c_value)
    net.add_production(update_factors_row1)
    net.add_production(update_factors_other_rows)
    net.add_production(update_factor_1_other)
    net.add_production(update_factor_2_other)
    net.add_production(sum_factors)
    net.add_production(update_sum_equals_b)
    net.add_production(create_first_expression)
    net.add_production(create_second_expression_first)
    net.add_production(create_second_expression_second)
    net.add_production(update_final_answer)
    net.add_production(select_done)

    return net


def factor_leading_one_kc_mapping():
    # key --> rule
    # value --> human readable value for kc (unique)

    kcs = {
        "update_b_value": "Extract b value",
        "update_c_value": "Extract c value",
        'update_factors_row1': 'Compute first factor',
        'update_factors_other_rows': 'Compute first factor',
        'update_factor_1_other': 'Compute second factor',
        'update_factor_2_other': 'Compute second factor',
        'sum_factors': "Compute sum of factors",
        'update_sum_equals_b': "Determine if sum of factors equals s",
        'create_first_expression':
            "Create first expression from factors when leading coef is 1",
        'create_second_expression_first':
            "Create second expression from factors when leading coef is 1",
        'create_second_expression_second':
            "Create second expression from factors when leading coef is 1",
        'update_final_answer':
            'Combine expressions to create final factored form',
        'select_done': "Determine if factoring is complete"

    }
    return kcs


def factor_leading_one_intermediate_hints():
    hints = {
        "update_b_value": [
            "The b value is extracted from the middle term of the trinomial."],
        "update_c_value": [
            "The c value is extracted from the last term of the trinomial."],
        'update_factors_row1': ["Enter a factor of r."],
        'update_factors_other_rows': ["Enter a factor of c."],
        'update_factor_1_other': ["Enter the value that when multipled with"
                                  " the other factor yields c."],
        'update_factor_2_other': ["Enter the value that when multipled with"
                                  " the other factor yields c."],
        'sum_factors': [
            "This value is computed by adding the two factors in this row."],
        'update_sum_equals_b': [
            "Check this box if the sum of the factors is equal to b."],
        'create_first_expression': ["This expression has the form (x+v) where"
                                    " v is one of the factors from the table"
                                    " above."],
        'create_second_expression_first': ["This expression has the form (x+v)"
                                           " where v is other factor you have"
                                           " not already used."],
        'create_second_expression_second': [
            "This expression has the form (x+v) where v is other factor you"
            " have not already used."],
        'update_final_answer': ["The final factored form is the"
                                " combination of the two expressions."],
        'select_done': ["Once you have found the final factored form you can"
                        " select the done button to move to the next problem."]
    }
    return hints

def factor_leading_one_studymaterial():
    study_material = studymaterial["factor_leading_one"]
    return study_material

loaded_models.register(CognitiveModel("factoring_polynomials",
                                      "factor_leading_one",
                                      factor_leading_one_model,
                                      factor_leading_one_problem,
                                      factor_leading_one_kc_mapping(),
                                      factor_leading_one_intermediate_hints(),
                                      factor_leading_one_studymaterial()))