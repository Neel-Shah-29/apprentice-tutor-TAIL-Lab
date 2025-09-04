from random import randint, choice

import sympy as sp
from sympy import latex, symbols, expand, sstr, Eq, solve
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re 

from py_rete import Fact, Production, ReteNetwork, V

from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def exponential_equations_different_base_problem():
    x = symbols('x')
    base_1 , base_2 = randint(2, 10), randint(2, 10)
    b = randint(-10, 10)
    while sp.Abs(b) <= 1 or base_1==base_2:
        base_1 , base_2 = randint(2, 10), randint(2, 10)
        b = randint(-10, 10)

    
    equation = latex(Eq(base_1**(x+b), base_2**x, evaluate=False)) ## not using a because math-field interprets a*x*log(base_1) as alog(base_1)
    return equation

'''
apply_one_to_one_property
solve_linear_equation
Generate power rule model
'''
def exponential_equations_different_base_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="ln_both_sides", disabled=False))
    def ln_both_sides(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        equation = Eq(sp.log(lhs, sp.E, evaluate=False), sp.ln(rhs, sp.E, evaluate=False), evaluate=False)
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="ln_both_sides", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="ln_both_sides", disabled=True) &
                Fact(field="apply_logarithms_power_rule", disabled=False))
    def apply_logarithms_power_rule(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        lhs = lhs.as_base_exp()[1]*sp.ln(lhs.as_base_exp()[0])
        rhs = rhs.as_base_exp()[1]*sp.ln(rhs.as_base_exp()[0])
        equation = Eq(lhs, rhs, evaluate=False)
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', re.sub(r'log\(([^)]+)\)', r'log(\1, E)', sstr(equation, order="grlex"))))
        hint = latex(equation)
        return [Fact(selection="apply_logarithms_power_rule", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="apply_logarithms_power_rule", disabled=True) &
                Fact(field="distributive_property", disabled=False))
    def distributive_property(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        lhs = lhs.as_base_exp()[1]*sp.ln(lhs.as_base_exp()[0])
        rhs = rhs.as_base_exp()[1]*sp.ln(rhs.as_base_exp()[0])
        equation = Eq(lhs.args[0].args[0]*lhs.args[1] + lhs.args[0].args[1]*lhs.args[1], rhs)
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', re.sub(r'log\(([^)]+)\)', r'log(\1, E)', sstr(equation, order="grlex"))))
        hint = latex(equation)
        return [Fact(selection="distributive_property", action="input change", input=answer, hint=hint)]
    

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="distributive_property", disabled=True) &
                Fact(field="group_for_x", disabled=False))
    def group_for_x(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        lhs = lhs.as_base_exp()[1]*sp.ln(lhs.as_base_exp()[0])
        rhs = rhs.as_base_exp()[1]*sp.ln(rhs.as_base_exp()[0])
        equation = Eq(lhs.args[0].args[0]*(lhs.args[1]-rhs.args[1]), -lhs.args[0].args[1]*lhs.args[1])
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', re.sub(r'log\(([^)]+)\)', r'log(\1, E)', sstr(equation, order="grlex").replace("x*(", "x("))))
        hint = latex(equation)
        return [Fact(selection="group_for_x", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="group_for_x", disabled=True) &
                Fact(field="properties_of_logarithms", disabled=False))
    def properties_of_logarithms(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        lhs = lhs.as_base_exp()[1]*sp.ln(lhs.as_base_exp()[0])
        rhs = rhs.as_base_exp()[1]*sp.ln(rhs.as_base_exp()[0])
        lhs_new = lhs.args[0].args[0]*sp.simplify((lhs.args[1]-rhs.args[1]))
        rhs_new = sp.Abs(lhs.args[0].args[1])*sp.ln(sp.Pow(sp.E**lhs.args[1], sp.sign(-lhs.args[0].args[1])), evaluate=False)
        equation = Eq(lhs_new, rhs_new)
        answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', re.sub(r'log\(([^)]+)\)', r'log(\1, E)', sstr(equation, order="grlex"))))
        hint = latex(equation)
        return [Fact(selection="properties_of_logarithms", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="properties_of_logarithms", disabled=True) &
                Fact(field="solve_for_x", disabled=False))
    def solve_for_x(init_value):
        x = symbols('x')
        lhs, rhs = parse_latex(init_value).lhs, parse_latex(init_value).rhs
        lhs = lhs.as_base_exp()[1]*sp.ln(lhs.as_base_exp()[0])
        rhs = rhs.as_base_exp()[1]*sp.ln(rhs.as_base_exp()[0])
        lhs_new = lhs.args[0].args[0]*sp.simplify((lhs.args[1]-rhs.args[1]))
        rhs_new = sp.Abs(lhs.args[0].args[1])*sp.ln(sp.Pow(sp.E**lhs.args[1], sp.sign(-lhs.args[0].args[1])), evaluate=False)
        equation = latex(Eq(lhs_new, rhs_new))
        equation = parse_latex(equation)
        # print(equation.lhs.args)
        # if equation.lhs.args[1] == x:
        #     solution = f"({equation.rhs.args[0]}*{equation.rhs.args[1]})/{equation.lhs.args[2]}"
        #     answer_1 = re.compile(re.sub(r'([-+^()*])', r'\\\1', solution))
        #     solution = f"{equation.rhs.args[0]}*({equation.rhs.args[1]}/{equation.lhs.args[2]})"
        #     answer_2 = re.compile(re.sub(r'([-+^()*])', r'\\\1', solution))
        #     solution = f"({equation.rhs.args[1]}/{equation.lhs.args[2]})*{equation.rhs.args[0]}"
        #     answer_3 = re.compile(re.sub(r'([-+^()*])', r'\\\1', solution))
        #     hint = latex((equation.rhs.args[0]*equation.rhs.args[1])/equation.lhs.args[2])
        #     return [Fact(selection="solve_for_x", action="input change", input=answer_1, hint=hint),
        #             Fact(selection="solve_for_x", action="input change", input=answer_2, hint=hint),
        #             Fact(selection="solve_for_x", action="input change", input=answer_3, hint=hint)]
        # else:
        solution = f"({equation.rhs.args[0]}*{equation.rhs.args[1]})/{equation.lhs.args[1]}"
        print(solution)
        answer_1 = re.compile(re.sub(r'([-+^()*])', r'\\\1', solution))
        solution = f"{equation.rhs.args[0]}*({equation.rhs.args[1]}/{equation.lhs.args[1]})"
        print(solution)
        answer_2 = re.compile(re.sub(r'([-+^()*])', r'\\\1', solution))
        solution = f"({equation.rhs.args[1]}/{equation.lhs.args[1]})*{equation.rhs.args[0]}"
        print(solution)
        answer_3 = re.compile(re.sub(r'([-+^()*])', r'\\\1', solution))
        hint = latex((equation.rhs.args[0]*equation.rhs.args[1])/equation.lhs.args[1])
        return [Fact(selection="solve_for_x", action="input change", input=answer_1, hint=hint),
                Fact(selection="solve_for_x", action="input change", input=answer_2, hint=hint),
                Fact(selection="solve_for_x", action="input change", input=answer_3, hint=hint)]
        
    @Production(Fact(field="solve_for_x", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    net.add_production(ln_both_sides)
    net.add_production(apply_logarithms_power_rule)
    net.add_production(distributive_property)
    net.add_production(group_for_x)
    net.add_production(properties_of_logarithms)
    net.add_production(solve_for_x)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def exponential_equations_different_base_kc_mapping():
    kcs = {
        "ln_both_sides": "ln_both_sides",
        "apply_logarithms_power_rule": "apply_logarithms_power_rule",
        "distributive_property": "distributive_property",
        "group_for_x": "group_for_x",
        "properties_of_logarithms": "properties_of_logarithms",
        "solve_for_x": "solve_for_x",
        "select_done": "Determine if exponential equation with common base is complete"
    }
    return kcs


def exponential_equations_different_base_intermediate_hints():
    hints = {
        "ln_both_sides": ["Take the natural log of both sides of the equation"],
        "apply_logarithms_power_rule": ["Apply the logarithms power rule"],
        "distribution_property": ["Apply the distributive property"],
        "group_for_x": ["Group the \(x\) terms on one side of the equation"],
        "properties_of_logarithms": ["Apply the properties of logarithms"],
        "apply_one_to_one_property": ["Apply the one-to-one property for exponents"],
        "solve_for_x": ["Find the value of \(x\) without solving the logarithms."],
        "solve_linear_equation": ["Solve the linear equation for \(x\)."], 
    }
    return hints

def exponential_equations_different_base_studymaterial():
    study_material = studymaterial["exponential_equations_different_base"]
    return study_material

loaded_models.register(CognitiveModel("exponential_equations",
                                      "exponential_equations_different_base",
                                      exponential_equations_different_base_model,
                                      exponential_equations_different_base_problem,
                                      exponential_equations_different_base_kc_mapping(),
                                      exponential_equations_different_base_intermediate_hints(),
                                      exponential_equations_different_base_studymaterial()))