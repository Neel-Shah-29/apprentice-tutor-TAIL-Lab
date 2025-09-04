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

def htn_nursing_calculation_proportion_identify_info_problem():
    # Units
    solid_units = ["mg", "g", "mcg"]
    liquid_units = ["mL"]
    doses_per_day_options = ["twice a day", "daily", "every 6 hours"]

    # Determine whether to use solid or liquid units
    if random() < 0.5:  # 50% chance for solid units (caplets/tablets)
        is_tablet = True
        n3 = 1
        u3 = choice(["caplets", "tablets"])
    else:  # 50% chance for liquid units (mL)
        is_tablet = False
        n3 = randint(1, 5)
        u3 = "mL"

    def generate_values(n3, is_tablet):
        for _ in range(1000):  # Retry loop to ensure clean values
            n2 = round(uniform(10, 100), 1)

            if is_tablet:
                doses_per_unit = round(uniform(1, 10) * 2) / 2  # multiple of 0.5
            else:
                doses_per_unit = round(uniform(1, 10), 1)       # any tenth

            n1 = doses_per_unit * n2 / n3
            answer = n1 * n3 / n2

            if is_tablet:
                if round(answer * 2) == answer * 2:  # multiple of 0.5
                    return round(n1, 1), n2
            else:
                if round(answer, 1) == round(answer, 2):  # one decimal place
                    return round(n1, 1), n2

        raise ValueError("Failed to generate valid values after many attempts")

    n1, n2 = generate_values(n3, is_tablet)

    def strip_trailing_zero(val):
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        return str(val)

    u1 = u2 = choice(solid_units)
    if is_tablet:
        supply_statement = f"The pharmacy sends {strip_trailing_zero(n2)} {u2} {u3}."
    else:
        supply_statement = f"The pharmacy sends {strip_trailing_zero(n2)} {u2} / {strip_trailing_zero(n3)}{u3}."

    doses_per_day = choice(doses_per_day_options)
    order_statement = f"The order is for {strip_trailing_zero(n1)} {u1} {doses_per_day}."
    answer_statement = f"How many {u3} will the nurse administer per dose?"

    words = f"{order_statement} {supply_statement} {answer_statement}"
    prob = [words, n1, u1, n2, u2, u3, n3]
    return prob


def final_answer_numerator_units(init_value):
    answer = init_value.split(',')[5]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

def final_answer_denominator_units(init_value):
    answer = 'dose'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

def supply_numerator(init_value):
    answer = init_value.split(',')[3]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def supply_numerator_units(init_value):
    answer = init_value.split(',')[2]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

def supply_denominator(init_value):
    answer = init_value.split(',')[6]
    if init_value.split(',')[5] in ["caplets", "tablets"]:
        answer = '1'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def supply_denominator_units(init_value):
    answer = init_value.split(',')[5]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

def order_numerator(init_value):
    answer = init_value.split(',')[1]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def order_numerator_units(init_value):
    answer = init_value.split(',')[4]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])

def order_denominator(init_value):
    answer = 'x'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(answer), hint)])

def order_denominator_units(init_value):
    answer = init_value.split(',')[5]
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e')
    return tuple([(re.compile(re.escape(answer)), hint)])


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

    'identify_answer_units': Method(
        head=('identify_answer_units', V('equation')),
        preconditions=[
            Fact(scaffold='level_0'),
        ],
        subtasks=[
            (
                Task(head=('final_answer_denominator_units', V('equation'), ('final_answer_denominator_units',)), primitive=True),
                Task(head=('final_answer_numerator_units', V('equation'), ('final_answer_numerator_units',)), primitive=True),
            ),
        ]
    ),

    'identify_supply': Method(
        head=('identify_supply', V('equation')),
        preconditions=[
            Fact(scaffold='level_0'),
        ],
        subtasks=[
            (
                Task(head=('supply_denominator_units', V('equation'), ('supply_denominator_units',)), primitive=True),
                Task(head=('supply_denominator', V('equation'), ('supply_denominator',)), primitive=True),
                Task(head=('supply_numerator_units', V('equation'), ('supply_numerator_units',)), primitive=True),
                Task(head=('supply_numerator', V('equation'), ('supply_numerator',)), primitive=True),
            ),
        ]
    ),

    'identify_order': Method(
        head=('identify_order', V('equation')),
        preconditions=[
            Fact(scaffold='level_0'),
        ],
        subtasks=[
            (
                Task(head=('order_denominator_units', V('equation'), ('order_denominator_units',)), primitive=True),
                Task(head=('order_denominator', V('equation'), ('order_denominator',)), primitive=True),
                Task(head=('order_numerator_units', V('equation'), ('order_numerator_units',)), primitive=True),
                Task(head=('order_numerator', V('equation'), ('order_numerator',)), primitive=True),
            ),
        ]
    ),

    'solve': Method(
        head=('solve', V('equation')),
        preconditions=[
            Fact(scaffold='level_0'),
        ],
        subtasks=[
            [
                Task(head=('identify_answer_units', V('equation')), primitive=False),
                Task(head=('identify_supply', V('equation')), primitive=False),
                Task(head=('identify_order', V('equation')), primitive=False),
                Task(head=('done', ('done',)), primitive=True)
            ]
        ]
    ),
}

def htn_nursing_calculation_proportion_identify_info_kc_mapping():

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
        'done': 'done'
    }

    return kcs




def htn_nursing_calculation_proportion_identify_info_intermediate_hints():
    hints = {
        "final_answer_numerator_units": [
            "What unit will the nurse administer?"],
        "final_answer_denominator_units": [
            "When will the nurse administer the medicine?"],
        "supply_numerator": [
            "This is the number available in the pharmacy."],
        "supply_numerator_units": [
            "This is the unit of measurement that matches the order."],
        'supply_denominator': ["This number could be explicitly stated in the problem, or implied but not written."],
        'supply_denominator_units': ["What form is the medicine available in?"],
        'order_numerator': ["This is the number ordered by the doctor."],
        'order_numerator_units': ["What unit did the doctor order?"],
        'order_denominator': ["We do not know this part. What do we use for an unknown value?"],
        'order_denominator_units': ["This unit should match the supply's form. How do we measure solids or liquids?"],
        'done': ["Once you have identified all relevant information you can"
                        " select the done button to move to the next problem."]
    }
    return hints

def htn_nursing_calculation_proportion_identify_info_studymaterial():
    study_material = studymaterial["drug_calculations"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_nursing_proportion',    
                                             'htn_nursing_calculation_proportion_identify_info',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_nursing_calculation_proportion_identify_info_problem,
                                             htn_nursing_calculation_proportion_identify_info_kc_mapping(),
                                             htn_nursing_calculation_proportion_identify_info_intermediate_hints(),
                                             htn_nursing_calculation_proportion_identify_info_studymaterial()))