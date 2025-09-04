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

def is_perfect_square(x):
    return (x**.5) % 1 == 0

def new_find_factors(x):
    factors = []
    sq_factors = []
    for i in range(1, x + 1):
        if x % i == 0:
            factors.append(i)
            if is_perfect_square(i):
                sq_factors.append(i)
    return factors, sq_factors

def htn_radicals_product_rule_problem():
    radicand = (randint(2,9)) ** 2 * randint(1, 6)
    radicand_factors, square_factors = new_find_factors(radicand)
    largest_square = max(square_factors)
    radicand_factors.pop(0)
    random_factor_1 = choice(radicand_factors)
    random_factor_2 = int(radicand / random_factor_1)
    #return f"\sqrt{{{random_factor_1}}} \cdot \sqrt{{{random_factor_2}}}"
    return {"Problem" : f"\sqrt{{{random_factor_1}}} \cdot \sqrt{{{random_factor_2}}}", "Problem Args" : {"Perfect Square" : str(largest_square == radicand)}}

def apply_product_rule(init_value):
    n, m = [int(x) for x in re.findall(r'\d+', init_value)]
    answer = parse_latex(f"\\sqrt{{{n} * {m}}}")
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
    hint = f"\\sqrt{{{n}*{m}}}"
    return tuple([(answer, hint)])

def multiply_radicands(init_value):
    n, m = [int(x) for x in re.findall(r'\d+', init_value)]
    radicand = n * m
    answer = parse_latex(f"\\sqrt{{{radicand}}}")
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
    hint = f"\\sqrt{{{radicand}}}"
    return tuple([(answer, hint)])

def lesser_square_a(init_value):
    n, m = [int(x) for x in re.findall(r'\d+', init_value)]
    radicand = n * m
    max_square_factor = max(new_find_factors(radicand)[1])
    lesser_squares = [n for n in range(radicand, 0, -1) if is_perfect_square(n)]
    value = tuple([(re.compile(str(f)), str(max_square_factor)) for f in lesser_squares])
    return value

def is_factor_a(init_value, lesser_square):
    n, m = [int(x) for x in re.findall(r'\d+', init_value)]
    radicand = n * m
    factors, __ = new_find_factors(radicand)
    if int(lesser_square) in factors:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('yes')))), 'yes')])
    else:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('no')))), 'no')])
    return value

def is_greatest_a(init_value, lesser_square):
    n, m = [int(x) for x in re.findall(r'\d+', init_value)]
    radicand = n * m
    max_square_factor = max(new_find_factors(radicand)[1])
    if int(lesser_square) == max_square_factor:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('yes')))), 'yes')])
    else:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('no')))), 'no')])
    return value

def divide_out_a(init_value):
    n, m = [int(x) for x in re.findall(r'\d+', init_value)]
    __, squares = new_find_factors(n * m)
    max_square = max(squares)
    leftover = (n * m) // max_square
    answer = parse_latex(f"\\sqrt{{{max_square} * {leftover}}}")
    hint = latex(answer)
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
    return tuple([(answer, hint)])

def reduce_radical_a(init_value):
    n, m = [int(x) for x in re.findall(r'\d+', init_value)]
    __, squares = new_find_factors(n * m)
    max_square = max(squares)
    leftover = (n * m) // max_square
    if leftover == 1:
        answer = parse_latex(f"{sp.sqrt(max_square)}")
    else:
        answer = parse_latex(f"{sp.sqrt(max_square)} * \\sqrt{{{leftover}}}")
    hint = latex(answer)
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
    return tuple([(answer, hint)])

def solve_expr(init_value):
    n, m = [int(x) for x in re.findall(r'\d+', init_value)]
    __, squares = new_find_factors(n * m)
    max_square = max(squares)
    leftover = (n * m) // max_square
    if leftover == 1:
        answer = parse_latex(f"{sp.sqrt(max_square)}")
    else:
        answer = parse_latex(f"{sp.sqrt(max_square)} * \\sqrt{{{leftover}}}")
    hint = latex(answer)
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
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
    'multiply_radicands': Operator(head=('multiply_radicands', V('equation'), V('kc')),
                            precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                            effects=[Fact(field='multiply_radicands', value=(multiply_radicands, V('eq')), kc=V('kc'), answer=True)],
    ),

    'lesser_square_a': Operator(head=('lesser_square_a', V('equation'), V('kc')),
                            precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                            effects=[Fact(field='lesser_square_a', value=(lesser_square_a, V('eq')), kc=V('kc'), answer=True)],
    ),


    #'is_factor': Operator(head=('is_factor',  V('equation'), V('lesser_square'), V('kc')),
    #                     precondition=Fact(field=V('equation'), value=V('eq'), answer=False)&Fact(field=V('lesser_square'), value=V('lesser_square_value'), kc=V('lesser_square_kc'), answer=True),
    #                     effects=[Fact(field='is_factor', value=(is_factor, V('eq'), V('lesser_square_value')), kc=V('kc'), answer=True)],
    #),

    'is_greatest_a': Operator(head=('is_greatest_a',  V('equation'), V('lesser_square_a'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False)&Fact(field=V('lesser_square_a'), value=V('lesser_square_a_value'), kc=V('lesser_square_a_kc'), answer=True),
                         effects=[Fact(field='is_greatest_a', value=(is_greatest_a, V('eq'), V('lesser_square_a_value')), kc=V('kc'), answer=True)],
    ),


    'divide_out_a': Operator(head=('divide_out_a',  V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='divide_out_a', value=(divide_out_a, V('eq')), kc=V('kc'), answer=True)],
    ), 

    'reduce_radical_a': Operator(head=('reduce_radical_a', V('equation'), V('kc')),
                                       precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                       effects=[Fact(field='reduce_radical_a', value=(reduce_radical_a, V('eq')), kc=V('kc'), answer=True)],
    ),

    'solve_expr': Operator(head=('solve_expr', V('equation'), V('kc')),
                                       precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                       effects=[Fact(field='solve_expr', value=(solve_expr, V('eq')), kc=V('kc'), answer=True)],
    ),


    'reduce_radical_subproblem' : Method(head=('reduce_radical_subproblem', V('equation')),
                              preconditions=[
                                  Fact(scaffold=V('level'))&
                                  Filter(lambda level : type(level) == str and level.split('_')[1].split('r')[int('1')] == '2'),
                                  Fact(scaffold=V('level'))&
                                  Filter(lambda level : type(level) == str and level.split('_')[1].split('r')[int('1')] == '1'),
                                  Fact(scaffold=V('level'))&
                                  Filter(lambda level : type(level) == str and level.split('_')[1].split('r')[int('1')] == '0'),
                              ],
                              subtasks=[
                                  [
                                      Task(head=('lesser_square_a', V('equation'), ('lesser_square_a',)), primitive=True),
                                      #Task(head=('is_factor', V('equation'), 'lesser_square', ('is_factor',)), primitive=True),
                                      Task(head=('is_greatest_a', V('equation'), 'lesser_square_a', ('is_greatest_a',)), primitive=True),
                                      Task(head=('divide_out_a', V('equation'), ('divide_out_a',)), primitive=True),
                                      Task(head=('reduce_radical_a', V('equation'), ('reduce_radical_a',)), primitive=True),
                                  ],
                                  [
                                      Task(head=('divide_out_a', V('equation'), ('divide_out_a',)), primitive=True),
                                      Task(head=('reduce_radical_a', V('equation'), ('reduce_radical_a',)), primitive=True),
                                  ],
                                  [
                                      Task(head=('reduce_radical_a', V('equation'), ('reduce_radical_a',)), primitive=True),
                                  ]
                              ]
    ),


    'solve': Method(head=('solve', V('equation')),
                    preconditions=[
                        Fact(scaffold=V('level'))&
                                  Filter(lambda level : type(level) == str and level.split('_')[1].split('r')[int('0')] == '2'),
                                  Fact(scaffold=V('level'))&
                                  Filter(lambda level : type(level) == str and level.split('_')[1].split('r')[int('0')] == '1'),
                                  Fact(scaffold='level_0r0'),
                    ],
                    subtasks=[
                        [
                            Task(head=('apply_product_rule', V('equation'), ('apply_product_rule',)), primitive=True),
                            Task(head=('multiply_radicands', V('equation'), ('multiply_radicands',)), primitive=True),
                            Task(head=('reduce_radical_subproblem', V('equation'),), primitive=False),
                            Task(head=('solve_expr', V('equation'), ('solve_expr',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('apply_product_rule', V('equation'), ('apply_product_rule',)), primitive=True),
                            Task(head=('reduce_radical_subproblem', V('equation'),), primitive=False),
                            Task(head=('solve_expr', V('equation'), ('solve_expr',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('solve_expr', V('equation'), ('solve_expr',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ]
                    ]
    ),
}

def htn_radicals_product_rule_kc_mapping():
    kcs = {
        "apply_product_rule": "apply_product_rule",
        "multiply_radicands": "multiply_radicands",
        "lesser_square_a" : "lesser_square_a",
        #"is_factor" : "is_factor",
        "is_greatest_a" : "is_greatest_a",
        "divide_out_a" : "divide_out_a",
        "reduce_radical_a": "reduce_radical_a",
        "solve_expr": "solve_expr",
        "done": "done"
    }
    return kcs


def htn_radicals_product_rule_intermediate_hints():
    hints = {
        "apply_product_rule": ["Take both square roots under the same square root."],
        "multiply_radicands": ["The product can by found by multiplying the numbers under both square roots."],
        "lesser_square_a" : ["Think of perfect squares less than or equal to the product."],
        #"is_factor" : ["Select whether the perfect square is a factor of the product. Does it divide the product evenly?"],
        "is_greatest_a" : ["Select whether this perfect square is the greatest square factor of the product. This should not be true if it is not a factor."],
        "divide_out_a" : ["Rewrite the radicand as the product of the greatest square factor and the remaining factor"],
        "reduce_radical_a": ["Simplify the square root."],
        "solve_expr" : ["Solve the expression by applying the product rule and simplifying the result."]
    }
    return hints

def htn_radicals_product_rule_studymaterial():
    study_material = studymaterial["radicals_product_rule"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_radicals_redesign',
                                             'htn_radicals_product_rule_redesign',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_radicals_product_rule_problem,
                                             htn_radicals_product_rule_kc_mapping(),
                                             htn_radicals_product_rule_intermediate_hints(),
                                             htn_radicals_product_rule_studymaterial()))