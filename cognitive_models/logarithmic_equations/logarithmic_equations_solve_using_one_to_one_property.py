from random import randint, choice

import sympy as sp
from sympy import latex, symbols, expand, sstr, Eq, solve
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re 

from py_rete import Fact, Production, ReteNetwork, V

from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def logarithmic_equations_solve_using_one_to_one_property_problem():
    x = symbols('x')
    x1, x2 = randint(-10, 10), randint(-10, 10)
    while not (x1+x2) or not (x1*x2):
      x1, x2 = randint(-10, 10), randint(-10, 10)
    equation = latex(Eq(sp.ln(x**2),sp.ln(-(x1+x2)*x -(x1*x2)), evaluate=False))
    return equation

def logarithmic_equations_solve_using_one_to_one_property_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="ln_both_sides", disabled=False))
    def ln_both_sides(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        equation = Eq(sp.E**lhs, sp.E**rhs, evaluate=False)
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="ln_both_sides", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="ln_both_sides", value=V('equation'), disabled=True) &
                Fact(field="rhs_zero", disabled=False))
    def rhs_zero(equation):
        x = symbols('x')
        equation = parse_latex(equation)
        equation = parse_latex(latex(Eq(equation.lhs-equation.rhs, 0)))
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="rhs_zero", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="rhs_zero", value=V('equation'), disabled=True) &
                Fact(field="factorized_form", disabled=False))
    def factorized_form(equation):
        x = symbols('x')
        equation = parse_latex(equation)
        equation = Eq(equation.lhs-equation.rhs, 0)
        equation = sp.factor(equation)
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="factorized_form", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="factorized_form", value=V('equation'), disabled=True) &
                Fact(field="first_equation", disabled=False))
    def first_equation(equation):
        x = symbols('x')
        equation = parse_latex(equation)
        equation = Eq(equation.lhs-equation.rhs, 0)
        equation = sp.factor(equation)
        if equation.lhs.args[1] == 2:
            factor_eq = Eq(equation.lhs.args[0], 0)
            answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(factor_eq, order="grlex")))
            hint = latex(factor_eq)
            return [Fact(selection="first_equation", action="input change", input=answer, hint=hint)]

        facts = list()
        for factor in equation.lhs.args:
            factor_eq = Eq(factor, 0)
            answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(factor_eq, order="grlex")))
            hint = latex(factor_eq)
            facts.append(Fact(selection="first_equation", action="input change", input=answer, hint=hint))

        return facts
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="rhs_zero", value=V('equation'), disabled=True) &
                Fact(field="first_equation", value=V('factor_eq'), disabled=True) &
                Fact(field="second_equation", disabled=False))
    def second_equation(equation, factor_eq):
        x = symbols('x')
        equation = parse_latex(equation)
        equation = Eq(equation.lhs-equation.rhs, 0)
        equation = sp.factor(equation)
        first = parse_latex(factor_eq).lhs
        second = sp.div(equation.lhs, first)[0]
        equation = Eq(second, 0)
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="second_equation", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="first_equation", value=V('equation'), disabled=True) &
                Fact(field="first_root", disabled=False))
    def first_root(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        equation = Eq(sp.E**lhs, sp.E**rhs, evaluate=False)
        lhs, rhs = equation.lhs, equation.rhs
        equation = Eq(lhs-rhs, 0)
        equation = sp.factor(equation)
        if equation.lhs.args[1] == 2:
            print(equation)
            equation = -equation.lhs.args[0].args[0]
            answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
            hint = latex(equation)
            return [Fact(selection="logarithmic_equations_first_root_directly", action="input change", input=answer, hint=hint)]
        
        facts = list()
        for factor in equation.lhs.args:
            print(factor, -factor.args[0] )
            equation = -factor.args[0] 
            answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
            hint = latex(equation)
            facts.append(Fact(selection="first_root", action="input change", input=answer, hint=hint))
        return facts
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="first_root", value=V('first_root'), disabled=True) &
                Fact(field="second_root", disabled=False))
    def second_root(init_value, first_root):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        equation = Eq(sp.E**lhs, sp.E**rhs, evaluate=False)
        lhs, rhs = equation.lhs, equation.rhs
        equation = Eq(lhs-rhs, 0)
        first_expression = (x-parse_latex(first_root))
        equation = sp.div(equation.lhs, first_expression)[0]
        equation = -equation.args[0]
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="second_root", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="first_root", disabled=True) &
                Fact(field="second_root", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    net.add_production(ln_both_sides)
    net.add_production(rhs_zero)
    net.add_production(factorized_form)
    net.add_production(first_equation)
    net.add_production(second_equation)
    net.add_production(first_root)
    net.add_production(second_root)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def logarithmic_equations_solve_using_one_to_one_property_kc_mapping():
    kcs = {
        "ln_both_sides": "ln_both_sides",
        "rhs_zero": "rhs_zero",
        "factorized_form": "factorized_form",
        "first_equation": "first_equation",
        "second_equation": "second_equation",
        "first_root": "first_root",
        "second_root": "second_root",
        "select_done": "Determine if exponential equation with common base is complete"
    }
    return kcs


def logarithmic_equations_solve_using_one_to_one_property_intermediate_hints():
    hints = {
        "ln_both_sides": ["Take the natural log of both sides of the equation."],
        "rhs_zero": ["Set the right hand side equal to zero."],
        "factorized_form": ["Factor the left hand side of the equation using FOIL."],
        "first_equation": ["Set first factor equal to zero."],
        "second_equation": ["Set second factor equal to zero."],
        "first_root": ["Find value of \(e^{x}\) that makes first factor equal to zero."],
        "second_root": ["Find value of \(e^{x}\) that makes second factor equal to zero."]
    }
    return hints

def logarithmic_equations_solve_using_one_to_one_property_studymaterial():
    study_material = studymaterial["logarithmic_equations_solve_using_one_to_one_property"]
    return study_material

loaded_models.register(CognitiveModel("logarithmic_equations",
                                      "logarithmic_equations_solve_using_one_to_one_property",
                                      logarithmic_equations_solve_using_one_to_one_property_model,
                                      logarithmic_equations_solve_using_one_to_one_property_problem,
                                      logarithmic_equations_solve_using_one_to_one_property_kc_mapping(),
                                      logarithmic_equations_solve_using_one_to_one_property_intermediate_hints(),
                                      logarithmic_equations_solve_using_one_to_one_property_studymaterial()))