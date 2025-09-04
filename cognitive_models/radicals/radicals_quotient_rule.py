from functools import reduce
from random import randint
# from random import random
from random import choice
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

def generate_prime(x,y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False

        if isPrime:
            prime_list.append(n)

    prime_choice = choice(prime_list)
           
    return prime_choice


def radical_quotient_rule_problem():
    # need to roduct two fractions that can be simplified 
    numerator = generate_prime(1,50)
    denominator = (randint(2,20)) ** 2
    
    return "\sqrt{\\frac{" + str(numerator) + "}" + "{" + str(denominator) + "}"

'''
Generate quotient rule model
'''
def radical_quotient_rule_model():
    net = ReteNetwork()

    # compute radical quotient
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="combined_value", disabled=False))
    def update_quotient_value(init_value):
        split_value = init_value.split("{", 3)
        numerator = split_value[2].replace("}","")
        demonimator = split_value[3].replace("}","")
        answer = '\\frac{\sqrt{' + str(numerator) + '}}{\sqrt{' + str(demonimator) + '}}'
        return [Fact(selection="combined_value", action="input change", input=answer)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="combined_value", value=V('quotient'), disabled=True) &
                Fact(field="simplify_fraction", disabled=False))
    def simplify_quotient_value(quotient):
        quotient = quotient.split("{", 4)
        numerator = quotient[2].replace("}","")
        denominator = quotient[4].replace("}","")
        sqrt_denominator = int(math.sqrt(int(denominator)))
        answer = '\\frac{\sqrt{' + str(numerator) + '}}{' + str(sqrt_denominator) + '}'
        print(answer)
        return [Fact(selection="simplify_fraction", action="input change", input=answer)]

    @Production(Fact(field="simplify_fraction", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input="")]

    net.add_production(update_quotient_value)
    net.add_production(simplify_quotient_value)
    net.add_production(select_done)

    return net


def radical_quotient_rule_kc_mapping():
    kcs = {
        "update_quotient_value": "Apply radical quotient rule",
        "simplify_quotient_value": "Compute square root",
        "select_done": "Determine if radical quotient problem is complete"
    }
    return kcs


def radical_quotient_rule_intermediate_hints():
    hints = {
        "update_quotient_value": [
            "The quotient can by found by multiplying the numbers under both square roots."],
        "simplify_quotient_value": [
            "Simplify the square root."
        ]
    }
    return hints

def radicals_quotient_rule_studymaterial():
    study_material = studymaterial["radicals_quotient_rule"]
    return study_material

loaded_models.register(CognitiveModel("radicals", 
                                      "radicals_quotient_rule",
                                      radical_quotient_rule_model,
                                      radical_quotient_rule_problem,
                                      radical_quotient_rule_kc_mapping(),
                                      radical_quotient_rule_intermediate_hints(),
                                      radicals_quotient_rule_studymaterial()))