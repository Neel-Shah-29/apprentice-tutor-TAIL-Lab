from functools import reduce
from random import randint
from random import random
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

import sympy as sp
import re

def solve_quadratic(equation):
    # Parse the equation to extract coefficients
    x = sp.symbols('x')
    match = re.search(r'{\d}({.*?})', equation)
    expression = match.group(1)
    expression = expression.replace('^', '**').replace('{','').replace('}','')
    expression = re.sub(r'([a-zA-Z0-9])([a-zA-Z])', r'\1*\2', expression)
    denominator = sp.sympify(expression)
    
    # Get the coefficients of the quadratic equation
    coeff = sp.Poly(denominator, x).all_coeffs()
    a, b, c = coeff[0], coeff[1], coeff[2]

    # Calculate the solutions using the quadratic formula
    discriminant = b**2 - 4*a*c
    solution1 = (-b + sp.sqrt(discriminant)) / (2*a)
    solution2 = (-b - sp.sqrt(discriminant)) / (2*a)
    return solution2, solution1

def factors(n):
    fset = set(reduce(list.__add__,
               ([i, n//i] for i in range(1, int(abs(n)**0.5) + 1)
                if n % i == 0)))

    other_signs = set([-1 * f for f in fset])
    fset = fset.union(other_signs)

    return fset

# genarate the math problem 
def rational_equation_find_domain_problem():
    n1 = 1

    # print(type(random))

    n2 = randint(1, 5)
    if random() > 0.5:
        n2 *= -1

    n3 = 1

    n4 = randint(1, 5)
    if random() > 0.5:
        n4 *= -1

    problem = "x^2"

    b_value = n1*n4+n2*n3
    if b_value == 0:
        return rational_equation_find_domain_problem()

    if b_value > 0:
        problem += "+"

    problem += "{}x".format(b_value)

    c_value = n2 * n4
    if c_value > 0:
        problem += "+"

    problem += "{}".format(c_value)
    
    # render fraction in Latex style, example: f(x)=\frac{1}{x^2-3x-10}}=0
    return "f(x)=\\frac{" + "1"  + "}" + "{" + problem + "}" + "}"
    

'''
Generate rational equation specific value rule model
'''
def rational_equation_find_domain_model():
    net = ReteNetwork()
    # Set the denominator equals zero
    @Production(Fact(field = "initial_problem", value = V('init_value')) & Fact(field = "denominator_set_zero", disabled = False)) 
    def denominator_set_zero(init_value): 
        #parse the function and get the denominator
        init_value = init_value.replace("f(x)=\\frac{1}{","")
        init_value = init_value.replace("}}","")
        denominator_set_zero = init_value + "=0"
        return [Fact(selection = "denominator_set_zero", action = "input change", input = denominator_set_zero)]

    # Factor the trinomial
    @Production(Fact(field = "denominator_set_zero", value = V('denom')) & Fact(field = "denominator_set_zero", disabled = True) & Fact(field = "factor_trinomial", disabled = False)) 
    def factor_trinomial(denom):
        denom = denom.replace("=0","") 
        c_str = denom.split('x')[-1].replace('+', '')# get the str of c
        denom = denom.replace("x^2","")
        b_absolute = denom[denom.index("x") - 1]# get the absolute str of b
        b_symbol = denom[denom.index("x") - 2]# get the symbol of b
        b_str = b_symbol + b_absolute# get the str of b
        b = int(b_symbol + b_absolute)#get the value of b
        c = int(c_str)
        factor_1 = int((math.sqrt(b*b-4*c)-b)/2)
        factor_2 = int((-math.sqrt(b*b-4*c)-b)/2)
        if factor_1 > 0:
            str_factor_1 = "-" + str(abs(factor_1))
        else:
            str_factor_1 = "+" + str(abs(factor_1))
        
        if factor_2 > 0:
            str_factor_2 = "-" + str(abs(factor_2))
        else:
            str_factor_2 = "+" + str(abs(factor_2))

        answer1 = "(x" + str_factor_1 + ")" + "(x" + str_factor_2 + ")" + "=0"
        answer2 = "(x" + str_factor_2 + ")" + "(x" + str_factor_1 + ")" + "=0"
        answer3 = "\\left(x" + str_factor_1 + "\\right)" + "\\left(x" + str_factor_2 + "\\right)" + "=0"
        answer4 = "\\left(x" + str_factor_2 + "\\right)" + "\\left(x" + str_factor_1 + "\\right)" + "=0"
        
        # different answers
        return [Fact(selection = "factor_trinomial", action = "input change", input = answer1),
                Fact(selection = "factor_trinomial", action = "input change", input = answer2),
                Fact(selection = "factor_trinomial", action = "input change", input = answer3),
                Fact(selection = "factor_trinomial", action = "input change", input = answer4)]
   
    # Zero production property for the left box
    @Production(Fact(field = "factor_trinomial", value = V('factor_trinomial')) & Fact(field = "factor_trinomial", disabled = True) & Fact(field = "zero_product_1", disabled = False)) 
    def zero_product_left(factor_trinomial): 
        # print("-----")
        # print(factor_trinomial)
        # print("-----")
        # \left(x-1\right)\left(x+3\right)=0
        factor_trinomial = factor_trinomial.replace("=0","")
        if "\\right)" not in  factor_trinomial and "\\left(" not in  factor_trinomial:
            zero_product = factor_trinomial.split(")(")
            zero_product_1 = zero_product[0].replace("(","") + "=0" #first euqation
            zero_product_2 = zero_product[1].replace(")","") + "=0" #second euqation
        else:
            zero_product = factor_trinomial.split("\\right)\\left(")
            zero_product_1 = zero_product[0].replace("\\left(","") + "=0" #first euqation
            zero_product_2 = zero_product[1].replace("\\right)","") + "=0" #second euqation
            
       
        return [Fact(selection = "zero_product_1", action = "input change", input = zero_product_1),
        Fact(selection = "zero_product_1", action = "input change", input = zero_product_2)]
        
        
    # Zero production property for the right box
    @Production(Fact(field = "factor_trinomial", value = V('factor_trinomial')) & Fact(field = "zero_product_1", value = V('zero_product_1')) 
    & Fact(field = "zero_product_1", disabled = True) & Fact(field = "zero_product_2", disabled = False)) 
    def zero_product_right(zero_product_1, factor_trinomial): 
        # print("-----")
        # print(factor_trinomial)
        # print("-----")
        factor_trinomial = factor_trinomial.replace("=0","")
        if "\\right)" not in  factor_trinomial and "\\left(" not in  factor_trinomial:
            temp = factor_trinomial.split(")(")
            temp_1 = temp[0].replace("(","") + "=0"
            temp_2 = temp[1].replace(")","") + "=0"
        else:
            temp = factor_trinomial.split("\\right)\\left(")
            temp_1 = temp[0].replace("\\left(","") + "=0"
            temp_2 = temp[1].replace("\\right)","") + "=0"

        if temp_1 == zero_product_1:# the second euqation depends should not be the same as the first equation
            return [Fact(selection = "zero_product_2", action = "input change", input = temp_2)]
        else:
            return [Fact(selection = "zero_product_2", action = "input change", input = temp_1)]
        
    
    # Solve for the left box
    @Production(Fact(field = "zero_product_1", value = V('zero_product_1'))& Fact(field = "zero_product_2", value = V('zero_product_2')) & Fact(field = "zero_product_2", disabled = True) 
    & Fact(field = "solve_1", disabled = False)) 
    def solve_left(zero_product_1): 
        zero_product_1 = zero_product_1.replace(" ","")
        zero_product_1 = (zero_product_1[1] + zero_product_1[2])
        if zero_product_1[0] == "-":
            solve_1 = "x=" + zero_product_1[1]
        else:
            solve_1 = "x=-" + zero_product_1[1]
        
        return [Fact(selection = "solve_1", action = "input change", input = solve_1)]
    
    # Solve for the right box
    @Production(Fact(field = "zero_product_2", value = V('zero_product_2')) & Fact(field = "solve_1", value = V('solve_1')) 
    & Fact(field = "solve_1", disabled = True) & Fact(field = "solve_2", disabled = False)) 
    def solve_right(zero_product_2): 
        zero_product_2 = zero_product_2.replace(" ","")
        zero_product_2 = (zero_product_2[1] + zero_product_2[2])
        if zero_product_2[0] == "-":
            solve_2 = "x=" + zero_product_2[1]
        else:
            solve_2 = "x=-" + zero_product_2[1]
        return [Fact(selection = "solve_2", action = "input change", input = solve_2)]

    # Domian result for the left box
    @Production(Fact(field = "solve_1", value = V('solve_1')) & Fact(field = "solve_2", value = V('solve_2')) & Fact(field = "solve_2", disabled = True) & 
    Fact(field = "domain_1", disabled = False) & Fact(field = "initial_problem", value = V('init_value'))) 
    def domain_left(solve_2, solve_1, init_value): 
        solution_1, solution_2 = solve_quadratic(init_value)
        print(solution_1, solution_2)
        return [Fact(selection = "domain_1", action = "input change", input = str(solution_1))]

    # Domian result for the right box
    @Production(Fact(field = "solve_2", value = V('solve_2')) & Fact(field = "domain_1", value = V('domain_1')) & Fact(field = "domain_1", disabled = True) 
    & Fact(field = "domain_2", disabled = False) & Fact(field = "initial_problem", value = V('init_value'))) 
    def domain_right(domain_1, solve_2, init_value): 
        solution_1, solution_2 = solve_quadratic(init_value)
        return [Fact(selection = "domain_2", action = "input change", input = str(solution_2))]

        
    # Finish this math problem
    @Production(Fact(field="domain_2", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click",
                     input="")]


    net.add_production(denominator_set_zero)    
    net.add_production(factor_trinomial)   
    net.add_production(zero_product_left)
    net.add_production(zero_product_right)
    net.add_production(solve_left)
    net.add_production(solve_right)
    net.add_production(domain_left)
    net.add_production(domain_right)
    net.add_production(select_done)
    return net


def rational_equation_find_domain_kc_mapping():
    kcs = {
        "denominator_set_zero": "Set the denominator equal to zero",
        "factor_trinomial": "Factor the trinomial",
        "zero_product_left": "Use zero product property",
        "zero_product_right": "Use zero product property",
        "solve_right": "Solve the equation",
        "solve_left": "Solve the equation",
        "domain_left": "Write down the result",
        "domain_right": "Write down the result",
        "select_done": "Determine if find domain problem is complete"
    }
    return kcs


def rational_equation_find_domain_intermediate_hints():
    hints = {
        "denominator_set_zero": ["The domain of a rational function is all real numbers except those that make the rational expression undefined. ",
                                 "Set the denominator equal to zero"],
        "factor_trinomial": [
            "Factor the trinomial"
        ],
        "zero_product_left":["Use zero product property to set the first factor"],
        "zero_product_right":["Use zero product property to set the second factor"],
        "solve_left":["Solve the first equation"],
        "solve_right":["Solve the second equation"],
        "domain_left":["Write down the result"],
        "domain_right":["Write down the result"],
        "select_done":["Click on the done button to complete the problem"],
    }
    return hints

def rational_equation_find_domain_studymaterial():
    study_material = studymaterial["rational_equation_find_domain"]
    return study_material

loaded_models.register(CognitiveModel("rational_equation",
                                      "rational_equation_find_domain",
                                      rational_equation_find_domain_model,
                                      rational_equation_find_domain_problem,
                                      rational_equation_find_domain_kc_mapping(),
                                      rational_equation_find_domain_intermediate_hints(),
                                      rational_equation_find_domain_studymaterial()))
