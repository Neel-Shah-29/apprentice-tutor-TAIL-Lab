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

    
def htn_radicals_subtracting_square_roots_problem():
    c1 = generate_prime(2,10)
    ra =  generate_prime(2,10)
    rb = (randint(2,6))** 2
    rc = (randint(1,5))** 2
    c2 = generate_prime(2,10)
    return {"Problem" : f"{c1}\sqrt{{{ra * rb}}} - {c2}\sqrt{{{ra * rc}}}", "Problem Args" : {"Perfect Square" : False, "Subdivision Skill Mapping" : {2 : "reduce_radical_a", 3 : "reduce_radical_b"}}}


def lesser_square_a(init_value):
    ind = '1'
    c1, rarb, c2, rarc = re.findall(r'\d+', init_value)
    c1, rarb, c2, rarc = int(c1), int(rarb), int(c2), int(rarc)
    rad = rarb if ind == '1' else rarc

    max_square_factor = max(new_find_factors(rad)[1])
    lesser_squares = [n for n in range(rad, 0, -1) if is_perfect_square(n)]
    value = tuple([(re.compile(str(f)), str(max_square_factor)) for f in lesser_squares])
    return value

def lesser_square_b(init_value):
    ind = '2'
    c1, rarb, c2, rarc = re.findall(r'\d+', init_value)
    c1, rarb, c2, rarc = int(c1), int(rarb), int(c2), int(rarc)
    rad = rarb if ind == '1' else rarc

    max_square_factor = max(new_find_factors(rad)[1])
    lesser_squares = [n for n in range(rad, 0, -1) if is_perfect_square(n)]
    value = tuple([(re.compile(str(f)), str(max_square_factor)) for f in lesser_squares])
    return value


def is_factor(init_value, lesser_square):
    n, m = [int(x) for x in re.findall(r'\d+', init_value)]
    print("(!!!!!!!!!!!!) LESSER SQUARE", lesser_square)
    radicand = n * m
    factors, __ = new_find_factors(radicand)
    if int(lesser_square) in factors:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('checked')))), 'checked')])
    else:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('unchecked')))), 'unchecked')])
    return value

def is_greatest_a(init_value, lesser_square_a):
    ind ='1'
    c1, rarb, c2, rarc = re.findall(r'\d+', init_value)
    c1, rarb, c2, rarc = int(c1), int(rarb), int(c2), int(rarc)
    rad = rarb if ind == '1' else rarc

    max_square_factor = max(new_find_factors(rad)[1])
    if int(lesser_square_a) == max_square_factor:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('yes')))), 'yes')])
    else:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('no')))), 'no')])
    return value

def is_greatest_b(init_value, lesser_square_b):
    ind = '2'
    c1, rarb, c2, rarc = re.findall(r'\d+', init_value)
    c1, rarb, c2, rarc = int(c1), int(rarb), int(c2), int(rarc)
    rad = rarb if ind == '1' else rarc

    max_square_factor = max(new_find_factors(rad)[1])
    if int(lesser_square_b) == max_square_factor:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('yes')))), 'yes')])
    else:
        value = tuple([(re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(parse_latex('no')))), 'no')])
    return value


def divide_out_a(init_value):
    ind = '1'
    c1, rarb, c2, rarc = re.findall(r'\d+', init_value)
    c1, rarb, c2, rarc = int(c1), int(rarb), int(c2), int(rarc)
    rad = rarb if ind == '1' else rarc
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
    c1, rarb, c2, rarc = re.findall(r'\d+', init_value)
    c1, rarb, c2, rarc = int(c1), int(rarb), int(c2), int(rarc)
    rad = rarb if ind == '1' else rarc
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
    c1, rarb, c2, rarc = re.findall(r'\d+', init_value)
    c1, rarb, c2, rarc = int(c1), int(rarb), int(c2), int(rarc)
    rad = rarb if ind == '1' else rarc

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
    c1, rarb, c2, rarc = re.findall(r'\d+', init_value)
    c1, rarb, c2, rarc = int(c1), int(rarb), int(c2), int(rarc)
    rad = rarb if ind == '1' else rarc

    r1 = max(new_find_factors(rad)[1])
    ra = rad // r1
    if r1 == 1:
        answer = parse_latex(f"\\sqrt{{{ra}}}")
    else:
        answer = parse_latex(f"{sp.sqrt(r1)} * \\sqrt{{{ra}}}")
    hint = latex(answer)
    answer = re.compile(re.sub(r'([-+^()*])', r'\\\1', sstr(answer, order="grlex")))
    return tuple([(answer, hint)])



def evaluate_coefficient_a(init_value):
    c1, rarb, c2, rarc = re.findall(r'\d+', init_value)
    c1, rarb, c2, rarc = int(c1), int(rarb), int(c2), int(rarc)
    rb = max(new_find_factors(rarb)[1])
    
    ra = rarb // rb
    c3 = sp.sqrt(rb)*c1
    
    ans = re.compile(rf"{c3}\*sqrt\({ra}\)")
    answer = sp.Mul(c1, sp.sqrt(ra), sp.sqrt(rb))
    hint = latex(answer)
    return tuple([
        (ans, hint),
    ])

def evaluate_coefficient_b(init_value):
    c1, rarb, c2, rarc = re.findall(r'\d+', init_value)
    c1, rarb, c2, rarc = int(c1), int(rarb), int(c2), int(rarc)

    rc = max(new_find_factors(rarc)[1])
    ra = rarc // rc
    c4 = sp.sqrt(rc)*c2
    ans = re.compile(rf"{c4}\*sqrt\({ra}\)")
    answer = sp.Mul(c2, sp.sqrt(rc), sp.sqrt(ra))
    hint = latex(answer)
    return tuple([
        (ans, hint),
    ])


def subtracting_square_root(init_value):
    c1, rarb, c2, rarc = re.findall(r'\d+', init_value)
    c1, rarb, c2, rarc = int(c1), int(rarb), int(c2), int(rarc)
    rb = max(new_find_factors(rarb)[1])
    rc = max(new_find_factors(rarc)[1])
    ra = rarb // rb
    c3 = sp.sqrt(rb)*c1
    c4 = sp.sqrt(rc)*c2
    c5 = c3 - c4

    if c5 == 1:
        ans1 = re.compile(rf"sqrt\({ra}\)")
        ans2 = re.compile(rf"sqrt\({ra}\)")
    elif c5 == -1:
        ans1 = re.compile(rf"-sqrt\({ra}\)")
        ans2 = re.compile(rf"-sqrt\({ra}\)")
    else:
        ans1 = re.compile(rf"{c5}\*sqrt\({ra}\)")
        ans2 = re.compile(rf"sqrt\({ra}\)\*{c5}")
    answer = sp.simplify(sp.Add(sp.Mul(c1, sp.sqrt(ra), sp.sqrt(rb)), sp.Mul(-1 * c2, sp.sqrt(ra), sp.sqrt(rc))))
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


    'subtracting_square_root': Operator(head=('subtracting_square_root', V('equation'), V('kc')),
                                   precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                   effects=[Fact(field='subtracting_square_root', value=(subtracting_square_root, V('eq')), kc=V('kc'), answer=True)],
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

    'evaluate_coefficient_a': Operator(head=('evaluate_coefficient_a', V('equation'), V('kc')),
                                     precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                     effects=[Fact(field='evaluate_coefficient_a', value=(evaluate_coefficient_a, V('eq')), kc=V('kc'), answer=True)],
    ),

    'evaluate_coefficient_b': Operator(head=('evaluate_coefficient_b', V('equation'), V('kc')),
                                     precondition=Fact(field=V('equation'), value=V('eq'), answer=False),
                                     effects=[Fact(field='evaluate_coefficient_b', value=(evaluate_coefficient_b, V('eq')), kc=V('kc'), answer=True)],
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
                                      Task(head=('evaluate_coefficient_a', V('equation'), ('evaluate_coefficient_a',)), primitive=True),
                                  ],
                                  [
                                      Task(head=('divide_out_a', V('equation'), ('divide_out_a',)), primitive=True),
                                      Task(head=('reduce_radical_a', V('equation'), ('reduce_radical_a',)), primitive=True),
                                      Task(head=('evaluate_coefficient_a', V('equation'), ('evaluate_coefficient_a',)), primitive=True),
                                  ],
                                  [
                                      Task(head=('reduce_radical_a', V('equation'), ('reduce_radical_a',)), primitive=True),
                                      Task(head=('evaluate_coefficient_a', V('equation'), ('evaluate_coefficient_a',)), primitive=True),
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
                                      Task(head=('evaluate_coefficient_b', V('equation'), ('evaluate_coefficient_b',)), primitive=True),
                                  ],
                                  [
                                      Task(head=('divide_out_b', V('equation'), ('divide_out_b',)), primitive=True),
                                      Task(head=('reduce_radical_b', V('equation'), ('reduce_radical_b',)), primitive=True),
                                      Task(head=('evaluate_coefficient_b', V('equation'), ('evaluate_coefficient_b',)), primitive=True),
                                  ],
                                  [
                                      Task(head=('reduce_radical_b', V('equation'), ('reduce_radical_b',)), primitive=True),
                                      Task(head=('evaluate_coefficient_b', V('equation'), ('evaluate_coefficient_b',)), primitive=True),
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
                            Task(head=('reduce_radical_subproblem_a', V('equation')), primitive=False),
                            Task(head=('reduce_radical_subproblem_b', V('equation')), primitive=False),
                            Task(head=('subtracting_square_root', V('equation'), ('subtracting_square_root',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],

                        [
                            Task(head=('subtracting_square_root', V('equation'), ('subtracting_square_root',)), primitive=True),
                            Task(head=('done', ('done',)), primitive=True)
                        ],
                    ]
    ),
}

def htn_radicals_subtracting_square_roots_kc_mapping():
    kcs = {

        'lesser_square_a':'lesser_square_a',
        'is_greatest_a':'is_greatest_a',
        'divide_out_a':'divide_out_a',
        'reduce_radical_a':'reduce_radical_a',
        'lesser_square_b':'lesser_square_b',
        'is_greatest_b':'is_greatest_b',
        'divide_out_b':'divide_out_b',
        'reduce_radical_b':'reduce_radical_b',
        'evaluate_coefficient_a':'evaluate_coefficient_a',
        'evaluate_coefficient_b':'evaluate_coefficient_b',
        'subtracting_square_root':'subtracting_square_root',
        'done':'done',
    }
    return kcs


def htn_radicals_subtracting_square_roots_intermediate_hints():
    hints = {
        "lesser_square_a":["List perfect squares that are less than or equal to the first radicand until you find the greatest square factor (you can ignore the coefficient for now)."],
        "is_greatest_a":["Select yes if the lesser square is the greatest square factor for the first radicand (you can ignore the coefficient for now)."],
        "divide_out_a" : ["Rewrite the first radicand as the product of the greatest square factor and the remaining factor (you can ignore the coefficient for now)."],
        "reduce_radical_a":["Simplify the first radicand by pulling out the perfect square from under the radical."],
        "lesser_square_b":["List perfect squares that are less than or equal to the second radicand until you find the greatest square factor (you can ignore the coefficient for now)."],
        "is_greatest_b":["Select yes if the lesser square is the greatest square factor for the second radicand (you can ignore the coefficient for now)."],
        "divide_out_b" : ["Rewrite the second radicand as the product of the greatest square factor and the remaining factor (you can ignore the coefficient for now)."],
        "reduce_radical_b":["Simplify the second radicand by pulling out the perfect square from under the radical."],
        "evaluate_coefficient_a": ["Multiply the solved square roots with the coefficient."],
        "evaluate_coefficient_b": ["Multiply the solved square roots with the coefficient."],
        "subtracting_square_root": ["Subtract the coefficients square roots with the same radicand."],
        'done': [" You have solved the problem. Click the done button!"]
    }
    return hints

def htn_radicals_subtracting_square_roots_studymaterial():
    study_material = studymaterial["radicals_subtracting_square_roots"]
    return study_material

htn_loaded_models.register(HTNCognitiveModel('htn_radicals_redesign',
                                             'htn_radicals_subtracting_square_roots_redesign',
                                             Domain,
                                             Task(head=('solve', 'equation'), primitive=False),
                                             htn_radicals_subtracting_square_roots_problem,
                                             htn_radicals_subtracting_square_roots_kc_mapping(),
                                             htn_radicals_subtracting_square_roots_intermediate_hints(),
                                             htn_radicals_subtracting_square_roots_studymaterial()))