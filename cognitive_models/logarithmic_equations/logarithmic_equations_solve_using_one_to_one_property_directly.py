from random import randint, choice

import sympy as sp
from sympy import latex, symbols, expand, sstr, Eq, solve
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re 

from py_rete import Fact, Production, ReteNetwork, V

from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def logarithmic_equations_solve_using_one_to_one_property_directly_problem():
    x = symbols('x')
    x1, x2 = randint(-10, 10), randint(-10, 10)
    while not (x1+x2) or not (x1*x2):
      x1, x2 = randint(-10, 10), randint(-10, 10)
    equation = latex(Eq(sp.ln(x**2),sp.ln(-(x1+x2)*x -(x1*x2)), evaluate=False))
    return equation

def logarithmic_equations_solve_using_one_to_one_property_directly_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="logarithmic_equations_first_root_directly", disabled=False))
    def logarithmic_equations_first_root_directly(init_value):
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
            facts.append(Fact(selection="logarithmic_equations_first_root_directly", action="input change", input=answer, hint=hint))
        return facts
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="logarithmic_equations_first_root_directly", value=V('first_root'), disabled=True) &
                Fact(field="logarithmic_equations_second_root_directly", disabled=False))
    def logarithmic_equations_second_root_directly(init_value, first_root):
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
        return [Fact(selection="logarithmic_equations_second_root_directly", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="logarithmic_equations_first_root_directly", disabled=True) &
                Fact(field="logarithmic_equations_second_root_directly", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    net.add_production(logarithmic_equations_first_root_directly)
    net.add_production(logarithmic_equations_second_root_directly)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def logarithmic_equations_solve_using_one_to_one_property_directly_kc_mapping():
    kcs = {
        "logarithmic_equations_first_root_directly": "logarithmic_equations_first_root_directly",
        "logarithmic_equations_second_root_directly": "logarithmic_equations_second_root_directly",
        "select_done": "Determine if exponential equation with common base is complete"
    }
    return kcs


def logarithmic_equations_solve_using_one_to_one_property_directly_intermediate_hints():
    hints = {
        "logarithmic_equations_first_root_directly": ["Solve the equation for the first root."],
        "logarithmic_equations_second_root_directly": ["Sovle the equation for the second root"],
    }
    return hints

def logarithmic_equations_solve_using_one_to_one_property_directly_studymaterial():
    study_material = studymaterial["logarithmic_equations_solve_using_one_to_one_property_directly"]
    return study_material

loaded_models.register(CognitiveModel("logarithmic_equations",
                                      "logarithmic_equations_solve_using_one_to_one_property_directly",
                                      logarithmic_equations_solve_using_one_to_one_property_directly_model,
                                      logarithmic_equations_solve_using_one_to_one_property_directly_problem,
                                      logarithmic_equations_solve_using_one_to_one_property_directly_kc_mapping(),
                                      logarithmic_equations_solve_using_one_to_one_property_directly_intermediate_hints(),
                                      logarithmic_equations_solve_using_one_to_one_property_directly_studymaterial()))