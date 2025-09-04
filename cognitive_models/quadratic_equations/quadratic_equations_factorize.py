import math
from functools import reduce
from random import randint, random, choice
from pprint import pprint

from py_rete import Fact
from py_rete import Production
from py_rete import ReteNetwork
from py_rete import V
from py_rete import Filter

# from models import KnowledgeComponent
import sympy as sp
from sympy.parsing.latex._parse_latex_antlr import parse_latex
from sympy import symbols, expand, latex
# # from cognitive_models.base import check_sai
# # from cognitive_models.base import get_hint
from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

import re 

from studymaterial import studymaterial

def quadratic_equations_factorize_problem():
    x = sp.symbols('x')
    x1, x2, coeff = 0, 0, 0
    while not (x1*x2) or not coeff:
      x1, x2 = randint(-10, 10), randint(-10, 10)
      factorlist = [f for factor in sp.divisors(int(x1)) for f in (factor, -factor) if (f*x2+x1)]
      if factorlist: 
        coeff = choice(factorlist)
    equation = f"{latex(expand((coeff*x-x1) * (x-x2)))}=0"
    return equation

def quadratic_equations_factorize():
    net = ReteNetwork()

    # compute value of b 
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="b_value", disabled=False)) 
    def update_b_value(init_value):
        x = symbols('x')
        equation = sp.simplify(parse_latex(init_value.split("=")[0]))
        answer = re.compile(str(equation.coeff(x, 1)))
        hint = str(equation.coeff(x, 1))
        return [Fact(selection="b_value", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="ac_value", disabled=False))
    def update_ac_value(init_value):
        x = symbols('x')
        equation = sp.simplify(parse_latex(init_value.split("=")[0]))
        ac = sp.sstr(equation.coeff(x, 2) * equation.coeff(x, 0))
        answer = re.compile(ac)
        hint = ac
        return [Fact(selection="ac_value", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="b_value", value=V('sum_b'), disabled=True) &
                Fact(field="ac_value", value=V('product_ac'), disabled=True) &
                Fact(field=V('selection_1'), row=1, column=1, disabled=False) &
                Fact(field=V('selection_2'), row=1, column=2, disabled=False))
    def update_factors_row1(product_ac, sum_b, selection_1, selection_2):
        factors = [f for factor in sp.divisors(int(product_ac)) for f in (factor, -factor)]
        factorlist = [(abs((int(product_ac)/f+f)-int(sum_b)), f) for f in factors]
        factorlist.sort()
        sais = [Fact(selection=selection_1, action="input change", input=re.compile(str(f)), hint=str(f)) for _, f in factorlist]
        sais += [Fact(selection=selection_2, action="input change", input=re.compile(str(f)), hint=str(f)) for _, f in factorlist]
        return sais

    @Production(Fact(field="b_value", value=V('sum_b'), disabled=True) &
                Fact(field="ac_value", value=V('product_ac'), disabled=True) &
                Fact(field=V('selection_1'), row=V('row'), column=1,disabled=False) &
                Fact(row=V('prev_row'), column=1, disabled=True) &
                Filter(lambda row, prev_row: prev_row + 1 == row) &
                Fact(field=V('selection_2'), row=V('row'), column=2, disabled=False) &
                Fact(row=V('prev_row'), column=2, disabled=True) &
                Fact(column=4, disabled=False) &
                Fact(row=V('prev_row'), column=3, value=V('prev_sum'), disabled=True) &
                Filter(lambda prev_sum, sum_b: prev_sum != sum_b))
    def update_factors_other_rows(sum_b, product_ac, selection_1, selection_2):
        factors = [f for factor in sp.divisors(int(product_ac)) for f in (factor, -factor)]
        factorlist = [(abs((int(product_ac)/f+f)-int(sum_b)), f) for f in factors]
        factorlist.sort()
        sais = [Fact(selection=selection_1, action="input change", input=re.compile(str(f)), hint=str(f)) for _, f in factorlist]
        sais += [Fact(selection=selection_2, action="input change", input=re.compile(str(f)), hint=str(f)) for _, f in factorlist]
        return sais

    @Production(Fact(field="ac_value", value=V('product_ac'), disabled=True) &
                Fact(row=V('row'), column=1, value=V('other_factor'), disabled=True) &
                Fact(field=V('selection'), row=V('row'), column=2, disabled=False))
    def update_factor_2_other(product_ac, other_factor, selection):
        answer = re.compile(str(int(int(product_ac)/int(other_factor))))
        hint = str(int(int(product_ac)/int(other_factor)))
        return [Fact(selection=selection, action="input change", input=answer, hint=hint)]

    @Production(Fact(row=V('row'), column=1, value=V('first_factor'), disabled=True) &
                Fact(row=V('row'), column=2, value=V('second_factor'), disabled=True) &
                Fact(field=V('selection'), row=V('row'), column=3, disabled=False))
    def sum_factors(first_factor, second_factor, selection):
        answer = re.compile(str(int(int(first_factor) + int(second_factor))))
        hint = str(int(int(first_factor) + int(second_factor)))
        return [Fact(selection=selection, action="input change", input=answer ,hint=hint)]

    @Production(Fact(field="b_value", value=V('b'), disabled=True) &
                Fact(row=V('row'), column=3, value=V('b'), disabled=True) &
                Fact(field=V('selection'), row=V('row'), column=4, disabled=False))
    def update_sum_equals_b(selection):
        return [Fact(selection=selection, action="input change", input=re.compile("checked"))]
                
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(row=V('row'), column=4, disabled=True) & 
                Fact(row=V('row'), column=1, value=V('f1'), disabled=True) &
                Fact(row=V('row'), column=2, value=V('f2'), disabled=True) &
                Fact(field="expanded_equation", disabled=False))
    def factorized_equation(init_value, f1, f2):
        facts = list()
        x = symbols('x')
        equation = sp.simplify(parse_latex(init_value).lhs)
        a, c = equation.coeff(x, 2), equation.coeff(x, 0)
        for p in [(f1, f2), (f2, f1)]:
            factored = f"{a*x}^{2}+{p[0]}x+{p[1]}x+{c}=0".replace("+-", "-").replace("*", "")
            answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(parse_latex(factored), order='grlex')))
            hint = factored
            facts.append(Fact(selection="expanded_equation", action="input change", input=answer ,hint=hint))
        return facts

    @Production(Fact(field="expanded_equation", disabled=True) &
                Fact(row=V('row'), column=4, disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input="x")]

    net.add_production(update_b_value)
    net.add_production(update_ac_value)
    net.add_production(update_factors_row1)
    net.add_production(update_factors_other_rows)
    net.add_production(update_factor_2_other)
    net.add_production(sum_factors)
    net.add_production(update_sum_equals_b)
    net.add_production(factorized_equation)
    net.add_production(select_done)

    sp.core.cache.clear_cache() 
    return net


def factorize_kc_mapping():
    # key --> rule
    # value --> human readable value for kc (unique)

    kcs = {
        "update_b_value": "extract_b_value",
        "update_ac_value": "multiply_values",
        'update_factors_row1': "find_factor_of_value",
        'update_factors_other_rows': "find_factor_of_value",
        'update_factor_2_other': "find_factor_of_value",
        'sum_factors': "add_values",
        'update_sum_equals_b': "sum_of_factors_equals_b",
        'factorized_equation': "expand_equation",
        'select_done': "Determine if factoring is complete"
    }
    return kcs


def factorize_intermediate_hints():
    hints = {
        "update_b_value": ["Here \(b\) is coefficient of \(x\)."],
        "update_ac_value": ["Here \(ac\) is the product of the coefficients of \(x^2\) and constant."],
        'update_factors_row1': ["Enter a factor of \(ac\)."],
        'update_factors_other_rows': ["Enter a factor of \(ac\)."],
        'update_factor_2_other': ["Enter the other factor of \(ac\)."],
        'sum_factors': ["Add the two factos to get the sum."],
        'update_sum_equals_b': ["Check this box if the sum of the factors is equal to \(b\)."],
        'factorized_equation': ["Expand the \(x\) term using the factors"],
        'select_done': ["Once you have found the final factored form you can"
                        " select the done button to move to the next problem."]
    }
    return hints

def factorize_studymaterial():
    study_material = studymaterial["quadratic_equations_factorize"]
    return study_material

loaded_models.register(CognitiveModel("quadratic_equations",
                                      "quadratic_equations_factorize",
                                      quadratic_equations_factorize,
                                      quadratic_equations_factorize_problem,
                                      factorize_kc_mapping(),
                                      factorize_intermediate_hints(),
                                      factorize_studymaterial()))