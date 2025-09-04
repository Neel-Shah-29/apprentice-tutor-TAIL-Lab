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

def quadratic_equations_nature_of_solution_problem():
    x = sp.symbols('x')
    a, b, c = 0, 0, 0
    while not b or not c or not a:
       a, b, c = randint(-10, 10), randint(-10, 10), randint(-10, 10)
    equation = latex(sp.Eq(a*x**2+b*x+c, 0))
    return equation

def quadratic_equations_nature_of_solution():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="squared_b_value", disabled=False))
    def squared_b_value(init_value):
        x = symbols('x')
        init_equation = parse_latex(init_value)
        b = sp.simplify(init_equation.lhs).coeff(x, 1) 
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(b**2)))
        hint = latex(b**2)
        return [Fact(selection="squared_b_value", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="ac_product", disabled=False))
    def ac_product(init_value):
        x = symbols('x')
        init_equation = parse_latex(init_value)
        ac = sp.simplify(init_equation.lhs).coeff(x, 2) * sp.simplify(init_equation.lhs).coeff(x, 0) 
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(4*ac)))
        hint = latex(4*ac)
        return [Fact(selection="ac_product", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="squared_b_value", value=V('b_2'), disabled=True) &
                Fact(field="ac_product", value=V('ac'), disabled=True) &
                Fact(field="d_expression", disabled=False))
    def d_expression(b_2, ac):
        d = int(b_2) - int(ac)
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(d)))
        hint = latex(d)
        return [Fact(selection="d_expression", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="d_expression", value=V('d'), disabled=True) &
                Fact(field="type_of_roots", disabled=False))
    def type_of_roots(d):
        if int(d) > 0:
            answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(parse_latex("real and distinct"), order="grlex")))
            return [Fact(selection="type_of_roots", action="input change", input=answer, hint="real and distinct")]    
        if int(d) == 0:
            answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(parse_latex("real and equal"), order="grlex")))
            return [Fact(selection="type_of_roots", action="input change", input=answer, hint="real and equal")]
        if int(d) < 0:
            answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(parse_latex("imaginary"), order="grlex")))
            return [Fact(selection="type_of_roots", action="input change", input=answer, hint="real and distinct")]     

    @Production(Fact(field="type_of_roots", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input="x")]  
    

    net.add_production(squared_b_value)
    net.add_production(ac_product)
    net.add_production(d_expression)
    net.add_production(type_of_roots)
    net.add_production(select_done)
    

    sp.core.cache.clear_cache()
    return net


def nature_of_solution_kc_mapping():
    # key --> rule
    # value --> human readable value for kc (unique)

    kcs = {

        "squared_b_value": "square_b_value",
        "ac_product": "multiply_values",
        "d_expression": "compute_discriminant",
        "type_of_roots": "nature_of_root",
        'select_done': "Determine if factoring is complete",
    }
    return kcs


def nature_of_solution_intermediate_hints():
    hints = {

        'squared_b_value': ["Here \(b^2\) is coefficient of \(x\) squared."],
        'ac_product': ["Here \(ac\) is the product of the coefficients of \(x^2\) and constant."],
        'd_expression': ["Discriminat is \(b^2 - 4ac\)."],
        'type_of_roots': ["If \(D>0\) then roots are real and distinct. "
                          "If \(D=0\) then roots are real and equal. "
                          "If \(D<0\) then roots are imaginary."],
        'select_done': ["Once you are done finding the roots "
                        "select the done button to move to the next problem."]
    }
    return hints

def nature_of_solution_studymaterial():
    study_material = studymaterial["quadratic_equations_nature_of_solution"]
    return study_material

loaded_models.register(CognitiveModel("quadratic_equations",
                                      "quadratic_equations_nature_of_solution",
                                      quadratic_equations_nature_of_solution,
                                      quadratic_equations_nature_of_solution_problem,
                                      nature_of_solution_kc_mapping(),
                                      nature_of_solution_intermediate_hints(),
                                      nature_of_solution_studymaterial()))