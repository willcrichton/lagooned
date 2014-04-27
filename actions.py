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

* You may notice the default html (/templates/index.jinja2) has no HTML in the body. The HTML comes from
  the templates direction (/static/js/templates). We render these templates using a templating engine called
  Handlebars (http://handlebarsjs.com) which allows us to do simple loops/conditionals in the HTML.

* Syncing the front-end with the back-end is really easy because of Backbone. We use Backbone Models to store
  the User data that comes in over the socket. Any time that data changes, every relevant view.
'''

import random
from constants import C


#### Action framework ####

ACTIONS = []
CONSTRAINTS = []

# make an action JSON-serializable
def sanitize_action(action):
    return {
        'name': action['name'],
        'label': C[action['name']],
        'category': C[action['category']],
        'duration': action['duration']
    }

def register_action(name, duration, category, callback, verify):
    ACTIONS.append({
        'name': name,
        'duration': duration,
        'category': category,
            # Not shown: Success, Failure, Random_Event
            # Shown: Travel, Forage (Food), Scavenge (Non-edible materials), Craft, Build, Cook     
        'callback': callback,
        'verify': verify
    })

def register_constraint(callback):
    CONSTRAINTS.append(callback)

# for miscellaneous effects after an action is run
def on_action(user):
    user.food = max(user.food - 1, 0)



#### Individual actions ####

## Food
def forage_callback(user):
    chance = random.random()
    if user.location == 'LOCATION_BEACH':
        if chance < 0.33:
            user.add_item('ITEM_COCONUT')
            user.add_to_log('ACT_FORAGE_SUCCESS_COCONUTS')
        elif chance < 0.66:
            user.add_item('ITEM_SEA_GRASS')
            user.add_to_log('ACT_FORAGE_SUCCESS_SEA_GRASS')
        else:
            user.add_item('ITEM_CLAM')
            user.add_to_log('ACT_FORAGE_SUCCESS_CLAMS')
    else:
        if chance < 0.5:
            user.add_item('ITEM_BERRIES')
            user.add_to_log('ACT_FORAGE_SUCCESS_BERRIES')
        else:
            user.add_item('ITEM_FLOWERS')
            user.add_to_log('ACT_FORAGE_SUCCESS_FLOWERS')
        
    return True

def forage_verify(user):
    return True

register_action('ACT_FORAGE', 3, 'CATEGORY_FOOD', forage_callback, forage_verify)

def hunt_callback(user):
    chance = random.random() 
    animal = 'CRAB' if user.location == 'LOCATION_BEACH' else 'SHEEP'
    if chance > 0.7:
        user.add_item('ITEM_%s' % animal)
        user.add_to_log('ACT_HUNT_%s_SUCCESS' % animal)
        return True
    else:
        user.add_to_log('ACT_HUNT_%s_FAIL' % animal)
        return False

def hunt_verify(user):
    return True

register_action('ACT_HUNT', 3, 'CATEGORY_FOOD', hunt_callback, hunt_verify)

VEGGIES = ['ITEM_COCONUT', 'ITEM_BERRIES', 'ITEM_SEA_GRASS', 'ITEM_FLOWERS']
def eat_veggies_callback(user):
    for veggie in VEGGIES:
        if user.has_item(veggie):
            user.remove_item(veggie)
            user.food += 3
            user.add_to_log(veggie + '_EAT')
            return True

    return False

def eat_veggies_verify(user):
    return user.has_items(VEGGIES)

register_action('ACT_EAT_VEGGIES', 2, 'CATEGORY_FOOD', eat_veggies_callback, eat_veggies_verify)

MEAT = ['ITEM_CLAM', 'ITEM_CRAB', 'ITEM_SHEEP']
def eat_uncooked_callback(user):
    for meat in MEAT:
        if user.has_item(meat):
            user.remove_item(meat)
            user.food += 5
            user.add_to_log(meat + '_EAT_UNCOOKED')
            return True

    return False

def eat_uncooked_verify(user):
    return user.has_items(MEAT)

register_action('ACT_EAT_UNCOOKED', 2, 'CATEGORY_FOOD', eat_uncooked_callback, eat_uncooked_verify)

WOOD = ['ITEM_DRIFTWOOD', 'ITEM_TWIGS', 'ITEM_MOSS', 'ITEM_BRANCHES']
def cook_callback(user):
    for meat in MEAT:
        if not user.has_item(meat): continue
        user.remove_item(meat)
        
        for wood in WOOD:
            if not user.has_item(wood): continue

            user.remove_item(wood)
            user.food += 15
            user.add_to_log(meat + '_EAT_COOKED')
            return True

    return False

def cook_verify(user):
    return user.has_items(WOOD) and user.has_items(MEAT)

register_action('ACT_COOK', 5, 'CATEGORY_FOOD', cook_callback, cook_verify)


## Weapons

def weapon_gather_callback(user):
    chance = random.random()
    if user.location == 'LOCATION_BEACH':
        if chance < 0.2:
            user.add_item('ITEM_CLAMSHELL')
            user.add_to_log('ACT_WEAPON_GATHER_CLAMSHELL')
        elif chance < 0.4:
            user.add_item('ITEM_ROCK')
            user.add_to_log('ACT_WEAPON_GATHER_ROCK')
        else:
            user.add_to_log('ACT_WEAPON_GATHER_FAIL')
    elif user.location == 'LOCATION_CAVE':
        if chance < 0.7:
            user.add_item('ITEM_ROCK')
            user.add_to_log('ACT_WEAPON_GATHER_ROCK')
        else:
            user.add_to_log('ACT_WEAPON_GATHER_FAIL')
    else: #location: Forest
        if chance < 0.4:
            user.add_item('ITEM_STICK')
            user.add_to_log('ACT_WEAPON_GATHER_STICK')
        elif chance < 0.6:
            user.add_item('ITEM_BONE')
            user.add_to_log('ACT_WEAPON_GATHER_BONE')
        elif chance < 0.8:
            user.add_item('ITEM_ROCK')
            user.add_to_log('ACT_WEAPON_GATHER_ROCK')
        else:
            user.add_to_log('ACT_WEAPON_GATHER_FAIL')
        
    return True

def weapon_gather_verify(user):
    return True

register_action('ACT_WEAPON_GATHER', 3, 'CATEGORY_SCAVENGE', weapon_gather_callback, weapon_gather_verify)



## Firewood
def firewood_callback(user):
    if user.location == 'LOCATION_CAVE':
        user.add_to_log('ACT_FIREWOOD_FAIL')
        return False
    elif user.location == 'LOCATION_FOREST':
        chance = random.random()
        if chance < 0.33:
            user.add_item('ITEM_TWIGS')
            user.add_to_log('ACT_FIREWOOD_SUCCESS_TWIGS')
        elif chance < 0.66:
            user.add_item('ITEM_MOSS')
            user.add_to_log('ACT_FIREWOOD_SUCCESS_MOSS')
        else:
            user.add_item('ITEM_BRANCHES')
            user.add_to_log('ACT_FIREWOOD_SUCCESS_BRANCHES')
    else:
        user.add_item('ITEM_DRIFTWOOD')
        user.add_to_log('ACT_FIREWOOD_SUCCESS_DRIFTWOOD')

    return True

def firewood_verify(user):
    return True

register_action('ACT_FIREWOOD', 3, 'CATEGORY_MATERIALS', firewood_callback, firewood_verify)


## Shelter
def build_leanto_callback(user):
    items = user.get_items()
    wood_totals = {k: user.num_of_item(k) for k in ['ITEM_TWIGS', 'ITEM_DRIFTWOOD', 'ITEM_BRANCHES']}
    for i in range(0, 4):
        for k in wood_totals:
            if wood_totals[k] > 0: 
                wood_totals[k] -= 1
                user.remove_item(k)
                break
    
    # TODO: state indicating lean-to
    user.add_to_log('ACT_BUILD_LEANTO_SUCCESS')
    return True

def build_leanto_verify(user):
    total_wood = user.num_of_items(['ITEM_TWIGS', 'ITEM_DRIFTWOOD', 'ITEM_BRANCHES'])
    return total_wood >= 4

register_action('ACT_BUILD_LEANTO', 10, 'CATEGORY_BUILDING', build_leanto_callback, build_leanto_verify)

## Movements
def move_forest_callback(user):
    user.location = 'LOCATION_FOREST'
    user.add_to_log('ACT_MOVE_FOREST_SUCCESS')
    return True

def move_forest_verify(user):
    return user.location != 'LOCATION_FOREST' and user.has_done_actions(['ACT_FORAGE'])

def move_cave_callback(user):
    user.location = 'LOCATION_CAVE'
    user.add_to_log('ACT_MOVE_CAVE_SUCCESS')
    return True

def move_cave_verify(user):
    return user.location != 'LOCATION_CAVE' and user.has_done_actions(['ACT_MOVE_FOREST'])

def move_beach_callback(user):
    user.location = 'LOCATION_BEACH'
    user.add_to_log('ACT_MOVE_BEACH_SUCCESS')
    return True

def move_beach_verify(user):
    return user.location != 'LOCATION_BEACH'

register_action('ACT_MOVE_BEACH', 3, 'CATEGORY_MOVEMENT', move_beach_callback, move_beach_verify)
register_action('ACT_MOVE_FOREST', 3, 'CATEGORY_MOVEMENT', move_forest_callback, move_forest_verify)
register_action('ACT_MOVE_CAVE', 3, 'CATEGORY_MOVEMENT', move_cave_callback, move_cave_verify)


#### Action Constraints ####

# User has to find/make food if they have none
def food_constraint(user, action):
    actions = ['ACT_FORAGE', 'ACT_COOK', 'ACT_EAT_VEGGIES', 'ACT_EAT_RAW', 'ACT_EAT_COOKED', 'ACT_MOVE_BEACH','ACT_MOVE_FOREST', 'ACT_MOVE_CAVE']
    return user.food > 0 or action['name'] in actions

register_constraint(food_constraint)