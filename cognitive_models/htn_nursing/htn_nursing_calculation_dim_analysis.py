import sympy as sp
from random import randint, choice

import sympy as sp
from sympy import sstr, latex, symbols, Eq, solve
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re
import ast

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
from random import random, choice, uniform, shuffle
from functools import reduce

from random import choice, shuffle
import math

def htn_nursing_calculation_dim_analysis_problem():
    ROUTES = {
        "oral_tablet": {
            "unit": "tablets",
            "max_per_dose": 4.0,
            "answer_step": 0.5,
            "strength_unit": "mg/tablet",
            "unit_den_choices": [1], 
            "mg_choices": [25, 50, 75, 100, 150, 200],
            "route_pretty": "orally (PO)",
        },
        "subcutaneous": {
            "unit": "mL",
            "max_per_dose": 2.0,
            "answer_step": 0.1,
            "strength_unit": "mg/mL",
            "unit_den_choices": [1, 2, 5],
            "mg_choices": [5, 10, 20, 25, 50, 100],
            "route_pretty": "subcutaneously",
        },
        "im_deltoid": {
            "unit": "mL",
            "max_per_dose": 1.0,  # conservative adult limit
            "answer_step": 0.1,
            "strength_unit": "mg/mL",
            "unit_den_choices": [1, 2, 5],
            "mg_choices": [5, 10, 20, 25, 50, 100],
            "route_pretty": "intramuscularly (deltoid)",
        },
        "im_ventrogluteal": {
            "unit": "mL",
            "max_per_dose": 3.0,
            "answer_step": 0.1,
            "strength_unit": "mg/mL",
            "unit_den_choices": [1, 2, 5],
            "mg_choices": [5, 10, 20, 25, 50, 100],
            "route_pretty": "intramuscularly (ventrogluteal)",
        },
        "im_vastus": {
            "unit": "mL",
            "max_per_dose": 3.0,
            "answer_step": 0.1,
            "strength_unit": "mg/mL",
            "unit_den_choices": [1, 2, 5],
            "mg_choices": [5, 10, 20, 25, 50, 100],
            "route_pretty": "intramuscularly (vastus lateralis)",
        },
        "intravenous_bolus": {
            "unit": "mL",
            "max_per_dose": 100.0,  # arbitrary large, depends on drug
            "answer_step": 0.5,
            "strength_unit": "mg/mL",
            "unit_den_choices": [1, 5, 10],
            "mg_choices": [5, 10, 20, 50, 100],
            "route_pretty": "intravenously (bolus/push)",
        },
        "intravenous_infusion": {
            "unit": "mL",
            "max_per_dose": 1000.0,
            "answer_step": 10.0,
            "strength_unit": "mg/mL",
            "unit_den_choices": [1, 5, 10, 50],
            "mg_choices": [1, 2, 5, 10, 20, 50],
            "route_pretty": "intravenously (infusion)",
        },
        "rectal": {
            "unit": "mL",
            "max_per_dose": 60.0,
            "answer_step": 1.0,
            "strength_unit": "mg/mL",
            "unit_den_choices": [1, 5, 10],
            "mg_choices": [5, 10, 20, 50],
            "route_pretty": "rectally (PR)",
        },
        "otic": {
            "unit": "drops",
            "max_per_dose": 10.0,
            "answer_step": 1.0,
            "strength_unit": "mg/drop",
            "unit_den_choices": [1],
            "mg_choices": [1, 2, 5],
            "route_pretty": "in the ear (otic)",
        },
    }

    route_key = choice(list(ROUTES.keys()))
    cfg = ROUTES[route_key]
    unit = cfg["unit"]
    step = cfg["answer_step"]
    max_per_dose = cfg["max_per_dose"]

    doses_per_day = choice([1, 2, 3])

    possible_answers = [round(i * step, 2) for i in range(1, int(max_per_dose / step) + 1)]
    mg_choices = cfg["mg_choices"][:]
    shuffle(mg_choices)

    unit_den_choices = cfg["unit_den_choices"][:]
    shuffle(unit_den_choices)

    answer_value = None
    mg_per_unit_num = None
    unit_den_value = None

    for strength in mg_choices:
        for den_val in unit_den_choices:
            valid = [a for a in possible_answers if abs((a * strength / den_val) - round(a * strength / den_val)) < 1e-9]
            if valid:
                mg_per_unit_num = strength
                unit_den_value = den_val
                answer_value = choice(valid)
                break
        if answer_value is not None:
            break

    if answer_value is None or mg_per_unit_num is None or unit_den_value is None:
        mg_per_unit_num = mg_choices[0]
        unit_den_value = unit_den_choices[0]
        answer_value = possible_answers[-1]

    order_mg = int(round(answer_value * mg_per_unit_num / unit_den_value))

    if unit_den_value == 1:
        strength_str = f"{mg_per_unit_num:g} mg/{unit}"
    else:
        strength_str = f"{mg_per_unit_num:g} mg/{unit_den_value}{unit}"

    if cfg["answer_step"] == 1.0:
        rounding_text = "(Round the answer to the nearest whole number. Use a leading zero if it applies. Do not use a trailing zero.)"
    elif cfg["answer_step"] == 0.1:
        rounding_text = "(Round the answer to the nearest tenth. Use a leading zero if it applies. Do not use a trailing zero.)"
    else:
        rounding_text = ""

    words = (
        f"The order is for {order_mg} mg delivered {cfg['route_pretty']}. "
        f"The pharmacy sends {strength_str}. "
        f"How many {unit} will the nurse administer? {rounding_text}"
    )
    return [words, order_mg, "mg", mg_per_unit_num, unit_den_value, unit, doses_per_day]



def frac1_numerator(init_value):
    answer = init_value.split(',')[5]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def frac1_denominator(init_value):
    answer = init_value.split(',')[2]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex") \
        .replace('-1*s','-s').replace('-1*l','-l').replace('-1*e','-e')
    return tuple([(re.compile(answer), hint)])

def frac2_numerator(init_value):
    answer = init_value.split(',')[2]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def frac1_num_value(init_value):
    answer = str(init_value.split(',')[4])
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def frac1_den_value(init_value):
    answer = str(init_value.split(',')[3])
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def frac2_num_value(init_value):
    answer = str(init_value.split(',')[1])
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def frac2_den_value(init_value):
    answer = '1'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def product_num(init_value):
    answer = float(init_value.split(',')[4]) * float(init_value.split(',')[1])
    if float(answer) == int(answer):
        answer = int(answer)
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', str(answer))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def product_den(init_value):
    answer = float(init_value.split(',')[3]) 
    if float(answer) == int(answer):
        answer = int(answer)
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', str(answer))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])


def final_answer(init_value):
    numerator = float(init_value.split(',')[1]) * float(init_value.split(',')[4])
    denominator = float(init_value.split(',')[3])
    answer = numerator / denominator
    answer = round(answer, 1)
    if float(answer) == int(answer):
        answer = int(answer)
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}',str(answer))), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

Domain = {
    'done': Operator(head=('done', V('kc')),
                     precondition=[Fact(start=True)],
                     effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
    ),

    'frac1_numerator': Operator(head=('frac1_numerator', V('equation'), V('kc')),
                        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                        effects=[Fact(field='frac1_numerator', value=(frac1_numerator, V('eq')), kc=V('kc'), answer=True)],
    ),

    'frac1_denominator': Operator(head=('frac1_denominator', V('equation'), V('kc')),
                        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                        effects=[Fact(field='frac1_denominator', value=(frac1_denominator, V('eq')), kc=V('kc'), answer=True)],
    ),

    'frac2_numerator': Operator(head=('frac2_numerator', V('equation'), V('kc')),
                        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                        effects=[Fact(field='frac2_numerator', value=(frac2_numerator, V('eq')), kc=V('kc'), answer=True)],
    ),

    'frac1_num_value': Operator(head=('frac1_num_value', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='frac1_num_value', value=(frac1_num_value, V('eq')), kc=V('kc'), answer=True)],
    ),

    'frac1_den_value': Operator(head=('frac1_den_value', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='frac1_den_value', value=(frac1_den_value, V('eq')), kc=V('kc'), answer=True)],
    ),

    'frac2_num_value': Operator(head=('frac2_num_value', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='frac2_num_value', value=(frac2_num_value, V('eq')), kc=V('kc'), answer=True)],
    ),

    'frac2_den_value': Operator(head=('frac2_den_value', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='frac2_den_value', value=(frac2_den_value, V('eq')), kc=V('kc'), answer=True)],
    ),

    'product_num': Operator(head=('product_num', V('equation'), V('kc')),
                           precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                           effects=[Fact(field='product_num', value=(product_num, V('eq')), kc=V('kc'), answer=True)],
    ),

    'product_den': Operator(head=('product_den', V('equation'), V('kc')),
                           precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                           effects=[Fact(field='product_den', value=(product_den, V('eq')), kc=V('kc'), answer=True)],
    ),

    'final_answer': Operator(head=('final_answer', V('equation'), V('kc')),
                           precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                           effects=[Fact(field='final_answer', value=(final_answer, V('eq')), kc=V('kc'), answer=True)],
    ),

    'setup_units': Method(
        head=('setup_units', V('equation')),
        preconditions=[Fact(field=V('equation'), value=V('eq'), answer=False)],
        subtasks=[
            (
                Task(head=('frac2_numerator', V('equation'), ('frac2_numerator',)), primitive=True),
                Task(head=('frac1_denominator', V('equation'), ('frac1_denominator',)), primitive=True),
                Task(head=('frac1_numerator', V('equation'), ('frac1_numerator',)), primitive=True),
            )
        ]
    ),

    'fill_numbers': Method(
        head=('fill_numbers', V('equation')),
        preconditions=[Fact(field=V('equation'), value=V('eq'), answer=False)],
        subtasks=[
            (
                Task(head=('frac2_den_value', V('equation'), ('frac2_den_value',)), primitive=True),
                Task(head=('frac2_num_value', V('equation'), ('frac2_num_value',)), primitive=True),
                Task(head=('frac1_den_value', V('equation'), ('frac1_den_value',)), primitive=True),
                Task(head=('frac1_num_value', V('equation'), ('frac1_num_value',)), primitive=True),
            )
        ]
    ),

    'multiply': Method(
        head=('multiply', V('equation')),
        preconditions=[Fact(field=V('equation'), value=V('eq'), answer=False)],
        subtasks=[
            (
                Task(head=('product_den', V('equation'), ('product_den',)), primitive=True),
                Task(head=('product_num', V('equation'), ('product_num',)), primitive=True),
            )
        ]
    ),

    'solve': Method(head=('solve', V('equation')),
                    preconditions=[
                        Fact(scaffold='level_2'),
                        Fact(scaffold='level_1'),
                        Fact(scaffold='level_0'),
                    ],
                    subtasks=[
                        [
                            Task(head=('setup_units', V('equation')), primitive=False),
                            Task(head=('fill_numbers', V('equation')), primitive=False),
                            Task(head=('multiply', V('equation')), primitive=False),
                            Task(head=('final_answer', V('equation'), ('final_answer',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('setup_units', V('equation')), primitive=False),
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

def htn_nursing_calculation_dim_analysis_kc_mapping():

    kcs = {
        'final_answer_numerator_units': 'final_answer_numerator_units',
        'final_answer_denominator_units': 'final_answer_denominator_units',
        'frac1_numerator': 'frac1_numerator',
        'frac1_denominator': 'frac1_denominator',
        'frac2_numerator': 'frac2_numerator',
        'frac2_denominator': 'frac2_denominator',
        'frac1_num_value': 'frac1_num_value',
        'frac2_num_value': 'frac2_num_value',
        'frac1_den_value': 'frac1_den_value',
        'frac2_den_value': 'frac2_den_value',
        'product_num': 'product_num',
        'product_den': 'product_den',
        'final_numerator': 'final_numerator',
        'final_answer': 'final_answer',
        'final_denominator': 'final_denominator',
        'done': 'done'
    }

    return kcs




def htn_nursing_calculation_dim_analysis_intermediate_hints():
    hints = {
        'frac1_numerator': [
            'What am I looking to give? (unit of administration, e.g., tablets, mL)'],
        'frac1_denominator': [
            'What do I have? (unit from pharmacy supply that matches order\'s unit)'],
        'frac2_numerator': [
            'What does each unit contain? (numerical amount with same unit as bottom of first fraction)'],
        'frac2_denominator': [
            'What is the quantity for that amount? (unit from pharmacy supply, e.g., tablet, mL)'],
        'frac1_num_value': [
            'How much is ordered? (numerical value of dose)'],
        'frac1_den_value': [
            'Numerical value for \'what I have\' (from pharmacy supply denominator)'],
        'frac2_num_value': [
            'Numerical value for \'what each contains\' (from pharmacy supply numerator)'],
        'frac2_den_value': [
            'Numerical value for the pharmacy unit (from supply denominator)'],
        'product_num': [
            'Multiply across all numerators.'],
        'product_den': [
            'Multiply across all denominators.'],
        'final_answer': [
            'Write the calculated dosage as a decimal.'],
        'done': ['Click the done button when you\'ve answered all fields.']
    }
    return hints

def htn_nursing_calculation_dim_analysis_studymaterial():
    study_material = studymaterial["drug_calculations"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_nursing_dimanalysis',    
                                             'htn_nursing_calculation_dim_analysis',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_nursing_calculation_dim_analysis_problem,
                                             htn_nursing_calculation_dim_analysis_kc_mapping(),
                                             htn_nursing_calculation_dim_analysis_intermediate_hints(),
                                             htn_nursing_calculation_dim_analysis_studymaterial()))