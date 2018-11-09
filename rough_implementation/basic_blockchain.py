from uuid import uuid4
from pprint import pprint as pp

class Block:
    # def __init__(self, id=uuid4(), from_user=User(), to_user=User(), value=0, *args, **kwargs):
    def __init__(self, from_user, to_user, value, *args, **kwargs):
        self.id = uuid4()
        self.from_user = from_user
        self.to_user = to_user
        self.value = value


class Blockchain:
    def __init__(self, blocks=[], *args, **kwargs):
        self.blocks = blocks
    
    def add(self, block):
        self.blocks.append(block)


class User:
    def __init__(self, children=[], value=0, blockchain=Blockchain(), *args, **kwargs):
        self.id = uuid4()
        self.children = children
        self.value = value
        self.blockchain = blockchain

    def make_transaction(self, receiver, value):
        updated_amount = receiver.cur_update(value)
        new_block = Block(uuid4(), self, receiver, value)
        self.emmit(new_block)
        return "transaction to " + str(receiver.id) + " was successful, amount: " + str(updated_amount)

    def cur_update(self, value):
        self.value += value
        return "new amount :" + str(self.value) + ". added amount: " + str(value)

    def make_connection(self, children_id):
        self.children.append(children_id)

    def emmit(self, block):
        # check if we need to update or not
        if block.id not in [b.id for b in self.blockchain]:
            self.blockchain.add(new_block)

        for child in self.children:
            child.emmit(block)

    def show_blockchain(self):
        return pp(self.blockchain.blocks, indent=4, depth=4)


user01 = User()
user02 = User()
user03 = User()
user04 = User()


user01.make_transaction(user02, 2)
print(user02.value)     # should be 2
print(user03.show_blockchain())


"""
    {
        "<id>": {
            "from": "user01",
            "to": "user02",
            "value": 2,
            # "is_verified": true
        }
    }
"""