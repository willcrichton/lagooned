### Items framework ###
ITEMS = []

class Item():
    name = ''
    
    def __init__(self, name):
        self.name = name

def add_item(name):
    ITEMS.append(Item(name))

### Individual items ###
add_item('ITEM_FIREWOOD')