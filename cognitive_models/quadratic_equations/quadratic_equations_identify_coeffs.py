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

from studymaterial import studymaterial

def quadratic_equations_identify_coeffs_problem():
    x = sp.symbols('x')
    x1, x2, coeff = 0, 0, 0
    while not (x1*x2) or not coeff:
      x1, x2 = randint(-10, 10), randint(-10, 10)
      factorlist = [f for factor in sp.divisors(int(x1)) for f in (factor, -factor) if (f*x2+x1)]
      if factorlist: 
        coeff = choice(factorlist)
    equation = f"{latex(expand(((coeff*x)-x1) * (x-x2)))}=0"
    return equation

def quadratic_equations_identify_coeffs():
    net = ReteNetwork()

    # compute value of a 
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="a_value", disabled=False)) 
    def update_a_value(init_value):
        x = symbols('x')
        equation = sp.simplify(parse_latex(init_value.split("=")[0]))
        answer = str(equation.coeff(x, 2))
        return [Fact(selection="a_value", action="input change", input=answer, hint=answer)]
    
    # compute value of b 
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="b_value", disabled=False)) 
    def update_b_value(init_value):
        x = symbols('x')
        equation = sp.simplify(parse_latex(init_value.split("=")[0]))
        answer = str(equation.coeff(x, 1))
        return [Fact(selection="b_value", action="input change", input=answer, hint=answer)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="c_value", disabled=False))
    def update_c_value(init_value):
        x = symbols('x')
        equation = sp.simplify(parse_latex(init_value.split("=")[0]))
        answer = str(equation.coeff(x, 0))
        return [Fact(selection="c_value", action="input change", input=answer, hint=answer)]
    
    @Production(Fact(field="a_value", value=V('a_value_'), disabled=True) &
                Fact(field="c_value", value=V('c_value_'), disabled=True) &
                Fact(field="ac_value", disabled=False))
    def update_ac_value(a_value_, c_value_):
        answer = str(int(a_value_)*int(c_value_))
        return [Fact(selection="ac_value", action="input change", input=answer, hint=answer)]

    @Production(Fact(field="ac_value", disabled=True) &
                Fact(field="b_value", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input="x")]

    net.add_production(update_a_value)
    net.add_production(update_b_value)
    net.add_production(update_c_value)
    net.add_production(update_ac_value)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def identify_coeffs_kc_mapping():
    # key --> rule
    # value --> human readable value for kc (unique)

    kcs = {
        "update_a_value": "extract_a_value",
        "update_b_value": "extract_b_value",
        "update_c_value": "extract_c_value",
        "update_ac_value": "multiply_values",
        'select_done': "Determine if factoring is complete"

    }
    return kcs


def identify_coeffs_intermediate_hints():
    hints = {
        "update_a_value": ["Here \(a\) is coefficient of \(x^2\)."],
        "update_b_value": ["Here \(b\) is coefficient of \(x\)."],
        "update_c_value": ["Here \(c\) is coefficient of the constant term."],
        "update_ac_value": ["Here \(ac\) is the product of the coefficients of \(x^2\) and constant."],
        'select_done': ["Once you have found the final factored form you can"
                        " select the done button to move to the next problem."]
    }
    return hints

def identify_coeffs_studymaterial():
    study_material = studymaterial["quadratic_equations_identify_coeffs"]
    return study_material

loaded_models.register(CognitiveModel("quadratic_equations",
                                      "quadratic_equations_identify_coeffs",
                                      quadratic_equations_identify_coeffs,
                                      quadratic_equations_identify_coeffs_problem,
                                      identify_coeffs_kc_mapping(),
                                      identify_coeffs_intermediate_hints(),
                                      identify_coeffs_studymaterial()))