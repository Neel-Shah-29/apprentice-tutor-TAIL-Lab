from random import randint, choice

import sympy as sp
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re 

from py_rete import Fact, Production, ReteNetwork, V

from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def logarithms_quotient_rule_problem():
    b, a = choice([(base, base**power) for power in range(1, 10) for base in range(2, 32) if base**power <= 1024])
    factor_pairs = [(a*num, num) for num in range(1, int(a**0.5)+1) if a*num <= 1024]
    m, n = choice(factor_pairs[1:]) if (len(factor_pairs)>1) else factor_pairs[0] 
    return f"\\log_{{{b}}}{{{m}}} - \\log_{{{b}}}{{{n}}}"
    

'''
Generate product rule model
'''
def logarithms_quotient_rule_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="apply_logarithms_quotient_rule", disabled=False))
    def apply_logarithms_quotient_rule(init_value):
        (n,b), (m, b)= re.findall(r'log\((\d+),\s*(\d+)\)', str(parse_latex(init_value)))
        print("check", m, n, str(parse_latex(init_value)))
        answer = re.compile(rf"log\({m}/{n}, {b}\)")
        hint = rf"\log_{{{b}}}({m}/{n})"
        return [Fact(selection="apply_logarithms_quotient_rule", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="apply_logarithms_quotient_rule", value=V('apply_logarithms_quotient_rule'), disabled=True) &
                Fact(field="divide_values", disabled=False))
    def divide_values(init_value):
        (n,b), (m, b)= re.findall(r'log\((\d+),\s*(\d+)\)', str(parse_latex(init_value)))
        answer = re.compile(rf"log\({int(m)//int(n)}, {b}\)")
        hint = rf"\log_{{{b}}}({int(m)//int(n)})"
        return [Fact(selection="divide_values", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="divide_values", value=V('divide_values'), disabled=True) &
                Fact(field="solve_logarithms", disabled=False))
    def solve_logarithms(init_value):
        answer = re.compile(rf"{sp.simplify(parse_latex(init_value))}")
        hint = rf"{sp.simplify(parse_latex(init_value))}"
        return [Fact(selection="solve_logarithms", action="input change", input=answer, hint=hint)]


    @Production(Fact(field="solve_logarithms", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    net.add_production(apply_logarithms_quotient_rule)
    net.add_production(divide_values)
    net.add_production(solve_logarithms)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    
    return net


def logarithms_quotient_rule_kc_mapping():
    kcs = {
        "apply_logarithms_quotient_rule": "apply_logarithms_quotient_rule",
        "divide_values": "divide_values",
        "solve_logarithms": "finding_logarithms_value",
        "select_done": "Determine if logarithms quotient problem is complete"
    }
    return kcs


def logarithms_quotient_rule_intermediate_hints():
    hints = {
        "apply_logarithms_quotient_rule": ["Use the quotient rule to reduce logarithms with the same base."],
        "divide_values": ["Divide the numbers inside the logarithms."],
        "solve_logarithms": ["Solve the logarithms expression."]
    }
    return hints

def logarithms_quotient_rule_studymaterial():
    study_material = studymaterial["logarithms_quotient_rule"]
    return study_material

loaded_models.register(CognitiveModel("logarithms",
                                      "logarithms_quotient_rule",
                                      logarithms_quotient_rule_model,
                                      logarithms_quotient_rule_problem,
                                      logarithms_quotient_rule_kc_mapping(),
                                      logarithms_quotient_rule_intermediate_hints(),
                                      logarithms_quotient_rule_studymaterial()))