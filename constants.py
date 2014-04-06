
# These are all the values for constants in the game, including
# action labels, item names, success/failure responses, and so on.
C = {
    
    # Gameplay
    'GAME_START': 'You wash up on a deserted island.',
    'LOG_MAX': 4,


    # Locations
    'LOCATION_START': 'empty beach',
    'LOCATION_FOREST': 'dense rainforest',
    'LOCATION_RUINS': 'scattered ruins',


    # --------------------------------------------
    #   ACTIONS
    # --------------------------------------------

    # Move
    'ACT_MOVE_FOREST': 'You walk toward the trees and find yourself in a dense rainforest. The sound of running water flows from afar.',
    'ACT_MOVE_RUINS': 'You find yourself in the scattered remains of an ancient building. Bricks and rotted wood lie buried in the sand.',
    'ACT_MOVE_START': 'You return to the beach and the ebbing shore.',


    # Scavenging / Foraging
    'ACT_SCAVENGE': 'Scavenge',
    'ACT_SCAVENGE_SUCCESS': 'You found some food lying around.',
    'ACT_SCAVENGE_FAIL': 'You failed to find any food.',
    
    'ACT_FIREWOOD': 'Gather wood',
    'ACT_FIREWOOD_SUCCESS_TWIGS': 'You gathered some twigs from the ground.',
    'ACT_FIREWOOD_SUCCESS_MOSS': 'You collected some dry moss growing on a trunk.',
    'ACT_FIREWOOD_SUCCESS_BRANCHES': 'You broke off a branch from a small tree.',
    'ACT_FIREWOOD_FAIL': 'You couldn\'t find any firewood.',
    
    'ACT_FORAGE': 'Forage for food',
    'ACT_FORAGE_SUCCESS_COCONUTS': 'You shook a tree, and a coconut fell to your feet.',
    'ACT_FORAGE_SUCCESS_BERRIES': 'You discovered some berries in a bush.',
    'ACT_FORAGE_SUCCESS_SEA_GRASS': 'You yanked some slimy grass from the seabed.',
    'ACT_FORAGE_SUCCESS_FLOWERS': 'You picked a bunch of sweet-smelling flowers.',
    'ACT_FORAGE_SUCCESS_CLAM': 'You found a clam lying on the seabed.',
    'ACT_FORAGE_FAIL': 'You failed to find any food.',
    
    'ACT_HUNT_CRABS': 'Hunt crabs',
    'ACT_HUNT_CRABS_SUCCESS': 'You trapped and slew a crab.',
    'ACT_HUNT_CRABS_FAIL': 'You attempt to grab a crab, but it snaps at you and scurries under a rock.',

    'ACT_HUNT_SHEEP': 'Hunt sheep',
    'ACT_HUNT_SHEEP_SUCCESS': 'You gut a sheep as its dying baa rings in your ears.',
    'ACT_HUNT_SHEEP_FAIL': 'You try to tackle a sheep, but it baas and kicks off instead.',
    
    'ACT_WEAPON_GATHER': 'Look for weapon materials',
    'ACT_WEAPON_GATHER_ROCK': 'You find badass rocks.',
    'ACT_WEAPON_GATHER_CLAMSHELL': 'You step on some sharp clamshells and decide to take them.',
    'ACT_WEAPON_GATHER_BRANCH': 'You picked up a formidable branch off the ground.',
    'ACT_WEAPON_GATHER_BONES': 'You salvaged a sizable femur from a picked clean corpse.',

    'ACT_BUILD_FIRE': 'You start a small fire.',
    
    
    # Building / Crafting
    'ACT_BUILD_AXE': 'You fashion a crude axe from the material you collected previously.',

    'ACT_BUILD_LEANTO': 'Tired of sleeping under the moon, you build a basic lean-to shelter.',

    'ACT_COOK': 'Cook',
    'ACT_COOK_SUCCESS': 'You cooked some food over a roaring fire.',


    # Random Events
    'RANDOM_WASHUP_SAIL': 'You notice a sail floating on the horizon.',
    'RANDOM_WASHUP_ROPE': 'A small rope floats amidst the flotsam.',
    'RANDOM_WASHUP_BOTTLE': 'You picked up a bottle drifting in the water. A small crumpled paper is sealed inside.',
    'RANDOM_WASHUP_DRIFTWOOD': 'You unearthed a piece of driftwood lying in the sand.',

    'RANDOM_TREASURE_GOLD': 'A glimmer catches your eye, and you discover an ingot of gold under a broken stone.',


    # --------------------------------------------
    #   ITEMS
    # --------------------------------------------

    'ITEM_FIREWOOD': 'Firewood',
    'ITEM_FIREWOOD_DESC': 'A hefty piece of dry wood.',
    'ITEM_DRIFTWOOD': 'Driftwood',
    'ITEM_DRIFTWOOD_DESC': 'Lonley wood that has been on a long sea adventure.',
    'ITEM_TWIGS': 'Twigs',
    'ITEM_TWIGS_DESC': 'These are the twiggiest twigs you\'ve ever seen',
    'ITEM_MOSS': 'Dry Moss',
    'ITEM_MOSS_DESC': 'Unlike other varieties, this moss is dry.',
    'ITEM_BRANCHES': 'Branches',
    'ITEM_BRANCHES_DESC': 'Branches can be useful for making tools, building fires, and more.',

    'ITEM_COCONUT': 'Coconut',
    'ITEM_COCONUT_DESC': 'Every survival game needs these.',
    'ITEM_BERRIES': 'Berries',
    'ITEM_BERRIES_DESC': 'Delicious and sweet, these berries are great to eat.',
    'ITEM_SEA_GRASS': 'Sea Grass',
    'ITEM_SEA_GRASS_DESC': 'Edible, but not your first choice.',
    'ITEM_FLOWERS': 'Flowers',
    'ITEM_FLOWERS_DESC': 'Sweet smelling, but sweet tasting.',
    'ITEM_CLAM': 'Clam',
    'ITEM_CLAM_DESC': 'Clams are scrumptious, raw or cooked!',

    'ITEM_CRAB': 'Crab',
    'ITEM_CRAB_DESC': 'A sizable chunk of crab meat and crab bits.',
    'ITEM_SHEEP': 'Sheep',
    'ITEM_SHEEP_DESC': 'Raw piece of sheep flesh.',

    'ITEM_SAIL': 'Sail',
    'ITEM_SAIL_DESC': 'A worn down but usable boat sail made of cotton.',
    'ITEM_ROPE': 'Rope',
    'ITEM_ROPE_DESC': 'A rope woven from fibers.',
    'ITEM_BOTTLE': 'Message-in-a-bottle',
    'ITEM_BOTTLE_DESC': 'Looks like there\'s something inside...',
    'ITEM_GOLD': 'Gold Nugget',
    'ITEM_GOLD_DESC': 'Eureka! Shiny and valuable.',

}