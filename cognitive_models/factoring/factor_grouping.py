import math
from functools import reduce
from random import randint
from random import random
import re
# from pprint import pprint

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


def factor_grouping_problem():
    n1 = randint(2, 5)
    # if random() > 0.5:
    #     n1 *= -1

    n2 = randint(1, 5)
    if random() > 0.5:
        n2 *= -1

    n3 = randint(1, 5)
    # if random() > 0.5:
    #     n3 *= -1

    n4 = randint(1, 5)
    if random() > 0.5:
        n4 *= -1

    if math.gcd(n1, n2) != 1 or math.gcd(n3, n4) != 1:
        return factor_grouping_problem()

    # (n1*x+n2)(n3*x+n4)
    # n1*n3*x^2 + (n1*n4 + n2*n3)*x + n2*n4

    problem = "{}x^2".format(n1*n3)

    # need to catch this edge case and regenerate.
    b_value = n1*n4+n2*n3
    if b_value == 0:
        return factor_grouping_problem()

    if b_value > 0:
        problem += "+"

    problem += "{}x".format(b_value)

    c_value = n2 * n4
    if c_value > 0:
        problem += "+"

    problem += "{}".format(c_value)

    return problem


def factor_grouping_model():

    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="a_value", disabled=False))
    def update_a_value(init_value):
        a = init_value.split('x')[0]
        return [Fact(selection="a_value", action="input change", input=a)]

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

    @Production(Fact(field="a_value", value=V('a_value'), disabled=True) &
                Fact(field="c_value", value=V('c_value'), disabled=True) &
                Fact(field="product_ac", disabled=False))
    def update_product_ac(a_value, c_value):
        a_value = int(a_value)
        c_value = int(c_value)
        ac = a_value * c_value
        return [Fact(selection="product_ac", action="input change",
                     input="{}".format(ac))]

    @Production(Fact(field="product_ac", value=V('product_ac'),
                     disabled=True) &
                Fact(field="b_value", value=V('sum_b'),
                     disabled=True) &
                Fact(field=V('selection1'), row=1, column=1,
                     disabled=False) &
                Fact(field=V('selection2'), row=1, column=2,
                     disabled=False))
    def update_factors_row1(product_ac, sum_b, selection1, selection2):
        product_ac = int(product_ac)
        all_factors = [(abs((product_ac/f + f) - int(sum_b)), f)
                       for f in factors(product_ac)]
        all_factors.sort()

        sais = [Fact(selection=selection1, action="input change",
                     input='{}'.format(f)) for _, f in all_factors]
        sais += [Fact(selection=selection2, action="input change",
                      input='{}'.format(f)) for _, f in all_factors]
        return sais

    @Production(Fact(field="product_ac", value=V('product_ac'),
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
                Fact(field="b_value", value=V('b_value'),
                     disabled=True) &
                Filter(lambda prev_sum, b_value: prev_sum != b_value))
    def update_factors_other_rows(product_ac, sum_b, selection1, selection2):
        product_ac = int(product_ac)
        all_factors = [(abs((product_ac/f + f) - int(sum_b)), f)
                       for f in factors(product_ac)]
        all_factors.sort()

        sais = [Fact(selection=selection1, action="input change",
                     input='{}'.format(f)) for _, f in all_factors]
        sais += [Fact(selection=selection2, action="input change",
                      input='{}'.format(f)) for _, f in all_factors]
        return sais

    @Production(Fact(field="product_ac", value=V('product_ac'),
                     disabled=True) &
                Fact(field=V('selection'), row=V('row'), column=1,
                     disabled=False) &
                Fact(row=V('row'), column=2, value=V('other_factor'),
                     disabled=True))
    def update_factor_1_other(product_ac, other_factor, selection):
        f = int(int(product_ac) / int(other_factor))
        return [Fact(selection=selection, action="input change",
                     input='{}'.format(f))]

    @Production(Fact(field="product_ac", value=V('product_ac'),
                     disabled=True) &
                Fact(row=V('row'), column=1, value=V('other_factor'),
                     disabled=True) &
                Fact(field=V('selection'), row=V('row'), column=2,
                     disabled=False))
    def update_factor_2_other(product_ac, other_factor, selection):
        f = int(int(product_ac) / int(other_factor))
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
                Fact(row=V('row'), column=2, disabled=True,
                     value=V('factor1')) &
                Fact(row=V('row'), column=1, disabled=True,
                     value=V('factor2')) &
                Fact(field="p_value", disabled=False) &
                Fact(field="q_value", disabled=False))
    def update_pq_first(factor1, factor2):
        return [Fact(selection="p_value", action="input change",
                     input=factor1),
                Fact(selection="p_value", action="input change",
                     input=factor2),
                Fact(selection="q_value", action="input change",
                     input=factor1),
                Fact(selection="q_value", action="input change",
                     input=factor2)]

    @Production(Fact(field="q_value", value=V('p_value'), disabled=True) &
                Fact(field="product_ac", value=V('product_ac'),
                     disabled=True) &
                Fact(field="p_value", disabled=False))
    def update_p_second(product_ac, q_value):
        p_value = int(int(product_ac) / int(q_value))
        return [Fact(selection="p_value", action="input change",
                     input="{}".format(p_value))]

    @Production(Fact(field="p_value", value=V('p_value'), disabled=True) &
                Fact(field="product_ac", value=V('product_ac'),
                     disabled=True) &
                Fact(field="q_value", disabled=False))
    def update_q_second(product_ac, p_value):
        q_value = int(int(product_ac) / int(p_value))
        return [Fact(selection="q_value", action="input change",
                     input="{}".format(q_value))]

    @Production(Fact(field="p_value", value=V('p_value'), disabled=True) &
                Fact(field="a_value", value=V('a_value'), disabled=True) &
                Fact(field='first_part', disabled=False))
    def get_first_part(p_value, a_value):
        answer = "{}x^2".format(a_value)
        if int(p_value) > 0:
            answer += "+"
        answer += "{}x".format(p_value)
        return [Fact(selection="first_part", action="input change",
                     input=answer)]

    @Production(Fact(field="q_value", value=V('q_value'), disabled=True) &
                Fact(field="c_value", value=V('c_value'), disabled=True) &
                Fact(field='second_part', disabled=False))
    def get_second_part(q_value, c_value):
        answer = "x" if int(q_value) == 1 else "{}x".format(q_value)
        if int(c_value) > 0:
            answer += "+"
        answer += "{}".format(c_value)
        return [Fact(selection="second_part", action="input change",
                     input=answer)]

    @Production(Fact(field='first_part', value=V('first_part'),
                     disabled=True) &
                Fact(field='gcf_factor_1', disabled=False))
    def gcf_part1(first_part):
        term1 = first_part.split('x')[0]
        term2 = first_part.split('^2')[1].split('x')[0].replace('+', '')
        gcf = math.gcd(int(term1), int(term2))

        if int(term1) < 0:
            gcf = -1 * gcf

        inner_1 = int(int(term1)/gcf)
        inner_2 = int(int(term2)/gcf)
        inside = "x" if inner_1 == 1 else "{}x".format(inner_1)
        if inner_2 > 0:
            inside += "+"
        inside += "{}".format(inner_2)
        if gcf == 1:
            answer = "x({})".format(inside)
        else:
            answer = "{}x({})".format(gcf, inside)
        return [Fact(selection="gcf_factor_1", action="input change",
                     input=answer)]

    @Production(Fact(field='second_part', value=V("second_part"),
                     disabled=True) &
                Fact(field='gcf_factor_2', disabled=False))
    def gcf_part2(second_part):
        term1 = second_part.split('x')[0]
        term2 = second_part.split('x')[1].replace('+', '')
        gcf = math.gcd(int(term1), int(term2))

        if int(term1) < 0:
            gcf = -1 * gcf
        inner_1 = int(int(term1)/gcf)
        inner_2 = int(int(term2)/gcf)
        inside = "x" if inner_1 == 1 else "{}x".format(inner_1)
        if inner_2 > 0:
            inside += "+"
        inside += "{}".format(inner_2)

        answer = "{}({})".format(gcf, inside)

        return [Fact(selection="gcf_factor_2", action="input change",
                     input=answer)]

    @Production(Fact(field="gcf_factor_1", value=V('gcf_factor_1'),
                     disabled=True) &
                Fact(field="gcf_factor_2", value=V('gcf_factor_2'),
                     disabled=True) &
                Fact(field='gcf_final_1', disabled=False))
    def gcf_final_1(gcf_factor_1, gcf_factor_2):
        inside = gcf_factor_1.split('(')[1].replace(")", "")
        return [Fact(selection="gcf_final_1", action="input change",
                     input=inside),
                Fact(selection="gcf_final_1", action="input change",
                     input="({})".format(inside))]

    @Production(Fact(field="gcf_factor_1", value=V('gcf_factor_1'),
                     disabled=True) &
                Fact(field="gcf_factor_2", value=V('gcf_factor_2'),
                     disabled=True) &
                Fact(field='gcf_final_2', disabled=False))
    def gcf_final_2(gcf_factor_1, gcf_factor_2):
        remaining_1 = gcf_factor_1.split('(')[0]
        remaining_2 = gcf_factor_2.split('(')[0]

        if remaining_2[0] == "-":
            answer = "{}{}".format(remaining_1, remaining_2)
        else:
            answer = "{}+{}".format(remaining_1, remaining_2)

        return [Fact(selection="gcf_final_2", action="input change",
                     input=answer),
                Fact(selection="gcf_final_2", action="input change",
                     input="({})".format(answer))]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field='final_answer', disabled=False))
    def update_final_answer(init_value):
        gcf_final_1, gcf_final_2 = quadratic_factorization(init_value)
        return [Fact(selection="final_answer", action="input change",
                     input="({})({})".format(gcf_final_1, gcf_final_2)),
                Fact(selection="final_answer", action="input change",
                     input="({})({})".format(gcf_final_2, gcf_final_1))]

    @Production(Fact(field="final_answer", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click",
                     input="")]

    net.add_production(update_a_value)
    net.add_production(update_b_value)
    net.add_production(update_c_value)
    net.add_production(update_product_ac)
    net.add_production(update_factors_row1)
    net.add_production(update_factors_other_rows)
    net.add_production(update_factor_1_other)
    net.add_production(update_factor_2_other)
    net.add_production(sum_factors)
    net.add_production(update_sum_equals_b)
    net.add_production(update_pq_first)
    net.add_production(update_p_second)
    net.add_production(update_q_second)
    net.add_production(get_first_part)
    net.add_production(get_second_part)
    net.add_production(gcf_part1)
    net.add_production(gcf_part2)
    net.add_production(gcf_final_1)
    net.add_production(gcf_final_2)
    net.add_production(update_final_answer)
    net.add_production(select_done)

    return net


def factor_grouping_kc_mapping():
    # net = factor_grouping_model()
    # skill_to_kc = {p.__wrapped__.__name__: p.__wrapped__.__name__ for p in
    #                net.productions}

    skill_to_kc = {
        'update_a_value': 'Extract a value',
        'update_b_value': 'Extract b value',
        'update_c_value': 'Extract c value',
        'update_product_ac': 'Update r value based on product of ac',
        'update_factors_row1': 'Compute first factor',
        'update_factors_other_rows': 'Compute first factor',
        'update_factor_1_other': 'Compute second factor',
        'update_factor_2_other': 'Compute second factor',
        'sum_factors': 'Compute sum of factors',
        'update_sum_equals_b': "Determine if sum of factors equals s",
        'update_pq_first': 'Extract first p or q value',
        'update_p_second': 'Extract second p or q value',
        'update_q_second': 'Extract second p or q value',
        'get_first_part':
            'Extract first half of trinomial for factoring by grouping',
        'get_second_part':
            'Extract second half of trinomial for factoring by grouping',
        'gcf_part1': 'Factor GCF out of expression',
        'gcf_part2': 'Factor GCF out of expression',
        'gcf_final_1': 'Extract GCF from two expressions',
        'gcf_final_2': 'Divide GCF out of two expressions',
        'update_final_answer':
            'Combine expressions to create final factored form',
        'select_done': 'Determine if factoring is complete',
        }

    return skill_to_kc


def factor_grouping_intermediate_hints():
    hints = {
        "update_a_value": [
            "The a value is extracted from the first term of the trinomial."],
        "update_b_value": [
            "The b value is extracted from the middle term of the trinomial."],
        "update_c_value": [
            "The c value is extracted from the last term of the trinomial."],
        "update_product_ac": [
            "The ac value is computed by multiplying a times c."],
        'update_factors_row1': ["Enter a factor of ac."],
        'update_factors_other_rows': ["Enter a factor of ac."],
        'update_factor_1_other': ["Enter the value that when multipled with"
                                  " the other factor yields ac."],
        'update_factor_2_other': ["Enter the value that when multipled with"
                                  " the other factor yields ac."],
        'sum_factors': [
            "This value is computed by adding the two factors in this row."],
        'update_sum_equals_b': [
            "Check this box if the sum of the factors is equal to b."],
        'update_pq_first': ["This is one of the factors from the table"
                            " above."],
        'update_p_second': ["This is the other factor from the table above."],
        'update_q_second': ["This is the other factor from the table above."],

        'get_first_part': [
            "This group has the form ax^2 + px."],
        'get_second_part': [
            "This group has the form qx + c."],
        'gcf_part1': ['Factor the greatest common factor out of the first'
                      ' group of terms.'],
        'gcf_part2': ['Factor the greatest common factor out of the second'
                      ' group of terms.'],
        'gcf_final_1': ['Enter the greatest common factor of the two'
                        ' factored groups of terms.'],
        'gcf_final_2': ['Enter the terms that remain after factoring the'
                        ' greatest common factor out of the two factored'
                        ' groups of terms.'],
        'update_final_answer': ["The final factored form is the"
                                " combination of the two expressions."],
        'select_done': ["Once you have found the final factored form you can"
                        " select the done button to move to the next problem."]
    }
    return hints

def factor_grouping_studymaterial():
    study_material = studymaterial["factor_grouping"]
    return study_material

loaded_models.register(CognitiveModel("factoring_polynomials",
                                      "factor_grouping",
                                      factor_grouping_model,
                                      factor_grouping_problem,
                                      factor_grouping_kc_mapping(),
                                      factor_grouping_intermediate_hints(),
                                      factor_grouping_studymaterial()))
