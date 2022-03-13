import pyhop
from math import sqrt, pow

def distance(c1, c2):
    x=pow(c1['X']-c2['X'],2)
    y=pow(c1['Y']-c2['Y'],2)
    return sqrt(x+y)

def travel_op(state, o, d):
    if o in state.coordinates and d in state.coordinates:
        state.ambulance["Location"] = d
        state.cost += distance(state.coordinates[o], state.coordinates[d])
        return state
    return False

def load_ambulance_op(state):
    if state.victim["Location"] == state.ambulance["Location"]:
        state.in_ambulance = True
        return state
    return False

def unload_ambulance_op(state):
    if state.in_ambulance:
        state.victim["Location"] = state.hospital["Location"]
        state.in_ambulance = False
        return state
    return False

def assist_op(state):
    state.victim["Gravedad"] = state.gravedad_limite
    return state

def already_with_victim(state,goal):
    x = state.ambulance["Location"]
    y = state.victim["Location"]
    if x==y:
        return []
    return False

def move_to_victim(state,goal):
    x = state.ambulance["Location"]
    y = state.victim["Location"]
    if x!=y:
        return [('travel_op',x, y)]
    return False

def already_there(state,goal):
    x=state.victim["Location"]
    y=goal.final
    if x==y:
        return []
    return False

def no_assist_victim(state,goal):
    g = state.victim["Gravedad"]
    if g > state.ambulance["GravedadMax"] or g <= state.gravedad_limite:
        return []
    return False

def assist_victim(state,goal):
    g = state.victim["Gravedad"]
    if g <= state.ambulance["GravedadMax"] and g > state.gravedad_limite:
        return [('assist_op',)]
    return False

def move_to_hospital(state, goal):
    a = state.ambulance["Location"]
    if goal.final != a and state.in_ambulance:
        return [("travel_op", a, goal.final), ("unload_ambulance_op",)]
    return False

def deliver_by_ambulance1(state,goal):
    x=state.victim["Location"]
    y=goal.final
    state.ambulance = state.ambulances["A1"]
    gv = state.victim["Gravedad"]
    gt = state.ambulance["GravedadMax"]
    if x!=y and gt >= gv:
        return [('go_to_victim',goal), ('load_ambulance_op',), ('evaluate_victim',goal),('go_to_hospital',goal)]
    return False

def deliver_by_ambulance2(state,goal):
    x=state.victim["Location"]
    y=goal.final
    state.ambulance = state.ambulances["A2"]
    gv = state.victim["Gravedad"]
    gt = state.ambulance["GravedadMax"]
    if x!=y and gt >= gv:
        return [('go_to_victim',goal), ('load_ambulance_op',), ('evaluate_victim',goal),('go_to_hospital',goal)]
    return False

def deliver_by_ambulance3(state,goal):
    x=state.victim["Location"]
    y=goal.final
    state.ambulance = state.ambulances["A3"]
    gv = state.victim["Gravedad"]
    gt = state.ambulance["GravedadMax"]
    if x!=y and gt >= gv:
        return [('go_to_victim',goal), ('load_ambulance_op',), ('evaluate_victim',goal),('go_to_hospital',goal)]
    return False

def deliver_by_ambulance4(state,goal):
    x=state.victim["Location"]
    y=goal.final
    state.ambulance = state.ambulances["A4"]
    gv = state.victim["Gravedad"]
    gt = state.ambulance["GravedadMax"]
    if x!=y and gt >= gv:
        return [('go_to_victim',goal), ('load_ambulance_op',), ('evaluate_victim',goal),('go_to_hospital',goal)]
    return False

pyhop.declare_methods('deliver_victim',
    deliver_by_ambulance1,
    deliver_by_ambulance2,
    deliver_by_ambulance3,
    deliver_by_ambulance4, 
    already_there)

pyhop.declare_methods('go_to_victim',move_to_victim, already_with_victim)
pyhop.declare_methods('evaluate_victim',assist_victim, no_assist_victim)
pyhop.declare_methods('go_to_hospital',move_to_hospital, already_there)

pyhop.declare_operators(travel_op, load_ambulance_op, assist_op, unload_ambulance_op)

print()
pyhop.print_methods()
print()
pyhop.print_operators()

#INITIAL STATE
state1 = pyhop.State('state1')
state1.in_ambulance = False
state1.gravedad_limite = 4 # se asiste a la victima si (gravedad > gravedad_limite)
state1.coordinates = {'Colon':{'X':25,'Y':275}, 'Alameda':{'X':200,'Y':50}, 
                      'Ayuntamiento':{'X':250,'Y':325},
                      'Benimaclet':{'X':475,'Y':450}, 
                      'Av Cid':{'X':550,'Y':100}, 'Tarongers':{'X':750,'Y':425},
                      'El Carmen':{'X':800,'Y':250}, 'Blasco Ibanez':{'X':1000,'Y':150}}

state1.victim = { 'Nombre':'Pedro',
                    'Edad':45,
                    'Location':'Av Cid',
                    'Gravedad':9 }

state1.hospital = { 'Nombre':'Clinic',
                     'Location':'Blasco Ibanez' }

state1.ambulances = {
    "A1":{"Nombre":"A1","Location":"El Carmen","GravedadMax":7},
    "A2":{"Nombre":"A2","Location":"Av Cid","GravedadMax":5},
    "A3":{"Nombre":"A3","Location":"Blasco Ibanez","GravedadMax":9},
    "A4":{"Nombre":"A4","Location":"Alameda","GravedadMax":2},
}

state1.ambulance = state1.ambulances["A1"] # by default, A1

state1.cost = 0

#GOAL
goal1 = pyhop.Goal('goal1')
goal1.final = state1.hospital["Location"]

result=pyhop.pyhop(state1,[('deliver_victim',goal1)],verbose=3)

print(result)