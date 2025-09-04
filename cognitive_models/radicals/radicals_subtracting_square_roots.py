from functools import reduce
from random import randint
# from random import random
from random import choice
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



def radical_subtracting_sqrt_problem():
    coefficient_1 = generate_prime(2,20)
    radicand_1_a =  generate_prime(2,20)
    radicand_1_b = (randint(2,6))** 2
    coefficient_2 = generate_prime(2,20)
    return str(coefficient_1) + "\sqrt{" + str(radicand_1_a * radicand_1_b) + "}" + "-" + str(coefficient_2) + "\sqrt{" + str(radicand_1_a) + "}"

'''
Generate subtracting square roots rule model
'''
def radical_subtracting_sqrt_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="factor_radicand", disabled=False))
    def factor_radicand(init_value):
        left_side = init_value.split("-")[0]
        left_constant = left_side.split("\sqrt{")[0]
        left_radicand = left_side.split("\sqrt{")[1].replace("}", "")
    
        right_side = init_value.split("-")[1]
        right_constant = right_side.split("\sqrt{")[0]
        right_radicand = right_side.split("\sqrt{")[1].replace("}", "")

        # divide left radicand by right radicand 
        other_radicand =  int(int(left_radicand) / int(right_radicand))

        answer1 = str(left_constant) + "\sqrt{" + str(right_radicand) + "\\times" +  str(other_radicand) + "}" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer2 = str(left_constant) + "\sqrt{" + str(other_radicand) + "\\times" +  str(right_radicand) + "}" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer3 = str(left_constant) + "\sqrt{" + str(right_radicand) + "\cdot" +  str(other_radicand) + "}" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer4 = str(left_constant) + "\sqrt{" + str(other_radicand) + "\cdot" +  str(right_radicand) + "}" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        ## Momin permute add
        answer5 =  "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + str(left_constant) + "\sqrt{" + str(right_radicand) + "\\times" +  str(other_radicand) + "}"
        answer6 =  "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + str(left_constant) + "\sqrt{" + str(other_radicand) + "\\times" +  str(right_radicand) + "}"
        answer7 =  "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + str(left_constant) + "\sqrt{" + str(right_radicand) + "\cdot" +  str(other_radicand) + "}"
        answer8 =  "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + str(left_constant) + "\sqrt{" + str(other_radicand) + "\cdot" +  str(right_radicand) + "}"

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
        left_side = init_value.split("-")[0]
        left_constant = left_side.split("\sqrt{")[0]
        left_radicand = left_side.split("\sqrt{")[1].replace("}", "")
    
        right_side = init_value.split("-")[1]
        right_constant = right_side.split("\sqrt{")[0]
        right_radicand = right_side.split("\sqrt{")[1].replace("}", "")

        # divide left radicand by right radicand 
        other_radicand =  int(int(left_radicand) / int(right_radicand))

        answer1 = str(left_constant) + "\sqrt{" + str(right_radicand) + "}" + "\sqrt{" + str(other_radicand)  + "}" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer2 = str(left_constant) + "\sqrt{" + str(other_radicand) + "}" + "\sqrt{" + str(right_radicand)  + "}" + "-" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer3 = str(left_constant) + "\cdot" + "\sqrt{" + str(other_radicand) + "}" + "\cdot" + "\sqrt{" + str(right_radicand)  + "}" + "-" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer4 = str(left_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "\cdot" + "\sqrt{" + str(other_radicand)  + "}" + "-" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer5 = str(left_constant) + "\\times" + "\sqrt{" + str(other_radicand) + "}" + "\\times" "\sqrt{" + str(right_radicand)  + "}" + "-" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer6 = str(left_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}" + "\\times" "\sqrt{" + str(other_radicand)  + "}" + "-" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        ### Momin permute add
        answer7 =  "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + str(left_constant) + "\sqrt{" + str(right_radicand) + "}" + "\sqrt{" + str(other_radicand)  + "}"
        answer8 =  "-" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + str(left_constant) + "\sqrt{" + str(other_radicand) + "}" + "\sqrt{" + str(right_radicand)  + "}"
        answer9 = "-" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + str(left_constant) + "\cdot" + "\sqrt{" + str(other_radicand) + "}" + "\cdot" + "\sqrt{" + str(right_radicand)  + "}" 
        answer10 =  "-" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + str(left_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "\cdot" + "\sqrt{" + str(other_radicand)  + "}"
        answer11 = "-" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + str(left_constant) + "\\times" + "\sqrt{" + str(other_radicand) + "}" + "\\times" "\sqrt{" + str(right_radicand)  + "}"
        answer12 = "-" +  str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + str(left_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}" + "\\times" "\sqrt{" + str(other_radicand)  + "}"

        # print(answer1)
        # print(answer2)
        # print(answer3)
        # print(answer4)
        # print(answer5)
        # print(answer6)

        # TODO: Multuple answers can have cdot or x between
        return [Fact(selection="product_rule", action="input change", input=answer1), 
                Fact(selection="product_rule", action="input change", input=answer2),
                Fact(selection="product_rule", action="input change", input=answer3),
                Fact(selection="product_rule", action="input change", input=answer4),
                Fact(selection="product_rule", action="input change", input=answer5),
                Fact(selection="product_rule", action="input change", input=answer6),
                Fact(selection="product_rule", action="input change", input=answer7), 
                Fact(selection="product_rule", action="input change", input=answer8),
                Fact(selection="product_rule", action="input change", input=answer9),
                Fact(selection="product_rule", action="input change", input=answer10),
                Fact(selection="product_rule", action="input change", input=answer11),
                Fact(selection="product_rule", action="input change", input=answer12)]


    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="product_rule", value=V('product_rule'), disabled=True) &
                Fact(field="solve_square_root", disabled=False))
    def solve_square_root(init_value, product_rule):
        
        left_side = init_value.split("-")[0]
        left_constant = left_side.split("\sqrt{")[0]
        left_radicand = left_side.split("\sqrt{")[1].replace("}", "")
    
        right_side = init_value.split("-")[1]
        right_constant = right_side.split("\sqrt{")[0]
        right_radicand = right_side.split("\sqrt{")[1].replace("}", "")

        # divide left radicand by right radicand 
        sqrt_other_radicand =  int(math.sqrt(int(left_radicand) / int(right_radicand)))

        # Momin hidden
        # answer1 = left_constant + "(" + str(sqrt_other_radicand) + ")" + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        # answer2 =  "(" + str(sqrt_other_radicand) + ")" + left_constant + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        # answer3 = left_constant + "\sqrt{" + str(right_radicand) + "}" + "(" + str(sqrt_other_radicand) + ")" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        # answer4 =  "\sqrt{" + str(right_radicand) + "}" + left_constant + "(" + str(sqrt_other_radicand) + ")" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        # answer5 =  "\sqrt{" + str(right_radicand) + "}" + "(" + str(sqrt_other_radicand) + ")" + left_constant + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        # answer6 = left_constant + "\cdot" + "(" + str(sqrt_other_radicand) + ")" + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        # answer7 = left_constant + "\\times" + "(" + str(sqrt_other_radicand) + ")" + "\\times" + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        # answer8 =  "(" + str(sqrt_other_radicand) + ")" + "\cdot" + left_constant + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        # answer9 =  "(" + str(sqrt_other_radicand) + ")" + "\\times" + left_constant + "\\times" + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}"
        # answer10 = left_constant + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "\cdot" + "(" + str(sqrt_other_radicand) + ")" + "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        # answer11 = left_constant + "\\times" + "\sqrt{" + str(right_radicand) + "}" + "\\times" + "(" + str(sqrt_other_radicand) + ")" + "-" + str(right_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}"
        # answer12 =  "\sqrt{" + str(right_radicand) + "}" + "\cdot" + left_constant + "\cdot" + "(" + str(sqrt_other_radicand) + ")" + "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        # answer13 =  "\sqrt{" + str(right_radicand) + "}" + "\\times" + left_constant + "\\times" + "(" + str(sqrt_other_radicand) + ")" + "-" + str(right_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}"
        # answer14 =  "\sqrt{" + str(right_radicand) + "}" + "\cdot" + "(" + str(sqrt_other_radicand) + ")" + left_constant + "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        # answer15 =  "\sqrt{" + str(right_radicand) + "}" + "\\times" + "(" + str(sqrt_other_radicand) + ")" + left_constant + "-" + str(right_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}"
        ## Momin permute add
        answer1 = left_constant + "(" + str(sqrt_other_radicand) + ")" + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer2 =  "(" + str(sqrt_other_radicand) + ")" + left_constant + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer3 = left_constant + "\sqrt{" + str(right_radicand) + "}" + "(" + str(sqrt_other_radicand) + "" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer4 =  "\sqrt{" + str(right_radicand) + "}" + left_constant + "(" + str(sqrt_other_radicand) + ")" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer5 =  "\sqrt{" + str(right_radicand) + "}" + "(" + str(sqrt_other_radicand) + ")" + left_constant + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer6 = left_constant + "\cdot" + "(" + str(sqrt_other_radicand) + ")" + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer7 = left_constant + "\times" + "(" + str(sqrt_other_radicand) + ")" + "\times" + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer8 =  "(" + str(sqrt_other_radicand) + ")" + "\cdot" + left_constant + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        answer9 =  "(" + str(sqrt_other_radicand) + ")" + "\times" + left_constant + "\times" + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\times" + "\sqrt{" + str(right_radicand) + "}"
        answer10 = left_constant + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "\cdot" + "(" + str(sqrt_other_radicand) + ")" + "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        answer11 = left_constant + "\times" + "\sqrt{" + str(right_radicand) + "}" + "\times" + "(" + str(sqrt_other_radicand) + ")" + "-" + str(right_constant) + "\times" + "\sqrt{" + str(right_radicand) + "}"
        answer12 =  "\sqrt{" + str(right_radicand) + "}" + "\cdot" + left_constant + "\cdot" + "(" + str(sqrt_other_radicand) + ")" + "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        answer13 =  "\sqrt{" + str(right_radicand) + "}" + "\times" + left_constant + "\times" + "(" + str(sqrt_other_radicand) + ")" + "-" + str(right_constant) + "\times" + "\sqrt{" + str(right_radicand) + "}"
        answer14 =  "\sqrt{" + str(right_radicand) + "}" + "\cdot" + "(" + str(sqrt_other_radicand) + ")" + left_constant + "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        answer15 =  "\sqrt{" + str(right_radicand) + "}" + "\times" + "(" + str(sqrt_other_radicand) + ")" + left_constant + "-" + str(right_constant) + "\times" + "\sqrt{" + str(right_radicand) + "}"

        answer16 = "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + left_constant + "(" + str(sqrt_other_radicand) + ")" + "\sqrt{" + str(right_radicand) + "}" 
        answer17 =  "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + "(" + str(sqrt_other_radicand) + ")" + left_constant + "\sqrt{" + str(right_radicand) + "}"
        answer18 = "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + left_constant + "\sqrt{" + str(right_radicand) + "}" + "(" + str(sqrt_other_radicand) + ")"
        answer19=  "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + "\sqrt{" + str(right_radicand) + "}" + left_constant + "(" + str(sqrt_other_radicand) + ")"
        answer20=  "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + "\sqrt{" + str(right_radicand) + "}" + "(" + str(sqrt_other_radicand) + ")" + left_constant
        answer21= "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + left_constant + "\cdot" + "(" + str(sqrt_other_radicand) + ")" + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        answer22 = "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + left_constant + "\times" + "(" + str(sqrt_other_radicand) + ")" + "\times" + "\sqrt{" + str(right_radicand) + "}"
        answer23 =  "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "+" + "(" + str(sqrt_other_radicand) + ")" + "\cdot" + left_constant + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        answer24 =  "-" + str(right_constant) + "\times" + "\sqrt{" + str(right_radicand) + "}" + "+" + "(" + str(sqrt_other_radicand) + ")" + "\times" + left_constant + "\times" + "\sqrt{" + str(right_radicand) + "}"
        answer25 = "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "+" + left_constant + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "\cdot" + "(" + str(sqrt_other_radicand) + ")"
        answer26 = "-" + str(right_constant) + "\times" + "\sqrt{" + str(right_radicand) + "}" + "+" + left_constant + "\times" + "\sqrt{" + str(right_radicand) + "}" + "\times" + "(" + str(sqrt_other_radicand) + ")"
        answer27 =  "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "+" + "\sqrt{" + str(right_radicand) + "}" + "\cdot" + left_constant + "\cdot" + "(" + str(sqrt_other_radicand) + ")"
        answer28 =  "-" + str(right_constant) + "\times" + "\sqrt{" + str(right_radicand) + "}" + "+" + "\sqrt{" + str(right_radicand) + "}" + "\times" + left_constant + "\times" + "(" + str(sqrt_other_radicand) + ")"
        answer29 =  "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "+" + "\sqrt{" + str(right_radicand) + "}" + "\cdot" + "(" + str(sqrt_other_radicand) + ")" + left_constant
        answer30 =  "-" + str(right_constant) + "\times" + "\sqrt{" + str(right_radicand) + "}" + "+" + "\sqrt{" + str(right_radicand) + "}" + "\times" + "(" + str(sqrt_other_radicand) + ")" + left_constant
        
        answer31 = "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + left_constant + "\left(" + str(sqrt_other_radicand) + "\\right)" + "\sqrt{" + str(right_radicand) + "}" 
        answer32 =  "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + "\left(" + str(sqrt_other_radicand) + "\\right)" + left_constant + "\sqrt{" + str(right_radicand) + "}"
        answer33 = "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + left_constant + "\sqrt{" + str(right_radicand) + "}" + "\left(" + str(sqrt_other_radicand) + "\\right)"
        answer34=  "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + "\sqrt{" + str(right_radicand) + "}" + left_constant + "\left(" + str(sqrt_other_radicand) + "\\right)"
        answer35=  "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + "\sqrt{" + str(right_radicand) + "}" + "\left(" + str(sqrt_other_radicand) + "\\right)" + left_constant
        answer36= "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + left_constant + "\cdot" + "\left(" + str(sqrt_other_radicand) + "\\right)" + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        answer37 = "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + left_constant + "\times" + "\left(" + str(sqrt_other_radicand) + "\\right)" + "\times" + "\sqrt{" + str(right_radicand) + "}"
        answer38 =  "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "+" + "\left(" + str(sqrt_other_radicand) + "\\right)" + "\cdot" + left_constant + "\cdot" + "\sqrt{" + str(right_radicand) + "}"
        answer39 =  "-" + str(right_constant) + "\times" + "\sqrt{" + str(right_radicand) + "}" + "+" + "\left(" + str(sqrt_other_radicand) + "\\right)" + "\times" + left_constant + "\times" + "\sqrt{" + str(right_radicand) + "}"
        answer40 = "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "+" + left_constant + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "\cdot" + "\left(" + str(sqrt_other_radicand) + "\\right)"
        answer41 = "-" + str(right_constant) + "\times" + "\sqrt{" + str(right_radicand) + "}" + "+" + left_constant + "\times" + "\sqrt{" + str(right_radicand) + "}" + "\times" + "\left(" + str(sqrt_other_radicand) + "\\right)"
        answer42 =  "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "+" + "\sqrt{" + str(right_radicand) + "}" + "\cdot" + left_constant + "\cdot" + "\left(" + str(sqrt_other_radicand) + "\\right)"
        answer43 =  "-" + str(right_constant) + "\times" + "\sqrt{" + str(right_radicand) + "}" + "+" + "\sqrt{" + str(right_radicand) + "}" + "\times" + left_constant + "\times" + "\left(" + str(sqrt_other_radicand) + "\\right)"
        answer44 =  "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "+" + "\sqrt{" + str(right_radicand) + "}" + "\cdot" + "\left(" + str(sqrt_other_radicand) + "\\right)" + left_constant
        answer45 =  "-" + str(right_constant) + "\times" + "\sqrt{" + str(right_radicand) + "}" + "+" + "\sqrt{" + str(right_radicand) + "}" + "\times" + "\left(" + str(sqrt_other_radicand) + "\\right)" + left_constant

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
                   Fact(selection="solve_square_root", action="input change", input=answer16),
                   Fact(selection="solve_square_root", action="input change", input=answer17),
                   Fact(selection="solve_square_root", action="input change", input=answer18),
                   Fact(selection="solve_square_root", action="input change", input=answer19),
                   Fact(selection="solve_square_root", action="input change", input=answer20),
                   Fact(selection="solve_square_root", action="input change", input=answer21),
                   Fact(selection="solve_square_root", action="input change", input=answer22),
                   Fact(selection="solve_square_root", action="input change", input=answer23),
                   Fact(selection="solve_square_root", action="input change", input=answer24),
                   Fact(selection="solve_square_root", action="input change", input=answer25),
                   Fact(selection="solve_square_root", action="input change", input=answer26),
                   Fact(selection="solve_square_root", action="input change", input=answer27),
                   Fact(selection="solve_square_root", action="input change", input=answer28),
                   Fact(selection="solve_square_root", action="input change", input=answer29),
                   Fact(selection="solve_square_root", action="input change", input=answer30),
                   Fact(selection="solve_square_root", action="input change", input=answer31),
                   Fact(selection="solve_square_root", action="input change", input=answer32),
                   Fact(selection="solve_square_root", action="input change", input=answer33),
                   Fact(selection="solve_square_root", action="input change", input=answer34),
                   Fact(selection="solve_square_root", action="input change", input=answer35),
                   Fact(selection="solve_square_root", action="input change", input=answer36),
                   Fact(selection="solve_square_root", action="input change", input=answer37),
                   Fact(selection="solve_square_root", action="input change", input=answer38),
                   Fact(selection="solve_square_root", action="input change", input=answer39),
                   Fact(selection="solve_square_root", action="input change", input=answer40),
                   Fact(selection="solve_square_root", action="input change", input=answer41),
                   Fact(selection="solve_square_root", action="input change", input=answer42),
                   Fact(selection="solve_square_root", action="input change", input=answer43),
                   Fact(selection="solve_square_root", action="input change", input=answer44),
                   Fact(selection="solve_square_root", action="input change", input=answer45),
                   ]

        values = [str(sqrt_other_radicand), left_constant, "\sqrt{" + str(right_radicand) + "}"]
        
        for order in permutations(values):
            cdot_answer = "\cdot".join(order) + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
            answers.append(Fact(selection="solve_square_root", action="input change", input=cdot_answer))
            partial_cdot_answer = cdot_answer.replace("\cdot\sqrt", "\sqrt")
            answers.append(Fact(selection="solve_square_root", action="input change", input=partial_cdot_answer))

            times_answer = "\\times".join(order) + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
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
        print("First:", init_value)
        left_side = init_value.split("-")[0]
        left_constant = left_side.split("\sqrt{")[0]
        left_radicand = left_side.split("\sqrt{")[1].replace("}", "")
    
        right_side = init_value.split("-")[1]
        right_constant = right_side.split("\sqrt{")[0]
        right_radicand = right_side.split("\sqrt{")[1].replace("}", "")

        sqrt_other_radicand =  int(math.sqrt(int(left_radicand) / int(right_radicand)))
        new_left_constant = int(int(sqrt_other_radicand) * int(left_constant))

        answer1 = str(new_left_constant) + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer2 = str(new_left_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}"
        answer3 = str(new_left_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" + "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"

        answer4 = "-" + str(right_constant) + "\sqrt{" + str(right_radicand) + "}" + "+" + str(new_left_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer5 = "-" + str(right_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}" + "+" + str(new_left_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}"
        answer6 = "-" + str(right_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}" +  "+" + str(new_left_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"

        # print(answer1)
        # print(answer2)
        # print(answer3)

        return [Fact(selection="evaluate_coefficient", action="input change", input=answer1),
                Fact(selection="evaluate_coefficient", action="input change", input=answer2),
                Fact(selection="evaluate_coefficient", action="input change", input=answer3),
                Fact(selection="evaluate_coefficient", action="input change", input=answer4),
                Fact(selection="evaluate_coefficient", action="input change", input=answer5),
                Fact(selection="evaluate_coefficient", action="input change", input=answer6)]

    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="product_rule", value=V('product_rule'), disabled=True) &
                Fact(field="solve_square_root", value=V('solve_square_root'), disabled=True) &
                Fact(field="evaluate_coefficient", value=V('evaluate_coefficient'), disabled=True) &
                Fact(field="subtracting_square_root", disabled=False))
    def subtracting_square_root(evaluate_coefficient):
        ### Momin add for commutative
        if evaluate_coefficient[0] == "-":
            symbol = "+"
        else: 
            symbol = "-"
        left_side = evaluate_coefficient.split(symbol)[0]
        print("HERE", left_side)

        ## Add curly brace condition to handle \sqrt{number} and \sqrtnumber
        if "{" in left_side:
            left_constant = left_side.split("\sqrt{")[0]
            left_radicand = left_side.split("\sqrt{")[1].replace("}", "")
        else:
            left_constant = left_side.split("\sqrt")[0]
            left_radicand = left_side.split("\sqrt")[1].replace("}", "")
    
        right_side = evaluate_coefficient.split(symbol)[1]
        if "{" in right_side:
            right_constant = right_side.split("\sqrt{")[0]
            right_radicand = right_side.split("\sqrt{")[1].replace("}", "")
        else: 
            right_constant = right_side.split("\sqrt")[0]
            right_radicand = right_side.split("\sqrt")[1].replace("}", "")
        print(right_side)
        if evaluate_coefficient[0] == "-":
            final_constant = int(left_constant) + int(right_constant)
        else:
            final_constant = int(left_constant) - int(right_constant)
        answer1 = str(final_constant) + "\sqrt{" + str(right_radicand) + "}"
        answer2 = str(final_constant) + "\\times" + "\sqrt{" + str(right_radicand) + "}"
        answer3 = str(final_constant) + "\cdot" + "\sqrt{" + str(right_radicand) + "}"

        # print(answer1)
        # print(answer2)
        # print(answer3)

       
        return [Fact(selection="subtracting_square_root", action="input change", input=answer1),
        Fact(selection="subtracting_square_root", action="input change", input=answer2),
        Fact(selection="subtracting_square_root", action="input change", input=answer3)]


    @Production(Fact(field="subtracting_square_root", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input="")]

    net.add_production(factor_radicand)
    net.add_production(product_rule)
    net.add_production(solve_square_root)
    net.add_production(evaluate_coefficient)
    net.add_production(subtracting_square_root)
    net.add_production(select_done)

    return net


def radical_subtracting_sqrt_kc_mapping():
    kcs = {
        "factor_radicand": "Factoring the radicand",
        "product_rule": "Using product rule",
        "solve_square_root": "Solving square root",
        "evaluate_coefficient": "Multiply square root with coefficient",
        "subtracting_square_root": "Subtracting square roots",
        "select_done": "Determine if subtracting square root problem is complete"
    }
    return kcs


def radical_subtracting_sqrt_intermediate_hints():
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
        "subtracting_square_root": [
            "Subtract the coefficients of the square roots with the same radicand."
        ]
    }
    return hints


def radical_subtracting_sqrt_studymaterial():
    study_material = studymaterial["radicals_subtracting_square_roots"]
    return study_material

loaded_models.register(CognitiveModel("radicals", 
                                      "radicals_subtracting_square_roots",
                                      radical_subtracting_sqrt_model,
                                      radical_subtracting_sqrt_problem,
                                      radical_subtracting_sqrt_kc_mapping(),
                                      radical_subtracting_sqrt_intermediate_hints(),
                                      radical_subtracting_sqrt_studymaterial()))
