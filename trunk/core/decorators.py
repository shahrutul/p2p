# http://www.dabeaz.com/coroutines/coroutine.py
# coroutine.py
#
# A decorator function that takes care of starting a coroutine
# automatically on call.

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start


# http://www.python.org/dev/peps/pep-0318/
def singleton(cls):
    """ A simple singleton pattern decorator """
    instances = {}

    def getinstance():
        """ Creates a single object and use instances dict as cache """
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance