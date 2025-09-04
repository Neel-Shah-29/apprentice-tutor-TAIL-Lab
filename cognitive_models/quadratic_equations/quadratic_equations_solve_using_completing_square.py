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

def quadratic_equations_solve_using_completing_square_problem():
    x = sp.symbols('x')
    b, c = 0, 0
    while not b:
        b, c = randint(-10, 10), randint(1, 10)
    equation = latex(sp.Eq(x**2+b*x, c))
    return equation

def quadratic_equations_solve_using_completing_square():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="b_by_2_square_lhs", disabled=False)) 
    def b_by_2_square_lhs(init_value):
        x = symbols('x')
        init_equation = parse_latex(init_value)
        b = init_equation.lhs.expand().coeff(x, 1)
        lhs = parse_latex(f"x^2+{b}x+{(b/2)**2}".replace("+-", "-"))
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(lhs, order="grlex")))
        hint = latex(lhs)
        return [Fact(selection="b_by_2_square_lhs", action="input change", input=answer, hint=hint)]

    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="b_by_2_square_rhs", disabled=False)) 
    def b_by_2_square_rhs(init_value):
        x = symbols('x')
        init_equation = parse_latex(init_value)
        b, c = init_equation.lhs.expand().coeff(x, 1), init_equation.rhs.coeff(x, 0)
        rhs = parse_latex(f"{c}+{(b/2)**2}".replace("+-", "-"))
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(rhs, order="grlex")))
        hint = latex(rhs)
        return [Fact(selection="b_by_2_square_rhs", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="b_by_2_square_lhs", value=V('b_by_2_square_lhs_'), disabled=True) &
                Fact(field="factor_lhs", disabled=False))
    def factor_lhs(init_value):
        x = symbols('x')
        init_equation = parse_latex(init_value)
        b = init_equation.lhs.expand().coeff(x, 1)
        factored = parse_latex(f"(x+{b/2})^2".replace("+-", "-"))
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sp.sstr(factored, order="grlex")))
        hint = latex(factored)
        return [Fact(selection="factor_lhs", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="b_by_2_square_rhs", value=V('b_by_2_square_rhs_'), disabled=True) &
                Fact(field="simplify_rhs", disabled=False))
    def simplify_rhs(b_by_2_square_rhs_):
        x = symbols('x')
        simplified = sp.simplify(parse_latex(b_by_2_square_rhs_))
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(simplified, order="grlex")))
        hint = latex(simplified)
        return [Fact(selection="simplify_rhs", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="factor_lhs", value=V('lhs'), disabled=True) &
                Fact(field="simplify_rhs", value=V('rhs'), disabled=True) &
                Fact(field="combine_lhs_rhs", disabled=False))
    def combine_lhs_rhs(lhs, rhs):
        x = symbols('x')
        lhs, rhs = parse_latex(lhs), parse_latex(rhs)
        equation = sp.Eq(lhs, rhs)
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="combine_lhs_rhs", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="simplify_rhs", value=V('rhs'), disabled=True) &
                Fact(field="combine_lhs_rhs", disabled=True) &
                Fact(field="positive_root_of_rhs", disabled=False))
    def positive_root_of_rhs(init_value, rhs):
        x = symbols('x')
        init_equation = parse_latex(init_value)
        b = init_equation.lhs.expand().coeff(x, 1)
        lhs, rhs = parse_latex(f"x+{b/2}".replace("+-", "-")), parse_latex(rhs)
        equation = sp.Eq(lhs, sp.sqrt(rhs))
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="positive_root_of_rhs", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="simplify_rhs", value=V('rhs'), disabled=True) &
                Fact(field="combine_lhs_rhs", disabled=True) &
                Fact(field="negative_root_of_rhs", disabled=False))
    def negative_root_of_rhs(init_value, rhs):
        x = symbols('x')
        init_equation = parse_latex(init_value)
        b = init_equation.lhs.expand().coeff(x, 1)
        lhs, rhs = parse_latex(f"x+{b/2}".replace("+-", "-")), parse_latex(rhs)
        equation = sp.Eq(lhs, -sp.sqrt(rhs))
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="negative_root_of_rhs", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="positive_root_of_rhs", value=V('positive'), disabled=True) &
                Fact(field="positive_root", disabled=False))
    def positive_root(positive):
        x = symbols('x')
        equation = parse_latex(positive)
        root = sp.solve(equation, x)[0]
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(root, order="grlex").replace("*","")))
        hint = latex(root)
        return [Fact(selection="positive_root", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="negative_root_of_rhs", value=V("negative"), disabled=True) &
                Fact(field="negative_root", disabled=False))
    def negative_root(negative):
        x = symbols('x')
        equation = parse_latex(negative)
        root = sp.solve(equation, x)[0]
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(root, order="grlex").replace("*","")))
        hint = latex(root)
        return [Fact(selection="negative_root", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="positive_root", disabled=True) &
                Fact(field="negative_root", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input="x")]  
    

    net.add_production(b_by_2_square_lhs)
    net.add_production(b_by_2_square_rhs)
    net.add_production(factor_lhs)
    net.add_production(simplify_rhs)
    net.add_production(combine_lhs_rhs)
    net.add_production(positive_root_of_rhs)
    net.add_production(negative_root_of_rhs)
    net.add_production(positive_root)
    net.add_production( negative_root)
    net.add_production(select_done)
    

    sp.core.cache.clear_cache()
    return net


def solve_using_completing_square_kc_mapping():
    # key --> rule
    # value --> human readable value for kc (unique)

    kcs = {
        "b_by_2_square_lhs": "b_by_2_square_lhs",
        "b_by_2_square_rhs": "b_by_2_square_rhs",
        "factor_lhs": "factor_lhs",
        "simplify_rhs": "simplify_rhs",
        "combine_lhs_rhs": "combine_lhs_rhs",
        "positive_root_of_rhs": "positive_root_of_rhs",
        "negative_root_of_rhs": "negative_root_of_rhs",
        "positive_root": "positive_root_of_quadratic_equation",
        "negative_root": "negative_root_of_quadratic_equation",
        'select_done': "Determine if factoring is complete",
    }
    return kcs


def solve_using_completing_square_intermediate_hints():
    hints = {
        'b_by_2_square_lhs': ["Add the value of \(b^2/4\) to left hand "
                              "side of the equation."],
        'b_by_2_square_rhs': ["Add the value of \(b^2/4\) to right hand "
                              "side of the equation."],
        'factor_lhs': ["Now left hand side is of \((x+b/2)\)"],
        'simplify_rhs': ["Simplify the right hand side."],
        'combine_lhs_rhs': ["Write the lhs and rhs together."],
        'positive_root_of_rhs': ["Take square root of both sides and put "
                                 "positive root on the right hand side."],
        'negative_root_of_rhs': ["Take square root of both sides and put "
                                 "negative root on the right hand side."],
        'positive_root': ["Solve for \(x\)."],
        'negative_root': ["Solve for \(x\)."],
        'select_done': ["Once you are done finding the roots "
                        "select the done button to move to the next problem."]
    }
    return hints

def solve_using_completing_square_studymaterial():
    study_material = studymaterial["quadratic_equations_solve_using_completing_square"]
    return study_material

loaded_models.register(CognitiveModel("quadratic_equations",
                                      "quadratic_equations_solve_using_completing_square",
                                      quadratic_equations_solve_using_completing_square,
                                      quadratic_equations_solve_using_completing_square_problem,
                                      solve_using_completing_square_kc_mapping(),
                                      solve_using_completing_square_intermediate_hints(),
                                      solve_using_completing_square_studymaterial()))