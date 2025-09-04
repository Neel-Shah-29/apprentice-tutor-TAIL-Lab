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
    problems = [
        ["A nurse is caring for a client who is to receive liquid medications via a gastrostomy tube. The client is prescribed phenytoin 250 mg. The amount available is phenytoin oral solution 25 mg/5 mL. How many mL should the nurse administer per dose?", 250, "mg", 25, 5, "mL", 1],
        ["A nurse is caring for a client who is receiving heparin 3,800 units subcutaneous daily. Available is heparin 5,000 units/mL. How many mL should the nurse administer?", 3800, "units", 5000, 1, "mL", 1],
        # ["A nurse is preparing to administer vancomycin 15 mg/kg/day divided equally every 12 hr. The client weighs 198 lb. How many mg should the nurse administer with each dose?", 15, "mg/kg/day", None, None, None, 2], 
        # ["A nurse is preparing to administer digoxin 8 mcg/kg/day PO to divide equally every 12 hr for a preschooler who weighs 33 lb. Available is digoxin elixir 0.05 mg/mL. How many mL should the nurse administer per dose?", 8, "mcg/kg/day", 0.05, 1, "mL", 2], 
        ["A nurse is caring for a client who has schizophrenia and is experiencing hallucinations. The provider prescribes chlorpromazine 50 mg IM every 4 hr as needed. Available is chlorpromazine injection 25 mg/mL. How many mL should the nurse administer per dose?", 50, "mg", 25, 1, "mL", 1], 
        # ["A nurse is caring for an infant who weighs 12 lb and is prescribed cefuroxime sodium 15 mg/kg/dose PO every 12 hr. Available is cefuroxime sodium oral solution 125 mg/5 mL. How many mL should the nurse administer per dose?", 15, "mg/kg/dose", 125, 5, "mL", 2], 
        ["A nurse is caring for a client who has heart failure and a prescription for digoxin 125 mcg PO daily. Available is digoxin PO 250 mg/tablet. How many tablets should the nurse administer per dose?", 125, "mcg", 0.25, 1, "tablet", 1], 
        ["A nurse is preparing to administer chlordiazepoxide 50 mg PO every 8 hr to a client. The amount available is chlordiazepoxide 25 mg/capsule. How many capsules should the nurse administer per dose?", 50, "mg", 25, 1, "capsule", 3], 
        # ["A nurse is caring for a client who has heart failure and a prescription for digoxin 125 mcg PO daily. Available is digoxin PO 0.25 mg/tablet. How many tablets should the nurse administer per dose?", 125, "mcg", 0.25, 1, "tablet", 1], 
        ["A nurse is caring for a client who is to receive liquid medications via a gastrostomy tube. The client is prescribed phenytoin 250 mg. The amount available is phenytoin oral solution 25 mg/5 mL. How many mL should the nurse administer per dose?", 250, "mg", 25, 5, "mL", 1], 
        ["A nurse is preparing to administer digoxin 0.25 mg PO daily. The amount available is digoxin 0.125 mg tablets. How many tablets should the nurse administer?", 0.25, "mg", 0.125, 1, "tablet", 1], 
        ["A nurse is preparing to administer amoxicillin 350 mg PO. Available is amoxicillin 250 mg/5 mL. How many mL should the nurse administer?", 350, "mg", 250, 5, "mL", 1], 
        ["A nurse is preparing to administer aspirin 650 mg PO every 12 hr. The amount available is aspirin 325 mg tablets. How many tablets should the nurse administer?", 650, "mg", 325, 1, "tablet", 2], 
        ["A nurse is preparing to administer amitriptyline 150 mg PO at bedtime. The amount available is amitriptyline 75 mg/tablet. How many tablets should the nurse administer per dose?", 150, "mg", 75, 1, "tablet", 1], 
        ["A nurse is preparing to administer clonidine 0.3 mg at bedtime to a client. The amount available is clonidine 0.1 mg/tablet. How many tablets should the nurse administer per dose?", 0.3, "mg", 0.1, 1, "tablet", 1], 
        ["A nurse is preparing to administer levothyroxine 275 mg PO daily to a client. The amount available is levothyroxine 137 mcg/tablet. How many tablets should the nurse administer?", 0.275, "mg", 137, 1, "tablet", 1], 
        ["A nurse is preparing to administer erythromycin ethylsuccinate 800 mg PO every 4 hr. Available is erythromycin ethylsuccinate 200 mg/5 mL. How many mL should the nurse administer?", 800, "mg", 200, 5, "mL", 6], 
        ["A nurse is preparing to administer buspirone 7.5 mg PO every 12 hr to a client. The amount available is buspirone 15 mg/tablet. How many tablets should the nurse administer per dose?", 7.5, "mg", 15, 1, "tablet", 2]
    ]
    return choice(problems)



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

htn_loaded_models.register(HTNCognitiveModel('htn_nursing_dim',    
                                             'htn_nursing_calculation_dim_analysis_problem_bank',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_nursing_calculation_dim_analysis_problem,
                                             htn_nursing_calculation_dim_analysis_kc_mapping(),
                                             htn_nursing_calculation_dim_analysis_intermediate_hints(),
                                             htn_nursing_calculation_dim_analysis_studymaterial()))