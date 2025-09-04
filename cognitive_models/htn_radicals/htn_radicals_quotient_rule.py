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



def generate_prime(x,y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False

        if isPrime:
            prime_list.append(n)

    prime_choice = choice(prime_list)
           
    return prime_choice

    
def htn_radicals_quotient_rule_problem():
    numerator = generate_prime(1,50)
    denominator = (randint(2,20)) ** 2
    return f"\sqrt{{\\frac{{{numerator}}}{{{denominator}}}}}"

def update_quotient_value(init_value):
    n, m = re.findall(r'\d+', init_value)
    answer = parse_latex(f"\\frac{{\\sqrt{{{n}}}}}{{\\sqrt{{{m}}}}}")
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
    hint = f"\\frac{{\\sqrt{{{n}}}}}{{\\sqrt{{{m}}}}}"
    return tuple([(answer, hint)])

def simplify_quotient_value(init_value):
    n, m = re.findall(r'\d+', init_value)
    answer = parse_latex(f"\\frac{{\\sqrt{{{n}}}}}{{{sp.sqrt(int(m))}}}")
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
    hint = f"\\frac{{\\sqrt{{{n}}}}}{{{sp.sqrt(int(m))}}}"
    return tuple([(answer, hint)])

Domain = {
    'done': Operator(head=('done', V('kc')),
                     precondition=[Fact(start=True)],
                     effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
    ),

    'update_quotient_value': Operator(head=('update_quotient_value', V('equation'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                effects=[Fact(field='update_quotient_value', value=(update_quotient_value, V('eq')), kc=V('kc'), answer=True)],
    ),
    'simplify_quotient_value': Operator(head=('simplify_quotient_value', V('equation'), V('kc')),
                            precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                            effects=[Fact(field='simplify_quotient_value', value=(simplify_quotient_value, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve': Method(head=('solve', V('equation')),
                    preconditions=[
                        Fact(scaffold='level_1'),
                        Fact(scaffold='level_0'),
                    ],
                    subtasks=[

                        [
                            Task(head=('update_quotient_value', V('equation'), ('update_quotient_value',)), primitive=True),
                            Task(head=('simplify_quotient_value', V('equation'), ('simplify_quotient_value',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('simplify_quotient_value', V('equation'), ('simplify_quotient_value',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],
                    ]
    ),
}

def htn_radicals_quotient_rule_kc_mapping():
    kcs = {
        "update_quotient_value": "update_quotient_value",
        "simplify_quotient_value": "simplify_quotient_value",
        "done": "done"
    }
    return kcs


def htn_radicals_quotient_rule_intermediate_hints():
    hints = {
        "update_quotient_value": ["The quotient can by found by multiplying the numbers under both square roots."],
        "simplify_quotient_value": ["Simplify the square root."]
    }
    return hints

def htn_radicals_quotient_rule_studymaterial():
    study_material = studymaterial["radicals_quotient_rule"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_radicals',
                                             'htn_radicals_quotient_rule',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_radicals_quotient_rule_problem,
                                             htn_radicals_quotient_rule_kc_mapping(),
                                             htn_radicals_quotient_rule_intermediate_hints(),
                                             htn_radicals_quotient_rule_studymaterial()))