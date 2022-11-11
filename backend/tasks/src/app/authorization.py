from .get_token import get_token
from .get_user import get_user
from .get_email_permission import get_email_permission
from flask import Request


def authorization(request: Request):
    auth_headers = request.headers.get("Authorization")
    token = get_token(auth_headers)
    if not token:
        raise ValueError()
    else:
        user = get_user(token)
        if user is None:
            raise ValueError()
        else:
            is_permission_exist = get_email_permission(user.username)
            if is_permission_exist:
                return (token, user)
            else:
                raise ValueError()
