### Items framework ###
ITEMS = []

class Item():
    name = ''
    description = ''
    
    def __init__(self, name, description):
        self.name = name
        self.description = description

def add_item(name):
    ITEMS.append(Item(name))

### Individual items ###
add_item('ITEM_FIREWOOD', 'ITEM_FIREWOOD_DESC')
add_item('ITEM_DRIFTWOOD', 'ITEM_DRIFTWOOD_DESC')