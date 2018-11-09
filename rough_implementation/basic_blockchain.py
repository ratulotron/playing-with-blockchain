from uuid import uuid4
from pprint import pprint as pp

class Block:
    def __init__(self, from_user, to_user, value, *args, **kwargs):
        self.id = uuid4()
        self.from_user = from_user
        self.to_user = to_user
        self.value = value

    def __str__(self):
        return str(self.id)


class Blockchain:
    def __init__(self, blocks=[], *args, **kwargs):
        self.blocks = blocks
    
    # def __iter__(self):
    #     for value in self.blocks:
    #         # yield (key, 'Value for {}'.format(key))
    #         yield {
    #             "id": value.id,
    #             "from": value.from_user,
    #             "to": value.to_user,
    #             "value": value.value
    #         }

    def add(self, block):
        self.blocks.append(block)


class User:
    def __init__(self, children, value, blockchain, *args, **kwargs):
        self.id = uuid4()
        self.children = children
        self.value = value
        self.blockchain = blockchain

    def make_transaction(self, receiver, value):
        updated_amount = receiver.cur_update(value)
        self.value = self.value - value
        new_block = Block(self.id, receiver.id, value)
        self.emmit(new_block)
        return "transaction to " + str(receiver.id) + " was successful, amount: " + str(updated_amount)

    def cur_update(self, value):
        self.value += value
        return "new amount :" + str(self.value) + ". added amount: " + str(value)

    def make_connection(self, children_id):
        self.children.append(children_id)

    def emmit(self, block):
        # check if we need to update or not
        if block.id not in [b.id for b in self.blockchain.blocks]:
            self.blockchain.add(block)

        for child in self.children:
            child.emmit(block)

    def show_blockchain(self):
        blockchains_data = []
        for b in self.blockchain.blocks:
            blockchains_data.append(b.__dict__)
        return blockchains_data


user01 = User(
    children=[],
    value=0,
    blockchain=(lambda: Blockchain())()
    )
user02 = User(
    children=[],
    value=0,
    blockchain=(lambda: Blockchain())()
    )
user03 = User(
    children=[],
    value=0,
    blockchain=(lambda: Blockchain())()
    )
user04 = User(
    children=[],
    value=0,
    blockchain=(lambda: Blockchain())()
    )

users = [user01, user02, user03, user04]

def print_all():
    for u in users:
        print("***")
        print("User ID: {}".format(u.id))
        print("Child nodes:")
        pp(u.children, indent=4, depth=4)
        print("Value: {}".format(u.value))
        print("Current blockchain:")
        pp(u.show_blockchain())

print("Before making any transaction:")
print_all()

# Do some transactions
print("After making first transaction:")
print("First user should have -2, second user should have 2")
user01.make_transaction(user02, 2)
print_all()

# user03.make_transaction(user02, 2)
# user01.make_transaction(user03, 2)

# print(user02.value)     # should be 2
# pp(user03.show_blockchain())


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