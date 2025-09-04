from random import randint, choice

import sympy as sp
from sympy import latex, symbols, expand, sstr, Eq, solve
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re 

from py_rete import Fact, Production, ReteNetwork, V

from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def exponential_equations_solve_Aekt_directly_problem():
    x = symbols('x')
    a, k = randint(1, 10), randint(-10, 10)
    base = randint(2, 10)
    c1, c2 = randint(-5, 10), randint(-5, 10)
    while (c2-c1) <= 0 or  sp.Abs(k) <= 1:
        c1, c2, k = randint(-10, 10), randint(-10, 10), randint(-10, 10)
    equation = latex(Eq(a*sp.E**(k*x)+c1, c2, evaluate=False))
    return equation

def exponential_equations_solve_Aekt_directly_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="solve_for_Aekt_directly", disabled=False))
    def solve_for_Aekt_directly(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        equation = Eq(lhs-lhs.coeff(x, 0), rhs-lhs.coeff(x,0))
        lhs, rhs = equation.lhs, equation.rhs
        coeffk = lhs.args[0]
        equation = Eq(lhs/coeffk, rhs/coeffk)
        lhs, rhs = equation.lhs, equation.rhs
        equation = Eq(lhs.args[1], sp.ln(rhs))
        lhs, rhs = equation.lhs, equation.rhs
        k = lhs.args[0]
        equation = rhs/k
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', re.sub(r'log\(([^)]+)\)', r'log(\1, E)', sstr(equation, order="grlex"))))
        hint = latex(equation)
        return [Fact(selection="solve_for_Aekt_directly", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="solve_for_Aekt_directly", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    net.add_production(solve_for_Aekt_directly)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def exponential_equations_solve_Aekt_directly_kc_mapping():
    kcs = {
        "solve_for_Aekt_directly": "solve_for_Aekt_directly",
        "select_done": "Determine if exponential equation with common base is complete"
    }
    return kcs


def exponential_equations_solve_Aekt_directly_intermediate_hints():
    hints = {
        "solve_for_Aekt_directly" : ["Solve for x."],
    }
    return hints

def exponential_equations_solve_Aekt_directly_studymaterial():
    study_material = studymaterial["exponential_equations_solve_Aekt_directly"]
    return study_material

loaded_models.register(CognitiveModel("exponential_equations",
                                      "exponential_equations_solve_Aekt_directly",
                                      exponential_equations_solve_Aekt_directly_model,
                                      exponential_equations_solve_Aekt_directly_problem,
                                      exponential_equations_solve_Aekt_directly_kc_mapping(),
                                      exponential_equations_solve_Aekt_directly_intermediate_hints(),
                                      exponential_equations_solve_Aekt_directly_studymaterial()))