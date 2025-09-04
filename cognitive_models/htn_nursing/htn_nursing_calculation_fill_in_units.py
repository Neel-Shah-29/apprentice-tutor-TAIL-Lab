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
from random import random, choice, uniform
from functools import reduce

def htn_nursing_fill_in_units_problem():
    # Units
    solid_units = ["mg", "g", "mcg"]
    liquid_units = ["mL"]

    # Dose frequency options
    doses_per_day = choice([1, 2, 3])
    doses_per_day_statement = f"{doses_per_day} time{'s' if doses_per_day > 1 else ''} per day"

    # Determine whether to use solid or liquid units first
    if random() < 0.5:  # 50% chance for solid units (caplets/tablets)
        is_tablet = True
        n3 = 1  # Set n3 to 1 for tablets/caplets
        u3 = choice(["caplets", "tablets"])
    else:  # 50% chance for liquid units (mL)
        is_tablet = False
        n3 = randint(1, 5)  # n3 can be between 1 and 5 for liquids
        u3 = choice(liquid_units)
    def generate_values(n3):
    # Generate n2 (the amount per unit) with a resolution of 0.5
        n2 = round(uniform(10, 100), 0)

        # Generate a clean doses_per_unit (answer) which can be a whole number or a multiple of 0.5
        doses_per_unit = round(uniform(1, 10) * 2) / 2

    # Calculate n1 ensuring n1 * n3 / n2 gives a clean doses_per_unit
        if n3 == 1:
            n1 = doses_per_unit * n2  # Ensure n1 is an integer for tablets
        else:
            # Ensure n1 is calculated to make n1 * n3 / n2 a clean number
            n1 = doses_per_unit * n2 / n3 # For liquids, n1 should be a float
        if n1 != round(n1, 1):
            n1, n2 = generate_values(n3)

        return n1, n2

    n1, n2 = generate_values(n3)
    # Prepare the pharmacy statement
    u1 = u2 = choice(solid_units)
    if is_tablet:
        supply_statement = f"The pharmacy sends {n2} {u2} {u3}."
    else:
        supply_statement = f"The pharmacy sends {n2} {u2} / {n3 if n3 > 1 else ''}{u3}."

    # Prepare the order statement
    answer_statement = f"How many {u3} will the nurse administer per dose?"
    order_statement = f"The order is for {n1} {u1} {doses_per_day_statement}."

    words = f"{order_statement} {supply_statement} {answer_statement}"
    prob = [words, n1, u1, n2, u2, u3, n3, doses_per_day]
    return prob


def final_answer_numerator_units(init_value):
    answer = init_value.split(',')[5]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def final_answer_denominator_units(init_value):
    answer = 'dose'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

# def frac1_numerator(init_value):
#     answer = 'mg'
#     hint = answer
#     answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
#     return tuple([(re.compile(answer), hint)])

# def frac1_denominator(init_value):
#     answer = 'day'
#     hint = answer
#     answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
#     return tuple([(re.compile(answer), hint)])

# def frac2_numerator(init_value):
#     answer = 'tablet'
#     hint = answer
#     answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
#     return tuple([(re.compile(answer), hint)])

# def frac2_denominator(init_value):
#     answer = 'mg'
#     hint = answer
#     answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
#     return tuple([(re.compile(answer), hint)])

def frac1_num_value(init_value):
    answer = str(init_value.split(',')[1])
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def frac1_den_value(init_value):
    answer = '1'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def frac2_num_value(init_value):
    answer = str(init_value.split(',')[6])
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def frac2_den_value(init_value):
    answer = init_value.split(',')[3]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def frac3_num_value(init_value):
    answer = '1'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def frac3_den_value(init_value):
    answer = init_value.split(',')[7]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

Domain = {
    'done': Operator(head=('done', V('kc')),
                     precondition=[Fact(start=True)],
                     effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
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

    'frac3_num_value': Operator(head=('frac3_num_value', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='frac3_num_value', value=(frac3_num_value, V('eq')), kc=V('kc'), answer=True)],
    ),

    'frac3_den_value': Operator(head=('frac3_den_value', V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='frac3_den_value', value=(frac3_den_value, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve': Method(head=('solve', V('equation')),
                    preconditions=[
                        Fact(scaffold='level_0'),
                    ],
                    subtasks=[
                        [
                            Task(head=('frac1_num_value', V('equation'), ('frac1_num_value',)), primitive=True),
                            Task(head=('frac1_den_value', V('equation'), ('frac1_den_value',)), primitive=True),
                            Task(head=('frac2_num_value', V('equation'), ('frac2_num_value',)), primitive=True),
                            Task(head=('frac2_den_value', V('equation'), ('frac2_den_value',)), primitive=True),
                            Task(head=('frac3_num_value', V('equation'), ('frac3_num_value',)), primitive=True),
                            Task(head=('frac3_den_value', V('equation'), ('frac3_den_value',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],
                    ]
    ),
}

def htn_nursing_fill_in_units_kc_mapping():

    kcs = {
        'final_answer_numerator_units': 'final_answer_numerator_units',
        'final_answer_denominator_units': 'final_answer_denominator_units',
        'frac1_numerator': 'frac1_numerator',
        'frac1_denominator': 'frac1_denominator',
        'frac2_numerator': 'frac2_numerator',
        'frac2_denominator': 'frac3_denominator',
        'frac1_num_value': 'frac1_num_value',
        'frac2_num_value': 'frac2_num_value',
        'frac3_num_value': 'frac3_num_value',
        'frac1_den_value': 'frac1_den_value',
        'frac2_den_value': 'frac2_den_value',
        'frac3_den_value': 'frac3_den_value',
        'done': 'done'
    }

    return kcs




def htn_nursing_fill_in_units_intermediate_hints():
    hints = {
        "final_answer_numerator_units": [
            "What unit will the nurse administer?"],
        "final_answer_denominator_units": [
            "When will the nurse administer the medicine?"],
        'frac1_num_value': ['How much is the order for?'],
        'frac2_num_value': ['Enter the denominator of the phramacy supply.'],
        'frac3_num_value': ['How many days is the order for?'],
        'frac1_den_value': ['How many days is the order for?'],
        'frac2_den_value': ['Enter the numerator of the pharmacy supply?'],
        'frac3_den_value': ['How many doses per each day?'],
        'done': ['Click the done button when you\'ve answered all fields']
    }
    return hints

def htn_nursing_fill_in_units_studymaterial():
    study_material = studymaterial["drug_calculations"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_nursing_dim',    
                                             'htn_nursing_calculation_fill_in_units',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_nursing_fill_in_units_problem,
                                             htn_nursing_fill_in_units_kc_mapping(),
                                             htn_nursing_fill_in_units_intermediate_hints(),
                                             htn_nursing_fill_in_units_studymaterial()))