from random import randint, choice

import sympy as sp
from sympy import latex, symbols, expand, sstr, Eq, solve
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re 

from py_rete import Fact, Production, ReteNetwork, V

from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def exponential_equations_solve_quadratic_form_problem():
    x = symbols('x')
    ex = sp.E**x
    x1, x2 = randint(-10, 10), randint(-10, 10)
    while not (x1+x2) or not (x1*x2):
      x1, x2 = randint(-10, 10), randint(-10, 10)

    equation = latex(Eq(ex**2+(x1+x2)*ex, -(x1*x2), evaluate=False))
    return equation

def exponential_equations_solve_quadratic_form_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="rhs_zero", disabled=False))
    def rhs_zero(init_value):
        x = symbols('x')
        equation = parse_latex(init_value)
        equation = parse_latex(latex(Eq((equation.lhs)-equation.rhs, 0)))
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="rhs_zero", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="rhs_zero", disabled=True) &
                Fact(field="factorized_form", disabled=False))
    def factorized_form(init_value):
        x = symbols('x')
        equation = parse_latex(init_value)
        equation = Eq(equation.lhs-equation.rhs, 0)
        equation = sp.factor(equation)
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="factorized_form", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="factorized_form", disabled=True) &
                Fact(field="first_equation", disabled=False))
    def first_equation(init_value):
        x = symbols('x')
        print("WHAT IS IT", init_value)
        equation = parse_latex(init_value)
        print("WHAT IS IT", init_value)
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
                Fact(field="factorized_form", disabled=True) &
                Fact(field="first_equation", value=V('factor_eq'), disabled=True) &
                Fact(field="second_equation", disabled=False))
    def second_equation(init_value, factor_eq):
        x = symbols('x')
        equation = parse_latex(init_value)
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
    def first_root(equation):
        x = symbols('x')
        lhs = parse_latex(equation).lhs
        equation = Eq(lhs.args[0] , -lhs.args[1])
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="first_root", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="second_equation", value=V('equation'), disabled=True) &
                Fact(field="second_root", disabled=False))
    def second_root(equation):
        x = symbols('x')
        lhs = parse_latex(equation).lhs
        equation = Eq(lhs.args[0] , -lhs.args[1])
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="second_root", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="first_equation", value=V('equation'), disabled=True) &
                Fact(field="first_root", disabled=True) &
                Fact(field="first_x", disabled=False))
    def first_x(equation):
        x = symbols('x')
        lhs = parse_latex(equation).lhs
        root = Eq(lhs.args[0] , -lhs.args[1])
        # root = parse_latex(root)
        equation  = sp.ln(root.rhs) if root.rhs >=0 else parse_latex("NA")
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', re.sub(r'log\(([^)]+)\)', r'log(\1, E)', sstr(equation, order="grlex"))))
        hint = latex(sp.ln(root.rhs)) if root.rhs >=0 else "NA"
        return [Fact(selection="first_x", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="second_equation", value=V('equation'), disabled=True) &
                Fact(field="second_root", disabled=True) &
                Fact(field="second_x", disabled=False))
    def second_x(equation):
        x = symbols('x')
        lhs = parse_latex(equation).lhs
        root = Eq(lhs.args[0] , -lhs.args[1])
        # root = parse_latex(root)
        equation  = sp.ln(root.rhs) if root.rhs >=0 else parse_latex("NA")
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', re.sub(r'log\(([^)]+)\)', r'log(\1, E)', sstr(equation, order="grlex"))))
        hint = latex(sp.ln(root.rhs)) if root.rhs >=0 else "NA"
        return [Fact(selection="second_x", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="first_x", disabled=True) &
                Fact(field="second_x", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    net.add_production(rhs_zero)
    net.add_production(factorized_form)
    net.add_production(first_equation)
    net.add_production(second_equation)
    net.add_production(first_root)
    net.add_production(second_root)
    net.add_production(first_x)
    net.add_production(second_x)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def exponential_equations_solve_quadratic_form_kc_mapping():
    kcs = {
        "rhs_zero" : "rhs_zero",
        "factorized_form" : "factorized_form",
        "first_equation" : "first_equation",
        "second_equation" : "second_equation",
        "first_root" : "first_root",
        "second_root" : "second_root",
        "first_x" : "first_x",
        "second_x" : "second_x",
        "select_done": "Determine if exponential equation with common base is complete"
    }
    return kcs


def exponential_equations_solve_quadratic_form_intermediate_hints():
    hints = {
        "rhs_zero": ["Set the right hand side equal to zero."],
        "factorized_form": ["Factor the left hand side of the equation using FOIL."],
        "first_equation": ["Set first factor equal to zero."],
        "second_equation": ["Set second factor equal to zero."],
        "first_root": ["Find value of \(e^{x}\) that makes first factor equal to zero."],
        "second_root": ["Find value of \(e^{x}\) that makes second factor equal to zero."],
        "first_x": ["Solve for x."],
        "second_x": ["Solve for x."],
        "solve_for_x" : ["Solve for x."],
    }
    return hints

def exponential_equations_solve_quadratic_form_studymaterial():
    study_material = studymaterial["exponential_equations_solve_quadratic_form"]
    return study_material

loaded_models.register(CognitiveModel("exponential_equations",
                                      "exponential_equations_solve_quadratic_form",
                                      exponential_equations_solve_quadratic_form_model,
                                      exponential_equations_solve_quadratic_form_problem,
                                      exponential_equations_solve_quadratic_form_kc_mapping(),
                                      exponential_equations_solve_quadratic_form_intermediate_hints(),
                                      exponential_equations_solve_quadratic_form_studymaterial()))