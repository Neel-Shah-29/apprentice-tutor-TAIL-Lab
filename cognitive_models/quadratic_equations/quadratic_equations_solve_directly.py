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

def quadratic_equations_solve_directly_problem():
    x = sp.symbols('x')
    a, b, c = 0, 0, 0
    while not (a*b*c) or (b**2 - 4*a*c) < 0:
       a, b, c = randint(-5, 5), randint(-10, 10), randint(-5, 5)
    equation = latex(sp.Eq(a*x**2+b*x+c, 0))
    return equation

def quadratic_equations_solve_directly():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
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
    
    
    net.add_production(first_root)
    net.add_production(second_root)
    net.add_production(select_done)
    

    sp.core.cache.clear_cache()
    return net


def solve_directly_kc_mapping():
    # key --> rule
    # value --> human readable value for kc (unique)

    kcs = {
        "first_root": "first_root",
        "second_root": "second_root",
        'select_done': "Determine if factoring is complete",
    }
    return kcs


def solve_directly_intermediate_hints():
    hints = {

        'first_root':["First root is equal to \(\\frac{-b+\sqrt{b^2-4ac}}{2a}\)"],
        'second_root':["Second root is equal to \(\\frac{-b-\sqrt{b^2-4ac}}{2a}\)"],
        'select_done': ["Once you are done finding the roots "
                        "select the done button to move to the next problem."]
    }
    return hints

def solve_directly_studymaterial():
    study_material = studymaterial["quadratic_equations_solve_directly"]
    return study_material

loaded_models.register(CognitiveModel("quadratic_equations",
                                      "quadratic_equations_solve_directly",
                                      quadratic_equations_solve_directly,
                                      quadratic_equations_solve_directly_problem,
                                      solve_directly_kc_mapping(),
                                      solve_directly_intermediate_hints(),
                                      solve_directly_studymaterial()))