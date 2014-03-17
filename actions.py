import random
from constants import C

''' 
******* ABRIDGED GUIDE TO DEVELOPING FOR LAGOONED ********
Please take a moment to read this!

-- SERVER ARCHITECTURE --
* The client and server communicate through a WEBSOCKET (see: the socket function in server.py).

* The server keeps track of all data in a SQLite database. We abstract this in the USER class.
  The User class contains all relevant data about a user (and helper functions!). See the implementation 
  inside of server.py for more details. It's as simple as: user.food += 1; user.save();
  But don't forget to save!!

* Users talk to the server in the form of ACTIONS. Each action has a name, duration, and callback.
  The callback is called at the end of the duration and determines what happens when an action finishes.
  - Each action also has a "verify" function. This determines if a user can use a particular action.
  - You can also create CONSTRAINTS, which are functions applied to all verification checks.
    For example, a constraint might be: you can only use this action if you have enough food.
  - The on_action function below is run after every action. Use this for global effects
    (e.g. you eat some food after every action).

* The constants.py file keeps track of game messages, item/action names, and more. If you're adding
  to the log, for example, you add the name of the message (e.g 'ACT_COOK_SUCCESS') instead of the 
  name itself (e.g. 'You cooked some meat.').

* The items.py file is like the actions.py file and has helper functions for the items system.
  It's pretty empty right now, but you can add stuff there if the items system gets complicated.

* I created the backend such that you should only have to edit the actions/constants.py files, and
  not the core functionality inside server.py. You should only look there for reference on the User class.

-- CLIENT ARCHITECTURE --
* The interface is split up into VIEWS. Each view corresponds to an element on the page, like the statistics
  pane, or the actions panel. Each view updates whenever the User data changes. After every action, the User 
  is notified of all changes to the User model, and all views update accordingly.

* More to fill in here...
'''

#### Action framework ####

ACTIONS = []
CONSTRAINTS = []

# make an action JSON-serializable
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

# for miscellaneous effects after an action is run
def on_action(user):
    user.food = max(user.food - 1, 0)



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
    return user.has_done_actions(['ACT_SCAVENGE'])

register_action('ACT_FIREWOOD', 3, firewood_callback, firewood_verify)



#### Action Constraints ####

# User has to find/make food if they have none
def food_constraint(user, action):
    return user.food > 0 or action['name'] in ['ACT_SCAVENGE', 'ACT_COOK']

register_constraint(food_constraint)        