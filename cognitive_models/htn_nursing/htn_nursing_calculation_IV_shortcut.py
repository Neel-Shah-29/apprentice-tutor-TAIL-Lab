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

def htn_nursing_calculation_IV_shortcut_problem():
    # Define possible time intervals and drop factors
    time_options = [30, 60, 90, 120, 150, 180, 210, 240]  # Time in minutes (30 min, 1 hr, 2 hrs, 4 hrs)
    drop_factors_constant = [60, 20, 15, 12, 10]  # Possible drop factors (gtt/mL)
    
    # Pick a random time and drop factor
    time_in_minutes = choice(time_options)
    drop_factor_choice = choice(drop_factors_constant)
    
    # Ensure that volume results in a nice, whole gtt/min when using the formula
    def generate_nice_volume():
        # We want (60 * volume / time) / (60 / drop_factor) to be a whole number
        # Rearranging: volume = (gtt_per_min * time) / drop_factor
        gtt_per_min = randint(1, 50)  # Random whole number gtt/min
        volume = gtt_per_min * time_in_minutes / drop_factor_choice
        return volume, gtt_per_min
    
    # Generate a volume and ensure it's an integer
    volume, gtt_per_min = generate_nice_volume()
    
    # Create the word problem
    problem_statement = (f"The order is for {volume} mL to be infused in {time_in_minutes} minutes. "
                         f"The drop factor is {drop_factor_choice} gtt/mL. "
                         f"How many gtt/min will be administered?")
    
    # Return the problem and solution
    return [problem_statement, volume, time_in_minutes, drop_factor_choice, gtt_per_min]


def final_answer_numerator_units(init_value):
    answer = 'drops'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

def final_answer_denominator_units(init_value):
    answer = 'minute'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

def supply_numerator(init_value):
    answer = init_value.split(',')[1]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def supply_numerator_units(init_value):
    answer = 'mL'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

def supply_denominator(init_value):
    answer = init_value.split(',')[2]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def supply_denominator_units(init_value):
    answer = 'minutes'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

def order_numerator(init_value):
    answer = 'x'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

def order_numerator_units(init_value):
    answer = 'mL'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

def order_denominator(init_value):
    answer = '60'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def order_denominator_units(init_value):
    answer = 'minutes'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

def cross_multiply_left_side(init_value):
    answer = init_value.split(',')[2] + 'x'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

def cross_multiply_right_side(init_value):
    # print('cross multiply left side')
    answer = 60 * int(init_value.split(',')[1])
    hint = answer
    # print(answer)
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', str(answer))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def solve_x_left_side(init_value):
    answer = 'x'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

def solve_x_right_side(init_value):
    answer = int(60 * int(init_value.split(',')[1]) / int(init_value.split(',')[2]))
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', str(answer))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def drop_factor(init_value):
    answer = init_value.split(',')[3]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def drop_factor_constant(init_value):
    answer = int(60 / int(init_value.split(',')[3]))
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', str(answer))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def divide_by_constant(init_value):
    right_side = 60 * int(init_value.split(',')[1]) / int(init_value.split(',')[2])
    drop_factor = 60 / int(init_value.split(',')[3])
    answer = int(right_side / drop_factor)
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', str(answer))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def final_answer(init_value):
    answer = init_value.split(',')[4]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', str(answer))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

Domain = {
    'done': Operator(head=('done', V('kc')),
                     precondition=[Fact(start=True)],
                     effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
    ),
    'final_answer_denominator_units': Operator(head=('final_answer_denominator_units', V('equation'), V('kc')),
                        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                        effects=[Fact(field='final_answer_denominator_units', value=(final_answer_denominator_units, V('eq')), kc=V('kc'), answer=True)],
    ),

    'final_answer_numerator_units': Operator(head=('final_answer_numerator_units', V('equation'), V('kc')),
                        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                        effects=[Fact(field='final_answer_numerator_units', value=(final_answer_numerator_units, V('eq')), kc=V('kc'), answer=True)],
    ),

    'supply_numerator': Operator(head=('supply_numerator', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='supply_numerator', value=(supply_numerator, V('eq')), kc=V('kc'), answer=True)],
    ),

    'supply_numerator_units': Operator(head=('supply_numerator_units', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='supply_numerator_units', value=(supply_numerator_units, V('eq')), kc=V('kc'), answer=True)],
    ),

    'supply_denominator': Operator(head=('supply_denominator', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='supply_denominator', value=(supply_denominator, V('eq')), kc=V('kc'), answer=True)],
    ),

    'supply_denominator_units': Operator(head=('supply_denominator_units', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='supply_denominator_units', value=(supply_denominator_units, V('eq')), kc=V('kc'), answer=True)],
    ),

    'order_numerator': Operator(head=('order_numerator', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='order_numerator', value=(order_numerator, V('eq')), kc=V('kc'), answer=True)],
    ),

    'order_numerator_units': Operator(head=('order_numerator_units', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='order_numerator_units', value=(order_numerator_units, V('eq')), kc=V('kc'), answer=True)],
    ),

    'order_denominator': Operator(head=('order_denominator', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='order_denominator', value=(order_denominator, V('eq')), kc=V('kc'), answer=True)],
    ),

    'order_denominator_units': Operator(head=('order_denominator_units', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='order_denominator_units', value=(order_denominator_units, V('eq')), kc=V('kc'), answer=True)],
    ),

    'cross_multiply_left_side': Operator(head=('cross_multiply_left_side', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='cross_multiply_left_side', value=(cross_multiply_left_side, V('eq')), kc=V('kc'), answer=True)],
    ),

    'cross_multiply_right_side': Operator(head=('cross_multiply_right_side', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='cross_multiply_right_side', value=(cross_multiply_right_side, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve_x_left_side': Operator(head=('solve_x_left_side', V('equation'), V('kc')),
                           precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                           effects=[Fact(field='solve_x_left_side', value=(solve_x_left_side, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve_x_right_side': Operator(head=('solve_x_right_side', V('equation'), V('kc')),
                           precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                           effects=[Fact(field='solve_x_right_side', value=(solve_x_right_side, V('eq')), kc=V('kc'), answer=True)],
    ),

    'drop_factor': Operator(head=('drop_factor', V('equation'), V('kc')),
                           precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                           effects=[Fact(field='drop_factor', value=(drop_factor, V('eq')), kc=V('kc'), answer=True)],
    ),

    'drop_factor_constant': Operator(head=('drop_factor_constant', V('equation'), V('kc')),
                           precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                           effects=[Fact(field='drop_factor_constant', value=(drop_factor_constant, V('eq')), kc=V('kc'), answer=True)],
    ),

    'divide_by_constant': Operator(head=('divide_by_constant', V('equation'), V('kc')),
                           precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                           effects=[Fact(field='divide_by_constant', value=(divide_by_constant, V('eq')), kc=V('kc'), answer=True)],
    ),

    'final_answer': Operator(head=('final_answer', V('equation'), V('kc')),
                           precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                           effects=[Fact(field='final_answer', value=(final_answer, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve': Method(head=('solve', V('equation')),
                    preconditions=[
                        Fact(scaffold='level_6'),
                        Fact(scaffold='level_5'),
                        Fact(scaffold='level_4'),
                        Fact(scaffold='level_3'),
                        Fact(scaffold='level_2'),
                        Fact(scaffold='level_1'),
                        Fact(scaffold='level_0'),
                    ],
                    subtasks=[

                        [
                            Task(head=('final_answer_numerator_units', V('equation'), ('final_answer_numerator_units',)), primitive=True),
                            Task(head=('final_answer_denominator_units', V('equation'), ('final_answer_denominator_units',)), primitive=True),
                            Task(head=('supply_numerator', V('equation'), ('supply_numerator',)), primitive=True),
                            Task(head=('supply_numerator_units', V('equation'), ('supply_numerator_units',)), primitive=True),
                            Task(head=('supply_denominator', V('equation'), ('supply_denominator',)), primitive=True),
                            Task(head=('supply_denominator_units', V('equation'), ('supply_denominator_units',)), primitive=True),
                            Task(head=('order_numerator', V('equation'), ('order_numerator',)), primitive=True),
                            Task(head=('order_numerator_units', V('equation'), ('order_numerator_units',)), primitive=True),
                            Task(head=('order_denominator', V('equation'), ('order_denominator',)), primitive=True),
                            Task(head=('order_denominator_units', V('equation'), ('order_denominator_units',)), primitive=True),
                            Task(head=('cross_multiply_left_side', V('equation'), ('cross_multiply_left_side',)), primitive=True),
                            Task(head=('cross_multiply_right_side', V('equation'), ('cross_multiply_right_side',)), primitive=True),
                            Task(head=('solve_x_left_side', V('equation'), ('solve_x_left_side',)), primitive=True),
                            Task(head=('solve_x_right_side', V('equation'), ('solve_x_right_side',)), primitive=True),
                            Task(head=('drop_factor', V('equation'), ('drop_factor',)), primitive=True),
                            Task(head=('drop_factor_constant', V('equation'), ('drop_factor_constant',)), primitive=True),
                            Task(head=('divide_by_constant', V('equation'), ('divide_by_constant',)), primitive=True),
                            Task(head=('final_answer', V('equation'), ('final_answer',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('final_answer_numerator_units', V('equation'), ('final_answer_numerator_units',)), primitive=True),
                            Task(head=('final_answer_denominator_units', V('equation'), ('final_answer_denominator_units',)), primitive=True),
                            Task(head=('supply_numerator', V('equation'), ('supply_numerator',)), primitive=True),
                            Task(head=('supply_numerator_units', V('equation'), ('supply_numerator_units',)), primitive=True),
                            Task(head=('supply_denominator', V('equation'), ('supply_denominator',)), primitive=True),
                            Task(head=('supply_denominator_units', V('equation'), ('supply_denominator_units',)), primitive=True),
                            Task(head=('order_numerator', V('equation'), ('order_numerator',)), primitive=True),
                            Task(head=('order_numerator_units', V('equation'), ('order_numerator_units',)), primitive=True),
                            Task(head=('order_denominator', V('equation'), ('order_denominator',)), primitive=True),
                            Task(head=('order_denominator_units', V('equation'), ('order_denominator_units',)), primitive=True),
                            Task(head=('cross_multiply_left_side', V('equation'), ('cross_multiply_left_side',)), primitive=True),
                            Task(head=('cross_multiply_right_side', V('equation'), ('cross_multiply_right_side',)), primitive=True),
                            Task(head=('solve_x_left_side', V('equation'), ('solve_x_left_side',)), primitive=True),
                            Task(head=('solve_x_right_side', V('equation'), ('solve_x_right_side',)), primitive=True),
                            Task(head=('drop_factor', V('equation'), ('drop_factor',)), primitive=True),
                            Task(head=('drop_factor_constant', V('equation'), ('drop_factor_constant',)), primitive=True),
                            Task(head=('final_answer', V('equation'), ('final_answer',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('final_answer_numerator_units', V('equation'), ('final_answer_numerator_units',)), primitive=True),
                            Task(head=('final_answer_denominator_units', V('equation'), ('final_answer_denominator_units',)), primitive=True),
                            Task(head=('supply_numerator', V('equation'), ('supply_numerator',)), primitive=True),
                            Task(head=('supply_numerator_units', V('equation'), ('supply_numerator_units',)), primitive=True),
                            Task(head=('supply_denominator', V('equation'), ('supply_denominator',)), primitive=True),
                            Task(head=('supply_denominator_units', V('equation'), ('supply_denominator_units',)), primitive=True),
                            Task(head=('order_numerator', V('equation'), ('order_numerator',)), primitive=True),
                            Task(head=('order_numerator_units', V('equation'), ('order_numerator_units',)), primitive=True),
                            Task(head=('order_denominator', V('equation'), ('order_denominator',)), primitive=True),
                            Task(head=('order_denominator_units', V('equation'), ('order_denominator_units',)), primitive=True),
                            Task(head=('cross_multiply_left_side', V('equation'), ('cross_multiply_left_side',)), primitive=True),
                            Task(head=('cross_multiply_right_side', V('equation'), ('cross_multiply_right_side',)), primitive=True),
                            Task(head=('solve_x_left_side', V('equation'), ('solve_x_left_side',)), primitive=True),
                            Task(head=('solve_x_right_side', V('equation'), ('solve_x_right_side',)), primitive=True),
                            Task(head=('final_answer', V('equation'), ('final_answer',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],
                        [
                            Task(head=('final_answer_numerator_units', V('equation'), ('final_answer_numerator_units',)), primitive=True),
                            Task(head=('final_answer_denominator_units', V('equation'), ('final_answer_denominator_units',)), primitive=True),
                            Task(head=('supply_numerator', V('equation'), ('supply_numerator',)), primitive=True),
                            Task(head=('supply_numerator_units', V('equation'), ('supply_numerator_units',)), primitive=True),
                            Task(head=('supply_denominator', V('equation'), ('supply_denominator',)), primitive=True),
                            Task(head=('supply_denominator_units', V('equation'), ('supply_denominator_units',)), primitive=True),
                            Task(head=('order_numerator', V('equation'), ('order_numerator',)), primitive=True),
                            Task(head=('order_numerator_units', V('equation'), ('order_numerator_units',)), primitive=True),
                            Task(head=('order_denominator', V('equation'), ('order_denominator',)), primitive=True),
                            Task(head=('order_denominator_units', V('equation'), ('order_denominator_units',)), primitive=True),
                            Task(head=('cross_multiply_left_side', V('equation'), ('cross_multiply_left_side',)), primitive=True),
                            Task(head=('cross_multiply_right_side', V('equation'), ('cross_multiply_right_side',)), primitive=True),
                            Task(head=('final_answer', V('equation'), ('final_answer',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('final_answer_numerator_units', V('equation'), ('final_answer_numerator_units',)), primitive=True),
                            Task(head=('final_answer_denominator_units', V('equation'), ('final_answer_denominator_units',)), primitive=True),
                            Task(head=('supply_numerator', V('equation'), ('supply_numerator',)), primitive=True),
                            Task(head=('supply_numerator_units', V('equation'), ('supply_numerator_units',)), primitive=True),
                            Task(head=('supply_denominator', V('equation'), ('supply_denominator',)), primitive=True),
                            Task(head=('supply_denominator_units', V('equation'), ('supply_denominator_units',)), primitive=True),
                            Task(head=('order_numerator', V('equation'), ('order_numerator',)), primitive=True),
                            Task(head=('order_numerator_units', V('equation'), ('order_numerator_units',)), primitive=True),
                            Task(head=('order_denominator', V('equation'), ('order_denominator',)), primitive=True),
                            Task(head=('order_denominator_units', V('equation'), ('order_denominator_units',)), primitive=True),
                            Task(head=('final_answer', V('equation'), ('final_answer',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('final_answer_numerator_units', V('equation'), ('final_answer_numerator_units',)), primitive=True),
                            Task(head=('final_answer_denominator_units', V('equation'), ('final_answer_denominator_units',)), primitive=True),
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

def htn_nursing_calculation_IV_shortcut_kc_mapping():

    kcs = {
        'final_answer_numerator_units': 'final_answer_numerator_units',
        'final_answer_denominator_units': 'final_answer_denominator_units',
        'supply_numerator': 'supply_numerator',
        'supply_numerator_units': 'supply_numerator_units',
        'supply_denominator': 'supply_denominator',
        'supply_denominator_units': 'supply_denominator_units',
        'order_numerator': 'order_numerator',
        'order_numerator_units': 'order_numerator_units',
        'order_denominator': 'order_denominator',
        'order_denominator_units': 'order_denominator_units',
        'cross_multiply_left_side': 'cross_multiply_left_side',
        'cross_multiply_right_side': 'cross_multiply_right_side',
        'solve_x_left_side': 'solve_x_left_side',
        'solve_x_right_side': 'solve_x_right_side',
        'drop_factor': 'drop_factor',
        'drop_factor_constant': 'drop_factor_constant',
        'divide_by_constant': 'divide_by_constant',
        'final_answer': 'final_answer',
        'done': 'done'
    }

    return kcs




def htn_nursing_calculation_IV_shortcut_intermediate_hints():
    hints = {
        "final_answer_numerator_units": [
            "What unit will the nurse administer?"],
        "final_answer_denominator_units": [
            "When will the nurse administer the medicine?"],
        "supply_numerator": [
            "This is the number ordered by the doctor."],
        "supply_numerator_units": [
            "What unit did the doctor order?"],
        'supply_denominator': ["How long is the infusion?"],
        'supply_denominator_units': ["What units does the problem use to measure time?"],
        'order_numerator': ["We do not know this part. What do we use for an unknown value?"],
        'order_numerator_units': ["These units should match the order."],
        'order_denominator': ["This will always be 60 minutes."],
        'order_denominator_units': ["This unit should match the order."],
        'cross_multiply_left_side': ['Multiply the order\'s numerator by the other fraction\'s denominator.'],
        'cross_multiply_right_side': ['Multiply the order\'s denominator by the other fractions\'s numerator.'],
        'solve_x_left_side': ['Divide by the coefficient of x.'],
        'solve_x_right_side': ['Divide by the coefficient of x.'],
        'drop_factor': ['Identify the drop factor given in the problem.'],
        'drop_factor_constant': ['The drop factor constant is 60 divided by the drop factor'],
        'divide_by_constant': ['Divide what x equals by the drop factor constant.'],
        'final_answer': ['What is your final result?'],
        'done': ["Once you have identified all relevant information you can"
                        " select the done button to move to the next problem."],
    }
    return hints

def htn_nursing_calculation_IV_shortcut_studymaterial():
    study_material = studymaterial["drug_calculations"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_nursing_iv_therapy',    
                                             'htn_nursing_calculation_IV_shortcut',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_nursing_calculation_IV_shortcut_problem,
                                             htn_nursing_calculation_IV_shortcut_kc_mapping(),
                                             htn_nursing_calculation_IV_shortcut_intermediate_hints(),
                                             htn_nursing_calculation_IV_shortcut_studymaterial()))