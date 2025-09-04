import sympy as sp
import sympy as sp
from sympy import sstr, latex, symbols, Eq, solve
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re

from random import randint
from shop2.domain import Task, Operator, Method
# from shop2.planner import SHOP2
from shop2.fact import Fact
from shop2.conditions import Filter
from shop2.common import V

from htn_cognitive_models import HTNCognitiveModel
from htn_cognitive_models import htn_loaded_models
from studymaterial import studymaterial
import math
from random import random, choice, uniform
from functools import reduce

# TODO:: add more conversions, handle lbs and kg conversion, household to mL (NOT JUST MOVING DECIMAL POINT), could be separate tutor?

conversion_factors = {
    "L": {"mL": 1000},
    "mg": {"g": 0.001, "mcg": 1000},
    "mcg": {"mg": 0.001, "g":0.00001},
    "mL": {"L": 0.001},
    "kg": {"g": 1000, "mg":100000},
}

def htn_nursing_calculation_converting_units_problem():
    problems = [(from_unit, to_unit) for from_unit in conversion_factors for to_unit in conversion_factors[from_unit]]
    
    from_unit, to_unit = choice(problems)
    
    number = round(uniform(0.01, 1000), 2)
    
    problem = f"{number} {from_unit} = _____________________ {to_unit}"
    prob = [problem, number, from_unit, to_unit, conversion_factors[from_unit][to_unit], 0]
    return prob


def convert_value(init_value):
    number_str, from_unit, to_unit = init_value.split(',')[1:4]
    conversion_factor_str = str(conversion_factors[from_unit][to_unit])
    
    number_parts = number_str.split('.')
    conversion_parts = conversion_factor_str.split('.')
    
    number_decimal_places = len(number_parts[1]) if len(number_parts) > 1 else 0
    conversion_decimal_places = len(conversion_parts[1]) if len(conversion_parts) > 1 else 0
    total_decimal_places = number_decimal_places + conversion_decimal_places
    
    number_no_decimal = number_parts[0] + (number_parts[1] if len(number_parts) > 1 else '')
    conversion_no_decimal = conversion_parts[0] + (conversion_parts[1] if len(conversion_parts) > 1 else '')
    
    multiplied_value = str(int(number_no_decimal) * int(conversion_no_decimal))
    
    if len(multiplied_value) <= total_decimal_places:
        multiplied_value = '0' * (total_decimal_places - len(multiplied_value) + 1) + multiplied_value
        multiplied_value = '0.' + multiplied_value[-total_decimal_places:]
    else:
        multiplied_value = multiplied_value[:-total_decimal_places] + '.' + multiplied_value[-total_decimal_places:]
    
    multiplied_value = multiplied_value.rstrip('0').rstrip('.')
    if multiplied_value.startswith('.'):
        multiplied_value = '0' + multiplied_value
    # print(multiplied_value)

    return tuple([(re.compile(multiplied_value), multiplied_value)])



Domain = {
    'done': Operator(head=('done', V('kc')),
                     precondition=[Fact(start=True)],
                     effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
    ),
    'convert_value': Operator(head=('convert_value', V('equation'), V('kc')),
                        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                        effects=[Fact(field='convert_value', value=(convert_value, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve': Method(head=('solve', V('equation')),
                    preconditions=[
                        Fact(scaffold='level_1'),
                        Fact(scaffold='level_0'),
                    ],
                    subtasks=[
                        [
                            Task(head=('convert_value', V('equation'), ('convert_value',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],
                        [
                            Task(head=('convert_value', V('equation'), ('convert_value',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],
                    ]
    ),
}

def htn_nursing_calculation_converting_units_kc_mapping():

    kcs = {
        'conversion_factor1': 'conversion_factor1',
        'conversion_factor1_units': 'conversion_factor1_units',
        'conversion_factor2': 'conversion_factor2',
        'conversion_factor2_units': 'conversion_factor2_units',
        'convert_given': 'convert_given',
        'convert_given_units': 'convert_given_units',
        'convert_units': 'convert_units',
        'convert_value': 'convert_value',
        'done': 'done'
    }

    return kcs




def htn_nursing_calculation_converting_units_intermediate_hints():
    hints = {
        'convert_value': ["Use the conversion factor to create a proportion."],
        'done': ["Once you have found the final factored form you can"
                        " select the done button to move to the next problem."]
    }
    return hints

def htn_nursing_calculation_converting_units_studymaterial():
    study_material = studymaterial["metric_conversions"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_nursing_conversions',    
                                             'htn_nursing_calculation_converting_units',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_nursing_calculation_converting_units_problem,
                                             htn_nursing_calculation_converting_units_kc_mapping(),
                                             htn_nursing_calculation_converting_units_intermediate_hints(),
                                             htn_nursing_calculation_converting_units_studymaterial()))