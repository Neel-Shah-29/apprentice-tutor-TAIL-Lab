from random import randint, choice

import sympy as sp
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re 

from py_rete import Fact, Production, ReteNetwork, V

from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def logarithms_product_rule_problem():
    b, a = choice([(base, base**power) for power in range(1, 10) for base in range(2, 32) if base**power <= 1024])
    m, n = choice([(num, a//num) for num in range(1, int(a**0.5)+1) if a%num==0])
    return f"\\log_{{{b}}}{{{m}}} + \\log_{{{b}}}{{{n}}}"
    

'''
Generate product rule model
'''
def logarithms_product_rule_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="apply_logarithms_product_rule", disabled=False))
    def apply_logarithms_product_rule(init_value):
        (m,b), (n, b)= re.findall(r'log\((\d+),\s*(\d+)\)', str(parse_latex(init_value)))
        answer = re.compile(rf'log\(({m}\*{n}|{n}\*{m}), {b}\)')
        hint = rf"\log_{{{b}}}({m}*{n})"
        return [Fact(selection="apply_logarithms_product_rule", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="apply_logarithms_product_rule", value=V('apply_logarithms_product_rule'), disabled=True) &
                Fact(field="multiply_values", disabled=False))
    def multiply_values(init_value):
        (m,b), (n, b)= re.findall(r'log\((\d+),\s*(\d+)\)', str(parse_latex(init_value)))
        answer = re.compile(rf"log\({int(m)*int(n)}, {b}\)")
        hint = rf"\log_{{{b}}}({int(m)*int(n)})"
        return [Fact(selection="multiply_values", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="multiply_values", value=V('multiply_values'), disabled=True) &
                Fact(field="solve_logarithms", disabled=False))
    def solve_logarithms(init_value):
        answer = re.compile(rf"{sp.simplify(parse_latex(init_value))}")
        hint = rf"{sp.simplify(parse_latex(init_value))}"
        return [Fact(selection="solve_logarithms", action="input change", input=answer, hint=hint)]


    @Production(Fact(field="solve_logarithms", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    net.add_production(apply_logarithms_product_rule)
    net.add_production(multiply_values)
    net.add_production(solve_logarithms)
    net.add_production(select_done)

    sp.core.cache.clear_cache()
    
    return net


def logarithms_product_rule_kc_mapping():
    kcs = {
        "apply_logarithms_product_rule": "apply_logarithms_product_rule",
        "multiply_values": "multiply_values",
        "solve_logarithms": "finding_logarithms_value",
        "select_done": "Determine if logarithms product problem is complete"
    }
    return kcs


def logarithms_product_rule_intermediate_hints():
    hints = {
        "apply_logarithms_product_rule": ["Use the product rule to reduce logarithms with the same base."],
        "multiply_values": ["Multipy the numbers inside the logarithms."],
        "solve_logarithms": ["Solve the logarithms expression."]
    }
    return hints

def logarithms_product_rule_studymaterial():
    study_material = studymaterial["logarithms_product_rule"]
    return study_material

loaded_models.register(CognitiveModel("logarithms",
                                      "logarithms_product_rule",
                                      logarithms_product_rule_model,
                                      logarithms_product_rule_problem,
                                      logarithms_product_rule_kc_mapping(),
                                      logarithms_product_rule_intermediate_hints(),
                                      logarithms_product_rule_studymaterial()))