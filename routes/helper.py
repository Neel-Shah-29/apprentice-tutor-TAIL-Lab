from models import db, User, UserCourse, KnowledgeComponent, UserKnowledgeComponent, TutorTransaction
from bkt import bkt_update
from cognitive_models import loaded_models
from htn_cognitive_models import htn_loaded_models
import statistics
import matplotlib.pyplot as plt
import numpy as np
import io

###################################################
# Helper methods
###################################################
def update_kcs(kc_names, correctness, user):
    print('UPDATING KCS')
    print(kc_names)
    for kc_name in kc_names:
        # print(kc_name)
        kc = KnowledgeComponent.query.filter_by(name=kc_name).first()
        print(kc.name)
        for user_kc in UserKnowledgeComponent.query.filter_by(user_id=user.id,
                                                              kc_id=kc.id):
            user_kc.skill_level = bkt_update(correctness, user_kc.skill_level,
                                             kc.learn, kc.guess, kc.slip)
            print('Updated {} kc to: {}'.format(kc_name, user_kc.skill_level))
            print('Updated others {}, {}, {}'.format(kc.learn, kc.guess, kc.slip))
            # print('Updated {} kc to: {}'.format(kc_name,
            # user_kc.skill_level))
            db.session.add(user_kc)
    db.session.commit()

def get_kc_performance(user, tt=None):
    user_kcs = UserKnowledgeComponent.query.filter_by(user_id=user.id)

    # Getting models for each tutor
    tutoring_performance_map = {}
    class_payload = {}
    # may use defaultdict()

    # try:
    if tt == 'htn':
        for tutor in htn_loaded_models.tutor_interfaces:
            if tutor not in class_payload:
                class_payload[tutor] = {}
            for interface in htn_loaded_models.tutor_interfaces[tutor]:
                if interface not in class_payload[tutor]:
                    class_payload[tutor][interface] = {}
                    class_payload[tutor][interface]['progress'] = {}
                    class_payload[tutor][interface]['list'] = []    
                for user_kc in user_kcs:
                    if user_kc.kc.name in htn_loaded_models.models[interface].kc_mapping.values():
                        class_payload[tutor][interface]['progress'][user_kc.kc.name] = user_kc.skill_level
                        class_payload[tutor][interface]['list'].append(user_kc.skill_level)
                readable_tutor_name = tutor + ":" + interface.replace("_", " ")
                if len(class_payload[tutor][interface]["list"]) == 0: 
                    tutoring_performance_map[readable_tutor_name] = 0.0
                else: 
                    tutoring_performance_map[readable_tutor_name] = statistics.mean(class_payload[tutor][interface]["list"])
    else:
        for tutor in loaded_models.tutor_interfaces:
            if tutor not in class_payload:
                class_payload[tutor] = {}
            for interface in loaded_models.tutor_interfaces[tutor]:
                if interface not in class_payload[tutor]:
                    class_payload[tutor][interface] = {}
                    class_payload[tutor][interface]['progress'] = {}
                    class_payload[tutor][interface]['list'] = []    
                for user_kc in user_kcs:
                    if user_kc.kc.name in loaded_models.models[interface].kc_mapping.values():
                        class_payload[tutor][interface]['progress'][user_kc.kc.name] = user_kc.skill_level
                        class_payload[tutor][interface]['list'].append(user_kc.skill_level)
                readable_tutor_name = tutor + ":" + interface.replace("_", " ")
                if len(class_payload[tutor][interface]["list"]) == 0: 
                    tutoring_performance_map[readable_tutor_name] = 0.0
                else: 
                    tutoring_performance_map[readable_tutor_name] = statistics.mean(class_payload[tutor][interface]["list"])
   
    return (user_kcs, tutoring_performance_map, class_payload )


def get_tutor_kc_performance(user, tutor, tt=None):
    user_kcs = UserKnowledgeComponent.query.filter_by(user_id=user.id)

    # Getting models for each tutor
    tutoring_performance_map = {}
    class_payload = {}

    class_payload[tutor] = {}
    if tt == 'htn':
        for interface in htn_loaded_models.tutor_interfaces[tutor]:
            if interface not in class_payload[tutor]:
                class_payload[tutor][interface] = {}
                class_payload[tutor][interface]['progress'] = {}
                class_payload[tutor][interface]['list'] = []  
            
            for user_kc in user_kcs:
                if user_kc.kc.name in htn_loaded_models.models[interface].kc_mapping.values():
                    class_payload[tutor][interface]['progress'][user_kc.kc.name] = user_kc.skill_level
                    class_payload[tutor][interface]['list'].append(user_kc.skill_level)
                readable_tutor_name = tutor + ":" + interface.replace("_", " ")
                if len(class_payload[tutor][interface]["list"]) == 0: 
                    tutoring_performance_map[readable_tutor_name] = 0.0
                else: 
                    tutoring_performance_map[readable_tutor_name] = statistics.mean(class_payload[tutor][interface]["list"])
    else:
        for interface in loaded_models.tutor_interfaces[tutor]:
            if interface not in class_payload[tutor]:
                class_payload[tutor][interface] = {}
                class_payload[tutor][interface]['progress'] = {}
                class_payload[tutor][interface]['list'] = []  
            
            for user_kc in user_kcs:
                if user_kc.kc.name in loaded_models.models[interface].kc_mapping.values():
                    class_payload[tutor][interface]['progress'][user_kc.kc.name] = user_kc.skill_level
                    class_payload[tutor][interface]['list'].append(user_kc.skill_level)
                readable_tutor_name = tutor + ":" + interface.replace("_", " ")
                if len(class_payload[tutor][interface]["list"]) == 0: 
                    tutoring_performance_map[readable_tutor_name] = 0.0
                else: 
                    tutoring_performance_map[readable_tutor_name] = statistics.mean(class_payload[tutor][interface]["list"])
        
    return tutoring_performance_map
        

    # try:
    # for tutor in loaded_models.tutor_interfaces:
    #     if tutor not in class_payload:
    #         class_payload[tutor] = {}
    #     for interface in loaded_models.tutor_interfaces[tutor]:
    #         if interface not in class_payload[tutor]:
    #             class_payload[tutor][interface] = {}
    #             class_payload[tutor][interface]['progress'] = {}
    #             class_payload[tutor][interface]['list'] = []    
    #         for user_kc in user_kcs:
    #             if user_kc.kc.name in loaded_models.models[interface].kc_mapping.values():
    #                 class_payload[tutor][interface]['progress'][user_kc.kc.name] = user_kc.skill_level
    #                 class_payload[tutor][interface]['list'].append(user_kc.skill_level)
    #         readable_tutor_name = tutor + ":" + interface.replace("_", " ")
    #         if len(class_payload[tutor][interface]["list"]) == 0: 
    #             tutoring_performance_map[readable_tutor_name] = 0.0
    #         else: 
    #             tutoring_performance_map[readable_tutor_name] = statistics.mean(class_payload[tutor][interface]["list"])
   
    # return (user_kcs, tutoring_performance_map, class_payload )

def create_plot(a, b, c, r1, r2):
    x = np.array([i for i in range(min(r1,r2)-5, max(r1,r2)+5)])
    y = a*x**2 + b*x +c
    indices_within_range = [i for i, val in enumerate(y) if -50<val<50]    
    y = y[indices_within_range]
    x = x[indices_within_range]

    x = np.linspace(min(x), max(x), 400)
    y = a*x**2 + b*x +c
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.axhline(0, color='black',linewidth=0.5)
    ax.axvline(0, color='black',linewidth=0.5)
    ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    ax.plot(x, y, color='blue')
    xmin, xmax, ymin, ymax = min(x), max(x), min(y), max(y)

    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Create 'x' and 'y' labels placed at the end of the axes
    ax.set_xlabel('x', size=14, labelpad=-24, x=1.03)
    ax.set_ylabel('y', size=14, labelpad=-21, y=1.02, rotation=0)

    x_ticks = np.arange(np.floor(xmin)-5, np.ceil(xmax)+6, 1)
    y_ticks = np.arange(np.floor(ymin)-5, np.ceil(ymax)+6, 5)
    ax.set_xticks(x_ticks[x_ticks != 0])
    ax.set_yticks(y_ticks[y_ticks != 0])

    # Create minor ticks placed at each integer to enable drawing of minor grid
    # lines: note that this has no effect in this example with ticks_frequency=1
    ax.set_xticks(np.arange(np.floor(xmin)-5, np.ceil(xmax)+6), minor=True)
    ax.set_yticks(np.arange(np.floor(ymin)-5, np.ceil(ymax)+6), minor=True)

    # Draw arrows
    arrow_fmt = dict(markersize=4, color='black', clip_on=False)
    ax.plot((1), (0), marker='>', transform=ax.get_yaxis_transform(), **arrow_fmt)
    ax.plot((0), (1), marker='^', transform=ax.get_xaxis_transform(), **arrow_fmt)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    return buf

    return buf