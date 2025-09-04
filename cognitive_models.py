from py_rete import Fact
from collections import defaultdict
import re
from models import KnowledgeComponent

class CognitiveModel:
    def __init__(self, tutor_name, interface_name, create_net_fn, new_problem_fn, kc_mapping, hints=None, study_material=None):
        self.tutor_name = tutor_name
        self.interface_name = interface_name
        self.create_net_fn = create_net_fn
        self.new_problem_fn = new_problem_fn
        self.kc_mapping = kc_mapping
        self.hints = hints
        self.study_material = study_material

    def rule_model(self):
        return self.create_net_fn()

    def create_kcs(self, db):
        for kc in set(self.kc_mapping.values()):
            if not KnowledgeComponent.query.filter_by(name=kc).first():
                kc = KnowledgeComponent(name=kc)
                db.session.add(kc)
        db.session.commit()

        net = self.rule_model()
        skill_to_kc = {p.__wrapped__.__name__: p.__wrapped__.__name__ for p in
                    net.productions}
        return skill_to_kc

    def check_sai(self, state, selection, action, input):
    
        # pprint(state)

        # print(kc_mapping)
        
        net = self.rule_model()

        for field in state:
            f = Fact(field=field)
            for attr in state[field]:
                f[attr] = state[field][attr]
            net.add_fact(f)

        kc = None
        idx = 0
        for m in net.matches:
            print("IDX:", idx)
            idx += 1
            result = m.fire()

            if result is None:
                continue
            for idx, sai in enumerate(result):
                # print('checking against', sai)
                # print(m.pnode.production.__wrapped__.__name__)
                # print("factor:", sai["input"], input, m.pnode.production.__wrapped__.__name__)
                if sai['selection'] == selection:
                    kc = self.kc_mapping[
                        m.pnode.production.__wrapped__.__name__]
            
                # try:
                # print("####")
                # print(sai['input'])
                # print(input.lower().replace(' ', ''))
                # print( sai['input'].lower().replace(" ", '') == input.lower().replace(' ', ''))
                # print("####")
                if (type(sai["input"]) == type(re.compile(""))):
                    print("ANSWER:", sai["input"], input)
                    # print("SELECTION:", sai["selection"], selection)
                    if (sai['selection'] == selection and
                            sai['action'] == action and
                            sai['input'].match(input)):
                        kc = self.kc_mapping[
                            m.pnode.production.__wrapped__.__name__]
                        return {"correct": True, "knowledge_components": [kc]}
                else:
                    print("ANSWER:", sai, input)
                    if (sai['selection'] == selection and
                            sai['action'] == action and
                            sai['input'].lower().replace(" ", '') ==
                            input.lower().replace(' ', '')):
                        kc = self.kc_mapping[
                            m.pnode.production.__wrapped__.__name__]
                        return {"correct": True, "knowledge_components": [kc]}
                # except:
            print("SELECTION:", result[-1]["selection"], selection)    #     print("An error has occured in base.py between lined 38-44")

        if kc is None:
            return {"correct": False, "knowledge_components": []}

        return {"correct": False, "knowledge_components": [kc]}

    def get_hint(self, state):
        if self.hints is None:
            hints = {}
        else: 
            hints = self.hints
        # hints = {}
        net = self.rule_model()
        for field in state:
            f = Fact(field=field)
            for attr in state[field]:
                f[attr] = state[field][attr]
            net.add_fact(f)

        for m in net.matches:
            result = m.fire()

            if result is None:
                continue
            ### Momin add hint here and look into the hints dict
            for sai in result:
                rule = m.pnode.production.__wrapped__.__name__
                kc = self.kc_mapping[rule]
                if (type(sai["input"]) == type(re.compile(""))):
                    response = {"selection": sai['selection'], "action": sai['action'],
                            "input": sai['hint'], "knowledge_components": [kc]}
                else:
                    response = {"selection": sai['selection'], "action": sai['action'],
                            "input": sai['input'], "knowledge_components": [kc]}

                if sai['action'] == 'input change':
                    response['hints'] = ['Try updating this field next.']
                    if rule in hints:
                        response['hints'].extend(hints[rule])
                    if (type(sai["input"]) == type(re.compile(""))):
                        response['hints'].append(
                            ## Momin Add start hints
                            'Enter the value {} in this field.'.format("\\({}\\)".format(sai['hint'])))
                    else: 
                        response['hints'].append(
                            ## Momin Add start hints
                            'Enter the value {} in this field.'.format("\\({}\\)".format(sai['input'])))
    
                elif sai['action'] == 'button click':
                    response['hints'] = []
                    if rule in hints:
                        response['hints'].extend(hints[rule])
                    response['hints'].append(
                        "You're done! Click the done button.")

                # pprint(response)
                return response
            
    def get_study_material(self, state):
        net = self.rule_model()
        for field in state:
            f = Fact(field=field)
            for attr in state[field]:
                f[attr] = state[field][attr]
            net.add_fact(f)

        for m in net.matches:
            result = m.fire()
            if result is None:
                continue
            
            for sai in result:
                rule = m.pnode.production.__wrapped__.__name__
                kc = self.kc_mapping[rule]

                response = {"action": sai['action'], "knowledge_components": [kc],
                            "study_material": self.study_material}

                return response

class LoadedModels:
    def __init__(self):
        self.models = {}
        self.tutor_interfaces = defaultdict(list)

    def register(self, model):
        self.models[model.interface_name] = model
        self.tutor_interfaces[model.tutor_name].append(model.interface_name)

loaded_models = LoadedModels()
