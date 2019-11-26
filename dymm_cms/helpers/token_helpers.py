from flask import request, redirect
from itsdangerous import URLSafeTimedSerializer

from dymm_cms import app
from dymm_cms.errors import forbidden
from dymm_cms.patterns import ErrorPattern, MsgPattern

msg_lib = MsgPattern()
code_lib = ErrorPattern()


def generate_url_token(seed):
    serializer = URLSafeTimedSerializer(
        app.config['SECRET_KEY'],
        salt=app.config['SECURITY_PASSWORD_SALT']
    )
    return serializer.dumps(seed)


# def confirm_url_token(token, expiration=1800):
def confirm_url_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(
        app.config['SECRET_KEY'],
        salt=app.config['SECURITY_PASSWORD_SALT']
    )
    try:
        serializer.loads(token, max_age=expiration)
    except:
        raise ValueError
    return True


def validate_token_before_request():
    try:
        token = request.cookies.get('dymm_url_token')
    except ValueError:
        return forbidden(msg_lib.EXPIRED, code_lib.EXPR_TOKEN)
    try:
        confirm_url_token(token)
    except ValueError:
        return forbidden(msg_lib.EXPIRED, code_lib.EXPR_TOKEN)


def validate_token_and_redirect():
    try:
        token = request.cookies.get('dymm_url_token')
    except ValueError:
        return redirect("/admin/sign-in")
    try:
        confirm_url_token(token)
    except ValueError:
        return redirect("/admin/sign-in")
