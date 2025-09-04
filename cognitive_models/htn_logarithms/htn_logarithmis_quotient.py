import sympy as sp
from random import randint, choice

import sympy as sp
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


def htn_logarithms_quotient_problem():
    b, a = choice([(base, base**power) for power in range(1, 10) for base in range(2, 32) if base**power <= 1024])
    factor_pairs = [(a*num, num) for num in range(1, int(a**0.5)+1) if a*num <= 1024]
    m, n = choice(factor_pairs[1:]) if (len(factor_pairs)>1) else factor_pairs[0] 
    return f"\\log_{{{b}}}{{{m}}} - \\log_{{{b}}}{{{n}}}"


def apply_quotient_rule(init_value):
    (n,b), (m, b)= re.findall(r'log\((\d+),\s*(\d+)\)', str(parse_latex(init_value)))
    answer = re.compile(rf"log\({m}/{n}, {b}\)")
    hint = rf"\log_{{{b}}}({m}/{n})"
    value = tuple([(answer, hint)])
    return value

def divide_values(init_value):
    (n,b), (m, b)= re.findall(r'log\((\d+),\s*(\d+)\)', str(parse_latex(init_value)))
    answer = re.compile(rf"log\({int(m)//int(n)}, {b}\)")
    hint = rf"\log_{{{b}}}({int(m)//int(n)})"
    value = tuple([(answer, hint)])
    return value

def solve_log(init_value):
    answer = re.compile(rf"{sp.simplify(parse_latex(init_value))}")
    hint = rf"{sp.simplify(parse_latex(init_value))}"
    value = tuple([(answer, hint)])
    return value

Domain = {
    'done': Operator(head=('done', V('kc')),
                     precondition=[Fact(start=True)],
                     effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
    ),

    'apply_quotient_rule': Operator(head=('apply_quotient_rule', V('equation'), V('kc')),
                                precondition=[Fact(field=V('equation'), value=V('eq'), answer=False)],
                                effects=[Fact(field='apply_quotient_rule', value=(apply_quotient_rule, V('eq')), kc=V('kc'), answer=True)],
    ),

    'divide_values': Operator(head=('divide_values', V('equation'), V('kc')),
                        precondition=[Fact(field=V('equation'), value=V('eq'), answer=False)],
                        effects=[Fact(field='divide_values', value=(divide_values, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve_log': Operator(head=('solve_log', V('equation'), V('kc')),
                            precondition=[Fact(field=V('equation'), value=V('eq'), answer=False)],
                            effects=[Fact(field='solve_log', value=(solve_log, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve': Method(head=('solve', V('equation')),
                    preconditions=[
                        Fact(scaffold='level_2'),
                        Fact(scaffold='level_1'),
                        Fact(field=V('equation'), value=V('eq'), answer=False),
                    ],
                    subtasks=[
                        [
                            Task(head=('apply_quotient_rule', V('equation'), ('apply_quotient_rule',)), primitive=True),
                            Task(head=('divide_values', V('equation'), ('divide_values',)), primitive=True),
                            Task(head=('solve_log', V('equation'), ('solve_log',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('apply_quotient_rule', V('equation'), ('apply_quotient_rule',)), primitive=True),
                            Task(head=('solve_log', V('equation'), ('divide_values', 'solve_log')), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('solve_log', V('equation'), ('apply_quotient_rule', 'divide_values', 'solve_log')), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ]
                    ]
    ),
}

def htn_logarithms_quotient_kc_mapping():
    kcs = {
        "apply_quotient_rule": "apply_quotient_rule",
        "divide_values": "divide_values",
        "solve_log": "solve_log",
        "done": "done"
    }
    return kcs


def htn_logarithms_quotient_intermediate_hints():
    hints = {
        "apply_quotient_rule": ["Use the quotient rule to reduce logarithms with the same base."],
        "divide_values": ["Divide the numbers inside the logarithms."], 
        "solve_log": ["Solve the logarithms expression."],
        'done': [" You have solved the problem. Click the done button!"]
    }
    return hints

def htn_logarithms_quotient_studymaterial():
    study_material = studymaterial["logarithms_quotient_rule"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_logarithms',
                                             'htn_logarithms_quotient',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_logarithms_quotient_problem,
                                             htn_logarithms_quotient_kc_mapping(),
                                             htn_logarithms_quotient_intermediate_hints(),
                                             htn_logarithms_quotient_studymaterial()))