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
from random import random, uniform, choice, randint
from functools import reduce

def htn_nursing_calculation_drug_calc_formula_problem():
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

def formula_desired(init_value):
    answer = init_value.split(',')[1]  # Order amount
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex")
    return tuple([(re.compile(answer), hint)])

def formula_have(init_value):
    answer = init_value.split(',')[3]  # Supply amount
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex")
    return tuple([(re.compile(answer), hint)])

def formula_quantity(init_value):
    answer = init_value.split(',')[6]  # Supply denominator
    if init_value.split(',')[5] in ["caplets", "tablets"]:
        answer = '1'
    hint = answer
    answer = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer)), order="grlex")
    return tuple([(re.compile(answer), hint)])


def final_answer(init_value):
    desired = float(init_value.split(',')[1])
    have = float(init_value.split(',')[3])
    quantity = float(init_value.split(',')[6])
    if init_value.split(',')[5] in ["caplets", "tablets"]:
        quantity = 1
    answer = round(desired / have * quantity, 1)
    hint = str(answer).rstrip("0").rstrip(".")
    answer_regex = re.compile(rf'^{hint}(?:\.0*|0+)?$')
    return tuple([(re.compile(answer_regex), hint)])

Domain = {
    'done': Operator(
        head=('done', V('kc')),
        precondition=[Fact(start=True)],
        effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
    ),
    'supply_numerator': Operator(
        head=('supply_numerator', V('equation'), V('kc')),
        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
        effects=[Fact(field='supply_numerator', value=(supply_numerator, V('eq')), kc=V('kc'), answer=True)],
    ),
    'supply_numerator_units': Operator(
        head=('supply_numerator_units', V('equation'), V('kc')),
        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
        effects=[Fact(field='supply_numerator_units', value=(supply_numerator_units, V('eq')), kc=V('kc'), answer=True)],
    ),
    'supply_denominator': Operator(
        head=('supply_denominator', V('equation'), V('kc')),
        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
        effects=[Fact(field='supply_denominator', value=(supply_denominator, V('eq')), kc=V('kc'), answer=True)],
    ),
    'supply_denominator_units': Operator(
        head=('supply_denominator_units', V('equation'), V('kc')),
        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
        effects=[Fact(field='supply_denominator_units', value=(supply_denominator_units, V('eq')), kc=V('kc'), answer=True)],
    ),
    'order_numerator': Operator(
        head=('order_numerator', V('equation'), V('kc')),
        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
        effects=[Fact(field='order_numerator', value=(order_numerator, V('eq')), kc=V('kc'), answer=True)],
    ),
    'order_numerator_units': Operator(
        head=('order_numerator_units', V('equation'), V('kc')),
        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
        effects=[Fact(field='order_numerator_units', value=(order_numerator_units, V('eq')), kc=V('kc'), answer=True)],
    ),
    'formula_desired': Operator(
        head=('formula_desired', V('equation'), V('kc')),
        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
        effects=[Fact(field='formula_desired', value=(formula_desired, V('eq')), kc=V('kc'), answer=True)],
    ),
    'formula_have': Operator(
        head=('formula_have', V('equation'), V('kc')),
        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
        effects=[Fact(field='formula_have', value=(formula_have, V('eq')), kc=V('kc'), answer=True)],
    ),
    'formula_quantity': Operator(
        head=('formula_quantity', V('equation'), V('kc')),
        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
        effects=[Fact(field='formula_quantity', value=(formula_quantity, V('eq')), kc=V('kc'), answer=True)],
    ),

    'final_answer': Operator(
        head=('final_answer', V('equation'), V('kc')),
        precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
        effects=[Fact(field='final_answer', value=(final_answer, V('eq')), kc=V('kc'), answer=True)],
    ),

    'identify_given': Method(
        head=('identify_given', V('equation')),
        preconditions=[Fact(field=V('equation'), value=V('eq'), answer=False)],
        subtasks=[
            (
                Task(head=('order_numerator_units', V('equation'), ('order_numerator_units',)), primitive=True),
                Task(head=('order_numerator', V('equation'), ('order_numerator',)), primitive=True),
                Task(head=('supply_denominator_units', V('equation'), ('supply_denominator_units',)), primitive=True),
                Task(head=('supply_denominator', V('equation'), ('supply_denominator',)), primitive=True),
                Task(head=('supply_numerator_units', V('equation'), ('supply_numerator_units',)), primitive=True),
                Task(head=('supply_numerator', V('equation'), ('supply_numerator',)), primitive=True),

            )
        ]
    ),

    'apply_formula': Method(
        head=('apply_formula', V('equation')),
        preconditions=[Fact(field=V('equation'), value=V('eq'), answer=False)],
        subtasks=[
            (
                Task(head=('formula_quantity', V('equation'), ('formula_quantity',)), primitive=True),
                Task(head=('formula_have', V('equation'), ('formula_have',)), primitive=True),
                Task(head=('formula_desired', V('equation'), ('formula_desired',)), primitive=True),
            )
        ]
    ),

    'provide_final_answer': Method(
        head=('provide_final_answer', V('equation')),
        preconditions=[Fact(field=V('equation'), value=V('eq'), answer=False)],
        subtasks=[
            (
                Task(head=('final_answer', V('equation'), ('final_answer',)), primitive=True),
            )
        ]
    ),

    'solve': Method(
        head=('solve', V('equation')),
        preconditions=[
            Fact(scaffold='level_2'),  
            Fact(scaffold='level_1'),  
            Fact(scaffold='level_0'),  
        ],
        subtasks=[
            [
                Task(head=('identify_given', V('equation')), primitive=False),
                Task(head=('apply_formula', V('equation')), primitive=False),
                Task(head=('provide_final_answer', V('equation')), primitive=False),
                Task(head=('done', ('done',)), primitive=True)
            ],
            [
                Task(head=('apply_formula', V('equation')), primitive=False),
                Task(head=('provide_final_answer', V('equation')), primitive=False),
                Task(head=('done', ('done',)), primitive=True)
            ],
            [
                Task(head=('provide_final_answer', V('equation')), primitive=False),
                Task(head=('done', ('done',)), primitive=True)
            ]
        ]
    ),
}


def htn_nursing_calculation_drug_calc_formula_kc_mapping():
    return {
        'supply_numerator': 'supply_numerator',
        'supply_numerator_units': 'supply_numerator_units',
        'supply_denominator': 'supply_denominator',
        'supply_denominator_units': 'supply_denominator_units',
        'order_numerator': 'order_numerator',
        'order_numerator_units': 'order_numerator_units',
        'formula_desired': 'formula_desired',
        'formula_have': 'formula_have',
        'formula_quantity': 'formula_quantity',
        'final_answer': 'final_answer',
        'done': 'done'
    }


def htn_nursing_calculation_drug_calc_formula_intermediate_hints():
    return {
        'supply_numerator': ["Number available in the pharmacy (Have)."],
        'supply_numerator_units': ["Unit matching the doctor's order."],
        'supply_denominator': ["Number of units per form (Quantity)."],
        'supply_denominator_units': ["Form of the medicine (tablet, mL, etc.)."],
        'order_numerator': ["Number ordered by the doctor (Desired)."],
        'order_numerator_units': ["Unit the doctor ordered."],
        'formula_desired': ["Enter the 'Desired' amount from the order."],
        'formula_have': ["Enter the 'Have' amount from the supply."],
        'formula_quantity': ["Enter the 'Quantity' from the supply packaging."],
        'final_answer': ["What is the dosage? (Desired / Have × Quantity)"],
        'done': ["Click done to move to the next problem."]
    }

def htn_nursing_calculation_drug_calc_formula_studymaterial():
    study_material = studymaterial["drug_calculations"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_nursing_formula_method',    
                                             'htn_nursing_calculation_drug_calc_formula',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_nursing_calculation_drug_calc_formula_problem,
                                             htn_nursing_calculation_drug_calc_formula_kc_mapping(),
                                             htn_nursing_calculation_drug_calc_formula_intermediate_hints(),
                                             htn_nursing_calculation_drug_calc_formula_studymaterial()))