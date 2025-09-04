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

def htn_nursing_calculation_proportion_IV_heparin_problem():
    units = ['L', 'mL']
    u1 = 'units'
    u2 = 'hour'
    n1 = 1500
    n2 = 20000
    u3 = 'L'
    print (n1, u1, n2, u2, u3)
    words = f"A newly admitted patient has an order for IV heparin to infuse at {n1} {u1} per {u2}. The solution is supplied with {n2} {u1} of heparin in 1 {u3} of D5W. What is the mL/hr?"
    prob = [words, n1, u1, n2, u2, u3]
    return prob


def final_answer_numerator_units(init_value):
    answer = 'mL'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), answer)])

def final_answer_denominator_units(init_value):
    answer = 'hours'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), answer)])

def yes_convert(init_value):
    answer = 'checked'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), answer)])

def no_convert(init_value):
    answer = 'unchecked'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), answer)])

def convert_value1(init_value):
    answer = '1'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), answer)])

def convert_unit1(init_value):
    answer = 'L'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), answer)])

def convert_value2(init_value):
    answer = '1000'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), answer)])

def convert_unit2(init_value):
    answer = 'mL'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), answer)])

def supply_numerator(init_value):
    answer = '20000'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), answer)])

def supply_numerator_units(init_value):
    answer = 'units'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), answer)])

def supply_denominator(init_value):
    answer = '1000'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), answer)])

def supply_denominator_units(init_value):
    answer = 'mL'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), answer)])

def order_numerator(init_value):
    answer = '1500'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), answer)])

def order_numerator_units(init_value):
    answer = 'units'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), answer)])

def order_denominator(init_value):
    answer = 'x'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), answer)])

def order_denominator_units(init_value):
    answer = 'mL'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), answer)])

def cross_multiply_left_side(init_value):
    answer = '20000x'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), answer)])

def cross_multiply_right_side(init_value):
    answer = '1500000'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), answer)])

def solve_x_left_side(init_value):
    answer = 'x'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), answer)])

def solve_x_right_side(init_value):
    answer = '75'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), answer)])

def final_answer(init_value):
    answer = '75'
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), answer)])

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

    'yes_convert': Operator(head=('yes_convert', V('equation'), V('kc')),
                        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                        effects=[Fact(field='yes_convert', value=(yes_convert, V('eq')), kc=V('kc'), answer=True)],
    ),

    'no_convert': Operator(head=('no_convert', V('equation'), V('kc')),
                        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                        effects=[Fact(field='no_convert', value=(no_convert, V('eq')), kc=V('kc'), answer=True)],
    ),

    'convert_value1': Operator(head=('convert_value1', V('equation'), V('kc')),
                        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                        effects=[Fact(field='convert_value1', value=(convert_value1, V('eq')), kc=V('kc'), answer=True)],
    ),

    'convert_unit1': Operator(head=('convert_unit1', V('equation'), V('kc')),
                        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                        effects=[Fact(field='convert_unit1', value=(convert_unit1, V('eq')), kc=V('kc'), answer=True)],
    ),

    'convert_value2': Operator(head=('convert_value2', V('equation'), V('kc')),
                        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                        effects=[Fact(field='convert_value2', value=(convert_value2, V('eq')), kc=V('kc'), answer=True)],
    ),

    'convert_unit2': Operator(head=('convert_unit2', V('equation'), V('kc')),
                        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                        effects=[Fact(field='convert_unit2', value=(convert_unit2, V('eq')), kc=V('kc'), answer=True)],
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

    'final_answer': Operator(head=('final_answer', V('equation'), V('kc')),
                           precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                           effects=[Fact(field='final_answer', value=(final_answer, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve': Method(head=('solve', V('equation')),
                    preconditions=[
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
                            # Task(head=('yes_convert', V('equation'), ('yes_convert',)), primitive=True),
                            Task(head=('convert_value1', V('equation'), ('convert_value1',)), primitive=True),
                            Task(head=('convert_unit1', V('equation'), ('convert_unit1',)), primitive=True),
                            Task(head=('convert_value2', V('equation'), ('convert_value2',)), primitive=True),
                            Task(head=('convert_unit2', V('equation'), ('convert_unit2',)), primitive=True),
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
                            # Task(head=('yes_convert', V('equation'), ('yes_convert',)), primitive=True),
                            Task(head=('convert_value1', V('equation'), ('convert_value1',)), primitive=True),
                            Task(head=('convert_unit1', V('equation'), ('convert_unit1',)), primitive=True),
                            Task(head=('convert_value2', V('equation'), ('convert_value2',)), primitive=True),
                            Task(head=('convert_unit2', V('equation'), ('convert_unit2',)), primitive=True),
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
                            # Task(head=('yes_convert', V('equation'), ('yes_convert',)), primitive=True),
                            Task(head=('convert_value1', V('equation'), ('convert_value1',)), primitive=True),
                            Task(head=('convert_unit1', V('equation'), ('convert_unit1',)), primitive=True),
                            Task(head=('convert_value2', V('equation'), ('convert_value2',)), primitive=True),
                            Task(head=('convert_unit2', V('equation'), ('convert_unit2',)), primitive=True),
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
                            # Task(head=('yes_convert', V('equation'), ('yes_convert',)), primitive=True),
                            Task(head=('convert_value1', V('equation'), ('convert_value1',)), primitive=True),
                            Task(head=('convert_unit1', V('equation'), ('convert_unit1',)), primitive=True),
                            Task(head=('convert_value2', V('equation'), ('convert_value2',)), primitive=True),
                            Task(head=('convert_unit2', V('equation'), ('convert_unit2',)), primitive=True),
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

def htn_nursing_calculation_proportion_IV_heparin_kc_mapping():

    kcs = {
        'final_answer_numerator_units': 'final_answer_numerator_units',
        'final_answer_denominator_units': 'final_answer_denominator_units',
        'yes_convert': 'yes_convert',
        'no_convert': 'no_convert',
        'convert_value1': 'convert_value1',
        'convert_unit1': 'convert_unit1',
        'convert_value2': 'convert_value2',
        'convert_unit2': 'convert_unit2',
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
        'final_answer': 'final_answer',
        'done': 'done'
    }

    return kcs




def htn_nursing_calculation_proportion_IV_heparin_intermediate_hints():
    hints = {
        "final_answer_numerator_units": [
            "The a value is extracted from the first term of the trinomial."],
        "final_answer_denominator_units": [
            "The b value is extracted from the middle term of the trinomial."],
        "frac1_numerator": [
            "The c value is extracted from the last term of the trinomial."],
        "frac1_denominator": [
            "The ac value is computed by multiplying a times c."],
        'frac2_numerator': ["Enter a factor of ac."],
        'frac2_denominator': ["Enter the value that when multipled with"
                                  " the other factor yields ac."],
        'p_value': ["This is one of the factors from the table"
                            " above."],
        'q_value': ["This is the other factor from the table above."],

        'first_part': [
            "This group has the form ax^2 + px."],
        'second_part': [
            "This group has the form qx + c."],
        'gcf_1_factor': ['Factor the greatest common factor out of the first'
                      ' group of terms.'],
        'gcf_2_factor': ['Factor the greatest common factor out of the second'
                      ' group of terms.'],
        'gcf_1_final': ['Enter the greatest common factor of the two'
                        ' factored groups of terms.'],
        'gcf_2_final': ['Enter the terms that remain after factoring the'
                        ' greatest common factor out of the two factored'
                        ' groups of terms.'],
        'final_answer': ["The final factored form is the"
                                " combination of the two expressions."],
        'done': ["Once you have found the final factored form you can"
                        " select the done button to move to the next problem."]
    }
    return hints

def htn_nursing_calculation_proportion_IV_heparin_studymaterial():
    study_material = studymaterial["drug_calculations"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_nursing_heparin',    
                                             'htn_nursing_calculation_proportion_IV_heparin',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_nursing_calculation_proportion_IV_heparin_problem,
                                             htn_nursing_calculation_proportion_IV_heparin_kc_mapping(),
                                             htn_nursing_calculation_proportion_IV_heparin_intermediate_hints(),
                                             htn_nursing_calculation_proportion_IV_heparin_studymaterial()))