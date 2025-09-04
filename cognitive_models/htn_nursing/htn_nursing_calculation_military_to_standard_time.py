import sympy as sp
from random import randint, choice

import sympy as sp
from sympy import sstr, latex, symbols, Eq, solve
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re
import random

from shop2.domain import Task, Operator, Method
# from shop2.planner import SHOP2
from shop2.fact import Fact
from shop2.conditions import Filter
from shop2.common import V

from htn_cognitive_models import HTNCognitiveModel
from htn_cognitive_models import htn_loaded_models
from studymaterial import studymaterial
import math
from random import random
from functools import reduce

#Non-Dynamic
def htn_nursing_calculation_military_to_standard_time_problem():
    
    hour = randint(0, 23)
    minute = randint(0, 59)
    military_time = f"{hour:02d}:{minute:02d}"
    words = f"Convert the military time {military_time} to the standard 12-hour AM/PM time."
    prob = [military_time, 0, 0, 0,0,words]
    #so now prob is in index five
    return prob


def convert_hour(init_value):
    words = init_value.split(",")[0]
    time = words.split(":")
    hours = int(time[0]) % 12
    # print(hours)
    return hours


def convert_am_pm(init_value):
    words = init_value.split(",")[0]
    time = words.split(":")
    hours = int(time[0])
    am_pm = "AM" if hours < 12 else "PM"
    # print(am_pm)
    return am_pm

#ini_value is a string representation of the list
def solve_time_conversion(init_value):
    hour_answer= convert_hour(init_value)  
    am_pm_answer = convert_am_pm(init_value)
    minutes = init_value.split(",")[0].split(':')[1]
    final_time = f"{hour_answer}:{minutes}{am_pm_answer}"
    # print(final_time)
    # answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', final_time)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(final_time), final_time), (re.compile(f"{hour_answer}:{minutes}{am_pm_answer.lower()}"), final_time)])
    
    

    print(answer)
    hint = final_time
    value = (answer, hint)
    return value

Domain = {
    'done': Operator(head=('done', V('kc')),
                     precondition=[Fact(start=True)],
                     effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
    ),
    

    'solve_time_conversion': Operator(head=('solve_time_conversion', V('equation'), V('kc')),
                           precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                           effects=[Fact(field='solve_time_conversion', value=(solve_time_conversion, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve': Method(head=('solve', V('equation')),
                    preconditions=[
                        Fact(scaffold='level_0'),
                    ],
                    subtasks=[
                        [
                            Task(head=('solve_time_conversion', V('equation'), ('solve_time_conversion',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],
                    ]
    ),
}

def htn_nursing_calculation_military_to_standard_time_kc_mapping():
    #Under the assumption it's equal to Knowledge Components
    kcs = {
        'solve_time_conversion': 'solve_time_conversion',
        'done': 'done'
    }

    return kcs


def htn_nursing_calculation_military_to_standard_time_studymaterial():
    study_material = studymaterial["military_to_standard_time"]
    return study_material




def htn_nursing_calculation_military_to_standard_time_intermediate_hints():
    hints = {
        "solve_time_conversion": [
            "Combine the converted hour and minutes with AM/PM to get the final time."
        ],
        "done": [
            "Once you have found the final HH:MM form you can select the done button to move to the next problem."
        ]
    }
    return hints


htn_loaded_models.register(HTNCognitiveModel('htn_nursing_military',    
                                             'htn_nursing_calculation_military_to_standard_time',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                            htn_nursing_calculation_military_to_standard_time_problem,
                                            htn_nursing_calculation_military_to_standard_time_kc_mapping(),
                                            htn_nursing_calculation_military_to_standard_time_intermediate_hints(),
                                            htn_nursing_calculation_military_to_standard_time_studymaterial()))