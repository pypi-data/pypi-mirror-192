from tinydb import Query, TinyDB

from . import utilities

db = TinyDB('db.json')
App = Query()

def insert(item):
    db.insert({'item': item, 'time': utilities.time()})

def all():
    result = db.all()
    return result

def reset():
    try:
        db.truncate()
        return "Database Reset Successfully"
    except:
        return "Something went wrong"