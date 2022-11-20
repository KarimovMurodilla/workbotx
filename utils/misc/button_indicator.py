from loader import db

def indicator(name):
    status = db.get_status(name)

    return f"{status} {name}"