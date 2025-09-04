from shop2.fact import Fact
from collections import defaultdict
import re
import sympy as sp
from sympy.parsing.latex._parse_latex_antlr import parse_latex
from models import KnowledgeComponent
from shop2.domain import Task, Operator, Method
from planner import planner

class HTNCognitiveModel:
    def __init__(self, tutor_name, interface_name, domain, task, new_problem_fn, kc_mapping, hints=None, study_material=None):
        self.tutor_name = tutor_name
        self.interface_name = interface_name
        self.domain = domain
        self.task = [task]
        self.new_problem_fn = new_problem_fn
        self.kc_mapping = kc_mapping
        self.hints = hints
        self.study_material = study_material

    def create_kcs(self, db):
        for kc in set(self.kc_mapping.values()):
            if not KnowledgeComponent.query.filter_by(name=kc).first():
                kc = KnowledgeComponent(name=kc)
                db.session.add(kc)
        db.session.commit()

        # some code excluded from original

    def replace_index(self, fstate, newInd):
        tempState = Fact(start=True)
        for f in fstate:
            if 'start' in f:
                pass
            if 'ind' in f:
                tempState = tempState&Fact(ind=newInd)
            else:
                tempState = tempState&f

        return tempState

    def check_sai(self, state, selection, action ,input):
        print("STATE:", state)
        print("SELECTION:", selection)
        print("ACTION:", action)
        print("INPUT:", input)

        fstate = Fact(start=True)
        answers = list()
        effect = None
        for fact_dict in state:
            if 'skill' in fact_dict:
                fstate = fstate&Fact(skill=fact_dict['skill'])
            elif 'scaffold' in fact_dict:
                fstate = fstate&Fact(scaffold=fact_dict['scaffold'])
            elif 'perfect_square' in fact_dict:
                fstate = fstate&Fact(perfect_square=fact_dict['perfect_square'])
            else:
                if fact_dict['answer'] is True:
                    answers.append(Fact(field=fact_dict['field'], value=fact_dict['value'], answer=fact_dict['answer']))
                else:
                    fstate = fstate&Fact(field=fact_dict['field'], value=fact_dict['value'], answer=fact_dict['answer'])
        
        plan = planner(fstate, self.task, self.domain)
        effect, fstate = plan.send(None)
        # in state find the dictionary whose's field is effect['field]

        #print("POST PLANNER: FSTATE", fstate)
        #print("POST PLANNER: Effect", effect)
        for answer in answers:
            value = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer['value'])), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e') if ':' not in answer['value'] else answer['value']
            while True:
                exitloop = False
                for evalue in effect['value']:
                    print("AVALUE:", value, evalue[0])
                    if (evalue[0].match(value) or evalue[0].pattern == value) and effect['field'] == answer['field']:
                        effect['value'] = answer['value']
  
                        effect, fstate = plan.send((fstate, True, effect))
                        exitloop = True
                        break
                if exitloop:
                    break
                
                effect, fstate = plan.send((fstate, False, effect))
            
        
        expected = effect

        flag = False
        while True:
            for evalue in effect['value']:
                print("MATCHED", evalue, input, effect['field'], selection, evalue==input, evalue[0].match(input), effect['field'] == selection)
                if (evalue[0].match(input) or evalue[0].pattern == input) and effect['field'] == selection:
                    return {'correct': True, 'knowledge_components': [self.kc_mapping[kcx] for kcx in effect['kc']]}
            effect, fstate = plan.send((fstate, False, effect))
            if not effect:
                return {'correct': False, 'knowledge_components':[self.kc_mapping[kcx] for kcx in expected['kc']]}
                
    
    def get_hint(self, state):
        fstate = Fact(start=True)
        answers = list()
        effect = None
        for fact_dict in state:
            if 'skill' in fact_dict:
                fstate = fstate&Fact(skill=fact_dict['skill'])
            elif 'scaffold' in fact_dict:
                fstate = fstate&Fact(scaffold=fact_dict['scaffold'])
            elif 'perfect_square' in fact_dict:
                fstate = fstate&Fact(perfect_square=fact_dict['perfect_square'])
            else:
                if fact_dict['answer'] is True:
                    answers.append(Fact(field=fact_dict['field'], value=fact_dict['value'], answer=fact_dict['answer']))
                else:
                    fstate = fstate&Fact(field=fact_dict['field'], value=fact_dict['value'], answer=fact_dict['answer'])
        plan = planner(fstate, self.task, self.domain)
        effect, fstate = plan.send(None)
        for answer in answers:
            value = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer['value'])), order="grlex").replace('-1*s', '-s').replace('-1*l', '-l').replace('-1*e', '-e') if ':' not in answer['value'] else answer['value']
            while True:
                exitloop = False
                for evalue in effect['value']:
                    print("HVALUE:", value, evalue[0])
                    if (evalue[0].match(value) or evalue[0].pattern == value) and effect['field'] == answer['field']:
                        effect['value'] = answer['value']
                        effect, fstate = plan.send((fstate, True, effect))
                        exitloop = True
                        break
                if exitloop:
                    break
                effect, fstate = plan.send((fstate, False, effect))
        
        print("FSTATE", fstate)
        print("HINT", effect)
        hints = list()
        if effect['field'] != 'done':
            for kc in effect['kc']:
                hints.extend(self.hints[kc])

        response = {'selection':effect['field'], 'hints':['Try updating this field next.', *hints],
                    'input':effect['field'], 'knowledge_components':[self.kc_mapping[kcx] for kcx in effect['kc']]}
        
        if effect['field'] == 'done':
            response['hints'] = ['Click the button to submit your answer.',]
        else:
            response['hints'].append('Enter the value {} in this field.'.format("\\({}\\)".format(effect['value'][0][1])))


        return response
        
    def get_study_material(self, state):
        fstate = Fact(start=True)
        answers = list()
        effect = None
        for fact_dict in state:
            if 'skill' in fact_dict:
                fstate = fstate&Fact(skill=fact_dict['skill'])
            elif 'scaffold' in fact_dict:
                fstate = fstate&Fact(scaffold=fact_dict['scaffold'])
            else:
                if fact_dict['answer'] is True:
                    answers.append(Fact(field=fact_dict['field'], value=fact_dict['value'], answer=fact_dict['answer']))
                else:
                    fstate = fstate&Fact(field=fact_dict['field'], value=fact_dict['value'], answer=fact_dict['answer'])
        plan = planner(fstate, self.task, self.domain)
        effect, fstate = plan.send(None)

        for answer in answers:
            value = sp.sstr(parse_latex(re.sub(r'sqrt(\d+)', r'sqrt{\1}', answer['value'])), order="grlex")
            flag = False
            for evalue in effect['value']:
                flag = True
                while not (evalue.match(value) and effect['field'] == answer['field']):
                    effect['value'] = answer['value']
                    effect, fstate = plan.send((fstate, False, effect))
                    if not effect:
                        flag = False
                        break
                if flag:
                    break
                
            effect, fstate = plan.send((fstate, True, effect))
        response = {'action': 'click', 'knowledge_component': [self.kc_mapping[kcx] for kcx in effect['kc']],
                    'study_material': self.study_material}
        
        return response
    

class HTNLoadedModels:
    def __init__(self):
        self.models = {}
        self.tutor_interfaces = defaultdict(list)
    
    def register(self, model):
        self.models[model.interface_name] = model
        self.tutor_interfaces[model.tutor_name].append(model.interface_name)

htn_loaded_models = HTNLoadedModels()

        
        
        

        


        
        



