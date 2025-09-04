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
def htn_nursing_calculation_standard_time_to_military_problem():
    hour = randint(1, 12) 
    minute = randint(1, 59)  
    am_pm = randint(0, 1)
    vals = ["AM", "PM"]
    standard_time = f"{hour:02d}:{minute:02d} {vals[am_pm]}"
    words = f"Convert the standard 12-hour AM/PM time {standard_time} to military time."
    prob = [standard_time, hour, minute, vals[am_pm], 0, words]
    return prob



def solve_time_conversion(init_value):
    prob = init_value.split(",")
    hour = int(prob[1])
    minutes = f"{int(prob[2]):02d}"
    am_pm = prob[3] 
    # print(f"Hour: {hour} + Minutes: {minutes} + AM/PM: {am_pm}")
    if am_pm == "PM" and hour != 12:
        hour += 12
        
    elif am_pm == "AM" and hour == 12:
        hour = 0  
    final_time = f"{hour:02d}:{minutes}"
    # print(final_time)
    # final_time = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', final_time)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(final_time)), final_time)])
    #escapes the colon, looks for the exact colon character
    





    

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

def htn_nursing_calculation_standard_time_to_military_kc_mapping():
    #Under the assumption it's equal to Knowledge Components
    kcs = {
        'solve_time_conversion': 'solve_time_conversion',
        'done': 'done'
    }

    return kcs


def htn_nursing_calculation_standard_time_to_military_studymaterial():
    study_material = studymaterial["standard_to_military_time"]
    return study_material




def htn_nursing_calculation_standard_time_to_military_intermediate_hints():
    hints = {
        "solve_time_conversion": [
        "Remember, if it's AM, then the hour remains the same unless it's 12 AM, which becomes 00 in military time. However, If it's PM, add 12 to the hour unless it's 12 PM, which remains 12 in military time.",
        ],
        "done": [
            "Once you have found the final HH:MM military time you can select the done button to move to the next problem."
        ]
    }
    return hints


htn_loaded_models.register(HTNCognitiveModel('htn_nursing_military',    
                                             'htn_nursing_calculation_standard_time_to_military',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                            htn_nursing_calculation_standard_time_to_military_problem,
                                            htn_nursing_calculation_standard_time_to_military_kc_mapping(),
                                            htn_nursing_calculation_standard_time_to_military_intermediate_hints(),
                                            htn_nursing_calculation_standard_time_to_military_studymaterial()))