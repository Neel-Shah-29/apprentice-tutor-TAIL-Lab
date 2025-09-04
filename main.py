import os
import statistics
import json

import traceback
from pprint import pprint
import re
from collections import defaultdict
from sqlalchemy import func
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
import io
from base64 import b64encode

# from tempfile import mkdtemp
from flask import Flask, Blueprint, flash, render_template, jsonify, send_from_directory, redirect, url_for, request, session, abort, send_file
from flask_caching import Cache
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, current_user, LoginManager, logout_user, login_user
import uuid


# for login
from pylti1p3.contrib.flask import FlaskRequest, FlaskOIDCLogin, FlaskMessageLaunch, FlaskCacheDataStorage
from pylti1p3.tool_config import ToolConfJsonFile
from pylti1p3.deep_link_resource import DeepLinkResource
from pylti1p3.lineitem import LineItem

from datetime import datetime

from pylti1p3.grade import Grade
from pylti1p3.registration import Registration

from models import db, User, UserCourse, KnowledgeComponent, UserKnowledgeComponent, TutorTransaction, VisTransaction

from collections import defaultdict

from routes.helper import get_kc_performance, get_tutor_kc_performance
from routes.helper import update_kcs
from routes.helper import create_plot
from random import choice
from collections import Counter

## Momin add
from sympy.parsing.latex._parse_latex_antlr import parse_latex
import sympy as sp 

from cognitive_models import loaded_models
from htn_cognitive_models import htn_loaded_models

# create cache and session directories
if not os.path.exists('cache'):
    os.makedirs('cache')
if not os.path.exists('session'):
    os.makedirs('session')

# Import tutoring routes 
# from routes.routes import tutor_routes

# Setup the Flask app with the database
app = Flask(__name__)

# Routes for various apprentice tutors 
# app.register_blueprint(tutor_routes)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["CACHE_TYPE"] = "FileSystemCache"
app.config["CACHE_DIR"] = "cache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 600
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = 'session'
app.config["SESSION_COOKIE_NAME"] = "flask-session-id"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = None
app.config["APPEND_TIMEZONE"] = True


# Register cognitive models
import os
import os.path

for dirpath, dirnames, filenames in os.walk("cognitive_models"):
    for filename in [f for f in filenames if f.endswith(".py")]:
        # print(os.path.join(dirpath, filename))
        exec(open(os.path.join(dirpath, filename)).read())



db.init_app(app)

# Create the database if it does not exist.
with app.app_context():
    db.create_all()
    for model in loaded_models.models:
        print(model)
        loaded_models.models[model].create_kcs(db)  

    for model in htn_loaded_models.models:
        print(model)
        htn_loaded_models.models[model].create_kcs(db)
    
    # Query for all KnowledgeComponents in the database


# Setup flask caching, which is used by LTI
cache = Cache(app)

# Login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# Load user
@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in
    # the query for the user
    return User.query.get(int(user_id))


# Home Entry
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


###################################################
# LTI Integration
###################################################
PAGE_TITLE = 'ALOE AI Institute Tutors'


class ExtendedFlaskMessageLaunch(FlaskMessageLaunch):

    def validate_nonce(self):
        """
        Probably it is bug on "https://lti-ri.imsglobal.org":
        site passes invalid "nonce" value during deep links launch.
        Because of this in case of iss == http://imsglobal.org just skip nonce
        validation.
        """
        iss = self.get_iss()
        deep_link_launch = self.is_deep_link_launch()
        if iss == "http://imsglobal.org" and deep_link_launch:
            return self
        return super(ExtendedFlaskMessageLaunch, self).validate_nonce()


def get_lti_config_path():
    return os.path.join(app.root_path, 'configs', 'tutor.json')


def get_launch_data_storage():
    return FlaskCacheDataStorage(cache)


@app.route('/lti/login/', methods=['GET', 'POST'])
def lti_login():

    tool_conf = ToolConfJsonFile(get_lti_config_path())
    launch_data_storage = get_launch_data_storage()

    flask_request = FlaskRequest(cookies=request.cookies,
                                 session=session,
                                 request_data=request.values,
                                 request_is_secure=request.is_secure)

    target_link_uri = flask_request.get_param('target_link_uri')
    if not target_link_uri:
        raise Exception('Missing "target_link_uri" param')

    oidc_login = FlaskOIDCLogin(flask_request,
                                tool_conf,
                                launch_data_storage=launch_data_storage)

    return oidc_login\
        .enable_check_cookies()\
        .redirect(target_link_uri)


@app.route('/lti/launch/', methods=['POST'])
def lti_launch():

    tool_conf = ToolConfJsonFile(get_lti_config_path())
    flask_request = FlaskRequest(cookies=request.cookies,
                                 session=session,
                                 request_data=request.values,
                                 request_is_secure=request.is_secure)

    launch_data_storage = get_launch_data_storage()
    message_launch = ExtendedFlaskMessageLaunch(
        flask_request, tool_conf, launch_data_storage=launch_data_storage)


    registration = tool_conf.find_registration(message_launch.get_iss())
    message_launch._registration = registration

    message_launch_data = message_launch.get_launch_data()

    user_id = message_launch_data['sub']
    course_id = message_launch_data['https://purl.imsglobal.org/spec/lti/claim/context']['id']
    course_name = message_launch_data['https://purl.imsglobal.org/spec/lti/claim/context']['title']
    deployment_id = message_launch_data['https://purl.imsglobal.org/spec/lti/claim/deployment_id']

    # Getting custom blackboard values if needed
    bb_key = "https://blackboard.com/webapps/foundations-connector/foundations-ids"
    if bb_key in message_launch_data:
        bb_data = message_launch_data[bb_key]
        bb_user_id = bb_data['user-id']
        bb_course_id = bb_data['course-id']


    # course_name = message_launch_data[
    #     'https://purl.imsglobal.org/spec/lti/claim/lis']['course_section_sourcedid']

    if 'http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor' in message_launch_data[
            'https://purl.imsglobal.org/spec/lti/claim/roles']:
        role = "Instructor"
    else:
        role = "Learner"

    user = User.query.filter_by(lti_user_id=user_id).first()
    
    current_conditions = [x.scaffold_type for x in User.query.all()]
    condition_counts = Counter(current_conditions)
    conditions = ["flat", "sigmoid", "ucurve"]
    scaffold_type = min(conditions, key=lambda x: condition_counts.get(x, 0))

    # conditions = ["flat", "sigmoid", "ucurve"]
    # scaffold_type = choice(conditions)
    if not user:
        user = User(lti_user_id=user_id,
                    # lti_course_id=course_id,
                    lti_deployment_id=deployment_id,
                    # consent_given=False,
                    first_name=message_launch_data.get('given_name', "none"),
                    last_name=message_launch_data.get('family_name', "none"),
                    email=message_launch_data.get('email', "none"),
                    role=role,
                    scaffold_type=scaffold_type)
        db.session.add(user)
        db.session.commit()

    if not UserCourse.query.filter_by(user_id=user.id,
                                      lti_course_id=course_id).first():
        user_course = UserCourse(user_id=user.id, course_name=course_name, lti_course_id=course_id)
        db.session.add(user_course)
        db.session.commit()

    login_user(user, remember=False)

    # Setting Cache Message Launch ID
    message_launch_id = message_launch.get_launch_id()
    user_cache_key = "message_launch_id" + "_" + user_id
    if message_launch_id is not None:
        cache.set(user_cache_key, message_launch_id)

    if message_launch.is_deep_link_launch():

        return render_template('deep_links.html',
                launch_id=message_launch.get_launch_id())

    tutor_name = message_launch_data.get('https://purl.imsglobal.org/spec/lti'
                                         '/claim/custom', {}).get('tutor',
                                                                  None)

    accepted_tutors = [tutor for tutor in htn_loaded_models.tutor_interfaces]

    if tutor_name in accepted_tutors:
        # Temporary Fix
        return tutor(tutor_name, deep_link=True)
        return redirect(url_for('home'))
    
        # return redirect("/%s" %(tutor_name))
    else:
        return redirect(url_for('home'))

@app.route('/lti/tutor/<launch_id>/<tutor_name>/<grading>', methods=['GET', 'POST'])
def configure(launch_id, tutor_name, grading):
    tool_conf = ToolConfJsonFile(get_lti_config_path())

    flask_request = FlaskRequest(cookies=request.cookies,
                                 session=session,
                                 request_data=request.values,
                                 request_is_secure=request.is_secure)

    launch_data_storage = get_launch_data_storage()

    message_launch = ExtendedFlaskMessageLaunch.from_cache(
        launch_id,
        flask_request,
        tool_conf,
        launch_data_storage=launch_data_storage)

    # from pprint import pprint
    pprint(message_launch)

    if not message_launch.is_deep_link_launch():
        raise Exception('Must be a deep link!')

    launch_url = url_for('lti_launch', _external=True)

    resource = DeepLinkResource()
    # resource.set_url(launch_url + '?tutor=' + tutor_name) \
    # TODO: set gradable property
    resource.set_url(launch_url) \
        .set_custom_params({'tutor': tutor_name, 'grading': grading }) \
        .set_title("Apprentice Tutors: " + tutor_name) 

    jwt_val = message_launch.get_deep_link().get_response_jwt([resource])

    # return html
    return render_template('deep_links_submit.html',
                jwt_val=jwt_val,
                message_launch=message_launch
                )


@app.route('/lti/jwks/', methods=['GET'])
def lti_get_jwks():
    tool_conf = ToolConfJsonFile(get_lti_config_path())
    # return jsonify({'keys': tool_conf.get_jwks()})
    return jsonify(tool_conf.get_jwks())
    

def create_registration(tool_conf):
    registration = Registration()
    registration.set_issuer(tool_conf["issuer"]) \
                .set_client_id(tool_conf["client_id"]) \
                .set_key_set_url(tool_conf["key_set_url"]) \
                .set_auth_token_url(tool_conf["auth_token_url"]) \
                .set_auth_login_url(tool_conf["auth_login_url"]) \
                .set_tool_private_key(tool_conf["private_key_file"]) \
                .set_tool_public_key(tool_conf["public_key_file"]) 
    return registration

###################################################
# Grades
###################################################

# def manage_initial_assignments_grades(message_launch, tutor):
#     # check if assignment and grades avail 
#     try:
#         if message_launch.has_ags:
#             resource_link_id = message_launch.get_launch_data() \
#             .get('https://purl.imsglobal.org/spec/lti/claim/resource_link', {}).get('id')
            

#             # Initializing variables 
#             timestamp = datetime.utcnow().isoformat() + 'Z'
#             sub = message_launch.get_launch_data().get('sub')
#             # .set_user_id(message_launch._get_jwt_body().get("sub"))


#             # Building the grade object
#             grades = message_launch.get_ags()
#             sc = Grade()
#             # sc.set_score_given() \
#             sc.set_score_maximum(100) \
#             .set_timestamp(timestamp) \
#             .set_activity_progress('InProgress') \
#             .set_grading_progress('Pending') \
#             .set_user_id(sub)

#             # Building score line item
#             sc_line_item = LineItem()
#             sc_line_item.set_tag('factoring polynomials score') \
#             .set_score_maximum(100) \
#             .set_label('Apprentice Tutor: ' + tutor)
#             if resource_link_id:
#                 sc_line_item.set_resource_id(resource_link_id)

#             result = grades.put_grade(sc, sc_line_item)

#             return jsonify({'success': True, 'result': result.get('body')})
                
#         else:
#             print("Can not create grades")
#     except Exception as err:
#         print("---------------")
#         print("An exception occurred in manage_assignments_grades try catch")
#         print(err)
#         traceback.print_exc()
#         print("---------------")

def update_tutor_grade(tutor_type, grade, user_cache_key):

    user_cache = "message_launch_id_" + user_cache_key
    
    # Getting Message Lunch ID
    message_launch_id = cache.get(user_cache)

    tool_conf = ToolConfJsonFile(get_lti_config_path())

    flask_request = FlaskRequest(cookies=request.cookies,
                                 session=session,
                                 request_data=request.values,
                                 request_is_secure=request.is_secure)

    launch_data_storage = get_launch_data_storage()

    message_launch = ExtendedFlaskMessageLaunch.from_cache(
        message_launch_id,
        flask_request,
        tool_conf,
        launch_data_storage=launch_data_storage)

    try:
        if message_launch.has_ags:
            resource_link_id = message_launch.get_launch_data() \
            .get('https://purl.imsglobal.org/spec/lti/claim/resource_link', {}).get('id')
            

            # Initializing variables 
            timestamp = datetime.utcnow().isoformat() + 'Z'
            sub = message_launch.get_launch_data().get('sub')
            # .set_user_id(message_launch._get_jwt_body().get("sub"))


            grades = message_launch.get_ags()
            sc = Grade()
            sc.set_score_given(int(grade)) \
            .set_score_maximum(100) \
            .set_timestamp(timestamp) \
            .set_activity_progress('Completed') \
            .set_grading_progress('FullyGraded') \
            .set_user_id(sub)

            # Building score line item
            sc_line_item = LineItem()
            sc_line_item.set_tag('score ' + tutor_type) \
            .set_score_maximum(100) \
            .set_label('Apprentice Tutor: ' + tutor_type)
            if resource_link_id:
                sc_line_item.set_resource_id(resource_link_id)


            result = grades.put_grade(sc, sc_line_item)

            return jsonify({'success': True, 'result': result.get('body')})
                
        else:
            print("Can not create grades")
    except Exception as err:
        print("---------------")
        print("An exception occurred in manage_assignments_grades try catch")
        print(err)
        traceback.print_exc()
        print("---------------")

def get_tutor_mastery(tutor_type):
    # Getting all user tutor mastery
    user = User.query.filter_by(lti_user_id=current_user.lti_user_id, email=current_user.email).first()
    kc_performance = get_tutor_kc_performance(user, tutor_type)
    print("------222------")
    print(kc_performance)
    print("------222------")

    # TODO: Refactor, for interface in tutor type - only query tutor type 
    # stats = {}
    # for tutor in loaded_models.tutor_interfaces:
    #     if tutor not in stats: 
    #         stats[tutor] = {}
    #     stats[tutor]['mastery'] = {}

    #     for interface in loaded_models.tutor_interfaces[tutor]:    
    #         # print(interface)
    #         tutor_interface = tutor + ":" + interface.replace("_", " ")
    #         stats[tutor]['mastery'][interface] = kc_performance[tutor_interface]

    # # Calculating average mastery 
    # tutor_stats = stats[tutor_type]['mastery']
    result_grade = 0
    for value in kc_performance.values():
        result_grade += value
    
    # using len() to get total keys for mean computation
    result_grade = int((result_grade / len(kc_performance)) * 100)
    return result_grade


###################################################
# Tutoring Pages
###################################################
# Create another route, called Deep Link Tutor 
@app.route("/<tutor>")
@login_required
def tutor(tutor, deep_link=False): 

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

    print("TUTOR", tutor)
    return render_template("tutor/{}.html".format(tutor),
            tutor_type=str(tutor), interface_type=interface) ## Got rid of deep_link

@app.route("/get_image", methods=["POST"])
@login_required
def get_image():
    x = request.get_json()
    if "variables" not in x:
        raise Exception("Variables Missing")
    a, b, c, r1, r2 = [int(val) for val in x["variables"].split(",")]
    buf = create_plot(a, b, c, r1, r2)
    image_base64 = b64encode(buf.getvalue()).decode('utf-8')
    return jsonify({"image_base64": image_base64})

@app.route("/next_problem", methods=['POST'])
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

            

    scaffold_type = False
    if "adaptive_scaffolded_" in x['tutor']:
        scaffold_type = True
        x['tutor'] = x['tutor'].replace("adaptive_scaffolded_", "")
        x['interface'] = x['interface'].replace("adaptive_scaffolded_", "")

    if 'htn' in x['tutor']:
        scaffold_type = user.scaffold_type
        interfaces = htn_loaded_models.tutor_interfaces[x["tutor"]]
    else:
        interfaces = loaded_models.tutor_interfaces[x["tutor"]]
    
    models = {}
    if 'interface' in x and x['interface'] != 'adaptive':
        tutor_type = x['interface']
        if 'htn' in x['tutor']:
            models[tutor_type] = htn_loaded_models.models[tutor_type]
        else:
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
            if 'htn' in x['tutor']:
                models[interface] = htn_loaded_models.models[interface]
            else:
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
        if scaffold_type == True:
            problem_types = [item for item in problem_types if "directly" not in item]
        tutor_type = choice(list(problem_types))

    if "." in tutor_type: 
        tutor_type = tutor_type.split(".")[0]
    if 'htn' in x['tutor']:
        tutoring_performance = get_kc_performance(user, 'htn')[1]
    else:
        tutoring_performance = get_kc_performance(user)[1]

    resp = {"tutor": x["tutor"], 
            "interface": tutor_type+".html",
            "start_state": {"initial_problem": models[tutor_type].new_problem_fn()},
            "kc_progress" : tutoring_performance[f"{x['tutor']}:{tutor_type.replace('_', ' ')}"],
            "scaffold_type": scaffold_type}
    
    # if resp is None:
    #     raise ValueError("Invalid response (None), unable to render.")
    mode = "none"
    if 'interface' in x:
        mode = x['interface']
    if scaffold_type == True:
        resp['interface'] = "adaptive_scaffolded_" + resp['interface']
        
    transaction = TutorTransaction(user_id=user.id,
                                   tutor=resp['tutor'],
                                   interface=resp['interface'],
                                   start_state=str(resp['start_state']),
                                   selection="",
                                   action="start new problem-{}".format(mode),
                                   input="",
                                   correctness="",
                                   kc_labels="",
                                   scaffold_type=user.scaffold_type)
    db.session.add(transaction)
    db.session.commit()
    return jsonify(resp)

@app.route("/get_tutorial", methods=['POST'])
@login_required
def get_tutorial():
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

    if 'htn' in x['interface']:
        model = htn_loaded_models.models[x["interface"]]
    else:
        model = loaded_models.models[x["interface"]]

    resp = model.get_study_material(x['state'])

    if resp is None:
        resp = {'study_material': ["No study_material available."]}

    # if ('selection' in resp and 'knowledge_components' in resp):
    #     if resp['selection'] not in x['attempted']:
    #         update_kcs(resp['knowledge_components'], False, user)

    transaction = TutorTransaction(
        user_id=user.id,
        tutor=x['tutor'],
        interface=x['interface'],
        start_state=str(x['start_state']),
        action=resp['action'] if 'action' in resp else "",
        correctness=f"TUTORIAL",
        kc_labels=str(resp['knowledge_components']) if 'knowledge_components' in resp else "",
        scaffold_type=user.scaffold_type)
    db.session.add(transaction)
    db.session.commit()

    return jsonify(resp)

@app.route("/get_scaffold", methods=['POST'])
@login_required
def get_scaffold():
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

    if 'htn' in x['tutor']:
        model = htn_loaded_models.models[x["interface"]]
    else:
        model = loaded_models.models[x["interface"]] 
    resp = model.get_study_material(x['state'])

    if resp is None:
        resp = {'study_material': ["No study_material available."]}

    # if ('selection' in resp and 'knowledge_components' in resp):
    #     if resp['selection'] not in x['attempted']:
    #         update_kcs(resp['knowledge_components'], False, user)

    transaction = TutorTransaction(
        user_id=user.id,
        tutor=x['tutor'],
        interface=x['interface'],
        start_state=str(x['start_state']),
        action=resp['action'] if 'action' in resp else "",
        correctness=f"SCAFFOLD",
        kc_labels=str(resp['knowledge_components']) if 'knowledge_components' in resp else "",
        scaffold_type=user.scaffold_type)
    db.session.add(transaction)
    db.session.commit()

    return jsonify(resp)


# This function returns user hints
@app.route("/get_hint", methods=['POST'])
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

    user = User.query.filter_by(email=current_user.email,
                                lti_user_id=current_user.lti_user_id
                                ).first()

    resp = None

    # print("@@@@@@@")
    # print(x["interface"])
    # print("@@@@@@@")
    if 'htn' in x['tutor']:
        model = htn_loaded_models.models[x["interface"]]
    else:
        model = loaded_models.models[x["interface"]] 

    print(x["state"])
    resp = model.get_hint(x['state'])
    
    if resp is None:
        resp = {'hints': ["No hint available."]}

    if x['hints'] is None:
        hints_match = False
    else:
        hints_match = resp.get('hints') == x['hints'].get('hints')

    hint_counter = x["hint_counter"]
    if hints_match:
        hint_counter += 1
        if hint_counter >= len(resp['hints']):
            hint_counter = len(resp['hints']) - 1
    else:
        hint_counter = 0

    hint_type = "HINT" if hint_counter == 0 else "NEXT_HINT"

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
        input=resp['hints'][hint_counter] if 'hints' in resp else "",
        correctness=hint_type,
        kc_labels=str(resp['knowledge_components'])if 'knowledge_components' in resp else "",
        scaffold_type=user.scaffold_type)
    db.session.add(transaction)
    db.session.commit()

    return jsonify(resp)

# This function logs user hints
@app.route("/log_hint", methods=['POST'])
@login_required
def log_hint():
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

    user = User.query.filter_by(email=current_user.email,
                                lti_user_id=current_user.lti_user_id
                                ).first()
    resp = {"action" : x['action'] if 'action' in x else "",
        "input" : x['hint'] if 'hint' in x else "" }
    # print("LOGGING HINT", user.id, x['tutor'], x['interface'], str(x['start_state']), 
    #     x['action'], x['hint'], x['hint_counter'])
    transaction = TutorTransaction(
        user_id=user.id,
        tutor=x['tutor'],
        interface=x['interface'],
        start_state=str(x['start_state']),
        action=x['action'] if 'action' in x else "",
        input=x['hint'] if 'hint' in x else "",
        correctness="HINT",
        kc_labels=str(x['knowledge_components'])if 'knowledge_components' in x else "",
        scaffold_type=user.scaffold_type)
    db.session.add(transaction)
    db.session.commit()

    return jsonify(resp)

# This function logs scaffold clicks
@app.route("/log_scaffold", methods=['POST'])
@login_required
def log_scaffold():
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

    user = User.query.filter_by(email=current_user.email,
                                lti_user_id=current_user.lti_user_id
                                ).first()
    resp = {"action" : x['action'] if 'action' in x else "",
        "correctness" : "SCAFFOLD" }
    # print("LOGGING SCAFFOLD", user.id, x['tutor'], x['interface'], str(x['start_state']), x['action'])
    transaction = TutorTransaction(
        user_id=user.id,
        tutor=x['tutor'],
        interface=x['interface'],
        start_state=str(x['start_state']),
        action=x['action'] if 'action' in x else "",
        correctness="SCAFFOLD",
        kc_labels=str(x['knowledge_components'])if 'knowledge_components' in x else "",
        scaffold_type=user.scaffold_type)
    db.session.add(transaction)
    db.session.commit()

    return jsonify(resp)

@app.route("/get_video", methods=['POST'])
@login_required
def get_video():
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

    if 'htn' in x['interface']:
        model = htn_loaded_models.models[x["interface"]]
    else:
        model = loaded_models.models[x["interface"]]

    resp = model.get_study_material(x['state'])

    if resp is None:
        resp = {'study_material': ["No study_material available."]}

    # if ('selection' in resp and 'knowledge_components' in resp):
    #     if resp['selection'] not in x['attempted']:
    #         update_kcs(resp['knowledge_components'], False, user)

    transaction = TutorTransaction(
        user_id=user.id,
        tutor=x['tutor'],
        interface=x['interface'],
        start_state=str(x['start_state']),
        action=resp['action'] if 'action' in resp else "",
        correctness=f"STUDYMATERIAL_{x['mode']}",
        kc_labels=str(resp['knowledge_components']) if 'knowledge_components' in resp else "",
        scaffold_type=user.scaffold_type)
    db.session.add(transaction)
    db.session.commit()

    return jsonify(resp)


@app.route("/get_read", methods=['POST'])
@login_required
def get_read():
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

    if 'htn' in x['interface']:
        model = htn_loaded_models.models[x["interface"]]
    else:
        model = loaded_models.models[x["interface"]]

    resp = model.get_study_material(x['state'])

    if resp is None:
        resp = {'study_material': ["No study_material available."]}

    # if ('selection' in resp and 'knowledge_components' in resp):
    #     if resp['selection'] not in x['attempted']:
    #         update_kcs(resp['knowledge_components'], False, user)

    transaction = TutorTransaction(
        user_id=user.id,
        tutor=x['tutor'],
        interface=x['interface'],
        start_state=str(x['start_state']),
        action=resp['action'] if 'action' in resp else "",
        correctness=f"STUDYMATERIAL_{x['mode']}",
        kc_labels=str(resp['knowledge_components']) if 'knowledge_components' in resp else "",
        scaffold_type=user.scaffold_type)
    db.session.add(transaction)
    db.session.commit()

    return jsonify(resp)


@app.route("/check_correctness", methods=['POST'])
@login_required
async def check_correctness():
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

    if 'htn' in x['tutor'] and 'htn_nursing_military' not in x['tutor']:
        model = htn_loaded_models.models[x["interface"]]
        print("HTNNNNN", x['input'])
        resp = model.check_sai(x['state'], x['selection'], x['action'], 
                               re.sub(r'(\d+)\*sqrt\((x)\)', r'\1sqrt(\2)', 
                                      sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', x['input'])), 
                                              order="grlex")).replace("-1*", "-"))  
    elif 'htn' in x['tutor']:
        model = htn_loaded_models.models[x["interface"]]
        resp = model.check_sai(x['state'], x['selection'],
                            x['action'], x['input'])
    else:    
        model = loaded_models.models[x["interface"]]   

        ## Momin add Correctness start
        # if (x["tutor"] == "logarithms" or x["tutor"] == "quadratic_equations") and (x["input"] != "checked"):
        if any(word in x["tutor"] for word in ["logarithm", "quadratic_equations", "quadratic_functions", "exponential_equations"]) and (x["input"] != "checked"):
            try:
                resp = model.check_sai(x['state'], x['selection'],
                                x['action'], re.sub(r'(\d+)\*sqrt\((x)\)', r'\1sqrt(\2)', 
                                                    sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', x['input'])), 
                                                    order="grlex")).replace("-1*", "-"))
            except sp.parsing.latex.errors.LaTeXParsingError:
                print("Incomplete LaTeX answer")
            except:
                print("Unknown Error")
        else: 
            resp = model.check_sai(x['state'], x['selection'],
                            x['action'], re.sub(r'\\sqrt(\d+)', r'\\sqrt{\1}', x['input']))
    
    print("RESP", resp)
    if 'knowledge_components' in resp and x['first_attempt']:
        print("KCS", resp['knowledge_components'])
        update_kcs(resp['knowledge_components'], resp['correct'], user)

    transaction = TutorTransaction(
        user_id=user.id,
        tutor=x['tutor'],
        interface=x['interface'],
        start_state=str(x['start_state']),
        selection=x['selection'],
        action=x['action'],
        input=x['input'],
        correctness="CORRECT" if resp['correct'] else "INCORRECT",
        kc_labels=str(resp['knowledge_components']) if 'knowledge_components' in resp else "",
        scaffold_type=user.scaffold_type)
    db.session.add(transaction)
    db.session.commit()

    # Get user cache details
    user_cache_key = current_user.lti_user_id

    if user_cache_key is not None:
        # Check if grading enabled
        user_cache = "message_launch_id_" + user_cache_key
        
        # Getting Message Lunch ID
        message_launch_id = cache.get(user_cache)


        tool_conf = ToolConfJsonFile(get_lti_config_path())

        flask_request = FlaskRequest(cookies=request.cookies,
                                    session=session,
                                    request_data=request.values,
                                    request_is_secure=request.is_secure)

        launch_data_storage = get_launch_data_storage()

        # async with ExtendedFlaskMessageLaunch.from_cache(
        #     message_launch_id,
        #     flask_request,
        #     tool_conf,
        #     launch_data_storage=launch_data_storage) as message_launch:

        #     message_launch_data = message_launch.get_launch_data()
        #     async with message_launch_data.get('https://purl.imsglobal.org/spec/lti'
        #                                     '/claim/custom', {}).get('grading',
        #                                                             None) as grading:
        
        #         if grading == "true":
        #             # Get tutor grade
        #             grade = get_tutor_mastery(x['tutor'])

        #             # Update grade
        #             result = await update_tutor_grade(x['tutor'], grade, user_cache_key)



    return jsonify(resp)


###################################################
# Authentication
###################################################
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("/auth/login.html")

    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(lti_user_id=None, email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the
        # hashed
        # password in the database
        if (not user or user.lti_user_id
                or not check_password_hash(user.password, password)):

            if user and user.lti_user_id:
                flash(
                    "Account is associated with a learning management system"
                    " (e.g., BlackBoard Learn), try logging in through that"
                    " system."
                )
            else:
                flash('Please check your login details and try again.')

            return redirect(url_for('login'))

        # if the above check passes, then we know the user has the right
        # credentials
        login_user(user, remember=remember)

        return redirect(url_for('home'))


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        else:
            return render_template("/auth/signup.html")

    elif request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        if (len(first_name) == 0 or len(last_name) == 0 or len(email) == 0 or
                len(password) == 0):
            flash("All entries required.")
            return redirect(url_for('signup'))

        # if this returns a user, then the email already exists in database
        user = User.query.filter_by(lti_user_id=None, email=email).first()

        # if a user is found, we want to redirect back to signup page so user
        # can try again
        if user:
            flash("Account with email already exists, try logging in.")
            return redirect(url_for('login'))

        # create a new user with the form data. Hash the password so the
        # plaintext version isn't saved.
        # bb_learn_id,first_name,last_name,email,password,school
        current_conditions = [x.scaffold_type for x in User.query.all()]
        condition_counts = Counter(current_conditions)
        conditions = ["flat", "sigmoid", "ucurve"]
        scaffold_type = min(conditions, key=lambda x: condition_counts.get(x, 0))


        # conditions = ["flat", "sigmoid", "ucurve"]
        # scaffold_type = choice(conditions)
        # query for what is the condition assigned ratio, and pick one that is behind

        new_user = User(first_name=first_name,
                        last_name=last_name,
                        # consent_given=False,
                        email=email,
                        password=generate_password_hash(password),
                        scaffold_type=scaffold_type,)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # if the above check passes, then we know the user has the right
        # credentials
        login_user(new_user, remember=False)

        return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

###################################################
# Misc Pages
###################################################

@app.route('/analytics', methods=["GET", 'POST'])
@login_required
def analytics():
    user = User.query.filter_by(lti_user_id=current_user.lti_user_id,
                                email=current_user.email).first()

    if user.role != "Instructor":
        return redirect("/")

    transaction = VisTransaction(
        user_id=user.id,
        student_id="",
        problem_type="",
        problem="",
        interaction="click",
        source="analytics_menu",
        input="init_session",
        version="1.0")
    db.session.add(transaction)
    db.session.commit()

    instructor_courses = UserCourse.query.filter_by(user_id=user.id)

    courses = []
    members = []
    for user_course in instructor_courses:
        student_courses = UserCourse.query.filter_by(
                lti_course_id=user_course.lti_course_id)

        course_name = user_course.course_name
        course_id = user_course.lti_course_id
        courses.append([course_id, course_name])
        for student_course in student_courses:
            m = User.query.filter_by(id=student_course.user_id).first()
            firstname = m.first_name
            lastname = m.last_name
            
            members.append({"id":m.id,
                            "name":str(m.id) + " " + firstname + " " + lastname,
                            "courseName":course_name,
                            "courseID":course_id})

    all_data = TutorTransaction.query.all()

    data = []
    students = set()
    problem_types = set()

    firstname = user.first_name
    lastname = user.last_name

    for row in all_data:

        step = {}
        step['id'] = row.id
        step['userid'] = row.user_id
        step['tutor'] = row.tutor
        step['interface'] = row.interface
        step['start_state'] = row.start_state
        step['selection'] = row.selection
        step['action'] = row.action
        step['input'] = row.input
        step['correctness'] = row.correctness
        step['kc_labels'] = row.kc_labels
        step['time'] = row.time
        step['name'] = firstname + " " + lastname

        data.append(step)
        students.add(row.user_id)
        if row.interface[-5:] == '.html':
            problem_types.add(row.interface[0:-5])
        else:
            problem_types.add(row.interface)

    stats = {}
    stats["data"] = data
    stats["students"] = members
    stats["courses"] = courses

    problem_list = list(problem_types)
    problem_list.sort()
    problem_list.insert(0, "all")
    stats["problem_types"] = problem_list

    return render_template("analytics.html", stats=stats)


# Obscure analytics link for experiment
@app.route('/qHFT89ehaggbFU3d54u0FOj1HPfoTTqht/<path:lti_id>', methods=["GET", 'POST'])
def direct_analytics(lti_id):

    user = User.query.filter_by(lti_user_id=lti_id).first()

    # cache.set("user_information", user)

    if user is None:
       return redirect("/")
    else:
        pass
   

    transaction = VisTransaction(
        user_id=user.id,
        student_id="",
        problem_type="",
        problem="",
        interaction="click",
        source="analytics_menu",
        input="init_session",
        version="1.0")
    db.session.add(transaction)
    db.session.commit()

    instructor_courses = UserCourse.query.filter_by(user_id=user.id)

    courses = []
    members = []
    for user_course in instructor_courses:
        student_courses = UserCourse.query.filter_by(
                lti_course_id=user_course.lti_course_id)

        course_name = user_course.course_name
        course_id = user_course.lti_course_id
        courses.append([course_id, course_name])
        for student_course in student_courses:
            m = User.query.filter_by(id=student_course.user_id).first()
            firstname = m.first_name
            lastname = m.last_name
            
            members.append({"id":m.id,
                            "name":str(m.id) + " " + firstname + " " + lastname,
                            "courseName":course_name,
                            "courseID":course_id})

    all_data = TutorTransaction.query.all()

    data = []
    students = set()
    problem_types = set()

    firstname = user.first_name
    lastname = user.last_name

    for row in all_data:

        step = {}
        step['id'] = row.id
        step['userid'] = row.user_id
        step['tutor'] = row.tutor
        step['interface'] = row.interface
        step['start_state'] = row.start_state
        step['selection'] = row.selection
        step['action'] = row.action
        step['input'] = row.input
        step['correctness'] = row.correctness
        step['kc_labels'] = row.kc_labels
        step['time'] = row.time
        step['name'] = firstname + " " + lastname

        data.append(step)
        students.add(row.user_id)
        if row.interface[-5:] == '.html':
            problem_types.add(row.interface[0:-5])
        else:
            problem_types.add(row.interface)

    stats = {}
    stats["data"] = data
    stats["students"] = members
    stats["courses"] = courses

    problem_list = list(problem_types)
    problem_list.sort()
    problem_list.insert(0, "all")
    stats["problem_types"] = problem_list

    return render_template("analytics.html", stats=stats)

@app.route('/vis_transaction', methods=['POST'])
def vis_transaction():
    
    x = request.get_json()    

    if current_user.is_authenticated:
        print("authenticated")
        # For login from LTI
        user = User.query.filter_by(lti_user_id=current_user.lti_user_id,
                                email=current_user.email).first()
    else:
        print("User is not authenticated.")

        # For unauthenticated login moments
        user_id = x['current_url'].split('/')[-1]
        user = User.query.filter_by(lti_user_id=user_id).first()



    transaction = VisTransaction(
        user_id=user.id,
        student_id=x['student'],
        problem_type=x['problemType'],
        problem=x['problem'],
        interaction=x['interaction'],
        source=x['source'],
        input=x['input'],
        version="1.0")
    db.session.add(transaction)
    db.session.commit()

    resp = None

    if resp is None:
        resp = {'response': ["Vis transaction recorded."]}

    return jsonify(resp)

def merge_tutors(stats):
    merged_stats = {}

    for tutor in list(stats.keys()):  # Convert to list to avoid modifying while iterating
        base_tutor = tutor.replace("_redesign", "")  # Merge `_redesign` tutors into base
        clean_tutor = base_tutor.replace("htn_", "")  # Remove `htn_` prefix

        if clean_tutor not in merged_stats:
            merged_stats[clean_tutor] = {}

        for student, data in stats[tutor].items():
            if student not in merged_stats[clean_tutor]:
                # Initialize merged student data
                merged_stats[clean_tutor][student] = {
                    "lti_user_id": data["lti_user_id"],
                    "steps": {},
                    "solved": {},
                    "mastery": {},
                }

            # Merge steps, solved, and mastery for interfaces
            for category in ["steps", "solved", "mastery"]:
                for interface, value in data[category].items():
                    base_interface = interface.replace("_redesign", "")  # Merge `_redesign` interfaces
                    clean_interface = base_interface.replace("htn_", "")  # Remove `htn_` prefix

                    merged_stats[clean_tutor][student][category].setdefault(clean_interface, 0)

                    if category == "mastery":
                        merged_stats[clean_tutor][student][category][clean_interface] = max(
                            merged_stats[clean_tutor][student][category].get(clean_interface, 0), value
                        )
                    else:
                        merged_stats[clean_tutor][student][category][clean_interface] += value

    return merged_stats




@app.route('/class', methods=["GET", 'POST'])
@login_required
def course():
    user = User.query.filter_by(lti_user_id=current_user.lti_user_id,
                                email=current_user.email).first()

    # ALTERNING to == but change back to !=
    if user.role != "Instructor":
        return redirect("/")

    instructor_courses = UserCourse.query.filter_by(user_id=user.id)

    members = []
    course_members = {}

    for user_course in instructor_courses:
        student_courses = UserCourse.query.filter_by(
                lti_course_id=user_course.lti_course_id)
        for student_course in student_courses:
            member = User.query.filter_by(id=student_course.user_id).first()
            members.append(member)

            if user_course.course_name not in course_members:
                course_members[user_course.course_name] = []
            course_members[user_course.course_name].append({
                "name":  "{} {}".format(member.first_name, member.last_name),
                "lti_user_id": member.lti_user_id
            })  

    if not members:
        return render_template("class.html", stats={}, course_sections=[], course_members={})

    # Fetch all transactions in a single query
    transactions = TutorTransaction.query.filter(
        TutorTransaction.user_id.in_([m.id for m in members])
    ).all()

    # Convert transactions to a DataFrame
    df = pd.DataFrame([{
        "user_id": t.user_id,
        "interface": t.interface.replace(".html", ""),
        "action": t.action,
        "correctness": t.correctness
    } for t in transactions])
    # print(df.head())  # Should show transaction data


    # Fetch user details
    user_info = {m.id: f"{m.first_name} {m.last_name}" for m in members}

    # Count steps per interface per user
    steps = df.groupby(["user_id", "interface"]).size().unstack(fill_value=0)

    # Count total steps per user
    steps["total_steps"] = df.groupby("user_id").size()

    # Count solved problems per interface per user
    solved = df[df["action"] == "button click"]
    solved = solved[solved["correctness"] == "CORRECT"].groupby(["user_id", "interface"]).size().unstack(fill_value=0)

    # Count total solved problems per user
    solved["total_solved"] = df[(df["action"] == "button click") & (df["correctness"] == "CORRECT")].groupby("user_id").size()
    print(solved.head())
    print(steps.head())
    # Fetch mastery scores in a batch
    mastery = {}
    for member in members:
        mastery[member.id] = get_kc_performance(member, 'htn') if 'htn' in steps.columns else get_kc_performance(member)

    # Structure the final output
    stats = {}
    for tutor, interfaces in htn_loaded_models.tutor_interfaces.items():
        stats[tutor] = {}
        
        for member in members:
            name = user_info[member.id]
            
            # Get steps and solved data, but only for relevant tutor interfaces
            relevant_steps = {iface: steps.loc[member.id][iface] if (member.id in steps.index and iface in steps.columns) else 0 for iface in interfaces}
            relevant_solved = {iface: solved.loc[member.id][iface] if (member.id in solved.index and iface in solved.columns) else 0 for iface in interfaces}

            stats[tutor][name] = {
                "lti_user_id": member.lti_user_id,
                "steps": relevant_steps,
                "solved": relevant_solved,
                "mastery": {iface: mastery[member.id][1].get(f"{tutor}:{iface.replace('_', ' ')}", 0) for iface in interfaces}
            }
            total_steps = sum(relevant_steps.values())
            total_solved = sum(relevant_solved.values())
            stats[tutor][name]["steps"]["total_steps"] = total_steps
            stats[tutor][name]["solved"]["total_solved"] = total_solved
    stats = merge_tutors(stats)
    # print(stats)
    # getting all possible courses
    course_sections = []
    for course in UserCourse.query.filter_by():
        course_sections.append(course.course_name)

#     temp_payload = {'exponents': {'N/A N/A': {'lti_user_id': '00df14ac9c684c0db99ac55caa655f33',
#                             'steps': {'exponents_power_rule': 0.1,
#                                         'exponents_product_rule': 0.1,
#                                         'exponents_quotient_rule': 0.1},
#                             'mastery': {'exponents_power_rule': 0.1,
#                                         'exponents_product_rule': 0.1,
#                                         'exponents_quotient_rule': 0.1},
#                             'solved': {'exponents_power_rule': 0,
#                                        'exponents_product_rule': 0,
#                                        'exponents_quotient_rule': 0}}},
#   'factoring_polynomials': {'N/A N/A': {'lti_user_id': '00df14ac9c684c0db99ac55caa655f33',
#                                         'mastery': {'factor_area_box': 0.24802797202797203,
#                                                     'factor_grouping': 0.3176881941587824,
#                                                     'factor_leading_one': 0.4700699300699301,
#                                                     'factor_slip_slide': 0.2947736474052264},
#                                         'solved': {'factor_area_box': 0,
#                                                    'factor_grouping': 0,
#                                                    'factor_leading_one': 0,
#                                                    'factor_slip_slide': 0}}},
#   'radicals': {'N/A N/A': {'lti_user_id': '00df14ac9c684c0db99ac55caa655f33',
#                            'mastery': {'radicals_adding_square_roots': 0.10140023337222871,
#                                        'radicals_product_rule': 0.1,
#                                        'radicals_quotient_rule': 0.1,
#                                        'radicals_subtracting_square_roots': 0.3069946389666343},
#                            'solved': {'radicals_adding_square_roots': 0,
#                                       'radicals_product_rule': 0,
#                                       'radicals_quotient_rule': 0,
#                                       'radicals_subtracting_square_roots': 0}}},
#   'rational_equation': {'N/A N/A': {'lti_user_id': '00df14ac9c684c0db99ac55caa655f33',
#                                     'mastery': {'rational_equation_find_domain': 0.0,
#                                                 'rational_equation_specific_variable': 0.0},
#                                     'solved': {'rational_equation_find_domain': 0,
#                                                'rational_equation_specific_variable': 0}}}}


    # return render_template("class.html", stats=stats, course_sections=temp_payload, course_members=course_members)
    return render_template("class.html", stats=stats, course_sections=course_sections, course_members=course_members)

@app.route('/profile', methods=["GET", 'POST'])
@login_required
def profile():
    user = User.query.filter_by(lti_user_id=current_user.lti_user_id,
                                email=current_user.email).first()

    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        db.session.add(user)
        db.session.commit()

    tutoring_performance = get_kc_performance(user, 'htn')
    # print("--------")
    # pprint(tutoring_performance[1])
    # print("--------")
    user_kcs = tutoring_performance[0]
    tutoring_performance_map = tutoring_performance[1]

    slip_slide_progress = tutoring_performance[2]["htn_factoring_polynomials"]["htn_factor_slip_slide"]["progress"]
    # box_progress = tutoring_performance[2]["htn_factoring_polynomials"]["htn_factor_area_box"]["progress"]
    leading_progress = tutoring_performance[2]["htn_factoring_polynomials"]["htn_factor_leading_one"]["progress"]
    grouping_progress = tutoring_performance[2]["htn_factoring_polynomials"]["htn_factor_grouping"]["progress"]
    product_rule_progress = tutoring_performance[2]["htn_radicals"]["htn_radicals_product_rule"]["progress"]
    quotient_rule_progress = tutoring_performance[2]["htn_radicals"]["htn_radicals_quotient_rule"]["progress"]
    adding_sqrt_progress = tutoring_performance[2]["htn_radicals"]["htn_radicals_adding_square_roots"]["progress"]
    subtracting_sqrt_progress = tutoring_performance[2]["htn_radicals"]["htn_radicals_subtracting_square_roots"]["progress"]
    exponent_product_progress = tutoring_performance[2]["htn_exponents"]["htn_exponents_product"]["progress"]
    exponent_power_progress = tutoring_performance[2]["htn_exponents"]["htn_exponents_power"]["progress"]
    exponent_quotient_progress = tutoring_performance[2]["htn_exponents"]["htn_exponents_quotient"]["progress"]
    logarithm_product_progress = tutoring_performance[2]["htn_logarithms"]["htn_logarithms_product"]["progress"]
    logarithm_power_progress = tutoring_performance[2]["htn_logarithms"]["htn_logarithms_power"]["progress"]
    logarithm_quotient_progress = tutoring_performance[2]["htn_logarithms"]["htn_logarithms_quotient"]["progress"]
    # quadratic_equations_solve_directly_progress = tutoring_performance[2]["htn_quadratic_equations"]["htn_quadratic_equations_solve_directly"]["progress"]
    # quadratic_equations_factorize_directly_progress = tutoring_performance[2]["htn_quadratic_equations"]["htn_quadratic_equations_factorize_directly"]["progress"]
    quadratic_equations_identify_coeffs_progress = tutoring_performance[2]["htn_quadratic_equations"]["htn_quadratic_equations_identify_coeffs"]["progress"]
    quadratic_equations_factorize_progress = tutoring_performance[2]["htn_quadratic_equations"]["htn_quadratic_equations_factorize"]["progress"]
    quadratic_equations_solve_using_factors_progress = tutoring_performance[2]["htn_quadratic_equations"]["htn_quadratic_equations_solve_using_factors"]["progress"]
    quadratic_equations_solve_using_square_root_property_progress = tutoring_performance[2]["htn_quadratic_equations"]["htn_quadratic_equations_solve_using_square_root_property"]["progress"]
    quadratic_equations_solve_using_completing_square_progress = tutoring_performance[2]["htn_quadratic_equations"]["htn_quadratic_equations_solve_using_completing_square"]["progress"]
    quadratic_equations_nature_of_solution_progress = tutoring_performance[2]["htn_quadratic_equations"]["htn_quadratic_equations_nature_of_solution"]["progress"]
    quadratic_equations_solve_using_quadratic_formula_progress = tutoring_performance[2]["htn_quadratic_equations"]["htn_quadratic_equations_solve_using_quadratic_formula"]["progress"]
    exponential_equations_common_base_progress = tutoring_performance[2]["htn_exponential_equations"]["htn_exponential_equations_common_base"]["progress"]
    exponential_equations_change_to_common_base_progress = tutoring_performance[2]["htn_exponential_equations"]["htn_exponential_equations_change_to_common_base"]["progress"]
    exponential_equations_fractional_exponents_common_base_progress = tutoring_performance[2]["htn_exponential_equations"]["htn_exponential_equations_fractional_exponents_common_base"]["progress"]
    exponential_equations_different_base_progress = tutoring_performance[2]["htn_exponential_equations"]["htn_exponential_equations_different_base"]["progress"]
    exponential_equations_solve_Aekt_progress = tutoring_performance[2]["htn_exponential_equations"]["htn_exponential_equations_solve_Aekt"]["progress"]
    exponential_equations_solve_quadratic_form_progress = tutoring_performance[2]["htn_exponential_equations"]["htn_exponential_equations_solve_quadratic_form"]["progress"]
    # logarithmic_equations_solve_algebraically_directly_progress = tutoring_performance[2]["htn_logarithmic_equations"]["htn_logarithmic_equations_solve_algebraically_directly"]["progress"]
    # logarithmic_equations_solve_using_one_to_one_property_directly_progress = tutoring_performance[2]["htn_logarithmic_equations"]["htn_logarithmic_equations_solve_using_one_to_one_property_directly"]["progress"]
    logarithmic_equations_solve_algebraically_progress = tutoring_performance[2]["htn_logarithmic_equations"]["htn_logarithmic_equations_solve_algebraically"]["progress"]
    logarithmic_equations_solve_algebraically_before_after_progress = tutoring_performance[2]["htn_logarithmic_equations"]["htn_logarithmic_equations_solve_algebraically_before_after"]["progress"]
    logarithmic_equations_solve_using_one_to_one_property_progress = tutoring_performance[2]["htn_logarithmic_equations"]["htn_logarithmic_equations_solve_using_one_to_one_property"]["progress"]
    # characterstics_of_quadratic_functions_progress = tutoring_performance[2]["quadratic_functions"]["characterstics_of_quadratic_functions"]["progress"]
    nursing_military_analog_to_military_progress = tutoring_performance[2]["htn_nursing_military"]["htn_nursing_calculation_analog_to_military"]["progress"]
    nursing_military_standard_time_to_military_progress = tutoring_performance[2]["htn_nursing_military"]["htn_nursing_calculation_standard_time_to_military"]["progress"]
    nursing_military_military_to_standard_time_progress = tutoring_performance[2]["htn_nursing_military"]["htn_nursing_calculation_military_to_standard_time"]["progress"]
    nursing_conversions_household_units_progress = tutoring_performance[2]["htn_nursing_conversions"]["htn_nursing_calculation_converting_household_units"]["progress"]
    nursing_conversions_metric_units_progress = tutoring_performance[2]["htn_nursing_conversions"]["htn_nursing_calculation_converting_units"]["progress"]
    nursing_dim_analysis_set_up_units_progress = tutoring_performance[2]["htn_nursing_dimanalysis"]["htn_nursing_calculation_set_up_units"]["progress"]
    nursing_dim_analysis_fill_in_units_progress = tutoring_performance[2]["htn_nursing_dimanalysis"]["htn_nursing_calculation_fill_in_units"]["progress"]
    nursing_dim_analysis_calculation_progress = tutoring_performance[2]["htn_nursing_dimanalysis"]["htn_nursing_calculation_dim_analysis"]["progress"]
    nursing_math_review_plavevalue_name_progress = tutoring_performance[2]["htn_nursing_math_review"]["htn_nursing_calculation_identify_placevalue_name"]["progress"]
    nursing_math_review_placevalue_number_progress = tutoring_performance[2]["htn_nursing_math_review"]["htn_nursing_calculation_identify_placevalue_number"]["progress"]
    nursing_math_review_rounding_progress = tutoring_performance[2]["htn_nursing_math_review"]["htn_nursing_calculation_round_placevalue"]["progress"]
    nursing_proportion_identify_info_progress = tutoring_performance[2]["htn_nursing_proportion"]["htn_nursing_calculation_proportion_identify_info"]["progress"]
    nursing_proportion_calculation_progress = tutoring_performance[2]["htn_nursing_proportion"]["htn_nursing_calculation_proportion"]["progress"]
    nursing_iv_shortcut_progress = tutoring_performance[2]["htn_nursing_iv_therapy"]["htn_nursing_calculation_IV_shortcut"]["progress"]
    nursing_iv_formula_progress = tutoring_performance[2]["htn_nursing_iv_therapy"]["htn_nursing_calculation_IV_formula"]["progress"]



    return render_template("profile.html", user=user, user_kcs=user_kcs,
                        tutors=tutoring_performance_map,
                        slip_slide_map=slip_slide_progress,
                        # box_map=box_progress,
                        leading_map=leading_progress,
                        grouping_map=grouping_progress,
                        product_rule_map=product_rule_progress,
                        quotient_rule_map=quotient_rule_progress,
                        adding_sqrt_map = adding_sqrt_progress,
                        subtracting_sqrt_map = subtracting_sqrt_progress,
                        exponent_product_map = exponent_product_progress,
                        exponent_power_map = exponent_power_progress,
                        exponent_quotient_map = exponent_quotient_progress,
                        logarithm_product_map = logarithm_product_progress,
                        logarithm_power_map = logarithm_power_progress,
                        logarithm_quotient_map = logarithm_quotient_progress,
                        # quadratic_equations_solve_directly_map = quadratic_equations_solve_directly_progress,
                        # quadratic_equations_factorize_directly_map = quadratic_equations_factorize_directly_progress,
                        quadratic_equations_identify_coeffs_map = quadratic_equations_identify_coeffs_progress,
                        quadratic_equations_factorize_map = quadratic_equations_factorize_progress,
                        quadratic_equations_solve_using_factors_map = quadratic_equations_solve_using_factors_progress,
                        quadratic_equations_solve_using_square_root_property_map = quadratic_equations_solve_using_square_root_property_progress,
                        quadratic_equations_solve_using_completing_square_map = quadratic_equations_solve_using_completing_square_progress,
                        quadratic_equations_nature_of_solution_map = quadratic_equations_nature_of_solution_progress,
                        quadratic_equations_solve_using_quadratic_formula_map = quadratic_equations_solve_using_quadratic_formula_progress,
                        exponential_equations_common_base_map = exponential_equations_common_base_progress,
                        exponential_equations_change_to_common_base_map = exponential_equations_change_to_common_base_progress,
                        exponential_equations_fractional_exponents_common_base_map = exponential_equations_fractional_exponents_common_base_progress,
                        exponential_equations_different_base_map = exponential_equations_different_base_progress,
                        exponential_equations_solve_Aekt_map = exponential_equations_solve_Aekt_progress,
                        exponential_equations_solve_quadratic_form_map = exponential_equations_solve_quadratic_form_progress,
                        # logarithmic_equations_solve_algebraically_directly_map = logarithmic_equations_solve_algebraically_directly_progress,
                        # logarithmic_equations_solve_using_one_to_one_property_directly_map = logarithmic_equations_solve_using_one_to_one_property_directly_progress,
                        logarithmic_equations_solve_algebraically_map = logarithmic_equations_solve_algebraically_progress,
                        logarithmic_equations_solve_algebraically_before_after_map = logarithmic_equations_solve_algebraically_before_after_progress,
                        logarithmic_equations_solve_using_one_to_one_property_map = logarithmic_equations_solve_using_one_to_one_property_progress,
                        # characterstics_of_quadratic_functions_map = characterstics_of_quadratic_functions_progress,
                        nursing_military_analog_to_military_map = nursing_military_analog_to_military_progress,
                        nursing_military_standard_time_to_military_map = nursing_military_standard_time_to_military_progress,
                        nursing_military_military_to_standard_time_map = nursing_military_military_to_standard_time_progress,
                        nursing_conversions_household_units_map = nursing_conversions_household_units_progress,
                        nursing_conversions_metric_units_map = nursing_conversions_metric_units_progress,
                        nursing_dim_analysis_set_up_units_map = nursing_dim_analysis_set_up_units_progress,
                        nursing_dim_analysis_fill_in_units_map = nursing_dim_analysis_fill_in_units_progress,
                        nursing_dim_analysis_calculation_map = nursing_dim_analysis_calculation_progress,
                        nursing_math_review_plavevalue_name_map = nursing_math_review_plavevalue_name_progress,
                        nursing_math_review_placevalue_number_map = nursing_math_review_placevalue_number_progress,
                        nursing_math_review_rounding_map = nursing_math_review_rounding_progress, 
                        nursing_proportion_identify_info_map = nursing_proportion_identify_info_progress,
                        nursing_proportion_calculation_map = nursing_proportion_calculation_progress,
                        nursing_iv_shortcut_map = nursing_iv_shortcut_progress,
                        nursing_iv_formula_map = nursing_iv_formula_progress,
                           )

@app.route("/home", methods=["GET", 'POST'])
@login_required
def home():

    # Momin add tutorial here
    user = User.query.filter_by(email=current_user.email,
                                        lti_user_id=current_user.lti_user_id
                                        ).first()
    print("SCAFFOLD", user.scaffold_type)
    # Momin end tutorial here
    return render_template("home.html", consent_given=user.consent_given)

@app.route("/consent/<tutor_name>/<interface_name>", methods=["GET", 'POST'])
@login_required
def consent(tutor_name, interface_name):
    if request.method == 'POST':
        user = User.query.filter_by(email=current_user.email,
                                        lti_user_id=current_user.lti_user_id
                                        ).first()

        if request.form['consent_submit'] == "Agree": 
            user.consent_given = 1
            db.session.add(user)
            db.session.commit()
        if request.form['consent_submit'] == "Disagree":
            user.consent_given = 0
            db.session.add(user)
            db.session.commit()
        return render_template("tutor/{}.html".format(tutor_name),
            tutor_type=str(tutor_name), interface_type=interface_name)

    return render_template("consent.html")

###################################################
# Helper methods
###################################################
@app.route('/<path:path>')
def send_files(path):
    """Serve up the static files"""
    return send_from_directory('static', path)

@app.route("/api", methods=['POST'])
def api_call():
    x = request.get_json()
    # print(x)
    # x = {"hello":"world"}
    return jsonify(x)

###################################################
###################################################

if __name__ == "__main__":
    app.run(debug=True)
