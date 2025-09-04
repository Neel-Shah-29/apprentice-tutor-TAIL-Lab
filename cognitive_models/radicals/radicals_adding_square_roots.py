from functools import reduce
from random import randint
# from random import random
from random import choice
# import random
from itertools import permutations

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


def radical_adding_sqrt_problem():
    coefficient_1 = generate_prime(2,10)
    radicand_1_a =  generate_prime(2,10)
    radicand_1_b = (randint(2,6))** 2
    coefficient_2 = generate_prime(2,10)
    return str(coefficient_1) + "\sqrt{" + str(radicand_1_a * radicand_1_b) + "}" + "+" + str(coefficient_2) + "\sqrt{" + str(radicand_1_a) + "}"

'''
Generate adding square roots rule model
'''
def radical_adding_sqrt_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="factor_radicand", disabled=False))
    def factor_radicand(init_value):
        left_side = init_value.split("+")[0]
        left_constant = left_side.split("\sqrt{")[0]
        left_radicand = left_side.split("\sqrt{")[1].replace("}", "")
    
        right_side = init_value.split("+")[1]
        right_constant = right_side.split("\sqrt{")[0]
        right_radicand = right_side.split("\sqrt{")[1].replace("}", "")

        # divide left radicand by right radicand 
        other_radicand =  int(int(left_radicand) / int(right_radicand))

        answer1 = str(left_constant) + "\sqrt{" + str(right_radicand) + "\\times" +  str(other_radicand) + "}" + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer2 = str(left_constant) + "\sqrt{" + str(other_radicand) + "\\times" +  str(right_radicand) + "}" + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer3 = str(left_constant) + "\sqrt{" + str(right_radicand) + "\cdot" +  str(other_radicand) + "}" + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer4 = str(left_constant) + "\sqrt{" + str(other_radicand) + "\cdot" +  str(right_radicand) + "}" + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        
        answer5 = str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" +  str(left_constant) + "\sqrt{" + str(right_radicand) + "\\times" +  str(other_radicand) + "}" 
        answer6 = str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + str(left_constant) + "\sqrt{" + str(other_radicand) + "\\times" +  str(right_radicand) + "}"
        answer7 = str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" +  str(left_constant) + "\sqrt{" + str(right_radicand) + "\cdot" +  str(other_radicand) + "}"
        answer8 = str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + str(left_constant) + "\sqrt{" + str(other_radicand) + "\cdot" +  str(right_radicand) + "}"

        # print(answer1)
        # print(answer2)
        # print(answer3)
        # print(answer4)

        # TODO: Multuple answers can have cdot or x between
        return [Fact(selection="factor_radicand", action="input change", input=answer1), 
                Fact(selection="factor_radicand", action="input change", input=answer2),
                Fact(selection="factor_radicand", action="input change", input=answer3),
                Fact(selection="factor_radicand", action="input change", input=answer4),
                Fact(selection="factor_radicand", action="input change", input=answer5),
                Fact(selection="factor_radicand", action="input change", input=answer6),
                Fact(selection="factor_radicand", action="input change", input=answer7),
                Fact(selection="factor_radicand", action="input change", input=answer8)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="factor_radicand", disabled=True ) &
                Fact(field="product_rule", disabled=False))
    def product_rule(init_value):
        left_side = init_value.split("+")[0]
        left_constant = left_side.split("\sqrt{")[0]
        left_radicand = left_side.split("\sqrt{")[1].replace("}", "")
    
        right_side = init_value.split("+")[1]
        right_constant = right_side.split("\sqrt{")[0]
        right_radicand = right_side.split("\sqrt{")[1].replace("}", "")

        # divide left radicand by right radicand 
        other_radicand =  int(int(left_radicand) / int(right_radicand))

        answer1 = str(left_constant) + "\sqrt{" + str(right_radicand) + "}" + "\sqrt{" + str(other_radicand)  + "}" + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer2 = str(left_constant) + "\sqrt{" + str(other_radicand) + "}" + "\sqrt{" + str(right_radicand)  + "}" + "+" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer3 = str(left_constant) + "\cdot" + "\sqrt{" + str(other_radicand) + "}" + "\cdot" + "\sqrt{" + str(right_radicand)  + "}" + "+" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer4 = str(left_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "\cdot" + "\sqrt{" + str(other_radicand)  + "}" + "+" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer5 = str(left_constant) + "\\times" + "\sqrt{" + str(other_radicand) + "}" + "\\times" "\sqrt{" + str(right_radicand)  + "}" + "+" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer6 = str(left_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}" + "\\times" "\sqrt{" + str(other_radicand)  + "}" + "+" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}"

        # print(answer1)
        # print(answer2)
        # print(answer3)
        # print(answer4)
        # print(answer5)
        # print(answer6)
        
        return [Fact(selection="product_rule", action="input change", input=answer1), 
                Fact(selection="product_rule", action="input change", input=answer2),
                Fact(selection="product_rule", action="input change", input=answer3),
                Fact(selection="product_rule", action="input change", input=answer4),
                Fact(selection="product_rule", action="input change", input=answer5),
                Fact(selection="product_rule", action="input change", input=answer6)]



    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="product_rule", value=V('product_rule'), disabled=True) &
                Fact(field="solve_square_root", disabled=False))
    def solve_square_root(init_value, product_rule):
        left_side = init_value.split("+")[0]
        left_constant = left_side.split("\sqrt{")[0]
        left_radicand = left_side.split("\sqrt{")[1].replace("}", "")
    
        right_side = init_value.split("+")[1]
        right_constant = right_side.split("\sqrt{")[0]
        right_radicand = right_side.split("\sqrt{")[1].replace("}", "")

        # divide left radicand by right radicand 
        sqrt_other_radicand =  int(math.sqrt(int(left_radicand) / int(right_radicand)))

        answer1 = left_constant + "(" + str(sqrt_other_radicand) + ")" + "\sqrt{" + str(right_radicand) + "}" + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer2 =  "(" + str(sqrt_other_radicand) + ")" + left_constant + "\sqrt{" + str(right_radicand) + "}" + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer3 = left_constant + "\sqrt{" + str(right_radicand) + "}" + "(" + str(sqrt_other_radicand) + ")" + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer4 =  "\sqrt{" + str(right_radicand) + "}" + left_constant + "(" + str(sqrt_other_radicand) + ")" + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer5 =  "\sqrt{" + str(right_radicand) + "}" + "(" + str(sqrt_other_radicand) + ")" + left_constant + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"

        answer6 = left_constant + "\cdot" + "(" + str(sqrt_other_radicand) + ")" + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer7 = left_constant + "\\times" + "(" + str(sqrt_other_radicand) + ")" + "\\times" + "\sqrt{" + str(right_radicand) + "}" + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer8 =  "(" + str(sqrt_other_radicand) + ")" + "\cdot" + left_constant + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "+" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        answer9 =  "(" + str(sqrt_other_radicand) + ")" + "\\times" + left_constant + "\\times" + "\sqrt{" + str(right_radicand) + "}" + "+" + str(right_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}"
        answer10 = left_constant + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "\cdot" + "(" + str(sqrt_other_radicand) + ")" + "+" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        answer11 = left_constant + "\\times" + "\sqrt{" + str(right_radicand) + "}" + "\\times" + "(" + str(sqrt_other_radicand) + ")" + "+" + str(right_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}"
        answer12 =  "\sqrt{" + str(right_radicand) + "}" + "\cdot" + left_constant + "\cdot" + "(" + str(sqrt_other_radicand) + ")" + "+" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        answer13 =  "\sqrt{" + str(right_radicand) + "}" + "\\times" + left_constant + "\\times" + "(" + str(sqrt_other_radicand) + ")" + "+" + str(right_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}"
        answer14 =  "\sqrt{" + str(right_radicand) + "}" + "\cdot" + "(" + str(sqrt_other_radicand) + ")" + left_constant + "+" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        answer15 =  "\sqrt{" + str(right_radicand) + "}" + "\\times" + "(" + str(sqrt_other_radicand) + ")" + left_constant + "+" + str(right_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}"

        answers = [Fact(selection="solve_square_root", action="input change", input=answer1),
                   Fact(selection="solve_square_root", action="input change", input=answer2),
                   Fact(selection="solve_square_root", action="input change", input=answer3),
                   Fact(selection="solve_square_root", action="input change", input=answer4),
                   Fact(selection="solve_square_root", action="input change", input=answer5),
                   Fact(selection="solve_square_root", action="input change", input=answer6),
                   Fact(selection="solve_square_root", action="input change", input=answer7),
                   Fact(selection="solve_square_root", action="input change", input=answer8),
                   Fact(selection="solve_square_root", action="input change", input=answer9),
                   Fact(selection="solve_square_root", action="input change", input=answer10),
                   Fact(selection="solve_square_root", action="input change", input=answer11),
                   Fact(selection="solve_square_root", action="input change", input=answer12),
                   Fact(selection="solve_square_root", action="input change", input=answer13),
                   Fact(selection="solve_square_root", action="input change", input=answer14),
                   Fact(selection="solve_square_root", action="input change", input=answer15),
                   ]


        values = [str(sqrt_other_radicand), left_constant, "\sqrt{" + str(right_radicand) + "}"]
        
        for order in permutations(values):
            cdot_answer = "\cdot".join(order) + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
            answers.append(Fact(selection="solve_square_root", action="input change", input=cdot_answer))
            partial_cdot_answer = cdot_answer.replace("\cdot\sqrt", "\sqrt")
            answers.append(Fact(selection="solve_square_root", action="input change", input=partial_cdot_answer))

            times_answer = "\\times".join(order) + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
            answers.append(Fact(selection="solve_square_root", action="input change", input=times_answer))
            partial_times_answer = times_answer.replace("\\times\sqrt", "\sqrt")
            answers.append(Fact(selection="solve_square_root", action="input change", input=partial_times_answer))

        for answer in answers:
            print(answer)
        
        return answers


    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="product_rule", value=V('product_rule'), disabled=True) &
                Fact(field="solve_square_root", value=V('solve_square_root'), disabled=True) &
                Fact(field="evaluate_coefficient", disabled=False))
    def evaluate_coefficient(init_value):
        left_side = init_value.split("+")[0]
        left_constant = left_side.split("\sqrt{")[0]
        left_radicand = left_side.split("\sqrt{")[1].replace("}", "")
    
        right_side = init_value.split("+")[1]
        right_constant = right_side.split("\sqrt{")[0]
        right_radicand = right_side.split("\sqrt{")[1].replace("}", "")

        sqrt_other_radicand =  int(math.sqrt(int(left_radicand) / int(right_radicand)))
        new_left_constant = int(int(sqrt_other_radicand) * int(left_constant))
       
        answer1 = str(new_left_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer2 = str(new_left_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}" + "+" + str(right_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}"
        answer3 = str(new_left_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "+" + str(right_constant)  + "\cdot" + "\sqrt{" + str(right_radicand) + "}"

        # print(answer1)
        # print(answer2)
        # print(answer3)

        return [Fact(selection="evaluate_coefficient", action="input change", input=answer1),
        Fact(selection="evaluate_coefficient", action="input change", input=answer2),
        Fact(selection="evaluate_coefficient", action="input change", input=answer3)]


    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="product_rule", value=V('product_rule'), disabled=True) &
                Fact(field="solve_square_root", value=V('solve_square_root'), disabled=True) &
                Fact(field="evaluate_coefficient", value=V('evaluate_coefficient'), disabled=True) &
                Fact(field="adding_square_root", disabled=False))
    def adding_square_root(evaluate_coefficient):
        left_side = evaluate_coefficient.split("+")[0]
        left_constant = left_side.split("\sqrt{")[0]
        left_radicand = left_side.split("\sqrt{")[1].replace("}", "")
    
        right_side = evaluate_coefficient.split("+")[1]
        right_constant = right_side.split("\sqrt{")[0]
        right_radicand = right_side.split("\sqrt{")[1].replace("}", "")

        final_constant = int(left_constant) + int(right_constant)

        answer1 = str(final_constant) + "\sqrt{" + str(right_radicand) + "}" 
        answer2 = str(final_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}" 
        answer3 = str(final_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" 

        # print(answer1)
        # print(answer2)
        # print(answer3)
       
        return [Fact(selection="adding_square_root", action="input change", input=answer1),
        Fact(selection="adding_square_root", action="input change", input=answer2),
        Fact(selection="adding_square_root", action="input change", input=answer3)]



    @Production(Fact(field="adding_square_root", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input="")]

    net.add_production(factor_radicand)
    net.add_production(product_rule)
    net.add_production(solve_square_root)
    net.add_production(evaluate_coefficient)
    net.add_production(adding_square_root)
    net.add_production(select_done)

    return net


def radical_adding_sqrt_kc_mapping():
    kcs = {
        "factor_radicand": "Factoring the radicand",
        "product_rule": "Using product rule",
        "solve_square_root": "Solving square root",
        "evaluate_coefficient": "Multiply square root with coefficient",
        "adding_square_root": "Adding square roots",
        "select_done": "Determine if adding square root problem is complete"
    }
    return kcs


def radical_adding_sqrt_intermediate_hints():
    hints = {
       "factor_radicand": [
           "Factor the radicand within the square root."
       ],
       "product_rule": [
            "Use the product rule to break down the radicand."],
        "solve_square_root": [
            "Solve the square root in the expression."],
         "evaluate_coefficient": [
            "Multiply the solved square root with the coefficient."],
        "adding_square_root": [
            "Add the coefficients square roots with the same radicand."
        ]
    }
    return hints

def radical_adding_sqrt_studymaterial():
    study_material = studymaterial["radicals_adding_square_roots"]
    return study_material

loaded_models.register(CognitiveModel("radicals",
                                      "radicals_adding_square_roots",
                                      radical_adding_sqrt_model,
                                      radical_adding_sqrt_problem,
                                      radical_adding_sqrt_kc_mapping(),
                                      radical_adding_sqrt_intermediate_hints(),
                                      radical_adding_sqrt_studymaterial()))
