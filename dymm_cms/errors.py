from flask import jsonify


def bad_req(message='Bad request'):
    return jsonify(ok=False,
                   message=message), 400


def unauthorized(message='Unauthorized'):
    return jsonify(ok=False,
                   message=message), 401


def forbidden(message='Forbidden', pattern=None, ):
    return jsonify(ok=False,
                   pattern=pattern,
                   message=message), 403


def ok(message='Ok', data=None):
    return jsonify(ok=True,
                   message=message,
                   data=data), 200
