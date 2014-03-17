import random
from constants import C

#### Action framework ####

ACTIONS = []
CONSTRAINTS = []

def sanitize_action(action):
    return {
        'name': action['name'],
        'label': C[action['name']],
        'duration': action['duration']
    }

def register_action(name, duration, callback, verify):
    ACTIONS.append({
        'name': name,
        'duration': duration,
        'callback': callback,
        'verify': verify
    })

def register_constraint(callback):
    CONSTRAINTS.append(callback)



#### Individual actions ####

## Scavenge
def scavenge_callback(user):
    chance = random.random() > 0.4
    if chance:
        user.food += 3
        user.add_to_log('ACT_SCAVENGE_SUCCESS')
    else:
        user.add_to_log('ACT_SCAVENGE_FAIL')

    return chance

def scavenge_verify(user):
    return True

register_action('ACT_SCAVENGE', 1, scavenge_callback, scavenge_verify)


## Cook
def cook_callback(user):
    user.food += 10
    user.remove_item('ITEM_FIREWOOD')
    user.add_to_log('ACT_COOK_SUCCESS')

    return True

def cook_verify(user):
    return user.has_item('ITEM_FIREWOOD')

register_action('ACT_COOK', 5, cook_callback, cook_verify)


## Firewood
def firewood_callback(user):
    chance = random.random() > 0.4
    if chance:
        user.add_item('ITEM_FIREWOOD')
        user.add_to_log('ACT_FIREWOOD_SUCCESS')
    else:
        user.add_to_log('ACT_FIREWOOD_FAIL')

    return chance

def firewood_verify(user):
    return user.done_actions(['ACT_SCAVENGE'])

register_action('ACT_FIREWOOD', 3, firewood_callback, firewood_verify)



#### Action Constraints ####

# User has to find/make food if they have none
def food_constraint(user, action):
    return user.food > 0 or action['name'] in ['ACT_SCAVENGE', 'ACT_COOK']

register_constraint(food_constraint)        