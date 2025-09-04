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


def factor_area_box_problem():
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
        factor_area_box_problem()

    # (n1*x+n2)(n3*x+n4)
    # n1*n3*x^2 + (n1*n4 + n2*n3)*x + n2*n4

    problem = "{}x^2".format(n1*n3)

    # need to catch this edge case and regenerate.
    b_value = n1*n4+n2*n3
    if b_value == 0:
        return factor_area_box_problem()

    if b_value > 0:
        problem += "+"

    problem += "{}x".format(b_value)

    c_value = n2 * n4
    if c_value > 0:
        problem += "+"

    problem += "{}".format(c_value)

    return problem


def factor_area_box_model():
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
                Fact(field="mx_value", disabled=False) &
                Fact(field="nx_value", disabled=False))
    def update_mnx_first(factor1, factor2):
        return [Fact(selection="mx_value", action="input change",
                     input="{}x".format(factor1)),
                Fact(selection="mx_value", action="input change",
                     input="{}x".format(factor2)),
                Fact(selection="nx_value", action="input change",
                     input="{}x".format(factor1)),
                Fact(selection="nx_value", action="input change",
                     input="{}x".format(factor2))]

    @Production(Fact(field="nx_value", value=V('nx_value'), disabled=True) &
                Fact(field="product_ac", value=V('product_ac'),
                     disabled=True) &
                Fact(field="mx_value", disabled=False))
    def update_mx_second(product_ac, nx_value):
        mx_value = int(int(product_ac) / int(nx_value.replace('x', '')))
        if mx_value == 1:
            mx_value = ""
        return [Fact(selection="mx_value", action="input change",
                     input="{}x".format(mx_value))]

    @Production(Fact(field="mx_value", value=V('mx_value'), disabled=True) &
                Fact(field="product_ac", value=V('product_ac'),
                     disabled=True) &
                Fact(field="nx_value", disabled=False))
    def update_nx_second(product_ac, mx_value):
        nx_value = int(int(product_ac) / int(mx_value.replace('x', '')))
        if nx_value == 1:
            nx_value = ""
        return [Fact(selection="nx_value", action="input change",
                     input="{}x".format(nx_value))]

    @Production(Fact(row=V('row'), column=4, disabled=True) &
                Fact(row=V('row'), column=2, disabled=True) &
                Fact(row=V('row'), column=1, disabled=True) &
                Fact(field="c_value", value=V('c_value'), disabled=True) &
                Fact(field="c_table_value", disabled=False))
    def update_c_box(c_value):
        return [Fact(selection="c_table_value", action="input change",
                     input="{}".format(c_value))]

    @Production(Fact(row=V('row'), column=4, disabled=True) &
                Fact(row=V('row'), column=2, disabled=True,
                     value=V('factor1')) &
                Fact(row=V('row'), column=1, disabled=True,
                     value=V('factor2')) &
                Fact(field="a_value", value=V('a_value'), disabled=True) &
                Fact(field="ax2_value", disabled=False))
    def update_ax_box(a_value):
        return [Fact(selection="ax2_value", action="input change",
                     input="{}x^2".format(a_value))]

    @Production(
        Fact(field="ax2_value", value=V('ax2_value'), disabled=True) &
        Fact(field="mx_value", value=V('mx_value'), disabled=True) &
        Fact(field="nx_value", value=V('nx_value'), disabled=True) &
        Fact(field="c_table_value", value=V('c_value'), disabled=True) &
        Fact(field="sx_value", disabled=False) &
        Fact(field="qx_value", disabled=False) &
        Fact(field="r_value", disabled=False) &
        Fact(field="t_value", disabled=False))
    def update_outer_table_first(ax2_value, mx_value, nx_value, c_value):
        resp = []

        if ax2_value.split('x')[0] == "":
            ax2_coef = 1
        else:
            ax2_coef = int(ax2_value.split('x')[0])

        if nx_value.split('x')[0] == "":
            nx_coef = 1
        else:
            nx_coef = int(nx_value.split('x')[0])

        gcd = math.gcd(ax2_coef, nx_coef)
        if gcd == 1:
            gcd = ""
        if ax2_coef < 0 and nx_coef < 0:
            resp.append(Fact(selection="sx_value", action="input change",
                             input="-{}x".format(gcd)))
        else:
            resp.append(Fact(selection="sx_value", action="input change",
                             input="{}x".format(gcd)))

        c_coef = int(c_value)
        mx_coef = int(mx_value.split('x')[0])
        gcd = math.gcd(c_coef, mx_coef)
        if mx_coef < 0:
            resp.append(Fact(selection="t_value", action="input change",
                             input="-{}".format(gcd)))
        else:
            resp.append(Fact(selection="t_value", action="input change",
                             input="{}".format(gcd)))

        gcd = math.gcd(ax2_coef, mx_coef)
        if gcd == 1:
            gcd = ""
        if ax2_coef < 0 and mx_coef < 0:
            resp.append(Fact(selection="qx_value", action="input change",
                             input="-{}x".format(gcd)))
        else:
            resp.append(Fact(selection="qx_value", action="input change",
                             input="{}x".format(gcd)))

        gcd = math.gcd(c_coef, nx_coef)
        if nx_coef < 0:
            resp.append(Fact(selection="r_value", action="input change",
                             input="-{}".format(gcd)))
        else:
            resp.append(Fact(selection="r_value", action="input change",
                             input="{}".format(gcd)))

        return resp

    @Production(
        Fact(field="ax2_value", value=V('ax2_value'), disabled=True)
        & Fact(field="sx_value", value=V('sx_value'), disabled=True)
        & Fact(field="qx_value", disabled=False))
    def update_qx_given_sx(ax2_value, sx_value):
        if ax2_value.split('x')[0] == "":
            ax2_coef = 1
        else:
            ax2_coef = int(ax2_value.split('x')[0])

        if sx_value.split('x')[0] == "":
            sx_coef = 1
        else:
            sx_coef = int(sx_value.split('x')[0])

        coef = int(ax2_coef / sx_coef)
        if coef == 1:
            coef = ""
        return [Fact(selection="qx_value", action="input change",
                     input="{}x".format(coef))]

    @Production(
        Fact(field="mx_value", value=V('mx_value'), disabled=True)
        & Fact(field="t_value", value=V('t_value'), disabled=True)
        & Fact(field="qx_value", disabled=False))
    def update_qx_given_t(mx_value, t_value):
        if mx_value.split('x')[0] == "":
            mx_coef = 1
        else:
            mx_coef = int(mx_value.split('x')[0])

        t_coef = int(t_value)
        coef = int(mx_coef / t_coef)
        if coef == 1:
            coef = ""
        return [Fact(selection="qx_value", action="input change",
                     input="{}x".format(coef))]

    @Production(
        Fact(field="ax2_value", value=V('ax2_value'), disabled=True)
        & Fact(field="qx_value", value=V('qx_value'), disabled=True)
        & Fact(field="sx_value", disabled=False))
    def update_sx_given_qx(ax2_value, qx_value):
        if ax2_value.split('x')[0] == "":
            ax2_coef = 1
        else:
            ax2_coef = int(ax2_value.split('x')[0])

        if qx_value.split('x')[0] == "":
            qx_coef = 1
        else:
            qx_coef = int(qx_value.split('x')[0])

        coef = int(ax2_coef / qx_coef)
        if coef == 1:
            coef = ""
        return [Fact(selection="sx_value", action="input change",
                     input="{}x".format(coef))]

    @Production(
        Fact(field="nx_value", value=V('nx_value'), disabled=True)
        & Fact(field="r_value", value=V('r_value'), disabled=True)
        & Fact(field="sx_value", disabled=False))
    def update_sx_given_r(nx_value, r_value):
        if nx_value.split('x')[0] == "":
            nx_coef = 1
        else:
            nx_coef = int(nx_value.split('x')[0])

        r_coef = int(r_value)
        coef = int(nx_coef / r_coef)
        if coef == 1:
            coef = ""
        return [Fact(selection="sx_value", action="input change",
                     input="{}x".format(coef))]

    @Production(
        Fact(field="nx_value", value=V('nx_value'), disabled=True)
        & Fact(field="sx_value", value=V('sx_value'), disabled=True)
        & Fact(field="r_value", disabled=False))
    def update_r_given_sx(nx_value, sx_value):
        if nx_value.split('x')[0] == "":
            nx_coef = 1
        else:
            nx_coef = int(nx_value.split('x')[0])

        if sx_value.split('x')[0] == "":
            sx_coef = 1
        else:
            sx_coef = int(sx_value.split('x')[0])

        coef = int(nx_coef / sx_coef)
        return [Fact(selection="r_value", action="input change",
                     input="{}".format(coef))]

    @Production(
        Fact(field="c_table_value", value=V('c_value'), disabled=True)
        & Fact(field="t_value", value=V('t_value'), disabled=True)
        & Fact(field="r_value", disabled=False))
    def update_r_given_t(c_value, t_value):
        c_coef = int(c_value)
        t_coef = int(t_value)
        coef = int(c_coef / t_coef)
        return [Fact(selection="r_value", action="input change",
                     input="{}".format(coef))]

    @Production(
        Fact(field="mx_value", value=V('mx_value'), disabled=True)
        & Fact(field="qx_value", value=V('qx_value'), disabled=True)
        & Fact(field="t_value", disabled=False))
    def update_t_given_qx(mx_value, qx_value):
        if mx_value.split('x')[0] == "":
            mx_coef = 1
        else:
            mx_coef = int(mx_value.split('x')[0])

        if qx_value.split('x')[0] == "":
            qx_coef = 1
        else:
            qx_coef = int(qx_value.split('x')[0])

        coef = int(mx_coef / qx_coef)
        return [Fact(selection="t_value", action="input change",
                     input="{}".format(coef))]

    @Production(
        Fact(field="c_table_value", value=V('c_value'), disabled=True)
        & Fact(field="r_value", value=V('r_value'), disabled=True)
        & Fact(field="t_value", disabled=False))
    def update_t_given_r(c_value, r_value):
        c_coef = int(c_value)
        r_coef = int(r_value)
        coef = int(c_coef / r_coef)
        return [Fact(selection="t_value", action="input change",
                     input="{}".format(coef))]

    @Production(
        Fact(field="sx_value", value=V('sx_value'), disabled=True) &
        Fact(field="t_value", value=V('t_value'), disabled=True) &
        Fact(field="qx_value", value=V('qx_value'), disabled=True) &
        Fact(field="r_value", value=V('r_value'), disabled=True) &
        Fact(field="first_expression", disabled=False) &
        Fact(field="second_expression", disabled=False))
    def update_expression_first(sx_value, t_value, qx_value, r_value):
        resp = []
        if int(t_value) > 0:
            t_value = "+" + t_value

        resp.append(Fact(selection="first_expression",
                    action="input change",
                    input="{}{}".format(sx_value, t_value)))
        resp.append(Fact(selection="second_expression",
                    action="input change",
                    input="{}{}".format(sx_value, t_value)))

        if int(r_value) > 0:
            r_value = "+" + r_value

        resp.append(Fact(selection="first_expression",
                    action="input change",
                    input="{}{}".format(qx_value, r_value)))
        resp.append(Fact(selection="second_expression",
                    action="input change",
                    input="{}{}".format(qx_value, r_value)))

        resp += [Fact(selection=f['selection'],
                      action=f['action'],
                      input="({})".format(f['input'])) for f in resp]

        return resp

    @Production(
        Fact(field="sx_value", value=V('sx_value'), disabled=True) &
        Fact(field="t_value", value=V('t_value'), disabled=True) &
        Fact(field="qx_value", value=V('qx_value'), disabled=True) &
        Fact(field="r_value", value=V('r_value'), disabled=True) &
        Fact(field="first_expression", disabled=False) &
        Fact(field="second_expression", value=V('second_exp'), disabled=True))
    def update_first_expression_second(sx_value, t_value, qx_value, r_value,
                                       second_exp):
        if int(t_value) > 0:
            t_value = "+" + t_value
        if int(r_value) > 0:
            r_value = "+" + r_value

        resp = []
        sx_exp = "{}{}".format(sx_value, t_value).replace(" ", '')
        if sx_exp == second_exp.replace(' ', '').replace(')', '').replace('(', ''):
            resp.append(Fact(selection="first_expression",
                        action="input change",
                        input="{}{}".format(qx_value, r_value)))
        else:
            resp.append([Fact(selection="first_expression",
                         action="input change",
                         input="{}{}".format(sx_value, t_value))])

        resp += [Fact(selection=f['selection'],
                      action=f['action'],
                      input="({})".format(f['input'])) for f in resp]
        return resp

    @Production(
        Fact(field="sx_value", value=V('sx_value'), disabled=True) &
        Fact(field="t_value", value=V('t_value'), disabled=True) &
        Fact(field="qx_value", value=V('qx_value'), disabled=True) &
        Fact(field="r_value", value=V('r_value'), disabled=True) &
        Fact(field="second_expression", disabled=False) &
        Fact(field="first_expression", value=V('first_exp'), disabled=True))
    def update_second_expression_second(sx_value, t_value, qx_value, r_value,
                                        first_exp):
        if int(t_value) > 0:
            t_value = "+" + t_value
        if int(r_value) > 0:
            r_value = "+" + r_value

        resp = []
        sx_exp = "{}{}".format(sx_value, t_value).replace(" ", '')
        if sx_exp == first_exp.replace(' ', '').replace(')', '').replace('(', ''):
            resp.append(Fact(selection="second_expression",
                        action="input change",
                        input="{}{}".format(qx_value, r_value)))
        else:
            resp.append(Fact(selection="second_expression",
                        action="input change",
                        input="{}{}".format(sx_value, t_value)))

        resp += [Fact(selection=f['selection'],
                      action=f['action'],
                      input="({})".format(f['input'])) for f in resp]
        return resp

    @Production(
        Fact(field="first_expression", value=V('first_exp'), disabled=True) &
        Fact(field="second_expression", value=V('second_exp'), disabled=True) &
        Fact(field="final_answer", disabled=False) & 
        Fact(field="initial_problem", value=V('init_value')))
    def update_final_answer(first_exp, second_exp, init_value):
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
    net.add_production(update_mnx_first)
    net.add_production(update_mx_second)
    net.add_production(update_nx_second)
    net.add_production(update_c_box)
    net.add_production(update_ax_box)
    net.add_production(update_outer_table_first)
    net.add_production(update_sx_given_qx)
    net.add_production(update_sx_given_r)
    net.add_production(update_qx_given_sx)
    net.add_production(update_qx_given_t)
    net.add_production(update_t_given_qx)
    net.add_production(update_t_given_r)
    net.add_production(update_r_given_sx)
    net.add_production(update_r_given_t)

    # net.add_production(update_sx_value)
    # net.add_production(update_t_value)
    # net.add_production(update_qx_value)
    # net.add_production(update_r_value)

    net.add_production(update_expression_first)
    net.add_production(update_first_expression_second)
    net.add_production(update_second_expression_second)
    net.add_production(update_final_answer)
    net.add_production(select_done)

    return net


def factor_area_box_kc_mapping():

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
        'update_mnx_first': 'Update area box first mx or nx',
        'update_mx_second': 'Update area box second mx or nx',
        'update_nx_second': 'Update area box second mx or nx',
        'update_c_box': 'Update area box c value',
        'update_ax_box': 'Update area box ax^2 value',
        'update_outer_table_first':
            "Update area box gcd of first row or column",
        'update_sx_given_qx': "Update area box sx given qx",
        'update_sx_given_r': "Update area box sx given r",
        'update_qx_given_sx': "Update area box qx given sx",
        'update_qx_given_t': "Update area box qx given t",
        'update_t_given_qx': "Update area box t given qx",
        'update_t_given_r': "Update area box t given sx",
        'update_r_given_sx': "Update area box r given sx",
        'update_r_given_t': "Update area box r given t",
        'update_expression_first': 'Create first expression from area box',
        'update_first_expression_second':
            'Create second expression from area box',
        'update_second_expression_second':
            'Create second expression from area box',
        'update_final_answer':
            'Combine expressions to create final factored form',
        'select_done': "Determine if factoring is complete"
    }

    return skill_to_kc


def factor_area_box_intermediate_hints():
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

        'update_mnx_first': ["Enter the value Vx where V is one of the factors"
                             " from the table above."],
        'update_mx_second': ["Enter the value Vx where V is the other factor"
                             " from the table above."],
        'update_nx_second': ["Enter the value Vx where V is the other factor"
                             " from the table above."],
        'update_c_box': ["Enter the value c from above."],
        'update_ax_box': ["Enter the value ax^2 from above."],
        'update_outer_table_first': ["Update this value by computing the"
                                     " greatest common divisor"
                                     " of the row or column."],
        'update_sx_given_qx': ["Enter a value that when multiplied by the"
                               " corresponding outer row value produces the"
                               " value of the cell where the row and column"
                               " intersect."],
        'update_sx_given_r': ["Enter a value that when multiplied by the"
                              " corresponding outer row value produces the"
                              " value of the cell where the row and column"
                              " intersect."],
        'update_qx_given_sx': ["Enter a value that when multiplied by the"
                               " corresponding outer column value produces the"
                               " value of the cell where the row and column"
                               " intersect."],
        'update_qx_given_t': ["Enter a value that when multiplied by the"
                              " corresponding outer column value produces the"
                              " value of the cell where the row and column"
                              " intersect."],
        'update_t_given_qx': ["Enter a value that when multiplied by the"
                              " corresponding outer row value produces the"
                              " value of the cell where the row and column"
                              " intersect."],
        'update_t_given_r': ["Enter a value that when multiplied by the"
                             " corresponding outer row value produces the"
                             " value of the cell where the row and column"
                             " intersect."],
        'update_r_given_sx': ["Enter a value that when multiplied by the"
                              " corresponding outer column value produces the"
                              " value of the cell where the row and column"
                              " intersect."],
        'update_r_given_t': ["Enter a value that when multiplied by the"
                             " corresponding outer column value produces the"
                             " value of the cell where the row and column"
                             " intersect."],
        'update_expression_first': ["This expression is the sum of either the"
                                    " outer row or outer column values"],
        'update_first_expression_second': ["This expression is the sum of the"
                                           " other outer row or outer column"
                                           " values."],
        'update_second_expression_second': ["This expression is the sum of the"
                                            " other outer row or outer column"
                                            " values."],
        'update_final_answer': ["The final factored form is the"
                                " combination of the two expressions."],
        'select_done': ["Once you have found the final factored form you can"
                        " select the done button to move to the next problem."]
    }
    return hints

def factor_area_box_studymaterial():
    study_material = studymaterial["factor_area_box"]
    return study_material

loaded_models.register(CognitiveModel("factoring_polynomials",
                                      "factor_area_box",
                                      factor_area_box_model,
                                      factor_area_box_problem,
                                      factor_area_box_kc_mapping(),
                                      factor_area_box_intermediate_hints(),
                                      factor_area_box_studymaterial()))