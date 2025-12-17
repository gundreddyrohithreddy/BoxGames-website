from flask import session, redirect

def login_required(role=None):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect("/login")

            if role and session.get("role") != role:
                return "Unauthorized", 403

            return fn(*args, **kwargs)
        wrapper.__name__ = fn.__name__
        return wrapper
    return decorator
