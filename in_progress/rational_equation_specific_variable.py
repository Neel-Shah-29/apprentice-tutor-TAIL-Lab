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


def rational_equation_specific_variable_problem():
    constant = randint(2,10)
    exponent_1 = randint(1,10)
    exponent_2 = randint(1,10)
    return str(constant) + "^" + "{" + str(exponent_1) + "}" + "\cdot" + str(constant) + "^" + "{" + str(exponent_2) + "}"


'''
Generate rational equation specific value rule model
'''
def rational_equation_specific_variable_model():
    net = ReteNetwork()
    #substititue the rational expression
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="substitution", disabled=False))
    def sub_rational_expression(init_value):
        return [Fact(selection = "substitution", action = "input change", input = "test")]

    # find the LCD of both sides
    @Production(Fact(field="substitution", value=V('substitution')) &
                Fact(field="find_LCD", disabled=False))
    def find_LCD(substitution):
        return [Fact(selection = "find_LCD", action = "input change", input = "test")]

    # multiply both sides by the LCD
    @Production(Fact(field="find_LCD", value=V('find_LCD')) &
                Fact(field="multiply_LCD", disabled=False))
    def multiply_LCD(find_LCD):
        return [Fact(selection = "multiply_LCD", action = "input change", input = "test")]
    
    #simplify the equation till only o at the right side of the equal sign
    @Production(Fact(field="multiply_LCD", value=V('multiply_LCD')) &
                Fact(field="simplify_equation", disabled=False))
    def simplify_equation(multiply_LCD):
        return [Fact(selection = "simplify_equation", action = "input change", input = "test")]

    #Factor the trinomial
    @Production(Fact(field="simplify_equation", value=V('simplify_equation')) &
                Fact(field="factor", disabled=False))
    def factor(simplify_equation):
        return [Fact(selection = "factor", action = "input change", input = "test")] 
    
    #Use zero product property left box
    @Production(Fact(field="factor", value=V('factor')) &
                Fact(field="zero_product_1", disabled=False))
    def zero_product_left(factor):
        return [Fact(selection = "zero_product_1", action = "input change", input = "test")] 

    #Use zero product property right box
    @Production(Fact(field="zero_product_1", value=V('zero_product_1')) &
                Fact(field="zero_product_2", disabled=False))
    def zero_product_right(zero_product_1):
        return [Fact(selection = "zero_product_2", action = "input change", input = "test")] 

    #solve left box
    @Production(Fact(field="zero_product_2", value=V('zero_product_2')) &
                Fact(field="solve_1", disabled=False))
    def solve_left(zero_product_2):
        return [Fact(selection = "solve_1", action = "input change", input = "test")] 

    #sove right box
    @Production(Fact(field="solve_1", value=V('solve_1')) &
                Fact(field="solve_2", disabled=False))
    def solve_right(solve_1):
        return [Fact(selection = "solve_2", action = "input change", input = "test")] 

    #denominator value left box
    @Production(Fact(field="solve_2", value=V('solve_2')) &
                Fact(field="denom_value_1", disabled=False))
    def denom_left(solve_2):
        return [Fact(selection = "denom_value_1", action = "input change", input = "test")] 

    #denominator value right box
    @Production(Fact(field="denom_value_1", value=V('denom_value_1')) &
                Fact(field="denom_value_2", disabled=False))
    def denom_right(denom_value_1):
        return [Fact(selection = "denom_value_2", action = "input change", input = "test")] 

    #final result 
    @Production(Fact(field="denom_value_2", value=V('denom_value_2')) &
                Fact(field="final_result", disabled=False))
    def final(denom_value_2):
        return [Fact(selection = "final_result", action = "input change", input = "test")] 
    
    #done button
    @Production(Fact(field="final_result", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click",
                     input="")]


    net.add_production(sub_rational_expression)
    net.add_production(find_LCD)
    net.add_production(multiply_LCD)
    net.add_production(simplify_equation)
    net.add_production(factor)
    net.add_production(zero_product_left)
    net.add_production(zero_product_right)
    net.add_production(solve_left)
    net.add_production(solve_right)
    net.add_production(denom_left)
    net.add_production(denom_right)
    net.add_production(final)
    net.add_production(select_done)

    

    return net


def rational_equation_specific_variable_kc_mapping():
    kcs = {
        "sub_rational_expression": "Substitute in the rational expression",
        "find_LCD": "Find the LCD of both sides",
        "multiply_LCD": "Multiply both sides by the LCD",
        "simplify_equation": "Simplify the equation, till only 0 at the right side of the equal sign",
        "factor": "factor the trinomial",
        "zero_product_left": "Use zero product property",
        "zero_product_right": "Use zero product property",
        "solve_left": "Solve the equation",
        "solve_right": "Solve the equation",
        "denom_left": "Denominator value of this result",
        "denom_right": "Denominator value of this result",
        "final": "Get the final result",
        "select_done": "Determine if find specific value problem is complete"





    }
    return kcs


def rational_equation_specific_variable_intermediate_hints():
    hints = {
        "multiply_values": ["Substitute in the rational expression."],
        "find_LCD": ["Find the LCD of both sides."],
        "multiply_LCD": ["Multiply both sides by the LCD."],
        "find_LCD": ["Find the LCD of both sides."],
        "simplify_equation": ["Simplify the equation, till only 0 at the right side of the equal sign."],
        "factor": ["Factor the trinomial."],
        "zero_product_left": ["Use zero product property."],
        "zero_product_right": ["Use zero product property."],
        "solve_left": ["Solve the equation."],
        "solve_right": ["Solve the equation."],
        "denom_left": ["Calculate the function denominator value for this result."],
        "denom_right": ["Calculate the function denominator value for this result."],
        "denom_final": ["The final result of the function should be the result that cannot make the function denominator 0."],
        "select_done":["Click on the done button to complete the problem"]



    }
    return hints


loaded_models.register(CognitiveModel("rational_equation",
                                      "rational_equation_specific_variable",
                                      rational_equation_specific_variable_model,
                                      rational_equation_specific_variable_problem,
                                      rational_equation_specific_variable_kc_mapping(),
                                      rational_equation_specific_variable_intermediate_hints()))