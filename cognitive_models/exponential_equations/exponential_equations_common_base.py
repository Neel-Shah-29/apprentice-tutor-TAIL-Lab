from random import randint, choice

import sympy as sp
from sympy import latex, symbols, expand, sstr, Eq, solve
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re 

from py_rete import Fact, Production, ReteNetwork, V

from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def exponential_equations_common_base_problem():
    x = symbols('x')
    base = randint(2, 10)
    a, b, c, d = randint(-10, 10), randint(-10, 10), randint(-10, 10), randint(-10, 10)
    while not (a*c) or (a==c):
        a, c = randint(-10, 10), randint(-10, 10)
    equation = latex(Eq(base**(a*x+b), base**(c*x+d), evaluate=False))
    return equation

def exponential_equations_common_base_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="apply_one_to_one_property", disabled=False))
    def apply_one_to_one_property(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        equation = Eq(lhs.as_base_exp()[1], rhs.as_base_exp()[1], evaluate=False)
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="apply_one_to_one_property", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="apply_one_to_one_property", disabled=True) &
                Fact(field="solve_linear_equation", disabled=False))
    def solve_linear_equation(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        equation = Eq(lhs.as_base_exp()[1], rhs.as_base_exp()[1], evaluate=False)
        # linear_equation = parse_latex(linear_equation)
        # solution = solve(linear_equation, x)[0]
        solution = solve(equation, x)[0]
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(solution, order="grlex")))
        hint = latex(solution)
        return [Fact(selection="solve_linear_equation", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="solve_linear_equation", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    net.add_production(apply_one_to_one_property)
    net.add_production(solve_linear_equation)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def exponential_equations_common_base_kc_mapping():
    kcs = {
        "apply_one_to_one_property": "apply_one_to_one_property",
        "solve_linear_equation": "solve_linear_equation",
        "select_done": "Determine if exponential equation with common base is complete"
    }
    return kcs


def exponential_equations_common_base_intermediate_hints():
    hints = {
        "apply_one_to_one_property": ["Apply the one-to-one property for exponents"],
        "solve_linear_equation": ["Solve the linear equation for \(x\)."], 
    }
    return hints

def exponential_equations_common_base_studymaterial():
    study_material = studymaterial["exponential_equations_common_base"]
    return study_material

loaded_models.register(CognitiveModel("exponential_equations",
                                      "exponential_equations_common_base",
                                      exponential_equations_common_base_model,
                                      exponential_equations_common_base_problem,
                                      exponential_equations_common_base_kc_mapping(),
                                      exponential_equations_common_base_intermediate_hints(),
                                      exponential_equations_common_base_studymaterial()))