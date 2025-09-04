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

def quadratic_equations_solve_using_square_root_property_problem():
    x = sp.symbols('x')
    c1, c2 = -1, -1
    while (c2-c1) <= 0:
        c1, c2 = randint(-10, 10), randint(-10, 10)
    a = randint(1, 10)**2
    equation = latex(sp.Eq(a*x**2+c1, c2))
    return equation

def quadratic_equations_solve_using_square_root_property():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="coeff0_to_rhs", disabled=False)) 
    def coeff0_to_rhs(init_value):
        x = symbols('x')
        init_equation = parse_latex(init_value)
        a, c1, c2 = init_equation.lhs.coeff(x, 2), init_equation.lhs.coeff(x, 0), init_equation.rhs.coeff(x, 0)
        equation = sp.Eq(a*x**2, sp.Add(c2, -c1, evaluate=False))
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="coeff0_to_rhs", action="input change", input=answer, hint=hint)]

    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="coeff0_to_rhs", disabled=True) &
                Fact(field="update_coeff0_on_rhs", disabled=False)) 
    def update_coeff0_on_rhs(init_value):
        x = symbols('x')
        init_equation = parse_latex(init_value)
        a, c1, c2 = init_equation.lhs.coeff(x, 2), init_equation.lhs.coeff(x, 0), init_equation.rhs.coeff(x, 0)
        equation = sp.Eq(a*x**2, sp.Add(c2, -c1))
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="update_coeff0_on_rhs", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="update_coeff0_on_rhs", disabled=True) &
                Fact(field="coeff2_to_rhs", disabled=False))
    def coeff2_to_rhs(init_value):
        x = symbols('x')
        init_equation = parse_latex(init_value)
        a, c1, c2 = init_equation.lhs.coeff(x, 2), init_equation.lhs.coeff(x, 0), init_equation.rhs.coeff(x, 0)
        equation = sp.Eq(x**2, sp.Mul(sp.Add(c2, -c1)/a, evaluate=False))
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(equation, order="grlex").replace("*(1", "")))
        hint = latex(equation)
        return [Fact(selection="coeff2_to_rhs", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="coeff2_to_rhs", disabled=True) &
                Fact(field="update_coeff2_on_rhs", disabled=False))
    def update_coeff2_on_rhs(init_value):
        x = symbols('x')
        init_equation = parse_latex(init_value)
        a, c1, c2 = init_equation.lhs.coeff(x, 2), init_equation.lhs.coeff(x, 0), init_equation.rhs.coeff(x, 0)
        equation = sp.Eq(x**2, sp.simplify(sp.Mul(sp.Add(c2, -c1),1/a)))
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="update_coeff2_on_rhs", action="input change", input=answer, hint=hint)]
    

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="update_coeff2_on_rhs", disabled=True) &
                Fact(field="positive_root", disabled=False))
    def positive_root(init_value):
        x = symbols('x')
        init_equation = parse_latex(init_value)
        root = sp.solve(init_equation, x)[1]
        answer =  sp.sstr(root, order="grlex").replace("*","")
        # if (len(answer) > 3) and (answer[:2] == "-s") and (not "+" in answer):
        #     answer = answer.replace("-sqrt", "-1*sqrt")
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', answer))
        hint = latex(root)
        return [Fact(selection="positive_root", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="update_coeff2_on_rhs", disabled=True) &
                Fact(field="negative_root", disabled=False))
    def negative_root(init_value):
        x = symbols('x')
        init_equation = parse_latex(init_value)
        root = sp.solve(init_equation, x)[0]
        answer =  sp.sstr(root, order="grlex").replace("*","")
        # if (len(answer) > 3) and (answer[:2] == "-s") and (not "+" in answer):
        #     answer = answer.replace("-sqrt", "-1*sqrt")
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', answer))
        hint = latex(root)
        return [Fact(selection="negative_root", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="positive_root", disabled=True) &
                Fact(field="negative_root", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input="x")]  
    
    net.add_production(coeff0_to_rhs)
    net.add_production(update_coeff0_on_rhs)
    net.add_production(coeff2_to_rhs)
    net.add_production(update_coeff2_on_rhs)
    net.add_production(positive_root)
    net.add_production(negative_root)
    net.add_production(select_done)
    

    sp.core.cache.clear_cache()
    return net


def solve_using_square_root_property_kc_mapping():
    # key --> rule
    # value --> human readable value for kc (unique)

    kcs = {
        'coeff0_to_rhs': "coeff0_to_rhs",
        'update_coeff0_on_rhs': 'subtract_values',
        'coeff2_to_rhs': 'coeff2_to_rhs',
        'update_coeff2_on_rhs': 'divide_values',
        'positive_root': 'positive_root_using_square_root_property',
        'negative_root': 'negative_root_using_square_root_property',
        'select_done': "Determine if factoring is complete",
    }
    return kcs


def solve_using_square_root_property_intermediate_hints():
    hints = {
        'coeff0_to_rhs': ["Move the constant term to the right hand side of the "
                          "equation."],
        'update_coeff0_on_rhs': ["Simplify the RHS"],
        'update_coeff2_on_rhs': ["Move the coeeficient of x^2 to the right hand."],
        'positive_root': ["Take square of both sides and solve for x."],
        'negative_root': ["Take square of both sides and solve for x."],
        'select_done': ["Once you are done finding the roots "
                        "select the done button to move to the next problem."]
    }
    return hints

def solve_using_square_root_property_studymaterial():
    study_material = studymaterial["quadratic_equations_solve_using_square_root_property"]
    return study_material

loaded_models.register(CognitiveModel("quadratic_equations",
                                      "quadratic_equations_solve_using_square_root_property",
                                      quadratic_equations_solve_using_square_root_property,
                                      quadratic_equations_solve_using_square_root_property_problem,
                                      solve_using_square_root_property_kc_mapping(),
                                      solve_using_square_root_property_intermediate_hints(),
                                      solve_using_square_root_property_studymaterial()))