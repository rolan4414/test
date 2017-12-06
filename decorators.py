from flask_jwt import current_identity
from functools import wraps
from models.user import Role

def requires_roles(roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
             if Role.query.filter_by(name=roles).first() not in current_identity.roles:
                return {"message": "You're not allowed to enter"}, 404
             return f(*args, **kwargs)
        return wrapped
    return wrapper


