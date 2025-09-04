''''''
'''Exponent SAIS'''
''''''
from random import choice
from flask import Blueprint, flash, jsonify, request, render_template, abort, session
from flask_login import login_required, current_user
from models import db, User, KnowledgeComponent, UserKnowledgeComponent, TutorTransaction
from routes.helper import update_kcs

from cognitive_models import loaded_models
from routes.helper import get_kc_performance

from pylti1p3.contrib.flask import FlaskRequest, FlaskOIDCLogin, FlaskMessageLaunch, FlaskCacheDataStorage
from pylti1p3.tool_config import ToolConfJsonFile
from pylti1p3.lineitem import LineItem

from pylti1p3.grade import Grade
from pylti1p3.lineitem import LineItem

from datetime import datetime

import os


#register page
tutor_routes = Blueprint('tutor_routes', __name__)

###################################################
# Tutoring Pages
###################################################
@tutor_routes.route("/<tutor>")
@login_required
def tutor(tutor):

    if 'favico' in tutor:
        abort(404)

    # check consent
    user = User.query.filter_by(email=current_user.email,
                                lti_user_id=current_user.lti_user_id
                                ).first()
    print(user.consent_given)
    if user.consent_given is None:
        return render_template("consent.html", tutor=tutor, interface_type="adaptive")

    interface = "adaptive"
    if 'interface' in request.args:
        interface = request.args['interface']

    return render_template("tutor/{}.html".format(tutor),
            tutor_type=str(tutor), interface_type=interface)

@tutor_routes.route("/next_problem", methods=['POST'])
@login_required
def next_problem():
    x = request.get_json()
    if "user" not in x:
        raise Exception("User Missing")
    if "tutor" not in x:
        raise Exception("tutor Missing")

    user = User.query.filter_by(email=current_user.email,
                                lti_user_id=current_user.lti_user_id
                                ).first()

    interfaces = loaded_models.tutor_interfaces[x["tutor"]]
    models = {}

    if 'interface' in x and x['interface'] != 'adaptive':
        tutor_type = x['interface']
        models[tutor_type] = loaded_models.models[tutor_type] 

        # print("-------2342342-------")
        # print(tutor_type)
        # print(interfaces)
        # # print( models[interface])
        # print("-------2342342-------")

    else:
        # Creating empty list of problem to append in line 410
        problem_types = set()

        kcs = set(
            ukc.kc.name
            for ukc in UserKnowledgeComponent.query.filter_by(user_id=user.id))

        # model = loaded_models.models[x["interface"]]  

        # interfaces = loaded_models.tutor_interfaces[x["tutor"]]
        # models = {}            

        # add missing kcs
        kcs_to_add = set()
        for interface in interfaces:
            models[interface] = loaded_models.models[interface]  
            kcs_to_add = kcs_to_add.union(set(models[interface].kc_mapping.values()))

        for kc_name in kcs_to_add:
            if kc_name in kcs:
                continue
            kc = KnowledgeComponent.query.filter_by(name=kc_name).first()
            user_kc = UserKnowledgeComponent(user_id=user.id, kc_id=kc.id)
            db.session.add(user_kc)

        db.session.commit()

        for user_kc in UserKnowledgeComponent.query.filter_by(user_id=user.id):
            if user_kc.skill_level < 0.95:
                for interface in models:
                    if user_kc.kc.name in models[interface].kc_mapping.values():
                        problem_types.add(interface)


        if len(problem_types) == 0:
            flash("You have mastered all of the problem types. Great job!")
            problem_types = interfaces

        tutor_type = choice(list(problem_types))


    if "." in tutor_type: 
        tutor_type = tutor_type.split(".")[0]


    resp = {"tutor": x["tutor"], "interface": tutor_type+".html",
                "start_state":
                    {"initial_problem": models[tutor_type].new_problem_fn()}}

    # if resp is None:
    #     raise ValueError("Invalid response (None), unable to render.")

    # TODO: TEST to see what this is doing
    mode = "none"
    if 'interface' in x:
        mode = x['interface']

    transaction = TutorTransaction(user_id=user.id,
                                   tutor=resp['tutor'],
                                   interface=resp['interface'],
                                   start_state=str(resp['start_state']),
                                   selection="",
                                   action="start new problem-{}".format(mode),
                                   input="",
                                   correctness="",
                                   kc_labels="")
    db.session.add(transaction)
    db.session.commit()

    return jsonify(resp)

# This function returns user hints
@tutor_routes.route("/get_hint", methods=['POST'])
@login_required
def get_hint():
    x = request.get_json()
    if "tutor" not in x:
        raise Exception("tutor Missing")
    if "interface" not in x:
        raise Exception("interface Missing")
    if "start_state" not in x:
        raise Exception("start_state Missing")
    if "state" not in x:
        raise Exception("state Missing")
    if "attempted" not in x:
        raise Exception("attempted Missing")

    # print(x)
    user = User.query.filter_by(email=current_user.email,
                                lti_user_id=current_user.lti_user_id
                                ).first()

    resp = None

    # print("@@@@@@@")
    # print(x["interface"])
    # print("@@@@@@@")
    print("MOMIN", x["interface"])
    model = loaded_models.models[x["interface"]]   
    resp = model.get_hint(x['state'])

    if resp is None:
        resp = {'hints': ["No hint available."]}

    if ('selection' in resp and 'knowledge_components' in resp):
        if resp['selection'] not in x['attempted']:
            update_kcs(resp['knowledge_components'], False, user)

    transaction = TutorTransaction(
        user_id=user.id,
        tutor=x['tutor'],
        interface=x['interface'],
        start_state=str(x['start_state']),
        selection=resp['selection'] if 'selection' in resp else "",
        action=resp['action'] if 'action' in resp else "",
        input=resp['input'] if 'input' in resp else "",
        correctness="HINT",
        kc_labels=str(resp['knowledge_components'])
        if 'knowledge_components' in resp else "")
    db.session.add(transaction)
    db.session.commit()

    return jsonify(resp)

@tutor_routes.route("/check_correctness", methods=['POST'])
@login_required
def check_correctness():
    x = request.get_json()
    if "user" not in x:
        raise Exception("User Missing")
    if "tutor" not in x:
        raise Exception("tutor Missing")
    if "interface" not in x:
        raise Exception("interface Missing")
    if "start_state" not in x:
        raise Exception("start_state Missing")
    if 'state' not in x:
        raise Exception('state missing')
    if 'action' not in x:
        raise Exception('action missing')
    if 'input' not in x:
        raise Exception('input missing')
    if 'first_attempt' not in x:
        raise Exception('first_attempt missing')

    user = User.query.filter_by(email=current_user.email,
                                lti_user_id=current_user.lti_user_id
                                ).first()

    model = loaded_models.models[x["interface"]]   
    resp = model.check_sai(x['state'], x['selection'],
                                         x['action'], x['input'])
    # print(resp)
    transaction = TutorTransaction(
        user_id=user.id,
        tutor=x['tutor'],
        interface=x['interface'],
        start_state=str(x['start_state']),
        selection=x['selection'],
        action=x['action'],
        input=x['input'],
        correctness="CORRECT" if resp['correct'] else "INCORRECT",
        kc_labels=str(resp['knowledge_components'])
        if 'knowledge_components' in resp else "")
    db.session.add(transaction)
    db.session.commit()

    # Get tutor grade
    # grade = get_tutor_mastery(x['tutor'])

    from main import update_tutor_grade
    # Update grade
    result = update_tutor_grade("polynomials", "10")



    return jsonify(resp)




