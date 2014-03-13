import random

ACTIONS = []

def sanitize_action(action):
    return {
        'name': action['name'],
        'duration': action['duration']
    }

def register_action(name, duration, callback, verify):
    ACTIONS.append({
        'name': name,
        'duration': duration,
        'callback': callback,
        'verify': verify
    })

def scavenge_callback(user):
    chance = random.random() > 0.4
    if chance:
        user.hunger += 1
        user.add_to_log('You scavenged for food.')
    else:
        user.add_to_log('You failed to scavenge.')

def scavenge_verify(user):
    return True

register_action('Scavenge', 2, scavenge_callback, scavenge_verify)

def cook_callback(user):
    user.hunger += 5
    user.add_to_log('You cooked some food.')

def cook_verify(user):
    return user.done_action('Scavenge')

register_action('Cook', 5, cook_callback, cook_verify)
