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




def find_factors(x):
    factors = []
    for i in range(1, x + 1):
       if x % i == 0:
           factors.append(i)
    return factors

def htn_radicals_product_rule_problem():
    perfect_square = (randint(2,9)) ** 2
    factors_of_perfect_square = find_factors(perfect_square)
    random_factor_1 = choice(factors_of_perfect_square)[0]
    random_factor_2 = int(perfect_square / random_factor_1)
    return f"\sqrt{{{random_factor_1}}} \cdot \sqrt{{{random_factor_2}}}"

def apply_product_rule(init_value):
    n, m = re.findall(r'\d+', init_value)
    answer = parse_latex(f"\\sqrt{{{n}*{m}}}")
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
    hint = f"\\sqrt{{{n}*{m}}}"
    return tuple([(answer, hint)])

def update_product_value(init_value):
    n, m = [int(x) for x in re.findall(r'\d+', init_value)]
    answer = parse_latex(f"\\sqrt{{{n*m}}}")
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
    hint = f"\\sqrt{{{n*m}}}"
    return tuple([(answer, hint)])

def simplify_product_value(init_value):
    n, m = [int(x) for x in re.findall(r'\d+', init_value)]
    answer = parse_latex(f"{sp.sqrt(n*m)}")
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
    hint = f"{sp.sqrt(n*m)}"
    return tuple([(answer, hint)])

Domain = {
    'done': Operator(head=('done', V('kc')),
                     precondition=[Fact(start=True)],
                     effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
    ),

    'apply_product_rule': Operator(head=('apply_product_rule', V('equation'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                effects=[Fact(field='apply_product_rule', value=(apply_product_rule, V('eq')), kc=V('kc'), answer=True)],
    ),
    'update_product_value': Operator(head=('update_product_value', V('equation'), V('kc')),
                            precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                            effects=[Fact(field='update_product_value', value=(update_product_value, V('eq')), kc=V('kc'), answer=True)],
    ),

    'simplify_product_value': Operator(head=('simplify_product_value', V('equation'), V('kc')),
                                       precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                       effects=[Fact(field='simplify_product_value', value=(simplify_product_value, V('eq')), kc=V('kc'), answer=True)],
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
                            Task(head=('update_product_value', V('equation'), ('update_product_value',)), primitive=True),
                            Task(head=('simplify_product_value', V('equation'), ('simplify_product_value',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('apply_product_rule', V('equation'), ('apply_product_rule',)), primitive=True),
                            Task(head=('simplify_product_value', V('equation'), ('update_product_value','simplify_product_value',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('simplify_product_value', V('equation'), ('apply_product_rule','update_product_value','simplify_product_value',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ]
                    ]
    ),
}

def htn_radicals_product_rule_kc_mapping():
    kcs = {
        "apply_product_rule": "apply_product_rule",
        "update_product_value": "update_product_value",
        "simplify_product_value": "simplify_product_value",
        "done": "done"
    }
    return kcs


def htn_radicals_product_rule_intermediate_hints():
    hints = {
        "apply_product_rule": ["Take both square roots under the same square root."],
        "update_product_value": ["The product can by found by multiplying the numbers under both square roots."],
        "simplify_product_value": ["Simplify the square root."]
    }
    return hints

def htn_radicals_product_rule_studymaterial():
    study_material = studymaterial["radicals_product_rule"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_radicals',
                                             'htn_radicals_product_rule',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_radicals_product_rule_problem,
                                             htn_radicals_product_rule_kc_mapping(),
                                             htn_radicals_product_rule_intermediate_hints(),
                                             htn_radicals_product_rule_studymaterial()))