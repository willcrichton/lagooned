ACTIONS = []

def sanitize_action(action):
    return {
        "name": action["name"],
        "duration": action["duration"]
    }

def register_action(name, duration, callback, verify):
    ACTIONS.append({
        "name": name,
        "duration": duration,
        "callback": callback,
        "verify": verify
    })

def scavenge_callback(user):
    user.hunger += 1

def scavenge_verify(user):
    return True

register_action("Scavenge", 5, scavenge_callback, scavenge_verify)
