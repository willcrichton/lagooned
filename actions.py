import random
from messages import M

### Action framework ###
ACTIONS = []

def sanitize_action(action):
    return {
        'name': action['name'],
        'label': M[action['name']],
        'duration': action['duration']
    }

def register_action(name, duration, callback, verify):
    ACTIONS.append({
        'name': name,
        'duration': duration,
        'callback': callback,
        'verify': verify
    })

### Individual actions ###

## Scavenge
def scavenge_callback(user):
    chance = random.random() > 0.4
    if chance:
        user.hunger += 1
        user.add_to_log('ACT_SCAVENGE_SUCCESS')
    else:
        user.add_to_log('ACT_SCAVENGE_FAIL')

    return chance

def scavenge_verify(user):
    return True

register_action('ACT_SCAVENGE', 2, scavenge_callback, scavenge_verify)


## Cook
def cook_callback(user):
    user.hunger += 5
    user.remove_item('ITEM_FIREWOOD')
    user.add_to_log('ACT_COOK_SUCCESS')

    return True

def cook_verify(user):
    return user.has_item('ITEM_FIREWOOD')

register_action('ACT_COOK', 10, cook_callback, cook_verify)


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

register_action('ACT_FIREWOOD', 5, firewood_callback, firewood_verify)