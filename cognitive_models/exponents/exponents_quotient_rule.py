from functools import reduce
from random import randint
# import random

from pprint import pprint
import math

from py_rete import Fact
from py_rete import Production
from py_rete import ReteNetwork
from py_rete import V
from py_rete import Filter

from models import KnowledgeComponent

# from cognitive_models.base import check_sai
# from cognitive_models.base import get_hint
from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def exponent_quotient_rule_problem():
    constant = randint(2,1000)
    exponent_1 = randint(10,20)
    exponent_2 = randint(2,9)

    return "\\frac{" + str(constant) + "^" + "{" + str(exponent_1) + "}" + "}" + "{" + str(constant) + "^" + "{" + str(exponent_2) + "}" + "}"
    

'''
Generate product rule model
'''
def exponent_quotient_rule_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="subtract_values", disabled=False))
    def subtract_values(init_value):
        # Need to parse: \frac{4^{2}}{4^{1}}
        base = init_value.split('^')[0].replace("\\frac{","")
        exponent_1 = init_value.split('^')[1].replace("}","").split("{",2)[1]
        exponent_2 = init_value.split("^",2)[2].replace("{","").replace("}","")

        answer3 =  str(base) + "^" + "{(" + str(exponent_1) + "-" + str(exponent_2)  + ")}" 
        answer2 =  str(base) + "^" + "{" + str(exponent_1) + "-" + str(exponent_2)  + "}"
        answer1 =  str(base) + "^" + "{\left(" + str(exponent_1) + "-" + str(exponent_2)  + "\\right)}"
        answer4 = "{}^{{{}-{}}}".format(base, exponent_1, exponent_2)
        return [Fact(selection="subtract_values", action="input change", input=answer4),
        Fact(selection="subtract_values", action="input change", input=answer1),
        Fact(selection="subtract_values", action="input change", input=answer2),
        Fact(selection="subtract_values", action="input change", input=answer3)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="subtract_values", value=V('subtract_values'), disabled=True) &
                Fact(field="simplify_expression", disabled=False))
    def simplify_expression(init_value):
        base = init_value.split('^')[0].replace("\\frac{","")
        exponent_1 = init_value.split('^')[1].replace("}","").split("{",2)[1]
        exponent_2 = init_value.split("^",2)[2].replace("{","").replace("}","")

        final_exponent = int(int(exponent_1) - int(exponent_2))
        answer1 = str(base) + "^" + "{\left{" + str(final_exponent) + "\\right}}"
        answer2 =  str(base) + "^" + "{" + str(final_exponent) + "}"
        answer3 =  str(base) + "^" + "{(" + str(final_exponent) + ")}"
        answer4 =  str(base) + "^" + str(final_exponent)
        answer5 = str(base) + "^" + "{\left(" + str(final_exponent) + "\\right)}"
        answer6 = "{}^{{{}}}".format(base, final_exponent)
        return [Fact(selection="simplify_expression", action="input change", input=answer6),
        Fact(selection="simplify_expression", action="input change", input=answer1),
        Fact(selection="simplify_expression", action="input change", input=answer2),
        Fact(selection="simplify_expression", action="input change", input=answer3),
        Fact(selection="simplify_expression", action="input change", input=answer4),
        Fact(selection="simplify_expression", action="input change", input=answer5)]

    @Production(Fact(field="simplify_expression", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input="")]

    net.add_production(subtract_values)
    net.add_production(simplify_expression)
    net.add_production(select_done)

    return net


def exponent_quotient_rule_kc_mapping():
    kcs = {
        "subtract_values": "Apply exponent quotient rule",
        "simplify_expression": "Subtract exponents with the same base",
        "select_done": "Determine if exponent power problem is complete"
    }
    return kcs


def exponent_quotient_rule_intermediate_hints():
    hints = {
        "subtract_values": [
            "Use the quotient rule to subtract the exponents with the same base."],
        "simplify_expression": [
            "Subtract the exponents."
        ]
    }
    return hints

def exponent_quotient_rule_studymaterial():
    study_material = studymaterial["exponents_quotient_rule"]
    return study_material

loaded_models.register(CognitiveModel("exponents",
                                      "exponents_quotient_rule",
                                      exponent_quotient_rule_model,
                                      exponent_quotient_rule_problem,
                                      exponent_quotient_rule_kc_mapping(),
                                      exponent_quotient_rule_intermediate_hints(),
                                      exponent_quotient_rule_studymaterial()))