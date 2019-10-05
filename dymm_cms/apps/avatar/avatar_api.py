from flask import request, render_template

from dymm_cms import app
from dymm_cms.errors import bad_req, forbidden, ok, unauthorized
from dymm_cms.helpers.string_helpers import str_to_bool
from . import avatar_api, _m, _r
from .avatar_helpers import AvatarHelper
from .avatar_forms import AvatarForm


# GET services
# -----------------------------------------------------------------------------
@avatar_api.route('/form', methods=['GET'])
@avatar_api.route('/<avatar_id>/form', methods=['GET'])
def fetch_filled_detail_avatar_form(avatar_id=None):
    if avatar_id is None:
        return bad_req(_m.EMPTY_PARAM.format('avatar_id'))
    avatar = AvatarHelper.get_a_avatar(avatar_id)
    if not avatar:
        return forbidden(_m.NONEXISTENT.format(avatar_id))
    form = AvatarHelper.get_filled_avatar_form(avatar)
    return render_template('avatar/bx_avatar_detail.html', avatar=avatar,
                           detail_form=form)


# POST services
# -----------------------------------------------------------------------------
@avatar_api.route('/import/<option>', methods=['POST'])
def import_avatar_list_file(option=None):
    if option == 'gen-avatar':
        dicts = request.get_records(field_name='csv', encoding='utf-8-sig')
        cnt = AvatarHelper.create_avatars_w_dicts(dicts)
        return ok(_m.OK_IMPORT.format(cnt, 'avatar'))
    elif option == 'mod-avatar':
        dicts = request.get_records(field_name='csv', encoding='utf-8-sig')
        cnt = AvatarHelper.update_avatars_w_dicts(dicts)
        return ok(_m.OK_IMPORT.format(cnt, 'avatar'))
    else:
        return bad_req(_m.BAD_PARAM.format('option'))


# PUT services
# -----------------------------------------------------------------------------
@avatar_api.route('/<avatar_id>/form', methods=['PUT'])
def put_a_banner_with_detail_form(avatar_id=None):
    if avatar_id is None:
        return bad_req(_m.EMPTY_PARAM.format('banner_id'))
    form = AvatarForm(request.form)
    if not form.validate():
        return bad_req(form.errors)
    avatar = AvatarHelper.get_a_avatar(avatar_id)
    if not avatar:
        return forbidden(_m.NONEXISTENT.format(avatar_id))
    AvatarHelper.update_a_avatar(avatar, form)
    return ok(_m.OK_PUT.format('Avatar'))
