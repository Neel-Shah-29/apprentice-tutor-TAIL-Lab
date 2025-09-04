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

def logarithmic_equations_solve_algebraically_problem():
    x = symbols('x')
    a, c1, c2 = randint(-10, 10), randint(-10, 10), randint(-10, 10)
    while not (c2-c1) or sp.Abs(a) <=1:
      a, c1, c2 = randint(-10, 10), randint(-10, 10), randint(-10, 10)
    equation = latex(Eq(a*sp.ln(x)+c1, c2, evaluate=False))
    equation = replace_log_with_ln(equation)
    return equation

def logarithmic_equations_solve_algebraically_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="coeff0_to_rhs", disabled=False))
    def coeff0_to_rhs(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        equation = Eq(lhs-lhs.coeff(x, 0), rhs-lhs.coeff(x, 0))
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex").replace("-1*", "-")))
        hint = latex(equation)
        hint = replace_log_with_ln(hint)
        return [Fact(selection="coeff0_to_rhs", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="coeff0_to_rhs", value=V('equation'), disabled=True) &
                Fact(field="coefflnx_to_rhs", disabled=False))
    def coefflnx_to_rhs(equation):
        x = symbols('x')
        lhs, rhs = parse_latex(equation).lhs, parse_latex(equation).rhs
        constant = lhs.args[0]
        if lhs.args[1].is_integer:
            constant *= lhs.args[1]
        equation = Eq(lhs.args[-1], rhs/constant)
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        hint = replace_log_with_ln(hint)
        return [Fact(selection="coefflnx_to_rhs", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="coefflnx_to_rhs", value=V('equation'), disabled=True) &
                Fact(field="exponential_both_sides", disabled=False))
    def exponential_both_sides(init_value):
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
        # print(lhs, ",", rhs)
        # print(lhs.args, ",", rhs.args)
        # constant = lhs.args[0]
        # if lhs.args[1].is_integer:
        #     constant *= lhs.args[1]
        # equation = rhs/constant
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        hint = replace_log_with_ln(hint)
        return [Fact(selection="exponential_both_sides", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="exponential_both_sides", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    net.add_production(coeff0_to_rhs)
    net.add_production(coefflnx_to_rhs)
    net.add_production(exponential_both_sides)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def logarithmic_equations_solve_algebraically_kc_mapping():
    kcs = {
        "coeff0_to_rhs": "coeff0_to_rhs",
        "coefflnx_to_rhs": "coefflnx_to_rhs",
        "exponential_both_sides": "exponential_both_sides",
        "select_done": "Determine if exponential equation with common base is complete"
    }
    return kcs


def logarithmic_equations_solve_algebraically_intermediate_hints():
    hints = {
        "coeff0_to_rhs": ["Move the constant term to the right-hand side of the equation"],
        "coefflnx_to_rhs": ["Move the coefficient of \(log(x)\) to the right-hand side of the equation"],
        "exponential_both_sides": ["Take the exponential of both sides of the equation"], 
    }
    return hints

def logarithmic_equations_solve_algebraically_studymaterial():
    study_material = studymaterial["logarithmic_equations_solve_algebraically"]
    return study_material

loaded_models.register(CognitiveModel("logarithmic_equations",
                                      "logarithmic_equations_solve_algebraically",
                                      logarithmic_equations_solve_algebraically_model,
                                      logarithmic_equations_solve_algebraically_problem,
                                      logarithmic_equations_solve_algebraically_kc_mapping(),
                                      logarithmic_equations_solve_algebraically_intermediate_hints(),
                                      logarithmic_equations_solve_algebraically_studymaterial()))