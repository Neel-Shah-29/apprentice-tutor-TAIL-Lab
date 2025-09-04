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

def exponent_product_rule_problem():
    constant = randint(2,1000)
    exponent_1 = randint(1,20)
    exponent_2 = randint(1,20)
    return str(constant) + "^" + "{" + str(exponent_1) + "}" + "\cdot" + str(constant) + "^" + "{" + str(exponent_2) + "}"

'''
Generate product rule model
'''
def exponent_product_rule_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="adding_values", disabled=False))
    def adding_values(init_value):
        # Need to parse: 10^{4}\cdot10^{2}
        product_left = init_value.split('\cdot')[0]
        base = product_left.split('^')[0]
        exponent_1 = product_left.split('^')[1].replace("{","").replace("}","")

        product_right = init_value.split('\cdot')[1]
        exponent_2 = product_right.split('^')[1].replace("{","").replace("}","")

        answer4 = str(base) + "^" + "{" + str(exponent_1) + "+" + str(exponent_2) +  "}"
        answer2 = str(base) + "^" + "{" + str(exponent_2) + "+" + str(exponent_1) +  "}"
        answer3 = str(base) + "^" + "{\left(" + str(exponent_2) + "+" + str(exponent_1) +  "\\right)}"
        answer1 = str(base) + "^" + "{\left(" + str(exponent_1) + "+" + str(exponent_2) +  "\\right)}"
        answer5 = "{}^{{{}+{}}}".format(base, exponent_1, exponent_2)
        return [Fact(selection="adding_values", action="input change", input=answer5),
                Fact(selection="adding_values", action="input change", input=answer1),
                Fact(selection="adding_values", action="input change", input=answer2),
                Fact(selection="adding_values", action="input change", input=answer3),
                Fact(selection="adding_values", action="input change", input=answer4)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="adding_values", value=V('adding_values'), disabled=True) &
                Fact(field="simplify_expression", disabled=False))
    def simplify_expression(init_value):
         # Need to parse: 10^{4}\cdot10^{2}
        product_left = init_value.split('\cdot')[0]
        base = product_left.split('^')[0]
        exponent_1 = product_left.split('^')[1].replace("{","").replace("}","")

        product_right = init_value.split('\cdot')[1]
        exponent_2 = product_right.split('^')[1].replace("{","").replace("}","")

        final_exponent = int(exponent_1) + int(exponent_2)

        answer1 = str(base) + "^" + "{\left(" + str(final_exponent) +  "\\right)}"  
        answer2 = str(base) + "^" + str(final_exponent)
        answer3 = str(base) + "^" + "{" + str(final_exponent) +  "}"
        answer4 = "{}^{{{}}}".format(base, final_exponent)
        return [Fact(selection="simplify_expression", action="input change", input=answer4),
                Fact(selection="simplify_expression", action="input change", input=answer1),
                Fact(selection="simplify_expression", action="input change", input=answer2),
                Fact(selection="simplify_expression", action="input change", input=answer3)]

    @Production(Fact(field="simplify_expression", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input="")]

    net.add_production(adding_values)
    net.add_production(simplify_expression)
    net.add_production(select_done)

    return net


def exponent_product_rule_kc_mapping():
    kcs = {
        "adding_values": "Apply exponent product rule",
        "simplify_expression": "Adding exponents with the same base",
        "select_done": "Determine if exponent product problem is complete"
    }
    return kcs


def exponent_product_rule_intermediate_hints():
    hints = {
        "adding_values": [
            "Use the product rule to add the exponents with the same base."],
        "simplify_expression": [
            "Add the exponents."
        ]
    }
    return hints

def exponent_product_rule_studymaterial():
    study_material = studymaterial["exponents_power_rule"]
    return study_material

loaded_models.register(CognitiveModel("exponents",
                                      "exponents_product_rule",
                                      exponent_product_rule_model,
                                      exponent_product_rule_problem,
                                      exponent_product_rule_kc_mapping(),
                                      exponent_product_rule_intermediate_hints(),
                                      exponent_product_rule_studymaterial()))