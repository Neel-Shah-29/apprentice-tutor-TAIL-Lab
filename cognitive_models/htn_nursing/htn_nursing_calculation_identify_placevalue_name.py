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

def htn_nursing_calculation_identify_placevalue_name_problem():
    place_value = {
        'tenths': 1,
        'hundredths': 2,
        'thousandths': 3,
        'ones': -1,
        'tens': -2,
        'hundreds': -3
    }
    chosen_place_value = choice(list(place_value.keys()))
    n1 = round(uniform(100, 999) + uniform(0.001, 0.999), 4)
    words = f"{n1}"
    decimal_index = words.find('.')
    position = decimal_index + place_value[chosen_place_value]

    highlighted_number = f"{words[:position]}<b>{words[position]}</b>{words[position+1:]}"

    prob = [highlighted_number, n1, chosen_place_value, 0, 0, 0, ]
    return prob

def final_answer(init_value):
    answer = init_value.split(',')[2].strip()
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

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

def htn_nursing_calculation_identify_placevalue_name_kc_mapping():

    kcs = {
        'final_answer': 'final_answer',
        'done': 'done'
    }

    return kcs




def htn_nursing_calculation_identify_placevalue_name_intermediate_hints():
    hints = {
        'final_answer': ["If the place value is to the left of the decimal point, its ones, tens or hundreds."
                         " If the place value is to the right of the decimal point, it's tenths, hundredths, or thousandths."],
        'done': ["Once you have named the place value you can"
                        " select the done button to move to the next problem."]
    }
    return hints

def htn_nursing_calculation_identify_placevalue_name_studymaterial():
    study_material = studymaterial["place_value"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_nursing_math_review',    
                                             'htn_nursing_calculation_identify_placevalue_name',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_nursing_calculation_identify_placevalue_name_problem,
                                             htn_nursing_calculation_identify_placevalue_name_kc_mapping(),
                                             htn_nursing_calculation_identify_placevalue_name_intermediate_hints(),
                                             htn_nursing_calculation_identify_placevalue_name_studymaterial()))