from behave import action
from pdb import set_trace


@action
def wow_large_number(x):
    print("WOW, %d is a large number!" % x)


set_trace()
tree = wow_large_number
bb = tree.blackboard(5)
state = bb.tick()
