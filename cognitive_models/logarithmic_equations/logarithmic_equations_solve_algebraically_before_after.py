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


def logarithmic_equations_solve_algebraically_before_after_problem():
    x = symbols('x')
    a, b, c1, c2 = randint(-10, 10), randint(-10, 10), randint(-10, 10), randint(-10, 10)
    while not b or (c2-c1)/b <= 0 or sp.Abs(a) <=1 or  sp.Abs(b) <=1:
      a, b, c1, c2 = randint(-10, 10), randint(-10, 10), randint(-10, 10), randint(-10, 10)
    equation = latex(Eq(b*sp.log(a*x)+c1, c2, evaluate=False))
    equation = replace_log_with_ln(equation)
    print(equation)
    return equation

def logarithmic_equations_solve_algebraically_before_after_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="coeff0_to_rhs", disabled=False))
    def coeff0_to_rhs(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        equation = parse_latex(latex(Eq(lhs-lhs.coeff(x, 0), rhs-lhs.coeff(x, 0))))
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
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
    def exponential_both_sides(equation):
        x = symbols('x')
        lhs, rhs = parse_latex(equation).lhs, parse_latex(equation).rhs
        equation = parse_latex(latex(Eq(sp.E**lhs, sp.E**rhs)))
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        hint = replace_log_with_ln(hint)
        return [Fact(selection="exponential_both_sides", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="exponential_both_sides", value=V('equation'), disabled=True) &
                Fact(field="solve_for_x", disabled=False))
    def solve_for_x(init_value):
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
        return [Fact(selection="solve_for_x", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="solve_for_x", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    net.add_production(coeff0_to_rhs)
    net.add_production(coefflnx_to_rhs)
    net.add_production(exponential_both_sides)
    net.add_production(solve_for_x)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def logarithmic_equations_solve_algebraically_before_after_kc_mapping():
    kcs = {
        "coeff0_to_rhs": "coeff0_to_rhs",
        "coefflnx_to_rhs": "coefflnx_to_rhs",
        "exponential_both_sides": "exponential_both_sides",
        "solve_for_x": "solve_for_x",
        "select_done": "Determine if exponential equation with common base is complete"
    }
    return kcs


def logarithmic_equations_solve_algebraically_before_after_intermediate_hints():
    hints = {
        "coeff0_to_rhs": ["Move the constant term to the right-hand side of the equation"],
        "coefflnx_to_rhs": ["Move the coefficient of \(log(x)\) to the right-hand side of the equation"],
        "exponential_both_sides": ["Take the exponential of both sides of the equation"], 
        "solve_for_x": ["Find the value of \(x\)"], 
    }
    return hints

def logarithmic_equations_solve_algebraically_before_after_studymaterial():
    study_material = studymaterial["logarithmic_equations_solve_algebraically_before_after"]
    return study_material

loaded_models.register(CognitiveModel("logarithmic_equations",
                                      "logarithmic_equations_solve_algebraically_before_after",
                                      logarithmic_equations_solve_algebraically_before_after_model,
                                      logarithmic_equations_solve_algebraically_before_after_problem,
                                      logarithmic_equations_solve_algebraically_before_after_kc_mapping(),
                                      logarithmic_equations_solve_algebraically_before_after_intermediate_hints(),
                                      logarithmic_equations_solve_algebraically_before_after_studymaterial()))