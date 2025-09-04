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

    
def htn_radicals_adding_square_roots_problem():
    c1 = generate_prime(2,10)
    ra =  generate_prime(2,10)
    rb = (randint(2,6))** 2
    c2 = generate_prime(2,10)
    return f"{c1}\sqrt{{{ra * rb}}} + {c2}\sqrt{{{ra}}}"

def factor_radicand(init_value):
    c1, rarb, c2, ra = re.findall(r'\d+', init_value)
    c1, rarb, c2, ra = int(c1), int(rarb), int(c2), int(ra)
    rb = rarb // ra
    ans1 = re.compile(rf"{c2}\*sqrt\({ra}\) \+ {c1}\*sqrt\({rb}\*{ra}\)")
    ans2 = re.compile(rf"{c2}\*sqrt\({ra}\) \+ {c1}\*sqrt\({ra}\*{rb}\)")
    ans3 = re.compile(rf"{c1}\*sqrt\({rb}\*{ra}\) \+ {c2}\*sqrt\({ra}\)")
    answer = sp.Add(sp.Mul(c1, sp.sqrt(sp.Mul(ra, rb, evaluate=False), evaluate=False), evaluate=False), sp.Mul(c2, sp.sqrt(ra)), evaluate=False)
    hint = latex(answer)
    return tuple([
        (ans1, hint),
        (ans2, hint),
        (ans3, hint)
    ])
def product_rule(init_value):
    c1, rarb, c2, ra = re.findall(r'\d+', init_value)
    c1, rarb, c2, ra = int(c1), int(rarb), int(c2), int(ra)
    rb = rarb // ra
    ans1 = re.compile(rf"{c2}\*sqrt\({ra}\) \+ {c1}\*\(sqrt\({rb}\)\*sqrt\({ra}\)\)")
    ans2 = re.compile(rf"{c2}\*sqrt\({ra}\) \+ {c1}\*\(sqrt\({ra}\)\*sqrt\({rb}\)\)")
    ans3 = re.compile(rf"{c1}\*\(sqrt\({rb}\)\*sqrt\({ra}\)\) \+ {c2}\*sqrt\({ra}\)")
    ans4 = re.compile(rf"{c1}\*\(sqrt\({ra}\)\*sqrt\({rb}\)\) \+ {c2}\*sqrt\({ra}\)")
    answer = sp.Add(sp.Mul(c1, sp.sqrt(ra), sp.sqrt(rb, evaluate=False), evaluate=False), sp.Mul(c2, sp.sqrt(ra)), evaluate=False)
    hint = latex(answer)

    return tuple([
        (ans1, hint),
        (ans2, hint),
        (ans3, hint),
        (ans4, hint)
    ])

def solve_square_root(init_value):
    c1, rarb, c2, ra = re.findall(r'\d+', init_value)
    c1, rarb, c2, ra = int(c1), int(rarb), int(c2), int(ra)
    rb = rarb // ra
    sqrtrb = sp.sqrt(rb) 
    ans1 = re.compile(rf"{c2}\*sqrt\({ra}\) \+ {c1}\*{sqrtrb}\*sqrt\({ra}\)")
    ans2 = re.compile(rf"{c2}\*sqrt\({ra}\) \+ {c1}\*sqrt\({ra}\)\*{sqrtrb}")
    ans3 = re.compile(rf"{c1}\*{sqrtrb}\*sqrt\({ra}\) \+ {c2}\*sqrt\({ra}\)")
    ans4 = re.compile(rf"{c1}\*sqrt\({ra}\)\*{sqrtrb} \+ {c2}\*sqrt\({ra}\)")

    ans5 = re.compile(rf"{c2}\*sqrt\({ra}\) \+ {c1}\*\({sqrtrb}\*sqrt\({ra}\)\)")
    ans6 = re.compile(rf"{c2}\*sqrt\({ra}\) \+ {c1}\*\(sqrt\({ra}\)\*{sqrtrb}\)")
    ans7 = re.compile(rf"{c1}\*\({sqrtrb}\*sqrt\({ra}\)\) \+ {c2}\*sqrt\({ra}\)")
    ans8 = re.compile(rf"{c1}\*\(sqrt\({ra}\)\*{sqrtrb}\) \+ {c2}\*sqrt\({ra}\)")

    ans9 = re.compile(rf"{c2}\*sqrt\({ra}\) \+ {c1}\*{sqrtrb}\*sqrt\({ra}\)")
    ans10 = re.compile(rf"{c2}\*sqrt\({ra}\) \+ \({c1}\*sqrt\({ra}\)\)\*{sqrtrb}")
    ans11 = re.compile(rf"\({c1}\*{sqrtrb}\)\*sqrt\({ra}\) \+ {c2}\*sqrt\({ra}\)")
    ans12 = re.compile(rf"\({c1}\*sqrt\({ra}\)\)\*{sqrtrb} \+ {c2}\*sqrt\({ra}\)")

    answer = sp.Add(sp.Mul(c1, sp.sqrt(ra), sp.sqrt(rb), evaluate=False), sp.Mul(c2, sp.sqrt(ra)), evaluate=False)
    hint = latex(answer)
    
    return tuple([
        (ans1, hint),
        (ans2, hint),
        (ans3, hint),
        (ans4, hint),
        (ans5, hint),
        (ans6, hint),
        (ans7, hint),
        (ans8, hint),
        (ans9, hint),
        (ans10, hint),
        (ans11, hint),
        (ans12, hint)
    ])

def evaluate_coefficient(init_value):
    c1, rarb, c2, ra = re.findall(r'\d+', init_value)
    c1, rarb, c2, ra = int(c1), int(rarb), int(c2), int(ra)
    rb = rarb // ra
    c3 = sp.sqrt(rb)*c1
    ans1 = re.compile(rf"{c3}\*sqrt\({ra}\) \+ {c2}\*sqrt\({ra}\)")
    ans2 = re.compile(rf"{c2}\*sqrt\({ra}\) \+ {c3}\*sqrt\({ra}\)")
    answer = sp.Add(sp.Mul(c1, sp.sqrt(ra), sp.sqrt(rb)), sp.Mul(c2, sp.sqrt(ra)), evaluate=False)
    hint = latex(answer)
    return tuple([
        (ans1, hint),
        (ans2, hint)
    ])


def adding_square_root(init_value):
    c1, rarb, c2, ra = re.findall(r'\d+', init_value)
    c1, rarb, c2, ra = int(c1), int(rarb), int(c2), int(ra)
    rb = rarb // ra
    c3 = sp.sqrt(rb)*c1
    c4 = c3+c2
    ans1 = re.compile(rf"{c4}\*sqrt\({ra}\)")
    ans2 = re.compile(rf"sqrt\({ra}\)\*{c4}")
    answer = sp.simplify(sp.Add(sp.Mul(c1, sp.sqrt(ra), sp.sqrt(rb)), sp.Mul(c2, sp.sqrt(ra))))
    hint = latex(answer)
    return tuple([
        (ans1, hint),
        (ans2, hint)
    ])

Domain = {
    'done': Operator(head=('done', V('kc')),
                     precondition=[Fact(start=True)],
                     effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
    ),

    'factor_radicand': Operator(head=('factor_radicand', V('equation'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                effects=[Fact(field='factor_radicand', value=(factor_radicand, V('eq')), kc=V('kc'), answer=True)],
    ),
    'product_rule': Operator(head=('product_rule', V('equation'), V('kc')),
                            precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                            effects=[Fact(field='product_rule', value=(product_rule, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve_square_root': Operator(head=('solve_square_root', V('equation'), V('kc')),
                                  precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                  effects=[Fact(field='solve_square_root', value=(solve_square_root, V('eq')), kc=V('kc'), answer=True)],
    ),

    'evaluate_coefficient': Operator(head=('evaluate_coefficient', V('equation'), V('kc')),
                                     precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                     effects=[Fact(field='evaluate_coefficient', value=(evaluate_coefficient, V('eq')), kc=V('kc'), answer=True)],
    ),

    'adding_square_root': Operator(head=('adding_square_root', V('equation'), V('kc')),
                                   precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                   effects=[Fact(field='adding_square_root', value=(adding_square_root, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve': Method(head=('solve', V('equation')),
                    preconditions=[
                        Fact(scaffold='level_4'),
                        Fact(scaffold='level_3'),
                        Fact(scaffold='level_2'),
                        Fact(scaffold='level_1'),
                        Fact(scaffold='level_0'),
                    ],
                    subtasks=[
                        [
                            Task(head=('factor_radicand', V('equation'), ('factor_radicand',)), primitive=True),
                            Task(head=('product_rule', V('equation'), ('product_rule',)), primitive=True),
                            Task(head=('solve_square_root', V('equation'), ('solve_square_root',)), primitive=True),
                            Task(head=('evaluate_coefficient', V('equation'), ('evaluate_coefficient',)), primitive=True),
                            Task(head=('adding_square_root', V('equation'), ('adding_square_root',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('factor_radicand', V('equation'), ('factor_radicand',)), primitive=True),
                            Task(head=('product_rule', V('equation'), ('product_rule',)), primitive=True),
                            Task(head=('solve_square_root', V('equation'), ('solve_square_root',)), primitive=True),
                            Task(head=('adding_square_root', V('equation'), ('adding_square_root',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('factor_radicand', V('equation'), ('factor_radicand',)), primitive=True),
                            Task(head=('product_rule', V('equation'), ('product_rule',)), primitive=True),
                            Task(head=('adding_square_root', V('equation'), ('adding_square_root',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('factor_radicand', V('equation'), ('factor_radicand',)), primitive=True),
                            Task(head=('adding_square_root', V('equation'), ('adding_square_root',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('adding_square_root', V('equation'), ('adding_square_root',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],
                    ]
    ),
}

def htn_radicals_adding_square_roots_kc_mapping():
    kcs = {

        'factor_radicand':'factor_radicand',
        'product_rule':'product_rule',
        'solve_square_root':'solve_square_root',
        'evaluate_coefficient':'evaluate_coefficient',
        'adding_square_root':'adding_square_root',
        'done':'done',
    }
    return kcs


def htn_radicals_adding_square_roots_intermediate_hints():
    hints = {
       "factor_radicand": ["Factor the radicand within the square root."],
       "product_rule": ["Use the product rule to break down the radicand."],
       "solve_square_root": ["Solve the square root in the expression."],
       "evaluate_coefficient": ["Multiply the solved square root with the coefficient."],
       "adding_square_root": ["Add the coefficients square roots with the same radicand."],
       'done': [" You have solved the problem. Click the done button!"]
    }
    return hints

def htn_radicals_adding_square_roots_studymaterial():
    study_material = studymaterial["radicals_adding_square_roots"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_radicals',
                                             'htn_radicals_adding_square_roots',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_radicals_adding_square_roots_problem,
                                             htn_radicals_adding_square_roots_kc_mapping(),
                                             htn_radicals_adding_square_roots_intermediate_hints(),
                                             htn_radicals_adding_square_roots_studymaterial()))