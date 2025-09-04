import sympy as sp
from random import randint, choice

import sympy as sp
from sympy import sstr, latex
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


    
def htn_logarithms_product_rule_problem():
    b, a = choice([(base, base**power) for power in range(1, 10) for base in range(2, 32) if base**power <= 1024])
    m, n = choice([(num, a//num) for num in range(1, int(a**0.5)+1) if a%num==0])
    return f"\\log_{{{b}}}{{{m}}} + \\log_{{{b}}}{{{n}}}"

def apply_product_rule(init_value):
    (m,b), (n, b)= re.findall(r'log\((\d+),\s*(\d+)\)', str(parse_latex(init_value)))
    answer = re.compile(rf'log\(({m}\*{n}|{n}\*{m}), {b}\)')
    hint = rf"\log_{{{b}}}({m}*{n})"
    return tuple([(answer, hint)])

def multiply_values(init_value):
    (m,b), (n, b)= re.findall(r'log\((\d+),\s*(\d+)\)', str(parse_latex(init_value)))
    answer = re.compile(rf"log\({int(m)*int(n)}, {b}\)")
    hint = rf"\log_{{{b}}}({int(m)*int(n)})"
    return tuple([(answer, hint)])

def solve_log(init_value):
    answer = re.compile(rf"{sp.simplify(parse_latex(init_value))}")
    hint = rf"{sp.simplify(parse_latex(init_value))}"
    return tuple([(answer, hint)])

Domain = {
    'done': Operator(head=('done', V('kc')),
                     precondition=[Fact(start=True)],
                     effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
    ),

    'apply_product_rule': Operator(head=('apply_product_rule', V('equation'), V('kc')),
                                precondition=[Fact(field=V('equation'), value=V('eq'), answer=False)],
                                effects=[Fact(field='apply_product_rule', value=(apply_product_rule, V('eq')), kc=V('kc'), answer=True)],
    ),

    'multiply_values': Operator(head=('multiply_values', V('equation'), V('kc')),
                                precondition=[Fact(field=V('equation'), value=V('eq'), answer=False)],
                                effects=[Fact(field='multiply_values', value=(multiply_values, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve_log': Operator(head=('solve_log', V('equation'), V('kc')),
                            precondition=[Fact(field=V('equation'), value=V('eq'), answer=False)],
                            effects=[Fact(field='solve_log', value=(solve_log, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve': Method(head=('solve', V('equation')),
                    preconditions=[
                        Fact(scaffold='level_2'),
                        Fact(scaffold='level_1'),
                        Fact(scaffold='level_0'),
                    ],
                    subtasks=[

                        [
                            Task(head=('apply_product_rule', V('equation'), ('apply_product_rule',)), primitive=True),
                            Task(head=('multiply_values', V('equation'), ('multiply_values',)), primitive=True),
                            Task(head=('solve_log', V('equation'), ('solve_log',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('apply_product_rule', V('equation'), ('apply_product_rule',)), primitive=True),
                            Task(head=('solve_log', V('equation'), ('solve_log',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('solve_log', V('equation'), ('solve_log',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],
                    ]
    ),
}

def htn_logarithms_product_rule_kc_mapping():
    kcs = {
        "apply_product_rule": "apply_product_rule",
        "multiply_values": "multiply_values",
        "solve_log": "solve_log",
        "done": "done"
    }
    return kcs


def htn_logarithms_product_rule_intermediate_hints():
    hints = {
        "apply_product_rule": ["Use the power rule to shift the exponent to multiplication with the logarithms."],
        "solve_log": ["Solve the logarithms."], 
        "multiply_values": ["Multiply the values"],
    }
    return hints

def htn_logarithms_product_rule_studymaterial():
    study_material = studymaterial["logarithms_product_rule"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_logarithms',
                                             'htn_logarithms_product',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_logarithms_product_rule_problem,
                                             htn_logarithms_product_rule_kc_mapping(),
                                             htn_logarithms_product_rule_intermediate_hints(),
                                             htn_logarithms_product_rule_studymaterial()))