from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import random

db = SQLAlchemy()


# database
class User(UserMixin, db.Model):
    __table_args__ = (
        db.UniqueConstraint('lti_user_id', 'email'),
    )
    id = db.Column(db.Integer, primary_key=True)
    lti_user_id = db.Column(db.String(200), unique=True)
    # lti_course_id = db.Column(db.String(200))
    lti_deployment_id = db.Column(db.String(200))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    consent_given = db.Column(db.Boolean, default=None)
    #role = db.Column(db.String(200), default="Learner")
    role = db.Column(db.String(200), default="Instructor")
    scaffold_type = db.Column(db.String(80))
    time_created = db.Column(db.DateTime(timezone=True),
                             server_default=db.func.now())


class UserCourse(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    course_name = db.Column(db.String(200))
    lti_course_id = db.Column(db.String(200), primary_key=True)


class KnowledgeComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    learn = db.Column(db.Float, nullable=False, default=0.1)
    guess = db.Column(db.Float, nullable=False, default=0.05)
    slip = db.Column(db.Float, nullable=False, default=0.02)


class UserKnowledgeComponent(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    kc_id = db.Column(db.Integer, db.ForeignKey(KnowledgeComponent.id),
                      primary_key=True)
    kc = db.relationship(KnowledgeComponent, lazy=False)
    skill_level = db.Column(db.Float, nullable=False, default=0.1)


class Tutor_Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_type_id = db.Column(db.Integer)


class TutorTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    tutor = db.Column(db.String(200))
    interface = db.Column(db.String(200))
    start_state = db.Column(db.String(200))
    selection = db.Column(db.String(200))
    action = db.Column(db.String(200))
    input = db.Column(db.String(200))
    correctness = db.Column(db.String(200))
    kc_labels = db.Column(db.String(200))
    scaffold_type=db.Column(db.String(200))
    time = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

class VisTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    student_id = db.Column(db.Integer, db.ForeignKey(User.id))
    problem_type = db.Column(db.String(200))
    problem = db.Column(db.String(200))
    interaction = db.Column(db.String(200))
    source = db.Column(db.String(200))
    input = db.Column(db.String(200))
    version = db.Column(db.String(200))
    time = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

