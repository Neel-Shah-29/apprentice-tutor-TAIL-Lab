from random import randint, choice

import sympy as sp
from sympy import latex, symbols, expand, sstr, Eq, solve
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re 

from py_rete import Fact, Production, ReteNetwork, V

from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def exponential_equations_solve_directly_problem():
    x = symbols('x')
    base_1 , base_2 = randint(2, 10), randint(2, 10)
    b = randint(-10, 10)
    while  sp.Abs(b) <=1 or base_1==base_2:
        base_1 , base_2 = randint(2, 10), randint(2, 10)
        b = randint(-10, 10)

    
    equation = latex(Eq(base_1**(x+b), base_2**x, evaluate=False)) ## not using a because math-field interprets a*x*log(base_1) as alog(base_1)
    return equation


def exponential_equations_solve_directly_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="exponential_equations_solve_directly", disabled=False))
    def exponential_equations_solve_directly(init_value):
        x = symbols('x')
        equation = parse_latex(init_value)
        lhs = equation.lhs.as_base_exp()[1]*sp.ln(equation.lhs.as_base_exp()[0])
        rhs = equation.rhs.as_base_exp()[1]*sp.ln(equation.rhs.as_base_exp()[0])
        equation = Eq(lhs, rhs, evaluate=False)
        lhs = equation.lhs.args[0].args[0]*sp.simplify((equation.lhs.args[1]-equation.rhs.args[1]))
        rhs = sp.Abs(equation.lhs.args[0].args[1])*sp.ln(sp.Pow(sp.E**equation.lhs.args[1], sp.sign(-equation.lhs.args[0].args[1])), evaluate=False)

        solution = f"({rhs.args[0]}*{rhs.args[1]})/{lhs.args[1]}"
        answer_1 = re.compile(re.sub(r'([-+^()*])', r'\\\1', re.sub(r'log\(([^)]+)\)', r'log(\1, E)',solution)))
        solution = f"{rhs.args[0]}*({rhs.args[1]}/{lhs.args[1]})"
        answer_2 = re.compile(re.sub(r'([-+^()*])', r'\\\1', re.sub(r'log\(([^)]+)\)', r'log(\1, E)',solution)))
        solution = f"({rhs.args[1]}/{lhs.args[1]})*{rhs.args[0]}"
        answer_3 = re.compile(re.sub(r'([-+^()*])', r'\\\1', re.sub(r'log\(([^)]+)\)', r'log(\1, E)',solution)))
        hint = latex((rhs.args[0]*rhs.args[1])/lhs.args[1])
        return [Fact(selection="exponential_equations_solve_directly", action="input change", input=answer_1, hint=hint),
                Fact(selection="exponential_equations_solve_directly", action="input change", input=answer_2, hint=hint),
                Fact(selection="exponential_equations_solve_directly", action="input change", input=answer_3, hint=hint)]
        
    @Production(Fact(field="exponential_equations_solve_directly", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    net.add_production(exponential_equations_solve_directly)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def exponential_equations_solve_directly_kc_mapping():
    kcs = {
        "exponential_equations_solve_directly": "exponential_equations_solve_directly",
        "select_done": "Determine if exponential equation with common base is complete"
    }
    return kcs


def exponential_equations_solve_directly_intermediate_hints():
    hints = {
        "exponential_equations_solve_directly": ["Find the value of \(x\) without solving the logarithms."],
        "solve_linear_equation": ["Solve the linear equation for \(x\)."], 
    }
    return hints

def exponential_equations_solve_directly_studymaterial():
    study_material = studymaterial["exponential_equations_solve_directly"]
    return study_material

loaded_models.register(CognitiveModel("exponential_equations",
                                      "exponential_equations_solve_directly",
                                      exponential_equations_solve_directly_model,
                                      exponential_equations_solve_directly_problem,
                                      exponential_equations_solve_directly_kc_mapping(),
                                      exponential_equations_solve_directly_intermediate_hints(),
                                      exponential_equations_solve_directly_studymaterial()))