from random import randint, choice

import sympy as sp
from sympy import latex, symbols, expand, sstr, Eq, solve
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re 

from py_rete import Fact, Production, ReteNetwork, V

from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def replace_log_with_ln(equation):
    return equation.replace('\log', '\ln')

def logarithmic_equations_solve_algebraically_directly_problem():
    x = symbols('x')
    a, b, c1, c2 = randint(-10, 10), randint(-10, 10), randint(-10, 10), randint(-10, 10)
    while not b or (c2-c1)/b <= 0 or sp.Abs(a) <=1 or  sp.Abs(b) <=1:
      a, b, c1, c2 = randint(-10, 10), randint(-10, 10), randint(-10, 10), randint(-10, 10)
    equation = latex(Eq(b*sp.ln(a*x)+c1, c2, evaluate=False))
    equation = replace_log_with_ln(equation)
    return equation

def logarithmic_equations_solve_algebraically_directly_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="solve_logarithm_algebraically", disabled=False))
    def solve_logarithm_algebraically(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        equation = Eq(lhs-lhs.coeff(x, 0), rhs-lhs.coeff(x, 0))
        lhs, rhs = equation.lhs, equation.rhs
        constant = lhs.args[0]
        if lhs.args[1].is_integer:
            constant *= lhs.args[1]
        equation = Eq(lhs.args[-1], rhs/constant)
        lhs, rhs = equation.lhs, equation.rhs
        equation = parse_latex(latex(Eq(sp.E**lhs, sp.E**rhs)))
        lhs, rhs = equation.lhs, equation.rhs
        constant = lhs.args[0]
        if lhs.args[1].is_integer:
            constant *= lhs.args[1]
        equation = rhs/constant
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        hint = replace_log_with_ln(hint)
        return [Fact(selection="solve_logarithm_algebraically", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="solve_logarithm_algebraically", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    
    net.add_production(solve_logarithm_algebraically)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def logarithmic_equations_solve_algebraically_directly_kc_mapping():
    kcs = {
        "solve_logarithm_algebraically": "solve_logarithm_algebraically",
        "select_done": "Determine if exponential equation with common base is complete"
    }
    return kcs


def logarithmic_equations_solve_algebraically_directly_intermediate_hints():
    hints = {
        "solve_logarithm_algebraically": ["Solve the logarithmic equation algebraically"],
    }
    return hints

def logarithmic_equations_solve_algebraically_directly_studymaterial():
    study_material = studymaterial["logarithmic_equations_solve_algebraically_directly"]
    return study_material

loaded_models.register(CognitiveModel("logarithmic_equations",
                                      "logarithmic_equations_solve_algebraically_directly",
                                      logarithmic_equations_solve_algebraically_directly_model,
                                      logarithmic_equations_solve_algebraically_directly_problem,
                                      logarithmic_equations_solve_algebraically_directly_kc_mapping(),
                                      logarithmic_equations_solve_algebraically_directly_intermediate_hints(),
                                      logarithmic_equations_solve_algebraically_directly_studymaterial()))