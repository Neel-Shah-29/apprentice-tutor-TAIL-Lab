import math
from functools import reduce
from random import randint, random, choice
from pprint import pprint
import re

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

from studymaterial import studymaterial

def quadratic_equations_solve_using_factors_problem():
    x = sp.symbols('x')
    x1, x2, coeff = 0, 0, 0
    while not (x1*x2) or not coeff:
        x1, x2 = randint(-10, 10), randint(-10, 10)
        factorlist = [f for factor in sp.divisors(int(x1)) for f in (factor, -factor) if (f*x2+x1) 
                                                                                    and abs((f*x1+x2)/f)/(2*sp.sqrt(abs(x1*x2/f)))!=1]
        if factorlist: 
            coeff = choice(factorlist)
    terms = [coeff*x*x, coeff*x*(-x1), (-x2)*x, (-x1)*(-x2)]
    equation = "+".join(map(str, terms)).replace("+-", "-").replace("x**2", "x^{2}").replace("*", "")
    equation = f"{equation}=0"
    return equation

def quadratic_equations_solve_using_factors():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="factorized_form", disabled=False))
    def update_factorized_form(init_value):
        fact = list()
        const, factors = sp.factor((parse_latex(init_value)).lhs).as_coeff_mul()   
        if len(factors) == 1:
            factors = (*factors, 1)
        for i in range(2):
            equation = sp.Eq(sp.Mul(const, factors[i])*factors[(i+1)%2], 0)
            answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(equation, order="grlex")))
            hint = f"{equation.lhs}={equation.rhs}".replace("*", "")
            fact.append(Fact(selection="factorized_form", action="input change", input=answer, hint=hint))
        return fact

    @Production(Fact(field="initial_problem") &
                Fact(field="factorized_form", value=V('factorized'), disabled=True) &
                Fact(field='first_equation', disabled=False))
    def update_first_equation(factorized):
        facts = list()
        for factor in parse_latex(factorized).lhs.as_coeff_mul()[1]:
            equation = sp.Eq(factor,0)
            # answer = re.compile(re.sub(r'([\.\+\*\?\[\^\]\$\(\)\{\}\=\!\<\>\|\:\-])', r'\\\1', sp.sstr(equation)))    
            answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(equation, order="grlex")))    
            hint = f"{equation.lhs}={equation.rhs}"
            facts.append(Fact(selection="first_equation", action="input change", input=answer, hint=hint))
        return facts

    @Production(Fact(field="factorized_form", value=V('factorized_eq')) &
                Fact(field="first_equation", value=V('factor'), disabled=True) &
                Fact(field='second_equation', disabled=False))
    def update_second_equation(factorized_eq, factor):
        equation = parse_latex(factorized_eq).lhs
        factor = parse_latex(factor).lhs
        quotient = sp.Eq(sp.div(equation, factor)[0],0)
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(quotient, order="grlex")))
        hint = f"{quotient.lhs}={quotient.rhs}"
        return [Fact(selection="second_equation", action="input change", input=answer, hint=hint)]
        

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="first_equation", value=V('factor'), disabled=True) &
                Fact(field="second_equation", disabled=True) &
                Fact(field="first_root", disabled=False))
    def update_first_root(factor):
        x = symbols("x")
        root = sp.sstr(sp.solve(parse_latex(factor), x)[0], order="grlex")
        answer = re.compile(root)
        hint = root
        return [Fact(selection="first_root", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="first_equation", disabled=True) &
                Fact(field="second_equation", value=V('factor'), disabled=True) &
                Fact(field="second_root", disabled=False))
    def update_second_root(factor):
        x = symbols("x")
        root = sp.sstr(sp.solve(parse_latex(factor), x)[0], order="grlex")
        answer = re.compile(root)
        hint = root
        return [Fact(selection="second_root", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="first_root", disabled=True) &
                Fact(field="second_root", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input="x")]

    
    
    net.add_production(update_factorized_form)
    net.add_production(update_first_equation)
    net.add_production(update_second_equation)
    net.add_production(update_first_root)
    net.add_production(update_second_root)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def solve_using_factors_kc_mapping():
    # key --> rule
    # value --> human readable value for kc (unique)

    kcs = {
        'update_factorized_form': "factorized_form_of_quadratic_equation",
        'update_first_equation': 'equation_of_factorization_of_quadratic_equation',
        'update_second_equation': 'equation_of_factorization_of_quadratic_equation',
        'update_first_root': 'root_of_quadratic_equation',
        'update_second_root': 'root_of_quadratic_equation',
        'select_done': "Determine if factoring is complete",
    }
    return kcs


def solve_using_factors_intermediate_hints():
    hints = {
        'update_factorized_form': ["The factored form of the equation in this "
                            "case is first two terms clubbed together and "
                            "the last two terms clubbed together."],
        'update_first_equation': ["Equate one of the above expressions to zero"],
        'update_second_equation': ["Equate the other expression to zero"],
        'update_first_root': ["The first root is the value of x that makes the "
                            "first expression equal to zero."],
        'update_second_root': ["The second root is the value of x that makes the "
                            "second expression equal to zero."],
        'select_done': ["Once you have found the final factored form you can "
                        "select the done button to move to the next problem."]
    }
    return hints

def solve_using_factors_studymaterial():
    study_material = studymaterial["quadratic_equations_solve_using_factors"]
    return study_material

loaded_models.register(CognitiveModel("quadratic_equations",
                                      "quadratic_equations_solve_using_factors",
                                      quadratic_equations_solve_using_factors,
                                      quadratic_equations_solve_using_factors_problem,
                                      solve_using_factors_kc_mapping(),
                                      solve_using_factors_intermediate_hints(),
                                      solve_using_factors_studymaterial()))