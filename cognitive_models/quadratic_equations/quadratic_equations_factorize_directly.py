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

def quadratic_equations_factorize_directly_problem():
    x = sp.symbols('x')
    x1, x2, coeff = 0, 0, 0
    print("FIND PROBLEM")
    while not (x1*x2) or not coeff:
      x1, x2 = randint(-10, 10), randint(-10, 10)
      factorlist = [f for factor in sp.divisors(int(x1)) for f in (factor, -factor) if (f*x2+x1)]
      if factorlist: 
        coeff = choice(factorlist)
    print("SOLUTION PROBLEM")
    equation = latex(sp.Eq(expand((coeff*x-x1) * (x-x2)), 0))
    return equation

def quadratic_equations_factorize_directly():
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
            # hint = f"{equation.lhs}={equation.rhs}".replace("*", "")
            hint = latex(equation)
            fact.append(Fact(selection="factorized_form", action="input change", input=answer, hint=hint))
        return fact

    @Production(Fact(field="factorized_form", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input="x")]

    
    
    net.add_production(update_factorized_form)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def factorize_directly_kc_mapping():
    # key --> rule
    # value --> human readable value for kc (unique)

    kcs = {
        'update_factorized_form': "factorized_form_of_quadratic_equation",
        'select_done': "Determine if factoring is complete",
    }
    return kcs


def factorize_directly_intermediate_hints():
    hints = {
        'update_factorized_form': ["The factored form of often looks like "
                                   "\((ax+b)(cx+d)=0\)."],
        'select_done': ["Once you have found the final factored form you can "
                        "select the done button to move to the next problem."]
    }
    return hints

def factorize_directly_studymaterial():
    study_material = studymaterial["quadratic_equations_factorize_directly"]
    return study_material

loaded_models.register(CognitiveModel("quadratic_equations",
                                      "quadratic_equations_factorize_directly",
                                      quadratic_equations_factorize_directly,
                                      quadratic_equations_factorize_directly_problem,
                                      factorize_directly_kc_mapping(),
                                      factorize_directly_intermediate_hints(),
                                      factorize_directly_studymaterial()))