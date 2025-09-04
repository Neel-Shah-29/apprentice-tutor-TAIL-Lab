from functools import reduce
from random import randint
# import random

from pprint import pprint
import math
from tokenize import ContStr

from py_rete import Fact
from py_rete import Production
from py_rete import ReteNetwork
from py_rete import V
from py_rete import Filter

from models import KnowledgeComponent

from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def exponent_power_rule_problem():
    constant = randint(2,1000)
    exponent_1 = randint(2,12)
    exponent_2 = randint(2,12)
    return  "(" + str(constant) + "^" + "{" + str(exponent_1) + "})"+ "^" + "{" + str(exponent_2) + "}"

'''
Generate product rule model
'''
def exponent_power_rule_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="multiply_values", disabled=False))
    def multiply_values(init_value):
        # Need to parse: 6^{3^{8}}
        base = init_value.split('^')[0][1:]
        exponent_1 = init_value.split('^')[1][1:-2]
        exponent_2 = init_value.split('^')[2][1:-1]
        # base = init_value.split('^')[0]
        # exponent_1 = init_value.split('^')[1].split('^')[0].replace("{","")
        # exponent_2 = init_value.split('^')[2].replace("{","").replace("}","")
        
        answer_7 = str(base) + "^{" + str(exponent_1) + "\cdot" + str(exponent_2) + "}"
        answer_2 = str(base) + "^{" + str(exponent_2) + "\cdot" + str(exponent_1) + "}"
        answer_3 = str(base) + "^{" + str(exponent_1) + "\\times" + str(exponent_2) + "}"
        answer_4 = str(base) + "^{" + str(exponent_2) + "\\times" + str(exponent_1) + "}"
        answer_5 = str(base) + "^{" + "(" + str(exponent_1) + ")"+ "(" +str(exponent_2) + ")" + "}"
        answer_6 = str(base) + "^{" + "(" + str(exponent_2) + ")"+ "(" +str(exponent_1) + ")" + "}"
        answer_1 = str(base) + "^{\left{" + str(exponent_1) + "\cdot" + str(exponent_2) + "\\right}}"
        answer_8 = str(base) + "^{\left{" + str(exponent_2) + "\cdot" + str(exponent_1) + "\\right}}"
        answer_9 = str(base) + "^{\left(" + str(exponent_1) + "\cdot" + str(exponent_2) + "\\right)}"
        answer_10 = str(base) + "^{\left(" + str(exponent_2) + "\cdot" + str(exponent_1) + "\\right)}"
        answer_11 = "{}^{{{}.{}}}".format(base, exponent_1, exponent_2)
       
        return [Fact(selection="multiply_values", action="input change", input=answer_11),
                Fact(selection="multiply_values", action="input change", input=answer_1),
                Fact(selection="multiply_values", action="input change", input=answer_2),
                Fact(selection="multiply_values", action="input change", input=answer_3),
                Fact(selection="multiply_values", action="input change", input=answer_4),
                Fact(selection="multiply_values", action="input change", input=answer_5),
                Fact(selection="multiply_values", action="input change", input=answer_6),
                Fact(selection="multiply_values", action="input change", input=answer_7),
                Fact(selection="multiply_values", action="input change", input=answer_8),
                Fact(selection="multiply_values", action="input change", input=answer_9),
                Fact(selection="multiply_values", action="input change", input=answer_10)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="multiply_values", value=V('multiply_values'), disabled=True) &
                Fact(field="simplify_expression", disabled=False))
    def simplify_expression(init_value):
        base = init_value.split('^')[0][1:]
        exponent_1 = init_value.split('^')[1][1:-2]
        exponent_2 = init_value.split('^')[2][1:-1]
        # base = init_value.split('^')[0]
        # exponent_1 = init_value.split('^')[1].split('^')[0].replace("{","")
        # exponent_2 = init_value.split('^')[2].replace("{","").replace("}","")

        final_exponent = int(int(exponent_1) * int(exponent_2))
        
        answer1 = str(base) + "^{\left(" + str(final_exponent) + "\\right)}"
        answer2 = str(base) + "^{" + str(final_exponent) + "}"
        answer3 = str(base) + "^{(" + str(final_exponent) + ")}"
        answer4 = str(base) + "^" + str(final_exponent)
        answer5 = "{}^{{{}}}".format(base, final_exponent)
       
        return [Fact(selection="simplify_expression", action="input change", input=answer5),
        Fact(selection="simplify_expression", action="input change", input=answer1),
        Fact(selection="simplify_expression", action="input change", input=answer2),
        Fact(selection="simplify_expression", action="input change", input=answer3),
        Fact(selection="simplify_expression", action="input change", input=answer4)]

    @Production(Fact(field="simplify_expression", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input="")]

    net.add_production(multiply_values)
    net.add_production(simplify_expression)
    net.add_production(select_done)

    return net


def exponent_power_rule_kc_mapping():
    kcs = {
        "multiply_values": "Apply exponent power rule",
        "simplify_expression": "Multiply exponents with the same base",
        "select_done": "Determine if exponent power problem is complete"
    }
    return kcs


def exponent_power_rule_intermediate_hints():
    hints = {
        "multiply_values": [
            "Use the power rule to multiply the exponents with the same base."],
        "simplify_expression": [
            "Multiply the exponents."
        ]
    }
    return hints

def exponent_power_rule_studymaterial():
    study_material = studymaterial["exponents_power_rule"]
    return study_material

loaded_models.register(CognitiveModel("exponents",
                                      "exponents_power_rule",
                                      exponent_power_rule_model,
                                      exponent_power_rule_problem,
                                      exponent_power_rule_kc_mapping(),
                                      exponent_power_rule_intermediate_hints(),
                                      exponent_power_rule_studymaterial()))