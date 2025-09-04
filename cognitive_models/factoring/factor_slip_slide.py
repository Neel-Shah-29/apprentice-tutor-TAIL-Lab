from dataclasses import field
import math
from functools import reduce
from random import randint
from random import random
from pprint import pprint
from typing import Mapping

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
    fset = set(
        reduce(list.__add__,
               ([i, n // i]
                for i in range(1,
                               int(abs(n)**0.5) + 1) if n % i == 0)))

    other_signs = set([-1 * f for f in fset])
    fset = fset.union(other_signs)

    return fset


def factor_slip_slide_problem():
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
        return factor_slip_slide_problem()

    problem = "{}x^2".format(n1 * n3)

    b_value = n1 * n4 + n2 * n3
    if b_value == 0:
        return factor_slip_slide_problem()

    if b_value > 0:
        problem += "+"

    problem += "{}x".format(b_value)

    c_value = n2 * n4
    if c_value > 0:
        problem += "+"

    problem += "{}".format(c_value)

    return problem


def factor_slip_slide_model():
    net = ReteNetwork()

    @Production(
        Fact(field="initial_problem", value=V('init_value'))
        & Fact(field="a_value", disabled=False))
    def update_a_value(init_value):
        a = init_value.split('x')[0]
        return [Fact(selection="a_value", action="input change", input=a)]

    @Production(
        Fact(field="initial_problem", value=V('init_value'))
        & Fact(field="b_value", disabled=False))
    def update_b_value(init_value):
        mid = init_value.split('x')[1]
        if "-" in mid:
            b = '-' + mid.split('-')[-1]
        else:
            b = mid.split('+')[1]
        return [Fact(selection="b_value", action="input change", input=b)]

    @Production(
        Fact(field="initial_problem", value=V('init_value'))
        & Fact(field="c_value", disabled=False))
    def update_c_value(init_value):
        c = init_value.split('x')[-1].replace('+', '')
        return [Fact(selection="c_value", action="input change", input=c)]

    @Production(
        Fact(field="a_value", value=V('a_value'), disabled=True)
        & Fact(field="c_value", value=V('c_value'), disabled=True)
        & Fact(field="product_ac", disabled=False))
    def update_product_ac(a_value, c_value):
        a_value = int(a_value)
        c_value = int(c_value)
        ac = a_value * c_value
        return [
            Fact(selection="product_ac",
                 action="input change",
                 input="{}".format(ac))
        ]

    @Production(
        Fact(field="b_value", value=V('b_value'), disabled=True) &
        Fact(field="product_ac", value=V('product_ac'), disabled=True) &
        Fact(field="new_equation", disabled=False))
    def update_new_trinomial(b_value, product_ac):
        b_value = int(b_value)
        product_ac = int(product_ac)

        if b_value > 0:
            b_value = "+{}".format(b_value)

        if product_ac > 0:
            product_ac = "+{}".format(product_ac)

        return [
            Fact(selection="new_equation",
                 action="input change",
                 input="x^2{}x{}".format(b_value, product_ac))
        ]

    @Production(
        Fact(field="new_equation", value=V('init_value'), disabled=True)
        & Fact(field="new_b_value", disabled=False))
    def update_new_b_value(init_value):
        mid = init_value.split('x')[1]
        if "-" in mid:
            b = '-' + mid.split('-')[-1]
        else:
            b = mid.split('+')[1]
        return [Fact(selection="new_b_value", action="input change", input=b)]

    @Production(
        Fact(field="new_equation", value=V('init_value'))
        & Fact(field="new_c_value", disabled=False))
    def update_new_c_value(init_value):
        c = init_value.split('x')[-1].replace('+', '')
        return [Fact(selection="new_c_value", action="input change", input=c)]

    @Production(Fact(field="new_c_value", value=V('product_c'),
                     disabled=True) &
                Fact(field="new_b_value", value=V('sum_b'),
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

    @Production(Fact(field="new_c_value", value=V('product_c'),
                     disabled=True) &
                Fact(field="new_b_value", value=V('sum_b'),
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

    @Production(Fact(field="new_c_value", value=V('product_c'),
                     disabled=True) &
                Fact(field=V('selection'), row=V('row'), column=1,
                     disabled=False) &
                Fact(row=V('row'), column=2, value=V('other_factor'),
                     disabled=True))
    def update_factor_1_other(product_c, other_factor, selection):
        f = int(int(product_c) / int(other_factor))
        return [Fact(selection=selection, action="input change",
                     input='{}'.format(f))]

    @Production(Fact(field="new_c_value", value=V('product_c'),
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

    @Production(Fact(field="new_b_value", value=V('b'), disabled=True) &
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
                Fact(field='new_first_expression', disabled=False) &
                Fact(field='new_second_expression', disabled=False))
    def create_first_expression(factor1, factor2):
        resp = []
        factor1 = int(factor1)
        factor2 = int(factor2)

        if factor1 < 0:
            resp.append(Fact(selection="new_first_expression",
                        action="input change",
                        input="(x-{})".format(abs(factor1))))
            resp.append(Fact(selection="new_second_expression",
                        action="input change",
                        input="(x-{})".format(abs(factor1))))
        else:
            resp.append(Fact(selection="new_first_expression",
                        action="input change",
                        input="(x+{})".format(abs(factor1))))
            resp.append(Fact(selection="new_second_expression",
                        action="input change",
                        input="(x+{})".format(abs(factor1))))

        if factor2 < 0:
            resp.append(Fact(selection="new_first_expression",
                        action="input change",
                        input="(x-{})".format(abs(factor2))))
            resp.append(Fact(selection="new_second_expression",
                        action="input change",
                        input="(x-{})".format(abs(factor2))))
        else:
            resp.append(Fact(selection="new_first_expression",
                        action="input change",
                        input="(x+{})".format(abs(factor2))))
            resp.append(Fact(selection="new_second_expression",
                        action="input change",
                        input="(x+{})".format(abs(factor2))))

        return resp

    @Production(Fact(row=V('row'), column=4, disabled=True) &
                Fact(row=V('row'), column=1, disabled=True,
                     value=V('factor1')) &
                Fact(row=V('row'), column=2, disabled=True,
                     value=V('factor2')) &
                Fact(field="new_first_expression", disabled=False) &
                Fact(field="new_second_expression", disabled=True,
                     value=V('second_exp')))
    def create_second_expression_first(factor1, factor2, second_exp):
        factor1 = int(factor1)
        factor2 = int(factor2)

        if '-' in second_exp:
            other = int('-' + second_exp.split('-')[-1].replace(')', ''))
        else:
            other = int(second_exp.split('+')[-1].replace(')', ''))

        if other == factor1 and factor2 < 0:
            return [Fact(selection="new_first_expression",
                    action="input change",
                    input="(x-{})".format(abs(factor2)))]
        if other == factor1:
            return [Fact(selection="new_first_expression",
                    action="input change",
                    input="(x+{})".format(abs(factor2)))]
        if other == factor2 and factor1 < 0:
            return [Fact(selection="new_first_expression",
                    action="input change",
                    input="(x-{})".format(abs(factor1)))]
        if other == factor2:
            return [Fact(selection="new_first_expression",
                    action="input change",
                    input="(x+{})".format(abs(factor1)))]

    @Production(Fact(row=V('row'), column=4, disabled=True) &
                Fact(row=V('row'), column=1, disabled=True,
                     value=V('factor1')) &
                Fact(row=V('row'), column=2, disabled=True,
                     value=V('factor2')) &
                Fact(field="new_first_expression", disabled=True,
                     value=V('first_exp')) &
                Fact(field="new_second_expression", disabled=False))
    def create_second_expression_second(factor1, factor2, first_exp):
        factor1 = int(factor1)
        factor2 = int(factor2)

        if '-' in first_exp:
            other = int('-' + first_exp.split('-')[-1].replace(')', ''))
        else:
            other = int(first_exp.split('+')[-1].replace(')', ''))

        if other == factor1 and factor2 < 0:
            return [Fact(selection="new_second_expression",
                    action="input change",
                    input="(x-{})".format(abs(factor2)))]
        if other == factor1:
            return [Fact(selection="new_second_expression",
                    action="input change",
                    input="(x+{})".format(abs(factor2)))]
        if other == factor2 and factor1 < 0:
            return [Fact(selection="new_second_expression",
                    action="input change",
                    input="(x-{})".format(abs(factor1)))]
        if other == factor2:
            return [Fact(selection="new_second_expression",
                    action="input change",
                    input="(x+{})".format(abs(factor1)))]

    @Production(
        Fact(field="a_value", value=V('a_value'), disabled=True) &
        Fact(field="new_first_expression", value=V('new_first_exp'),
             disabled=True) &
        Fact(field="raw_first_expression", disabled=False))
    def update_raw_first_expression(a_value, new_first_exp):
        return [Fact(selection="raw_first_expression",
                action="input change",
                input="{}/{})".format(
                     new_first_exp.replace(")", ''),
                     a_value))]

    @Production(
        Fact(field="a_value", value=V('a_value'), disabled=True) &
        Fact(field="new_second_expression", value=V('new_second_exp'),
             disabled=True) &
        Fact(field="raw_second_expression", disabled=False))
    def update_raw_second_expression(a_value, new_second_exp):
        return [Fact(selection="raw_second_expression",
                action="input change",
                input="{}/{})".format(
                     new_second_exp.replace(")", ''),
                     a_value))]

    @Production(
        Fact(field="raw_first_expression", value=V('raw_first_exp'),
             disabled=True) &
        Fact(field="simplified_first_expression", disabled=False))
    def update_simplified_first_expression(raw_first_exp):
        raw_first_exp = raw_first_exp.replace(' ', '').lower()
        numerator = int(raw_first_exp.split('x')[-1].split('/')[0])
        denominator = int(raw_first_exp.replace(')', '').split('/')[-1])
        gcd = math.gcd(numerator, denominator)
        
        if denominator / gcd == 1:
            value = numerator//gcd
            if value > 0:
                value = "+{}".format(value)
            return [Fact(selection="simplified_first_expression",
                    action="input change",
                    input="(x{})".format(value))]

        else:
            num = numerator//gcd
            if num > 0:
                num = "+{}".format(num)
            return [Fact(selection="simplified_first_expression",
                    action="input change",
                    input="(x{}/{})".format(num,
                                            denominator//gcd))]

    @Production(
        Fact(field="raw_second_expression", value=V('raw_second_exp'),
             disabled=True) &
        Fact(field="simplified_second_expression", disabled=False))
    def update_simplified_second_expression(raw_second_exp):
        raw_second_exp = raw_second_exp.replace(' ', '').lower()
        numerator = int(raw_second_exp.split('x')[-1].split('/')[0])
        denominator = int(raw_second_exp.replace(")", '').split('/')[-1])
        gcd = math.gcd(numerator, denominator)

        if denominator / gcd == 1:
            value = numerator//gcd
            if value > 0:
                value = "+{}".format(value)
            return [Fact(selection="simplified_second_expression",
                    action="input change",
                    input="(x{})".format(value))]

        else:
            num = numerator//gcd
            if num > 0:
                num = "+{}".format(num)
            return [Fact(selection="simplified_second_expression",
                    action="input change",
                    input="(x{}/{})".format(num,
                                            denominator//gcd))]

    @Production(
        Fact(field="simplified_first_expression",
             value=V('simplified_first_exp'), disabled=True) &
        Fact(field="final_first_expression", disabled=False))
    def update_final_first_expression(simplified_first_exp):
        if "/" not in simplified_first_exp:
            return [Fact(selection="final_first_expression",
                    action="input change",
                    input="{}".format(simplified_first_exp))]

        simplified_first_exp = simplified_first_exp.replace(' ', '').lower()
        numerator = int(simplified_first_exp.split('x')[-1].split('/')[0])
        denominator = int(simplified_first_exp.replace(")", '').split('/')[-1])

        if numerator > 0:
            numerator = "+{}".format(numerator)

        return [Fact(selection="final_first_expression",
                action="input change",
                input="({}x{})".format(denominator, numerator))]

    @Production(
        Fact(field="simplified_second_expression",
             value=V('simplified_second_exp'), disabled=True) &
        Fact(field="final_second_expression", disabled=False))
    def update_final_second_expression(simplified_second_exp):
        if "/" not in simplified_second_exp:
            return [Fact(selection="final_second_expression",
                    action="input change",
                    input="{}".format(simplified_second_exp))]

        simplified_second_exp = simplified_second_exp.replace(' ', '').lower()
        numerator = int(simplified_second_exp.split('x')[-1].split('/')[0])
        denominator = int(
            simplified_second_exp.replace(")", '').split('/')[-1])

        if numerator > 0:
            numerator = "+{}".format(numerator)

        return [Fact(selection="final_second_expression",
                action="input change",
                input="({}x{})".format(denominator, numerator))]

    @Production(
        Fact(field="final_first_expression",
             value=V('first_exp'), disabled=True) &
        Fact(field="final_second_expression",
             value=V('second_exp'), disabled=True)
        & Fact(field="final_answer", disabled=False) &
        Fact(field="initial_problem", value=V('init_value')))
    def update_final_answer(first_exp, second_exp, init_value):
        final_1, final_2 = quadratic_factorization(init_value)
        print(final_1, final_2)
        return [Fact(selection="final_answer", action="input change",
                     input="({})({})".format(final_1, final_2)),
                Fact(selection="final_answer", action="input change",
                     input="({})({})".format(final_2, final_1))]

    @Production(Fact(field="final_answer", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click",
                     input="")]

    net.add_production(update_a_value)
    net.add_production(update_b_value)
    net.add_production(update_c_value)
    net.add_production(update_product_ac)
    net.add_production(update_new_trinomial)
    net.add_production(update_new_b_value)
    net.add_production(update_new_c_value)
    net.add_production(update_factors_row1)
    net.add_production(update_factors_other_rows)
    net.add_production(update_factor_1_other)
    net.add_production(update_factor_2_other)
    net.add_production(sum_factors)
    net.add_production(update_sum_equals_b)
    net.add_production(create_first_expression)
    net.add_production(create_second_expression_first)
    net.add_production(create_second_expression_second)
    net.add_production(update_raw_first_expression)
    net.add_production(update_raw_second_expression)
    net.add_production(update_simplified_first_expression)
    net.add_production(update_simplified_second_expression)
    net.add_production(update_final_first_expression)
    net.add_production(update_final_second_expression)
    net.add_production(update_final_answer)
    net.add_production(select_done)

    return net


def factor_slip_slide_kc_mapping():

    skill_to_kc = {
        'update_a_value': 'Extract a value',
        'update_b_value': 'Extract b value',
        'update_c_value': 'Extract c value',
        'update_product_ac': 'Compute a times c for slip and slide',
        'update_new_trinomial':
            "Identify intermediate trinomial for slip and slide",
        'update_new_b_value': 'Extract b value',
        'update_new_c_value': 'Extract c value',
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
        'update_raw_first_expression':
            "Transform first expression for slip and slide",
        'update_raw_second_expression':
            "Transform second expression for slip and slide",
        'update_simplified_first_expression':
            "Simplify first expression for slip and slide",
        'update_simplified_second_expression':
            "Simplify second expression for slip and slide",
        'update_final_first_expression':
            "Finalize first expression for slip and slide",
        'update_final_second_expression':
            "Finalize second expression for slip and slide",
        'update_final_answer':
            'Combine expressions to create final factored form',
        'select_done': "Determine if factoring is complete"
    }

    return skill_to_kc


def factor_slip_slide_intermediate_hints():
    hints = {
        "update_a_value": [
            "The a value is extracted from the first term of the trinomial."],
        "update_b_value": [
            "The b value is extracted from the middle term of the trinomial."],
        "update_c_value": [
            "The c value is extracted from the last term of the trinomial."],
        "update_product_ac": [
            "Enter the value obtained by multiplying a and c."],
        "update_new_trinomial": ["This new trinomial is produced using the"
                                 " formula x^2 + bx + ac"],
        "update_new_b_value": [
            "The b value is extracted from the middle term of the new"
            " trinomial."],
        "update_new_c_value": [
            "The c value is extracted from the middle term of the new"
            " trinomial."],
        'update_factors_row1': ["Enter a factor of c from the new trinomial."],
        'update_factors_other_rows': ["Enter a factor of c from the new"
                                      " trinomial."],
        'update_factor_1_other': ["Enter the value that when multipled with"
                                  " the other factor yields c from the new"
                                  " trinomial."],
        'update_factor_2_other': ["Enter the value that when multipled with"
                                  " the other factor yields c from the new"
                                  " trinomial."],
        'sum_factors': [
            "This value is computed by adding the two factors in this row."],
        'update_sum_equals_b': [
            "Check this box if the sum of the factors is equal to b from the"
            " new trinomial."],
        'create_first_expression': ["This expression has the form (x+v) where"
                                    " v is one of the factors from the table"
                                    " above."],
        'create_second_expression_first': ["This expression has the form (x+v)"
                                           " where v is other factor you have"
                                           " not already used."],
        'create_second_expression_second': [
            "This expression has the form (x+v) where v is other factor you"
            " have not already used."],
        'update_raw_first_expression': [
            "This expression has the form (x+v/a), where (x+v) is the"
            " expression you just created directly above and a is the leading"
            " coefficient of the original trinomial."],
        'update_raw_second_expression': [
            "This expression has the form (x+v/a), where (x+v) is the"
            " expression you just created directly above and a is the leading"
            " coefficient of the original trinomial."],
        'update_simplified_first_expression': [
            "Simplify the expression above."],
        'update_simplified_second_expression': [
            "Simplify the expression above."],
        'update_final_first_expression': [
            "If the expression above still has a fraction for the second term"
            " (e.g., x+v/d), then rewrite to pull the denominator out (e.g.,"
            " dx+v)"],
        'update_final_second_expression': [
            "If the expression above still has a fraction for the second term"
            " (e.g., x+v/d), then rewrite to pull the denominator out (e.g.,"
            " dx+v)"],
        'update_final_answer': ["The final factored form is the"
                                " combination of the two expressions."],
        'select_done': ["Once you have found the final factored form you can"
                        " select the done button to move to the next problem."]
    }
    return hints

def factor_slip_slide_studymaterial():
    study_material = studymaterial["factor_slip_slide"]
    return study_material

loaded_models.register(CognitiveModel("factoring_polynomials",
                                      "factor_slip_slide",
                                      factor_slip_slide_model,
                                      factor_slip_slide_problem,
                                      factor_slip_slide_kc_mapping(),
                                      factor_slip_slide_intermediate_hints(),
                                      factor_slip_slide_studymaterial()))
