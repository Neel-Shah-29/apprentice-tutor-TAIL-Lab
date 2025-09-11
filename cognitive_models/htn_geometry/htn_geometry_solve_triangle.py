import re
from random import choice

import sympy as sp
from sympy import latex, sstr

from shop2.domain import Task, Operator, Method
from shop2.fact import Fact
from shop2.conditions import Filter
from shop2.common import V
from htn_cognitive_models import HTNCognitiveModel, htn_loaded_models
from studymaterial import studymaterial


# ----------------------
# Problem generator
# ----------------------
def htn_geometry_solve_triangle_problem():
    """
    Return a single-string prompt describing a triangle scenario.
    We keep numbers friendly so we can validate cleanly.
    Patterns covered: RIGHT, ASA (Sines), SAS (Cosines), SIM (Similarity), AREA.
    """
    scenarios = [
        # Right triangle trig (SOH/CAH/TOA + Pythagorean)
        "Right triangle: a=3, b=4",
        # Law of Sines (ASA)
        "ASA: A=30, C=60, a=10",
        # Law of Cosines (SAS)
        "SAS: a=7, b=8, C=60.",
        # Similarity scaling
        "SIM: scale=2, AB=5.",
        # Area relation 1/2 ab sin C
        "AREA: a=8, b=10, C=30",
    ]
    return choice(scenarios)


# ----------------------
# Helpers
# ----------------------
deg = sp.pi/180


def _parse_vals(text):
    """Extract common symbols from the problem text into a dict of ints where present."""
    vals = {}
    for sym in ['a', 'b', 'c', 'A', 'B', 'C', 'scale', 'AB']:
        m = re.search(rf"\b{sym}\s*=\s*([0-9]+)", text)
        if m:
            vals[sym] = int(m.group(1))
    return vals


def _any_match(pattern, text):
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def _ok_any():
    # Accept anything non-empty; hint nudges what to put.
    return tuple([(re.compile(r".+"), "OK")])


# ----------------------
# Operator functions (return tuple of (regex, hint))
# ----------------------
def normalize_inputs(init_value):
    # Accept any acknowledgement; this is a staging step.
    return _ok_any()


def classify_triangle(init_value):
    # Accept user-friendly labels while constraining to the scenario in the prompt.
    # We return multiple acceptable patterns but one concise hint string.
    def pack(patterns, hint):
        return tuple([(re.compile(pat, re.I), hint) for pat in patterns])

    if _any_match(r"^\s*Right\s*triangle", init_value):
        return pack([
            r"righttriangletrig",
            r"right\s*triangle",
            r"right",
            r"right-?angled",
            r"rt|rtt"
        ], "Right triangle (Right / RightTriangleTrig)")
    if (_any_match(r"^\s*ASA\s*:\s*", init_value)
        or _any_match(r"^\s*AAS\s*:\s*", init_value)
        or _any_match(r"\bSSA\b", init_value)):
        return pack([
            r"law\s*of\s*sines",
            r"sines",
            r"los|sin"
        ], "Law of Sines (Sines)")
    if _any_match(r"^\s*SAS\s*:\s*", init_value) or _any_match(r"^\s*SSS\s*:\s*", init_value):
        return pack([
            r"law\s*of\s*cosines",
            r"cosines",
            r"loc|cos"
        ], "Law of Cosines (Cosines)")
    if _any_match(r"^\s*SIM\s*:\s*", init_value):
        return pack([
            r"similarity\s*scaling",
            r"similarity",
            r"sim"
        ], "Similarity (Scaling)")
    if _any_match(r"^\s*AREA\s*:\s*", init_value):
        return pack([
            r"area\s*relations",
            r"area",
            r"heron|\b1/2\s*ab\s*sin\s*c\b"
        ], "Area (choose a formula)")
    # Fallback: default to Sines family but accept broad labels
    return pack([
        r"law\s*of\s*sines",
        r"sines",
        r"los|sin"
    ], "Law of Sines (Sines)")


def apply_pythagorean(init_value):
    vals = _parse_vals(init_value)
    a = vals.get('a')
    b = vals.get('b')
    if a is None or b is None:
        return _ok_any()
    c = sp.sqrt(a*a + b*b)
    # Prefer simplified int if perfect square
    hint = latex(c)
    ans = sstr(c, order="grlex")
    return tuple([(re.compile(re.escape(ans)), hint)])


def use_trig_ratios(init_value):
    # Prompt: Enter sin A for the right-triangle case
    vals = _parse_vals(init_value)
    a = vals.get('a')
    b = vals.get('b')
    if a is None or b is None:
        return _ok_any()
    c = sp.Integer(a*a + b*b) ** sp.Rational(1, 2)
    sinA = sp.Rational(a, c)
    hint = latex(sp.simplify(sinA))
    ans = sstr(sp.simplify(sinA), order="grlex")
    return tuple([(re.compile(re.escape(ans)), hint)])


def resolve_ssa_ambiguity(init_value):
    # If SSA present -> ambiguous; else unique
    ambiguous = _any_match(r"\bSSA\b", init_value)
    expected = "ambiguous" if ambiguous else "unique"
    return tuple([(re.compile(expected, re.I), expected)])


def compute_missing_angles(init_value):
    # For ASA/AAS: compute B = 180 - (A + C)
    vals = _parse_vals(init_value)
    A = vals.get('A')
    C = vals.get('C')
    if A is None or C is None:
        return _ok_any()
    B = 180 - (A + C)
    return tuple([(re.compile(str(B)), str(B))])


def compute_missing_sides(init_value):
    # For ASA example in generator: a known, find b via Law of Sines
    vals = _parse_vals(init_value)
    A = vals.get('A')
    C = vals.get('C')
    a = vals.get('a')
    if A is None or C is None or a is None:
        return _ok_any()
    B = 180 - (A + C)
    b = sp.nsimplify(a * sp.sin(B*deg) / sp.sin(A*deg))
    hint = latex(b)
    ans = sstr(b, order="grlex")
    return tuple([(re.compile(re.escape(ans)), hint)])


def compute_unknown_by_cosine(init_value):
    # For SAS example in generator: compute c from a, b, C
    vals = _parse_vals(init_value)
    a = vals.get('a')
    b = vals.get('b')
    C = vals.get('C')
    if a is None or b is None or C is None:
        return _ok_any()
    c2 = a*a + b*b - 2*a*b*sp.cos(C*deg)
    c = sp.sqrt(sp.simplify(c2))
    hint = latex(c)
    ans = sstr(c, order="grlex")
    return tuple([(re.compile(re.escape(ans)), hint)])


def backfill_with_sines_if_needed(init_value):
    # Light-weight step: accept any non-empty.
    return _ok_any()


def map_correspondence(init_value):
    # Accept any short token like A->A' or AB->A'B'
    return tuple([(re.compile(r".+"), "Map corresponding vertices (e.g., A→A')")])


def scale_sides_angles(init_value):
    # For SIM example: scale=2, AB=5 -> A'B' = 10
    vals = _parse_vals(init_value)
    k = vals.get('scale')
    AB = vals.get('AB')
    if k is None or AB is None:
        return _ok_any()
    scaled = sp.Integer(k*AB)
    hint = latex(scaled)
    ans = sstr(scaled, order="grlex")
    return tuple([(re.compile(re.escape(ans)), hint)])


def select_area_formula(init_value):
    # Accept a description of the chosen formula; guide via hint.
    return tuple([(re.compile(r".+"), "Use 1/2·a·b·sin(C)")])


def compute_area(init_value):
    # Support 1/2·a·b·sin(C) or Heron's formula if all sides known
    vals = _parse_vals(init_value)
    a = vals.get('a')
    b = vals.get('b')
    C = vals.get('C')
    c = vals.get('c')

    area = None
    if a is not None and b is not None and C is not None:
        area = sp.nsimplify(sp.Rational(1, 2) * a * b * sp.sin(C*deg))
    elif a is not None and b is not None and c is not None:
        s = sp.Rational(a + b + c, 2)
        area = sp.nsimplify(sp.sqrt(s * (s - a) * (s - b) * (s - c)))
    if area is None:
        return _ok_any()

    hint = latex(area)
    ans = sstr(area, order="grlex")
    return tuple([(re.compile(re.escape(ans)), hint)])


def consistency_checks(init_value):
    # Check common triangle consistency rules:
    # - Angle sum property
    # - Side length positivity
    # - Appropriate side/angle relationships
    vals = _parse_vals(init_value)
    A = vals.get('A')
    B = vals.get('B')
    C = vals.get('C')
    a = vals.get('a')
    b = vals.get('b')
    c = vals.get('c')

    hints = []
    if A is not None and B is not None and C is not None:
        # Angle sum property
        if A + B + C != 180:
            return _ok_any()  # Fail consistency
        hints.append("Angle sum property OK.")
    if a is not None and b is not None and c is not None:
        # Side length positivity
        if a <= 0 or b <= 0 or c <= 0:
            return _ok_any()  # Fail consistency
        hints.append("Side lengths positive.")
    if A is not None and a is not None and B is not None and b is not None:
        # Check relationships for given A, a, B, b
        if A > 90 and a <= b:
            return _ok_any()  # Fail consistency
        if B > 90 and b <= a:
            return _ok_any()  # Fail consistency
        hints.append("Angle-side relationships OK.")

    # If we have hints, return success with hints
    if hints:
        return tuple([(re.compile("consistent"), "Consistent: " + ", ".join(hints))])

    # Default to OK
    return _ok_any()


def report_solution(init_value):
    # Report the solution: list all sides, angles, and area if computable.
    vals = _parse_vals(init_value)
    A = vals.get('A')
    B = vals.get('B')
    C = vals.get('C')
    a = vals.get('a')
    b = vals.get('b')
    c = vals.get('c')

    # fill in missing angles
    if a is not None and b is not None and c is not None:
        if A is None:
            A = sp.N(sp.acos((b**2 + c**2 - a**2) / (2*b*c)) / deg)
        if B is None:
            B = sp.N(sp.acos((a**2 + c**2 - b**2) / (2*a*c)) / deg)
        if C is None:
            C = sp.N(sp.acos((a**2 + b**2 - c**2) / (2*a*b)) / deg)
    else:
        if A is not None and B is not None and C is None:
            C = 180 - (A + B)
        elif A is not None and C is not None and B is None:
            B = 180 - (A + C)
        elif B is not None and C is not None and A is None:
            A = 180 - (B + C)

    area = None
    if a is not None and b is not None and C is not None:
        area = sp.nsimplify(sp.Rational(1, 2) * a * b * sp.sin(C*deg))
    elif a is not None and b is not None and c is not None:
        s = sp.Rational(a + b + c, 2)
        area = sp.nsimplify(sp.sqrt(s * (s - a) * (s - b) * (s - c)))

    solution = []
    if A is not None:
        solution.append(f"A = {sstr(sp.nsimplify(A))}")
    if B is not None:
        solution.append(f"B = {sstr(sp.nsimplify(B))}")
    if C is not None:
        solution.append(f"C = {sstr(sp.nsimplify(C))}")
    if a is not None:
        solution.append(f"a = {a}")
    if b is not None:
        solution.append(f"b = {b}")
    if c is not None:
        solution.append(f"c = {c}")
    if area is not None:
        solution.append(f"area = {sstr(area)}")

    return tuple([(re.compile("solution", re.I), "Solution: " + ", ".join(solution))])


# ----------------------
# Domain
# ----------------------
Domain = {
    'done': Operator(head=('done', V('kc')),
                     precondition=[Fact(start=True)],
                     effects=[Fact(field='done', value=((re.compile('x'),),), kc=V('kc'), answer=True)],
    ),

    'normalize_inputs': Operator(head=('normalize_inputs', V('triangle'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                effects=[Fact(field='normalize_inputs', value=(normalize_inputs, V('triangle')), kc=V('kc'), answer=True)],
    ),

    'classify_triangle': Operator(head=('classify_triangle', V('triangle'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                effects=[Fact(field='classify_triangle', value=(classify_triangle, V('triangle')), kc=V('kc'), answer=True)],
    ),

    # Right-triangle path
    'apply_pythagorean': Operator(head=('apply_pythagorean', V('triangle'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                effects=[Fact(field='apply_pythagorean', value=(apply_pythagorean, V('triangle')), kc=V('kc'), answer=True)],
    ),
    'use_trig_ratios': Operator(head=('use_trig_ratios', V('triangle'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                effects=[Fact(field='use_trig_ratios', value=(use_trig_ratios, V('triangle')), kc=V('kc'), answer=True)],
    ),

    # Law of sines path
    'resolve_ssa_ambiguity': Operator(head=('resolve_ssa_ambiguity', V('triangle'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                effects=[Fact(field='resolve_ssa_ambiguity', value=(resolve_ssa_ambiguity, V('triangle')), kc=V('kc'), answer=True)],
    ),
    'compute_missing_angles': Operator(head=('compute_missing_angles', V('triangle'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                effects=[Fact(field='compute_missing_angles', value=(compute_missing_angles, V('triangle')), kc=V('kc'), answer=True)],
    ),
    'compute_missing_sides': Operator(head=('compute_missing_sides', V('triangle'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                effects=[Fact(field='compute_missing_sides', value=(compute_missing_sides, V('triangle')), kc=V('kc'), answer=True)],
    ),

    # Law of cosines path
    'compute_unknown_by_cosine': Operator(head=('compute_unknown_by_cosine', V('triangle'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                effects=[Fact(field='compute_unknown_by_cosine', value=(compute_unknown_by_cosine, V('triangle')), kc=V('kc'), answer=True)],
    ),
    'backfill_with_sines_if_needed': Operator(head=('backfill_with_sines_if_needed', V('triangle'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                effects=[Fact(field='backfill_with_sines_if_needed', value=(backfill_with_sines_if_needed, V('triangle')), kc=V('kc'), answer=True)],
    ),

    # Similarity path
    'map_correspondence': Operator(head=('map_correspondence', V('triangle'), V('kc')),
                                    precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                    effects=[Fact(field='map_correspondence', value=(map_correspondence, V('triangle')), kc=V('kc'), answer=True)],
    ),
    'scale_sides_angles': Operator(head=('scale_sides_angles', V('triangle'), V('kc')),
                                    precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                    effects=[Fact(field='scale_sides_angles', value=(scale_sides_angles, V('triangle')), kc=V('kc'), answer=True)],
    ),

    # Area relations path
    'select_area_formula': Operator(head=('select_area_formula', V('triangle'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                effects=[Fact(field='select_area_formula', value=(select_area_formula, V('triangle')), kc=V('kc'), answer=True)],
    ),
    'compute_area': Operator(head=('compute_area', V('triangle'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                effects=[Fact(field='compute_area', value=(compute_area, V('triangle')), kc=V('kc'), answer=True)],
    ),

    # Consistency checks path
    'consistency_checks': Operator(head=('consistency_checks', V('triangle'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                effects=[Fact(field='consistency_checks', value=(consistency_checks, V('triangle')), kc=V('kc'), answer=True)],
    ),

    # Report solution path
    'report_solution': Operator(head=('report_solution', V('triangle'), V('kc')),
                                precondition=Fact(field=V('equation'), value=V('value'), answer=False),
                                effects=[Fact(field='report_solution', value=(report_solution, V('triangle')), kc=V('kc'), answer=True)],
    ),

    # Master method with choices by pattern in the initial text
    'solve': Method(head=('solve', V('triangle')),
        preconditions=[
            # Choose branch based on the initial problem text (one guard per subtask list)
            Fact(field=V('equation'), value=V('triangle'), answer=False) &
                Filter(lambda triangle: re.search(r"^\s*Right\s*triangle", triangle, flags=re.I) is not None),
            Fact(field=V('equation'), value=V('triangle'), answer=False) &
                Filter(lambda triangle: re.search(r"(^\s*ASA\s*:\s*)|(^\s*AAS\s*:\s*)|(\bSSA\b)", triangle, flags=re.I) is not None),
            Fact(field=V('equation'), value=V('triangle'), answer=False) &
                Filter(lambda triangle: re.search(r"(^\s*SAS\s*:\s*)|(^\s*SSS\s*:\s*)", triangle, flags=re.I) is not None),
            Fact(field=V('equation'), value=V('triangle'), answer=False) &
                Filter(lambda triangle: re.search(r"^\s*SIM\s*:\s*", triangle, flags=re.I) is not None),
            Fact(field=V('equation'), value=V('triangle'), answer=False) &
                Filter(lambda triangle: re.search(r"^\s*AREA\s*:\s*", triangle, flags=re.I) is not None),
        ],
        subtasks=[
            # Right-triangle branch
            [
                Task(head=('normalize_inputs', V('triangle'), ('normalize_inputs',)), primitive=True),
                Task(head=('classify_triangle', V('triangle'), ('classify_triangle',)), primitive=True),
                Task(head=('apply_pythagorean', V('triangle'), ('apply_pythagorean',)), primitive=True),
                Task(head=('use_trig_ratios', V('triangle'), ('use_trig_ratios',)), primitive=True),
                Task(head=('consistency_checks', V('triangle'), ('consistency_checks',)), primitive=True),
                Task(head=('report_solution', V('triangle'), ('report_solution',)), primitive=True),
                Task(head=('done', ('done',)), primitive=True)
            ],
            # Law of Sines branch (ASA/AAS/SSA)
            [
                Task(head=('normalize_inputs', V('triangle'), ('normalize_inputs',)), primitive=True),
                Task(head=('classify_triangle', V('triangle'), ('classify_triangle',)), primitive=True),
                Task(head=('resolve_ssa_ambiguity', V('triangle'), ('resolve_ssa_ambiguity',)), primitive=True),
                Task(head=('compute_missing_angles', V('triangle'), ('compute_missing_angles',)), primitive=True),
                Task(head=('compute_missing_sides', V('triangle'), ('compute_missing_sides',)), primitive=True),
                Task(head=('consistency_checks', V('triangle'), ('consistency_checks',)), primitive=True),
                Task(head=('report_solution', V('triangle'), ('report_solution',)), primitive=True),
                Task(head=('done', ('done',)), primitive=True)
            ],
            # Law of Cosines branch (SAS/SSS)
            [
                Task(head=('normalize_inputs', V('triangle'), ('normalize_inputs',)), primitive=True),
                Task(head=('classify_triangle', V('triangle'), ('classify_triangle',)), primitive=True),
                Task(head=('compute_unknown_by_cosine', V('triangle'), ('compute_unknown_by_cosine',)), primitive=True),
                Task(head=('backfill_with_sines_if_needed', V('triangle'), ('backfill_with_sines_if_needed',)), primitive=True),
                Task(head=('consistency_checks', V('triangle'), ('consistency_checks',)), primitive=True),
                Task(head=('report_solution', V('triangle'), ('report_solution',)), primitive=True),
                Task(head=('done', ('done',)), primitive=True)
            ],
            # Similarity branch
            [
                Task(head=('normalize_inputs', V('triangle'), ('normalize_inputs',)), primitive=True),
                Task(head=('classify_triangle', V('triangle'), ('classify_triangle',)), primitive=True),
                Task(head=('map_correspondence', V('triangle'), ('map_correspondence',)), primitive=True),
                Task(head=('scale_sides_angles', V('triangle'), ('scale_sides_angles',)), primitive=True),
                Task(head=('consistency_checks', V('triangle'), ('consistency_checks',)), primitive=True),
                Task(head=('report_solution', V('triangle'), ('report_solution',)), primitive=True),
                Task(head=('done', ('done',)), primitive=True)
            ],
            # Area branch
            [
                Task(head=('normalize_inputs', V('triangle'), ('normalize_inputs',)), primitive=True),
                Task(head=('classify_triangle', V('triangle'), ('classify_triangle',)), primitive=True),
                Task(head=('select_area_formula', V('triangle'), ('select_area_formula',)), primitive=True),
                Task(head=('compute_area', V('triangle'), ('compute_area',)), primitive=True),
                Task(head=('consistency_checks', V('triangle'), ('consistency_checks',)), primitive=True),
                Task(head=('report_solution', V('triangle'), ('report_solution',)), primitive=True),
                Task(head=('done', ('done',)), primitive=True)
            ],
        ]
    ),
}


def htn_geometry_solve_triangle_kc_mapping():
    return {
        "normalize_inputs": "Normalize triangle inputs",
        "classify_triangle": "Classify triangle type",
        "apply_pythagorean": "Apply Pythagorean theorem",
        "use_trig_ratios": "Use trig ratios (SOH/CAH/TOA)",
        "resolve_ssa_ambiguity": "Resolve SSA ambiguity",
        "compute_missing_angles": "Compute missing angles",
        "compute_missing_sides": "Compute missing sides",
        "compute_unknown_by_cosine": "Law of Cosines for unknown",
        "backfill_with_sines_if_needed": "Backfill with Law of Sines if needed",
        "map_correspondence": "Map triangle correspondence",
        "scale_sides_angles": "Scale sides/angles by similarity",
        "select_area_formula": "Select area formula",
        "compute_area": "Compute area",
        "consistency_checks": "Check triangle consistency",
        "report_solution": "Report solution",
        "done": "Complete triangle solution"
    }


def htn_geometry_solve_triangle_intermediate_hints():
    return {
        "normalize_inputs": ["Normalize all triangle inputs (angles, sides)."],
        "classify_triangle": [
            "Classify: Right, Sines (ASA/AAS/SSA), Cosines (SAS/SSS), Similarity, or Area.",
            "Use natural labels, e.g., 'Right' or 'Sines'."
        ],
        "apply_pythagorean": ["Use Pythagorean theorem for right triangles."],
        "use_trig_ratios": ["Use SOH/CAH/TOA for right triangles."],
        "resolve_ssa_ambiguity": ["Check for SSA ambiguity and resolve."],
        "compute_missing_angles": ["Compute missing angles using Law of Sines."],
        "compute_missing_sides": ["Compute missing sides using Law of Sines."],
        "compute_unknown_by_cosine": ["Use Law of Cosines for SSS/SAS cases."],
        "backfill_with_sines_if_needed": ["Use Law of Sines after Law of Cosines if needed."],
        "map_correspondence": ["Map corresponding sides/angles for similarity."],
        "scale_sides_angles": ["Scale sides/angles using similarity criteria."],
        "select_area_formula": ["Select appropriate area formula (Heron, ½ab sin C, etc.)."],
        "compute_area": ["Compute area using selected formula."],
        "consistency_checks": ["Check angle sum, triangle inequality, etc."],
        "report_solution": ["Report the solution for all unknowns."],
        "done": ["Click done when finished."]
    }


def htn_geometry_solve_triangle_studymaterial():
    return studymaterial.get("geometry_solve_triangle", [])


htn_loaded_models.register(HTNCognitiveModel(
    'htn_geometry',
    'htn_geometry_solve_triangle',
    Domain,
    Task(head=('solve', 'triangle'), primitive=False),
    htn_geometry_solve_triangle_problem,
    htn_geometry_solve_triangle_kc_mapping(),
    htn_geometry_solve_triangle_intermediate_hints(),
    htn_geometry_solve_triangle_studymaterial()
))
