from random import randint, choice

import sympy as sp
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re 

from py_rete import Fact, Production, ReteNetwork, V

from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def logarithms_power_rule_problem():
    b, a = choice([(base, base**power) for power in range(1, 10) for base in range(2, 32) if base**power <= 1024])
    p = randint(0, 20)
    return f"\\log_{{{b}}}{{{a}}}^{{{p}}}"

'''
Generate power rule model
'''
def logarithms_power_rule_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="apply_logarithms_power_rule", disabled=False))
    def apply_logarithms_power_rule(init_value):
        a, p, b = re.findall(r'log\((\d+)\*\*(\d+),\s*(\d+)\)', str(parse_latex(init_value)))[0]
        answer = re.compile(rf"({p}\*log\({a}, {b}\)|log\({a}, {b}\)\*{p})")
        print("ANSWER", answer)
        hint = rf"{p}*\log_{{{b}}}({{{a}}})"
        return [Fact(selection="apply_logarithms_power_rule", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="apply_logarithms_power_rule", value=V('apply_logarithms_power_rule'), disabled=True) &
                Fact(field="solve_logarithms", disabled=False))
    def solve_logarithms(init_value):
        a, p, b = re.findall(r'log\((\d+)\*\*(\d+),\s*(\d+)\)', str(parse_latex(init_value)))[0]
        logba = sp.sympify(rf"log({a}, {b})")
        answer = re.compile(rf"({p}\*{logba}|{logba}\*{p})")
        hint = rf"{p}*{logba}"
        return [Fact(selection="solve_logarithms", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="solve_logarithms", value=V('solve_logarithms'), disabled=True) &
                Fact(field="multiply_values", disabled=False))
    def multiply_values(init_value):
        answer = re.compile(rf"{sp.simplify(parse_latex(init_value))}")
        hint = rf"{sp.simplify(parse_latex(init_value))}"
        return [Fact(selection="multiply_values", action="input change", input=answer, hint=hint)]


    @Production(Fact(field="multiply_values", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    net.add_production(apply_logarithms_power_rule)
    net.add_production(solve_logarithms)
    net.add_production(multiply_values)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    return net


def logarithms_power_rule_kc_mapping():
    kcs = {
        "apply_logarithms_power_rule": "apply_logarithms_power_rule",
        "solve_logarithms": "finding_logarithms_value",
        "multiply_values": "multiply_values",
        "select_done": "Determine if logarithms power problem is complete"
    }
    return kcs


def logarithms_power_rule_intermediate_hints():
    hints = {
        "apply_logarithms_power_rule": ["Use the power rule to shift the exponent to multiplication with the logarithms."],
        "solve_logarithms": ["Solve the logarithms."], 
        "multiply_values": ["Multiply the values"],
    }
    return hints

def logarithms_power_rule_studymaterial():
    study_material = studymaterial["logarithms_power_rule"]
    return study_material

loaded_models.register(CognitiveModel("logarithms",
                                      "logarithms_power_rule",
                                      logarithms_power_rule_model,
                                      logarithms_power_rule_problem,
                                      logarithms_power_rule_kc_mapping(),
                                      logarithms_power_rule_intermediate_hints(),
                                      logarithms_power_rule_studymaterial()))