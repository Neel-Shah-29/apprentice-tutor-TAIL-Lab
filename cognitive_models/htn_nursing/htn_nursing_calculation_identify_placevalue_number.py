import sympy as sp
from sympy import sstr, latex, symbols, Eq, solve
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re

from shop2.domain import Task, Operator, Method
# from shop2.planner import SHOP2
from shop2.fact import Fact
from shop2.conditions import Filter
from shop2.common import V

from htn_cognitive_models import HTNCognitiveModel
from htn_cognitive_models import htn_loaded_models
from studymaterial import studymaterial
import math
from random import uniform, choice
from functools import reduce

place_value = {
    'tenths': 0.1,
    'hundredths': 0.01,
    'thousandths': 0.001,
    'ones': 1,
    'tens': 10,
    'hundreds': 100
}

def htn_nursing_calculation_identify_placevalue_number_problem():

    chosen_place_value = choice(list(place_value.keys()))
    n1 = round(uniform(100, 999) + uniform(0.001, 0.999), 4)
    words = f"{n1}<br><br>What is the digit in the {chosen_place_value} place?"

    prob = [words, n1, chosen_place_value]
    return prob

def final_answer(init_value):
    # print(init_value)
    n1 = float(init_value.split(',')[1].strip())
    # print(n1)
    chosen_place_value = init_value.split(',')[2].strip()
    # print(chosen_place_value)
    # print(place_value[chosen_place_value])
    scaled_n1 = float(n1) / float(place_value[chosen_place_value])
    # print(scaled_n1)
    answer = int(scaled_n1) % 10    
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', str(answer))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    # print(hint, answer)
    return tuple([(re.compile(answer), hint)])

Domain = {
    'done': Operator(head=('done', V('kc')),
                     precondition=[Fact(start=True)],
                     effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
    ),
    'final_answer': Operator(head=('final_answer', V('equation'), V('kc')),
                           precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                           effects=[Fact(field='final_answer', value=(final_answer, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve': Method(head=('solve', V('equation')),
                    preconditions=[
                        Fact(scaffold='level_0'),
                    ],
                    subtasks=[
                        [
                            Task(head=('final_answer', V('equation'), ('final_answer',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],
                    ]
    ),
}

def htn_nursing_calculation_identify_placevalue_number_kc_mapping():

    kcs = {
        'final_answer': 'final_answer',
        'done': 'done'
    }

    return kcs




def htn_nursing_calculation_identify_placevalue_number_intermediate_hints():
    hints = {
        'final_answer': ["The ones, tens and hundreds are to the left of the decimal point."
                         " The tenths, hundredths, and thousandths are to the right of the decimal point."],
        'done': ["Once you have named the place value you can"
                        " select the done button to move to the next problem."]
    }
    return hints

def htn_nursing_calculation_identify_placevalue_number_studymaterial():
    study_material = studymaterial["place_value"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_nursing_math_review',    
                                             'htn_nursing_calculation_identify_placevalue_number',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_nursing_calculation_identify_placevalue_number_problem,
                                             htn_nursing_calculation_identify_placevalue_number_kc_mapping(),
                                             htn_nursing_calculation_identify_placevalue_number_intermediate_hints(),
                                             htn_nursing_calculation_identify_placevalue_number_studymaterial()))