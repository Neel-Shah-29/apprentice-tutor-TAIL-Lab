import sympy as sp
from random import randint, choice

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
from random import random
from functools import reduce

def htn_nursing_calculation_drug_calc_iv_problem():
    # Define possible time intervals and drop factors
    time_options = [1, 2, 3, 4, 6, 8, 12]  # Time in hours (30 min, 1 hr, 2 hrs, 4 hrs)
    drop_factors_constant = [60, 20, 15, 12, 10]  # Possible drop factors (gtt/mL)
    
    # Pick a random time and drop factor
    time_in_hours = choice(time_options)
    drop_factor_choice = choice(drop_factors_constant)
    
    # Ensure that volume results in a nice, whole gtt/min when using the formula
    def generate_nice_volume():
        # We want (60 * volume / time) / (60 / drop_factor) to be a whole number
        # Rearranging: volume = (gtt_per_min * time) / drop_factor
        gtt_per_min = choice(range(5, 61, 5))  # Random whole number gtt/min
        volume = gtt_per_min * time_in_hours * 60 / drop_factor_choice
        return volume, gtt_per_min
    
    # Generate a volume and ensure it's an integer
    volume, gtt_per_min = generate_nice_volume()
    
    def strip_trailing_zero(val):
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        return str(val)
    # Create the word problem
    if drop_factor_choice == 60:
        infusion_text = f"to be infused over {strip_trailing_zero(time_in_hours)} hours using micro drip tubing"
        drop_factor_text = ""
    else:
        infusion_text = f"to be infused over {strip_trailing_zero(time_in_hours)} hours"
        drop_factor_text = f"The drop factor is {drop_factor_choice} gtt/mL. "

    problem_statement = (
        f"The order is for {strip_trailing_zero(volume)} mL {infusion_text}. "
        f"{drop_factor_text}"
        f"How many gtt/min will be administered?"
    )
    
    # Return the problem and solution
    return [problem_statement, volume, time_in_hours, drop_factor_choice, gtt_per_min]


def convert_hours_to_minutes(init_value):
    hours = init_value.split(',')[2]
    minutes = int(hours) * 60
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', str(minutes))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), str(answer))])


def fill_in_volume(init_value):
    answer = init_value.split(',')[1]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def fill_in_time(init_value):
    answer = int(init_value.split(',')[2]) * 60
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', str(answer))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), str(hint))])

def fill_in_drop_factor(init_value):
    answer = init_value.split(',')[3]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def multiply_numerator(init_value):
    answer = int(init_value.split(',')[1]) * int(init_value.split(',')[3])
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', str(answer))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def multiply_denominator(init_value):
    answer = int(init_value.split(',')[2]) * 60
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', str(answer))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def final_answer(init_value):
    answer = round(int(init_value.split(',')[4]))
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', str(answer))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

Domain = {
    'done': Operator(head=('done', V('kc')),
                     precondition=[Fact(start=True)],
                     effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
    ),

    'convert_hours_to_minutes': Operator(head=('convert_hours_to_minutes', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='convert_hours_to_minutes', value=(convert_hours_to_minutes, V('eq')), kc=V('kc'), answer=True)],
    ),

    'fill_in_volume': Operator(head=('fill_in_volume', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='fill_in_volume', value=(fill_in_volume, V('eq')), kc=V('kc'), answer=True)],
    ),

    'fill_in_time': Operator(head=('fill_in_time', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='fill_in_time', value=(fill_in_time, V('eq')), kc=V('kc'), answer=True)],
    ),

    'fill_in_drop_factor': Operator(head=('fill_in_drop_factor', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='fill_in_drop_factor', value=(fill_in_drop_factor, V('eq')), kc=V('kc'), answer=True)],
    ),

    'multiply_numerator': Operator(head=('multiply_numerator', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='multiply_numerator', value=(multiply_numerator, V('eq')), kc=V('kc'), answer=True)],
    ),

    'multiply_denominator': Operator(head=('multiply_denominator', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='multiply_denominator', value=(multiply_denominator, V('eq')), kc=V('kc'), answer=True)],
    ),

    'final_answer': Operator(head=('final_answer', V('equation'), V('kc')),
                           precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                           effects=[Fact(field='final_answer', value=(final_answer, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve': Method(head=('solve', V('equation')),
                    preconditions=[
                        Fact(scaffold='level_3'),
                        Fact(scaffold='level_2'),
                        Fact(scaffold='level_1'),
                        Fact(scaffold='level_0'),
                    ],
                    subtasks=[

                        [
                            Task(head=('convert_hours_to_minutes', V('equation'), ('convert_hours_to_minutes',)), primitive=True),
                            Task(head=('fill_in_volume', V('equation'), ('fill_in_volume',)), primitive=True),
                            Task(head=('fill_in_time', V('equation'), ('fill_in_time',)), primitive=True),
                            Task(head=('fill_in_drop_factor', V('equation'), ('fill_in_drop_factor',)), primitive=True),
                            Task(head=('multiply_numerator', V('equation'), ('multiply_numerator',)), primitive=True),
                            Task(head=('multiply_denominator', V('equation'), ('multiply_denominator',)), primitive=True),
                            Task(head=('final_answer', V('equation'), ('final_answer',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('convert_hours_to_minutes', V('equation'), ('convert_hours_to_minutes',)), primitive=True),
                            Task(head=('fill_in_volume', V('equation'), ('fill_in_volume',)), primitive=True),
                            Task(head=('fill_in_time', V('equation'), ('fill_in_time',)), primitive=True),
                            Task(head=('fill_in_drop_factor', V('equation'), ('fill_in_drop_factor',)), primitive=True),
                            Task(head=('final_answer', V('equation'), ('final_answer',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('convert_hours_to_minutes', V('equation'), ('convert_hours_to_minutes',)), primitive=True),
                            Task(head=('final_answer', V('equation'), ('final_answer',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],
                        [
                            Task(head=('final_answer', V('equation'), ('final_answer',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],
                    ]
    ),
}

def htn_nursing_calculation_drug_calc_iv_kc_mapping():

    kcs = {
        'convert_hours_to_minutes':'convert_hours_to_minutes',
        'fill_in_volume': 'fill_in_volume',
        'fill_in_time': 'fill_in_time',
        'fill_in_drop_factor': 'fill_in_drop_factor',
        'fill_in_one': 'fill_in_one',
        'multiply_numerator': 'multiply_numerator',
        'multiply_denominator': 'multiply_denominator',
        'final_answer': 'final_answer',
        'done': 'done'
    }

    return kcs




def htn_nursing_calculation_drug_calc_iv_intermediate_hints():
    hints = {
        'convert_hours_to_minutes': ['Multiply the number of hours by 60 to calculate minutes'],
        'fill_in_volume': ['How many mLs are to be infused?'],
        'fill_in_time': ['How long is the infusion?'],
        'fill_in_drop_factor': ['What is the drop factor?'],
        'multiply_numerator': ['Multiply the volume by the drop factor.'],
        'multiply_denominator': ['Enter the time.'],
        'final_answer': ['Divide the numerator by the denominator.'],
        'done': ["Once you have identified all relevant information you can"
                        " select the done button to move to the next problem."]
    }
    return hints

def htn_nursing_calculation_drug_calc_iv_studymaterial():
    study_material = studymaterial["drug_calculations"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_nursing_formula_method',    
                                             'htn_nursing_calculation_drug_calc_iv',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_nursing_calculation_drug_calc_iv_problem,
                                             htn_nursing_calculation_drug_calc_iv_kc_mapping(),
                                             htn_nursing_calculation_drug_calc_iv_intermediate_hints(),
                                             htn_nursing_calculation_drug_calc_iv_studymaterial()))