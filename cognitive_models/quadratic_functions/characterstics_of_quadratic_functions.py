from random import randint, choice

import sympy as sp
from sympy import symbols, Eq, latex
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import re 

from py_rete import Fact, Production, ReteNetwork, V

from cognitive_models import CognitiveModel
from cognitive_models import loaded_models

from studymaterial import studymaterial

def characterstics_of_quadratic_functions_problem():
    def generate_quadratic():
        while True:
            r1, r2 = randint(-10, 10), randint(-10, 10)
            a = choice([i for i in range(-10, 11) if i != 0])
            b, c = (-a*(r1+r2)), (a*r1*r2) 
            if abs(a*b) < 40 and abs(c) < 40:
                return a, b, c, min(r1, r2), max(r1, r2)
    a, b, c, r1, r2 = generate_quadratic()

    return f"{a},{b},{c},{r1},{r2}"

    

'''
Generate product rule model
'''
def characterstics_of_quadratic_functions_model():
    net = ReteNetwork()

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="x1_value", disabled=False))
    def x1_value(init_value):
        answer = re.compile(init_value.split(",")[3])
        print("ANSWER",answer)
        hint = init_value.split(",")[3]
        return [Fact(selection="x1_value", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="x1_value", value=V('x1_value'), disabled=True) &
                Fact(field="x2_value", disabled=False))
    def x2_value(init_value):
        answer = re.compile(init_value.split(",")[4])
        hint = init_value.split(",")[4]
        return [Fact(selection="x2_value", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="x2_value", value=V('x2_value'), disabled=True) &
                Fact(field="y_value", disabled=False))
    def y_value(init_value):
        answer = re.compile(init_value.split(",")[2])
        hint = init_value.split(",")[2]
        return [Fact(selection="y_value", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="y_value", value=V('y_value'), disabled=True) &
                Fact(field="line_of_symmetry", disabled=False))
    def line_of_symmetry(init_value):
        x = symbols('x')
        x1, x2 = int(init_value.split(",")[3]), int(init_value.split(",")[4])
        mean = (x1+x2)/2 if (x1+x2)%2 else int((x1+x2)/2)
        equation = Eq(x, mean)
        answer = re.compile(re.sub(r'([-+()*])', r'\\\1', sp.sstr(equation, order="grlex")))
        hint = latex(equation)
        return [Fact(selection="line_of_symmetry", action="input change", input=answer, hint=hint)]
    
    
    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="line_of_symmetry", value=V('line_of_symmetry'), disabled=True) &
                Fact(field="vertex_of_parabola_x", disabled=False))
    def vertex_of_parabola_x(init_value):
        a, b, c, x1, x2 = [int(i) for i in init_value.split(",")]
        k = str((x1+x2)/2 if (x1+x2)%2 else int((x1+x2)/2))
        # h = a*k**2 + b*k + c
        answer = re.compile(k)
        hint = k
        return [Fact(selection="vertex_of_parabola_x", action="input change", input=answer, hint=hint)]

    @Production(Fact(field="initial_problem", value=V('init_value')) &
                Fact(field="line_of_symmetry", value=V('line_of_symmetry'), disabled=True) &
                Fact(field="vertex_of_parabola_y", disabled=False))
    def vertex_of_parabola_y(init_value):
        a, b, c, x1, x2 = [int(i) for i in init_value.split(",")]
        k = (x1+x2)/2 if (x1+x2)%2 else int((x1+x2)/2)
        h = str(a*k**2 + b*k + c)
        answer = re.compile(h)
        hint = h
        return [Fact(selection="vertex_of_parabola_y", action="input change", input=answer, hint=hint)]
    
    @Production(Fact(field="vertex_of_parabola_x", disabled=True) &
                Fact(field="vertex_of_parabola_y", disabled=True))
    def select_done():
        return [Fact(selection="done", action="button click", input=re.compile("x"), hint="")]

    net.add_production(x1_value)
    net.add_production(x2_value)
    net.add_production(y_value)
    net.add_production(line_of_symmetry)
    net.add_production(vertex_of_parabola_x)
    net.add_production(vertex_of_parabola_y)
    net.add_production(select_done)

    return net


def characterstics_of_quadratic_functions_kc_mapping():
    kcs = {
        "x1_value": "x1_value",
        "x2_value": "x2_value",
        "y_value": "y_value",
        "line_of_symmetry": "line_of_symmetry",
        "vertex_of_parabola_x": "vertex_of_parabola_x",
        "vertex_of_parabola_y": "vertex_of_parabola_y",
        "select_done": "Determine if characterstics_of_quadratic_functions problem is complete"
    }
    return kcs


def characterstics_of_quadratic_functions_intermediate_hints():
    hints = {
        "x1_value": ["Find the smaller x-intercept by looking at the intersections in x-axis."],
        "x2_value": ["Find the larger x-intercept by looking at the intersections in x-axis."],
        "y_value": ["Find y-intercept by looking at the intersection in y-axis."],
        "line_of_symmetry": ["Find line of symmetry by drawing line at mean of x-intercepts."],
        "vertex_of_parabola_x": ["Find vertex by finding intersection of line of symmetry at x-axis."],
        "vertex_of_parabola_y": ["Find vertex by finding intersection of line of symmetry at x-axis."],
    }
    return hints

def characterstics_of_quadratic_functions_studymaterial():
    study_material = studymaterial["characterstics_of_quadratic_functions"]
    return study_material

loaded_models.register(CognitiveModel("quadratic_functions",
                                      "characterstics_of_quadratic_functions",
                                      characterstics_of_quadratic_functions_model,
                                      characterstics_of_quadratic_functions_problem,
                                      characterstics_of_quadratic_functions_kc_mapping(),
                                      characterstics_of_quadratic_functions_intermediate_hints(),
                                      characterstics_of_quadratic_functions_studymaterial()))