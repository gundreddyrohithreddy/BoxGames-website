from flask import session, redirect

def login_required(role=None):
    def wrapper(fn):
        def decorated(*args, **kwargs):
            if "user_id" not in session:
                return redirect("/login")
            if role and session.get("role") != role:
                return "Unauthorized", 403
            return fn(*args, **kwargs)
        decorated.__name__ = fn.__name__
        return decorated
    return wrapper
