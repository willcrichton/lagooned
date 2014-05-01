### Items framework ###
ITEMS = []

class Item():
    name = ''
    description = ''
    
    def __init__(self, name, description):
        self.name = name
        self.description = description

def add_item(name, description):
    ITEMS.append(Item(name, description))

### Individual items ###
add_item('ITEM_FIREWOOD', 'ITEM_FIREWOOD_DESC')
add_item('ITEM_DRIFTWOOD', 'ITEM_DRIFTWOOD_DESC')
add_item('ITEM_TWIGS', 'ITEM_TWIGS_DESC')
add_item('ITEM_MOSS', 'ITEM_MOSS_DESC')
add_item('ITEM_BRANCHES', 'ITEM_BRANCHES_DESC')

add_item('ITEM_COCONUT', 'ITEM_COCONUT_DESC')
add_item('ITEM_BERRIES', 'ITEM_BERRIES_DESC')
add_item('ITEM_SEA_GRASS', 'ITEM_SEA_GRASS_DESC')
add_item('ITEM_FLOWERS', 'ITEM_FLOWERS_DESC')
add_item('ITEM_CLAM', 'ITEM_CLAM_DESC')

add_item('ITEM_CRAB', 'ITEM_CRAB_DESC')
add_item('ITEM_SHEEP', 'ITEM_SHEEP_DESC')

add_item('ITEM_SAIL', 'ITEM_SAIL_DESC')
add_item('ITEM_ROPE', 'ITEM_ROPES_DESC')
add_item('ITEM_BOTTLE', 'ITEM_BOTTLE_DESC')
add_item('ITEM_GOLD', 'ITEM_GOLD_DESC')

add_item('ITEM_AXE', 'ITEM_AXE_DESC')
add_item('ITEM_PICKAXE', 'ITEM_PICKAXE_DESC')
