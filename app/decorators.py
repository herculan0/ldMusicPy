from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permissao

def permissao_necessaria(permissao):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permissao):
                abort(403)
            return f(*args, **kwargs)
        return  decorated_function
    return decorator

def necessario_admin(f):
    return permissao_necessaria(Permissao.ADMIN)(f)
