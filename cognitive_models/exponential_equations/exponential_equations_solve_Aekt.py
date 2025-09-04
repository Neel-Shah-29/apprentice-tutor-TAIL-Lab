from random import randint, choice

import sympy as sp
from sympy import latex, symbols, expand, sstr, Eq, solve
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re 

from py_rete import Fact, Production, ReteNetwork, V

from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def exponential_equations_solve_Aekt_problem():
    x = symbols('x')
    a, k = randint(1, 10), randint(-10, 10)
    base = randint(2, 10)
    c1, c2 = randint(-5, 10), randint(-5, 10)
    while (c2-c1) <= 0 or  sp.Abs(k) <= 1:
        c1, c2, k = randint(-10, 10), randint(-10, 10), randint(-10, 10)
    equation = latex(Eq(a*sp.E**(k*x)+c1, c2, evaluate=False))
    return equation

def exponential_equations_solve_Aekt_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="coeff0_to_rhs", disabled=False))
    def coeff0_to_rhs(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        equation = Eq(lhs-lhs.coeff(x, 0), rhs-lhs.coeff(x,0))
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="coeff0_to_rhs", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="coeff0_to_rhs", disabled=True) &
                Fact(field="coeffk_to_rhs", disabled=False))
    def coeffk_to_rhs(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        equation = Eq(lhs-lhs.coeff(x, 0), rhs-lhs.coeff(x,0))
        lhs, rhs = equation.lhs, equation.rhs
        coeffk = lhs.args[0]
        equation = Eq(lhs/coeffk, rhs/coeffk)
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="coeffk_to_rhs", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="coeffk_to_rhs", disabled=True) &
                Fact(field="ln_both_sides", disabled=False))
    def ln_both_sides(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        equation = Eq(lhs-lhs.coeff(x, 0), rhs-lhs.coeff(x,0))
        lhs, rhs = equation.lhs, equation.rhs
        coeffk = lhs.args[0]
        equation = Eq(lhs/coeffk, rhs/coeffk)
        lhs, rhs = equation.lhs, equation.rhs
        equation = Eq(lhs.args[1], sp.ln(rhs))
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', re.sub(r'log\(([^)]+)\)', r'log(\1, E)', sstr(equation, order="grlex"))))
        hint = latex(equation)
        return [Fact(selection="ln_both_sides", action="input change", input=answer, hint=hint)]
    

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="ln_both_sides", disabled=True) &
                Fact(field="solve_for_x", disabled=False))
    def solve_for_x(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        equation = Eq(lhs-lhs.coeff(x, 0), rhs-lhs.coeff(x,0))
        lhs, rhs = equation.lhs, equation.rhs
        coeffk = lhs.args[0]
        equation = Eq(lhs/coeffk, rhs/coeffk)
        lhs, rhs = equation.lhs, equation.rhs
        equation = Eq(lhs.args[1], sp.ln(rhs))
        equation = parse_latex(latex(equation))
        lhs, rhs = equation.lhs, equation.rhs
        k = lhs.args[0]
        equation = rhs/k
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="solve_for_x", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="solve_for_x", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    net.add_production(coeff0_to_rhs)
    net.add_production(coeffk_to_rhs)
    net.add_production(ln_both_sides)
    net.add_production(solve_for_x)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def exponential_equations_solve_Aekt_kc_mapping():
    kcs = {
        "coeff0_to_rhs": "coeff0_to_rhs",
        "coeffk_to_rhs": "coeffk_to_rhs",
        "ln_both_sides": "ln_both_sides",
        "solve_for_x": "solve_for_x",
        "select_done": "Determine if exponential equation with common base is complete"
    }
    return kcs


def exponential_equations_solve_Aekt_intermediate_hints():
    hints = {
        "coeff0_to_rhs" : ["Move the constant term to the right-hand side of the equation."],
        "coeffk_to_rhs" : ["Move the coefficient of the exponential term to the right-hand side of the equation."],
        "ln_both_sides" : ["Take the natural log of both sides of the equation."],
        "solve_for_x" : ["Solve for x."],
    }
    return hints

def exponential_equations_solve_Aekt_studymaterial():
    study_material = studymaterial["exponential_equations_solve_Aekt"]
    return study_material

loaded_models.register(CognitiveModel("exponential_equations",
                                      "exponential_equations_solve_Aekt",
                                      exponential_equations_solve_Aekt_model,
                                      exponential_equations_solve_Aekt_problem,
                                      exponential_equations_solve_Aekt_kc_mapping(),
                                      exponential_equations_solve_Aekt_intermediate_hints(),
                                      exponential_equations_solve_Aekt_studymaterial()))