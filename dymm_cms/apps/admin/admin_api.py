from flask import request

from dymm_cms import b_crypt
from dymm_cms import app
from patterns import ForbiddenPattern, MessagePattern
from errors import bad_req, forbidden, ok
from helpers.token_helpers import generate_url_token, confirm_url_token
from . import admin_api
from .admin_forms import SignInAdminForm, SignUpAdminForm
from .admin_helpers import AdminHelper


@admin_api.route('/refresh', methods=['POST'])
def refresh_url_token():
    try:
        token = request.cookies.get('dymm_url_token')
    except ValueError:
        return forbidden(ForbiddenPattern.EXPR_TOKEN, MessagePattern.EXPIRED)
    try:
        confirm_url_token(token)
    except ValueError:
        return forbidden(ForbiddenPattern.EXPR_TOKEN, MessagePattern.EXPIRED)
    try:
        email = request.values.get('email')
    except ValueError:
        return bad_req(MessagePattern.EMPTY_PARAM.format('email'))
    admin = AdminHelper.get_admin_avatar(email)
    if admin is None:
        return forbidden(MessagePattern.NONEXISTENT.format('email'))
    admin_info = AdminHelper.get_admin_info_json(admin)
    url_token = generate_url_token(admin.email)
    return ok(data=dict(admin_info=admin_info, url_token=url_token))


@admin_api.route('/auth', methods=['POST'])
def auth_admin():
    form = SignInAdminForm(request.form)
    if not form.validate():
        return forbidden(form.errors)
    admin = AdminHelper.get_admin_avatar(form.email.data)
    if admin is None:
        return forbidden(MessagePattern.NONEXISTENT.format('email'))
    if not b_crypt\
            .check_password_hash(admin.password_hash, form.password.data):
        return forbidden(MessagePattern.INCORRECT.format('password'))
    admin_info = AdminHelper.get_admin_info_json(admin)
    url_token = generate_url_token(admin.email)
    return ok(data=dict(admin_info=admin_info, url_token=url_token))


@admin_api.route('/new', methods=['POST'])
def sign_up_admin():
    form = SignUpAdminForm(request.form)
    admin_key = app.config['ADMIN_MASTER_KEY']
    if form.master_key.data != admin_key:
        return bad_req(MessagePattern.EMPTY_PARAM.format('master_key'))
    if not form.validate():
        return forbidden(form.errors)
    if AdminHelper.is_admin_mail_duplicated(form.email.data):
        return forbidden(MessagePattern.DUPLICATED.format('email'))
    admin = AdminHelper.create_admin_avatar(form)
    admin_info = AdminHelper.get_admin_info_json(admin)
    url_token = generate_url_token(admin.email)
    return ok(data=dict(admin_info=admin_info, url_token=url_token))
