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
from itertools import permutations


# from cognitive_models.base import check_sai
# from cognitive_models.base import get_hint
from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def find_factors(x):
    factors = []
    for i in range(1, x + 1):
       if x % i == 0:
           factors.append(i)
    return factors


def radical_product_rule_problem():
    perfect_square = (randint(1,9)) ** 2
    factors_of_perfect_square = find_factors(perfect_square)
    random_factor_1 = choice(factors_of_perfect_square)
    random_factor_2 = int(perfect_square / random_factor_1)
    return "\sqrt{" + str(random_factor_1) + "}\cdot \sqrt{" + str(random_factor_2) + "}"


def radical_product_rule_model():
    """
    Generate product rule model
    """
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="product_rule", disabled=False))
    ## Momin check here
    def apply_product_rule(init_value):
        product_left = init_value.split('\cdot')[0]
        product_right = init_value.split('\cdot')[1]

        if 'sqrt' in product_left:
            left_int = int(product_left.replace("\sqrt{", "").replace("}", ""))
            right_int = int(product_right.replace("\sqrt{", "").replace("}", ""))

            answer1 = "\sqrt{" + "(" + str(left_int) + ")" + "(" + str(right_int) + ")" + "}"
            answer2 = "\sqrt{" + "(" + str(right_int) + ")" + "(" + str(left_int) + ")" + "}"

            answers = [
                Fact(selection="product_rule", action="input change", input=answer1),
                Fact(selection="product_rule", action="input change", input=answer2)
            ]

            values = [str(left_int), str(right_int)]
        
            for order in permutations(values):
                cdot_answer =  "\sqrt{" + "\cdot".join(order) + "}" 
                answers.append(Fact(selection="product_rule", action="input change", input=cdot_answer))
                
                times_answer = "\sqrt{" + "\\times".join(order) + "}" 
                answers.append(Fact(selection="product_rule", action="input change", input=times_answer))

            for answer in answers:
                print(answer)
            
            return answers

        else:
            pass


    @Production(Fact(field="initial_problem", value=V('init_value'), disabled=True) &
                Fact(field="product_value", disabled=False))
    def update_product_value(init_value):
        product_left = init_value.split('\cdot')[0].replace("\sqrt{", "").replace("}", "")
        product_right = init_value.split('\cdot')[1].replace("\sqrt{", "").replace("}", "")

        product = int(product_left) * int(product_right)
        
        return [Fact(selection="product_value", action="input change",
                     input="\sqrt{{{}}}".format(product))]

    @Production(Fact(field="product_value", value=V('product'),
                     disabled=True) &
                Fact(field="product_simplify_value", disabled=False))
    def simplify_product_value(product):
        sqrt = int(math.sqrt(int(product.replace("\sqrt{", "").replace("}", "").replace("\sqrt", ""))))
        return [Fact(selection="product_simplify_value", action="input change",
                     input="{}".format(sqrt))]

    @Production(Fact(field="product_simplify_value", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click",
                     input="")]

    net.add_production(apply_product_rule)
    net.add_production(update_product_value)
    net.add_production(simplify_product_value)
    net.add_production(select_done)

    return net


def radical_product_rule_kc_mapping():
    kcs = {
        "apply_product_rule": "Apply product rule to combine square roots",
        "update_product_value": "Multiply two values",
        "simplify_product_value": "Compute square root",
        "select_done": "Determine if square root product problem is complete"
        # "final_answer": "Final product answer"
    }
    return kcs


def radical_product_rule_intermediate_hints():
    hints = {
        "apply_product_rule": ["Since both terms are square roots, you can move the multiplication so it occurs within a single square root."],
        "update_product_value": ["Multiplying the numbers under the square root."],
        "simplify_product_value": ["Simplify the square root."]
    }
    return hints


def radicals_product_rule_studymaterial():
    study_material = studymaterial["radicals_product_rule"]
    return study_material

loaded_models.register(CognitiveModel("radicals", 
                                      "radicals_product_rule",
                                      radical_product_rule_model,
                                      radical_product_rule_problem,
                                      radical_product_rule_kc_mapping(),
                                      radical_product_rule_intermediate_hints(),
                                      radicals_product_rule_studymaterial()))
