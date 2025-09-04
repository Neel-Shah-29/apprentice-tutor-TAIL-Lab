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
from sympy import symbols, expand, latex, sstr
from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

import re 

from studymaterial import studymaterial

def quadratic_equations_solve_using_quadratic_formula_problem():
    x = sp.symbols('x')
    a, b, c = 0, 0, 0
    while not (a*b*c) or (b**2 - 4*a*c) < 0:
       a, b, c = randint(-5, 5), randint(-10, 10), randint(-5, 5)
    equation = latex(sp.Eq(a*x**2+b*x+c, 0))
    return equation

def quadratic_equations_solve_using_quadratic_formula():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="d_value", disabled=False)) 
    def d_value(init_value):
        x = symbols('x')
        init_equation = sp.simplify(parse_latex(init_value).lhs)
        a, b, c = init_equation.coeff(x, 2), init_equation.coeff(x, 1), init_equation.coeff(x, 0)
        d = b**2 - 4*a*c
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(d, order="grlex")))
        hint = latex(d)
        return [Fact(selection="d_value", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="d_value", disabled=True) &
                Fact(field="sqrt_d_value", disabled=False))
    def sqrt_d_value(init_value):
        x = symbols('x')
        init_equation = sp.simplify(parse_latex(init_value).lhs)
        a, b, c = init_equation.coeff(x, 2), init_equation.coeff(x, 1), init_equation.coeff(x, 0)
        root_d = sp.sqrt(b**2 - 4*a*c)
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(root_d, order="grlex")))
        hint = latex(root_d)
        return [Fact(selection="sqrt_d_value", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="sqrt_d_value", disabled=True) &
                Fact(field="first_numerator", disabled=False))
    def first_numerator(init_value):
        x = symbols('x')
        init_equation = sp.simplify(parse_latex(init_value).lhs)
        a, b, c = init_equation.coeff(x, 2), init_equation.coeff(x, 1), init_equation.coeff(x, 0)
        numerator = -b + sp.sqrt(b**2 - 4*a*c)
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(numerator, order="grlex")))
        hint = latex(numerator)
        return [Fact(selection="first_numerator", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="first_numerator", disabled=True) &
                Fact(field="second_numerator", disabled=False))
    def second_numerator(init_value):
        x = symbols('x')
        init_equation = sp.simplify(parse_latex(init_value).lhs)
        a, b, c = init_equation.coeff(x, 2), init_equation.coeff(x, 1), init_equation.coeff(x, 0)
        numerator = -b - sp.sqrt(b**2 - 4*a*c)
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(numerator, order="grlex")))
        hint = latex(numerator)
        return [Fact(selection="second_numerator", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="second_numerator", disabled=True) &
                Fact(field="denominator", disabled=False))
    def denominator(init_value):
        x = symbols('x')
        init_equation = sp.simplify(parse_latex(init_value).lhs)
        denominator = 2 * init_equation.coeff(x, 2)
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(denominator, order="grlex")))
        hint = latex(denominator)
        return [Fact(selection="denominator", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="denominator", disabled=True) &
                Fact(field="first_root", disabled=False))
    def first_root(init_value):
        x = symbols('x')
        init_equation = sp.simplify(parse_latex(init_value).lhs)
        a, b, c = init_equation.coeff(x, 2), init_equation.coeff(x, 1), init_equation.coeff(x, 0)
        numerator = -b + sp.sqrt(b**2 - 4*a*c)
        denominator = 2 * a
        root = sp.expand(numerator/denominator)
        answer = sp.sstr(root, order="grlex")
        # if (len(answer) > 3) and (answer[:2] == "-s") and (not "+" in answer):
        #     answer = answer.replace("-sqrt", "-1*sqrt")
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', answer))
        hint = latex(root)
        return [Fact(selection="first_root", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="first_root", disabled=True) &
                Fact(field="second_root", disabled=False))
    def second_root(init_value):
        x = symbols('x')
        init_equation = sp.simplify(parse_latex(init_value).lhs)
        a, b, c = init_equation.coeff(x, 2), init_equation.coeff(x, 1), init_equation.coeff(x, 0)
        numerator = -b - sp.sqrt(b**2 - 4*a*c)
        denominator = 2 * a
        root = sp.expand(numerator/denominator)
        answer = sp.sstr(root, order="grlex")
        # if (len(answer) > 3) and (answer[:2] == "-s") and (not "+" in answer):
        #     answer = answer.replace("-sqrt", "-1*sqrt")
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', answer))
        hint = latex(root)
        return [Fact(selection="second_root", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="second_root", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input="x")]  
    

    net.add_production(d_value)
    net.add_production(sqrt_d_value)
    net.add_production(first_numerator)
    net.add_production(second_numerator)
    net.add_production(denominator)
    net.add_production(first_root)
    net.add_production(second_root)
    net.add_production(select_done)
    

    sp.core.cache.clear_cache()
    return net


def solve_using_quadratic_formula_kc_mapping():
    # key --> rule
    # value --> human readable value for kc (unique)

    kcs = {
        "d_value": "compute_discriminant",
        "sqrt_d_value": "squared_compute_discriminant",
        "first_numerator": "numerator_of_quadratic_formula",
        "second_numerator": "numerator_of_quadratic_formula",
        "denominator": "denominator_of_quadratic_formula",
        "first_root": "first_root",
        "second_root": "second_root",
        'select_done': "Determine if factoring is complete",
    }
    return kcs


def solve_using_quadratic_formula_intermediate_hints():
    hints = {

        'd_value':["Discriminat is \(b^2 - 4ac\)."],
        'sqrt_d_value':["Square root of \(\sqrt{b^2 - 4ac}\)."],
        'first_numerator':["First numerator is equal to \(-b+\sqrt{b^2-4ac}\)"],
        'second_numerator':["Second numerator is equal to \(-b-\sqrt{b^2-4ac}\)"],
        'denominator':["Denominator is equal to \(2a\)."],
        'first_root':["First root is equal to \(\\frac{-b+\sqrt{b^2-4ac}}{2a}\)"],
        'second_root':["Second root is equal to \(\\frac{-b-\sqrt{b^2-4ac}}{2a}\)"],
        'select_done': ["Once you are done finding the roots "
                        "select the done button to move to the next problem."]
    }
    return hints

def solve_using_quadratic_formula_studymaterial():
    study_material = studymaterial["quadratic_equations_solve_using_quadratic_formula"]
    return study_material

loaded_models.register(CognitiveModel("quadratic_equations",
                                      "quadratic_equations_solve_using_quadratic_formula",
                                      quadratic_equations_solve_using_quadratic_formula,
                                      quadratic_equations_solve_using_quadratic_formula_problem,
                                      solve_using_quadratic_formula_kc_mapping(),
                                      solve_using_quadratic_formula_intermediate_hints(),
                                      solve_using_quadratic_formula_studymaterial()))