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
from decimal import Decimal, ROUND_HALF_UP

place_value = {
    'tenths': Decimal('0.1'),
    'hundredths': Decimal('0.01'),
    'thousandths': Decimal('0.001'),
    'ones': Decimal('1'),
    'tens': Decimal('10'),
    'hundreds': Decimal('100')
}


def htn_nursing_calculation_round_placevalue_problem():
    
    random_number = round(uniform(100, 999) + uniform(0.0001, 0.9999), 4)
    chosen_place_value = choice(list(place_value.keys()))

    words = f"Round {random_number} to the <b>{chosen_place_value}</b> place."
    prob = [words, random_number, chosen_place_value]
    return prob

def final_answer(init_value):
    random_number = Decimal(init_value.split(',')[1])
    chosen_place_value = init_value.split(',')[2]
    answer = (random_number / place_value[chosen_place_value]).quantize(Decimal('1'), rounding=ROUND_HALF_UP) * place_value[chosen_place_value]
    hint = str(answer)
    # print(answer)
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', str(answer))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    # print('after sp', answer)
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

def htn_nursing_calculation_round_placevalue_kc_mapping():

    kcs = {
        'final_answer': 'final_answer',
        'done': 'done'
    }

    return kcs




def htn_nursing_calculation_round_placevalue_intermediate_hints():
    hints = {
        'final_answer': ["Look at the place value after the one specified. If it is greater than five, increase the value. If it less than five, keep it the same."],
        'done': ["Once you have rounded you can"
                        " select the done button to move to the next problem."]
    }
    return hints

def htn_nursing_calculation_round_placevalue_studymaterial():
    study_material = studymaterial["place_value"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_nursing_math_review',    
                                             'htn_nursing_calculation_round_placevalue',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_nursing_calculation_round_placevalue_problem,
                                             htn_nursing_calculation_round_placevalue_kc_mapping(),
                                             htn_nursing_calculation_round_placevalue_intermediate_hints(),
                                             htn_nursing_calculation_round_placevalue_studymaterial()))