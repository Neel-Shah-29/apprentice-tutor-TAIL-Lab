import sympy as sp
from random import randint, choice
from fractions import Fraction

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

    
def htn_radicals_quotient_rule_problem():
    rad =  generate_prime(2,10)
    num = (randint(2,8))** 2
    denom = (randint(5,20))** 2
    chance = randint(0, 1)
    if chance == 1:
        denom = denom * rad
    return {"Problem" : f"\sqrt{{\\frac{{{num * rad}}}{{{denom}}}}}", "Problem Args" : {"Perfect Square" : False, "Subdivision Skill Mapping" : {2 : "reduce_radical_a", 3 : "reduce_radical_b"}}}

def apply_quotient_rule(init_value):
    n, m = re.findall(r'\d+', init_value)
    answer = parse_latex(f"\\frac{{\\sqrt{{{n}}}}}{{\\sqrt{{{m}}}}}")
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
    hint = f"\\frac{{\\sqrt{{{n}}}}}{{\\sqrt{{{m}}}}}"
    return tuple([(answer, hint)])

def lesser_square_a(init_value):
    ind = '1'
    numerator, denominator = re.findall(r'\d+', init_value)
    numerator, denominator = int(numerator), int(denominator)
    rad = numerator if ind == '1' else denominator

    max_square_factor = max(new_find_factors(rad)[1])
    lesser_squares = [n for n in range(rad, 0, -1) if is_perfect_square(n)]
    value = tuple([(re.compile(str(f)), str(max_square_factor)) for f in lesser_squares])
    return value

def lesser_square_b(init_value):
    ind = '2'
    numerator, denominator = re.findall(r'\d+', init_value)
    numerator, denominator = int(numerator), int(denominator)
    rad = numerator if ind == '1' else denominator

    max_square_factor = max(new_find_factors(rad)[1])
    lesser_squares = [n for n in range(rad, 0, -1) if is_perfect_square(n)]
    value = tuple([(re.compile(str(f)), str(max_square_factor)) for f in lesser_squares])
    return value


def is_factor(init_value, lesser_square):
    n, m = [int(x) for x in re.findall(r'\d+', init_value)]
    radicand = n * m
    factors, __ = new_find_factors(radicand)
    if int(lesser_square) in factors:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('checked')))), 'checked')])
    else:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('unchecked')))), 'unchecked')])
    return value

def is_greatest_a(init_value, lesser_square_a):
    ind ='1'
    numerator, denominator = re.findall(r'\d+', init_value)
    numerator, denominator = int(numerator), int(denominator)
    rad = numerator if ind == '1' else denominator

    max_square_factor = max(new_find_factors(rad)[1])
    if int(lesser_square_a) == max_square_factor:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('yes')))), 'yes')])
    else:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('no')))), 'no')])
    return value

def is_greatest_b(init_value, lesser_square_b):
    ind = '2'
    numerator, denominator = re.findall(r'\d+', init_value)
    numerator, denominator = int(numerator), int(denominator)
    rad = numerator if ind == '1' else denominator

    max_square_factor = max(new_find_factors(rad)[1])
    if int(lesser_square_b) == max_square_factor:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('yes')))), 'yes')])
    else:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('no')))), 'no')])
    return value


def divide_out_a(init_value):
    ind = '1'
    numerator, denominator = re.findall(r'\d+', init_value)
    numerator, denominator = int(numerator), int(denominator)
    rad = numerator if ind == '1' else denominator

    r1 = max(new_find_factors(rad)[1])
    r2 = rad // r1

    ans1 = parse_latex(f"\\sqrt{{{r1} * {r2}}}")
    ans2 = parse_latex(f"\\sqrt{{{r2} * {r1}}}")
    hint = latex(ans1)
    ans1 = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(ans1, order="grlex")))
    ans2 = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(ans2, order="grlex")))

    return tuple([
        (ans1, hint),
        (ans2, hint)
        ])

def divide_out_b(init_value):
    ind = '2'
    numerator, denominator = re.findall(r'\d+', init_value)
    numerator, denominator = int(numerator), int(denominator)
    rad = numerator if ind == '1' else denominator

    r1 = max(new_find_factors(rad)[1])
    r2 = rad // r1

    ans1 = parse_latex(f"\\sqrt{{{r1} * {r2}}}")
    ans2 = parse_latex(f"\\sqrt{{{r2} * {r1}}}")
    hint = latex(ans1)
    ans1 = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(ans1, order="grlex")))
    ans2 = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(ans2, order="grlex")))

    return tuple([
        (ans1, hint),
        (ans2, hint)
        ])

def reduce_radical_a(init_value):
    ind = '1'
    numerator, denominator = re.findall(r'\d+', init_value)
    numerator, denominator = int(numerator), int(denominator)
    rad = numerator if ind == '1' else denominator

    r1 = max(new_find_factors(rad)[1])
    ra = rad // r1
    if r1 == 1:
        answer = parse_latex(f"\\sqrt{{{ra}}}")
    else:
        answer = parse_latex(f"{sp.sqrt(r1)} * \\sqrt{{{ra}}}")
    hint = latex(answer)
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
    return tuple([(answer, hint)])

def reduce_radical_b(init_value):
    ind = '2'
    numerator, denominator = re.findall(r'\d+', init_value)
    numerator, denominator = int(numerator), int(denominator)
    rad = numerator if ind == '1' else denominator

    r1 = max(new_find_factors(rad)[1])
    ra = rad // r1
    if ra != 1:
        answer = parse_latex(f"{r1} * \\sqrt{{{ra}}}")
    else:
        answer = parse_latex(f"{sp.sqrt(rad)}")
    hint = latex(answer)
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
    return tuple([(answer, hint)])


def dividing_square_root(init_value):
    numerator, denominator = re.findall(r'\d+', init_value)
    numerator, denominator = int(numerator), int(denominator)
    num_sq = max(new_find_factors(numerator)[1])
    denom_sq = max(new_find_factors(denominator)[1])
    num_rad = numerator // num_sq
    if denominator // denom_sq != 1:
        num_rad = 1
    num = sp.sqrt(num_sq)
    denom = sp.sqrt(denom_sq)

    frac = Fraction(num, denom)
    num = frac.numerator
    denom = frac.denominator

    if num_rad != 1:
        if num != 1:
            answer = parse_latex(f"\\frac{{ {num} * \\sqrt{{{num_rad}}}}}{{{denom}}}")
        else:
            answer = parse_latex(f"\\frac{{\\sqrt{{{num_rad}}}}}{{{denom}}}")
    elif denom != 1:
        answer = parse_latex(f"\\frac{{{num}}}{{{denom}}}")
    else:
        if num != 1:
            answer = parse_latex(f"{num}")
        else:
            answer = parse_latex("1")
    hint = latex(answer)
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
    return tuple([
        (answer, hint)
    ])

Domain = {
    'done': Operator(head=('done', V('kc')),
                     precondition=[Fact(start=True)],
                     effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
    ),

    'apply_quotient_rule': Operator(head=('apply_quotient_rule', V('equation'), V('kc')),
                                   precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                   effects=[Fact(field='apply_quotient_rule', value=(apply_quotient_rule, V('eq')), kc=V('kc'), answer=True)],
    ),

    'dividing_square_root': Operator(head=('dividing_square_root', V('equation'), V('kc')),
                                   precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                   effects=[Fact(field='dividing_square_root', value=(dividing_square_root, V('eq')), kc=V('kc'), answer=True)],
    ),

    'lesser_square_a': Operator(head=('lesser_square_a', V('equation'), V('kc')),
                            precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                            effects=[Fact(field='lesser_square_a', value=(lesser_square_a, V('eq')), kc=V('kc'), answer=True)],
    ),

    'lesser_square_b': Operator(head=('lesser_square_b', V('equation'), V('kc')),
                            precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                            effects=[Fact(field='lesser_square_b', value=(lesser_square_b, V('eq')), kc=V('kc'), answer=True)],
    ),

    #'is_factor': Operator(head=('is_factor',  V('equation'), V('lesser_square'), V('kc')),
    #                     precondition=Fact(field=V('equation'), value=V('eq'), answer=False)&Fact(field=V('lesser_square'), value=V('lesser_square_value'), kc=V('lesser_square_kc'), answer=True),
    #                     effects=[Fact(field='is_factor', value=(is_factor, V('eq'), V('lesser_square_value')), kc=V('kc'), answer=True)],
    #),

    'is_greatest_a': Operator(head=('is_greatest_a',  V('equation'), V('lesser_square_a'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False)&Fact(field=V('lesser_square_a'), value=V('lesser_square_a_value'), kc=V('lesser_square_a_kc'), answer=True),
                         effects=[Fact(field='is_greatest_a', value=(is_greatest_a, V('eq'), V('lesser_square_a_value')), kc=V('kc'), answer=True)],
    ),

    'is_greatest_b': Operator(head=('is_greatest_b',  V('equation'), V('lesser_square_b'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False)&Fact(field=V('lesser_square_b'), value=V('lesser_square_b_value'), kc=V('lesser_square_b_kc'), answer=True),
                         effects=[Fact(field='is_greatest_b', value=(is_greatest_b, V('eq'), V('lesser_square_b_value')), kc=V('kc'), answer=True)],
    ),

    'divide_out_a': Operator(head=('divide_out_a',  V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='divide_out_a', value=(divide_out_a, V('eq')), kc=V('kc'), answer=True)],
    ),

    'divide_out_b': Operator(head=('divide_out_b',  V('equation'), V('kc')),
                         precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                         effects=[Fact(field='divide_out_b', value=(divide_out_b, V('eq')), kc=V('kc'), answer=True)],
    ),  

    'reduce_radical_a': Operator(head=('reduce_radical_a', V('equation'), V('kc')),
                                       precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                       effects=[Fact(field='reduce_radical_a', value=(reduce_radical_a, V('eq')), kc=V('kc'), answer=True)],
    ),

    'reduce_radical_b': Operator(head=('reduce_radical_b', V('equation'), V('kc')),
                                       precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                       effects=[Fact(field='reduce_radical_b', value=(reduce_radical_b, V('eq')), kc=V('kc'), answer=True)],
    ),


    'reduce_radical_subproblem_a' : Method(head=('reduce_radical_subproblem_a', V('equation')),
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

    'reduce_radical_subproblem_b' : Method(head=('reduce_radical_subproblem_b', V('equation')),
                              preconditions=[
                                  Fact(scaffold=V('level'))&
                                  Filter(lambda level : type(level) == str and level.split('_')[1].split('r')[int('2')] == '2'),
                                  Fact(scaffold=V('level'))&
                                  Filter(lambda level : type(level) == str and level.split('_')[1].split('r')[int('2')] == '1'),
                                  Fact(scaffold=V('level'))&
                                  Filter(lambda level : type(level) == str and level.split('_')[1].split('r')[int('2')] == '0'),
                              ],
                              subtasks=[
                                  [
                                      Task(head=('lesser_square_b', V('equation'), ('lesser_square_b',)), primitive=True),
                                      #Task(head=('is_factor', V('equation'), 'lesser_square', ('is_factor',)), primitive=True),
                                      Task(head=('is_greatest_b', V('equation'), 'lesser_square_b', ('is_greatest_b',)), primitive=True),
                                      Task(head=('divide_out_b', V('equation'), ('divide_out_b',)), primitive=True),
                                      Task(head=('reduce_radical_b', V('equation'), ('reduce_radical_b',)), primitive=True),
                                  ],
                                  [
                                      Task(head=('divide_out_b', V('equation'), ('divide_out_b',)), primitive=True),
                                      Task(head=('reduce_radical_b', V('equation'), ('reduce_radical_b',)), primitive=True),
                                  ],
                                  [
                                      Task(head=('reduce_radical_b', V('equation'), ('reduce_radical_b',)), primitive=True),
                                  ]
                              ]
    ),


    'solve': Method(head=('solve', V('equation')),
                    preconditions=[
                        Fact(scaffold=V('level'))&
                        Filter(lambda level : type(level) == str and level.split('_')[1].split('r')[0] == '1'),                    
                        Fact(scaffold='level_0r0r0'),
                    ],
                    subtasks=[

                        [
                            Task(head=('apply_quotient_rule', V('equation'), ('apply_quotient_rule',)), primitive=True),
                            Task(head=('reduce_radical_subproblem_a', V('equation')), primitive=False),
                            Task(head=('reduce_radical_subproblem_b', V('equation')), primitive=False),
                            Task(head=('dividing_square_root', V('equation'), ('dividing_square_root',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('dividing_square_root', V('equation'), ('dividing_square_root',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ]
                    ]
    ),
}

def htn_radicals_quotient_rule_kc_mapping():
    kcs = {
        'apply_quotient_rule':'apply_quotient_rule',
        'lesser_square_a':'lesser_square_a',
        'is_greatest_a':'is_greatest_a',
        'divide_out_a':'divide_out_a',
        'reduce_radical_a':'reduce_radical_a',
        'lesser_square_b':'lesser_square_b',
        'is_greatest_b':'is_greatest_b',
        'divide_out_b':'divide_out_b',
        'reduce_radical_b':'reduce_radical_b',
        'dividing_square_root':'dividing_square_root',
        'done':'done',
    }
    return kcs


def htn_radicals_quotient_rule_intermediate_hints():
    hints = {
        "apply_quotient_rule":["Use the quotient rule to rewrite the expression as the quotient of two radicals."],
        "lesser_square_a":["List perfect squares that are less than or equal to the numerator until you find the greatest square factor."],
        "is_greatest_a":["Select yes if the lesser square is the greatest square factor of the numerator."],
        "divide_out_a" : ["Rewrite the numerator as the product of the greatest square factor and the remaining factor."],
        "reduce_radical_a":["Simplify the numerator by pulling out the perfect square from under the radical."],
        "lesser_square_b":["List perfect squares that are less than or equal to the denominator until you find the greatest square factor.."],
        "is_greatest_b":["Select yes if the lesser square is the greatest square factor of the denominator."],
        "divide_out_b" : ["Rewrite the denominator radicand as the product of the greatest square factor and the remaining factor."],
        "reduce_radical_b":["Simplify the denominator radicand by pulling out the perfect square from under the radical."],
        "dividing_square_root": ["Divide the numerator by the denominator, simplifying when possible."],
        'done': [" You have solved the problem. Click the done button!"]
    }
    return hints

def htn_radicals_quotient_rule_studymaterial():
    study_material = studymaterial["radicals_quotient_rule"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_radicals_redesign',
                                             'htn_radicals_quotient_rule_redesign',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_radicals_quotient_rule_problem,
                                             htn_radicals_quotient_rule_kc_mapping(),
                                             htn_radicals_quotient_rule_intermediate_hints(),
                                             htn_radicals_quotient_rule_studymaterial()))