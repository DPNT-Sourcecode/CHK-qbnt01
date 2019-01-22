

# noinspection PyUnusedLocal
# friend_name = unicode string
def hello(friend_name):
    if not friend_name:
        friend_name = "World"
    return "Hello, " + friend_name + "!"
