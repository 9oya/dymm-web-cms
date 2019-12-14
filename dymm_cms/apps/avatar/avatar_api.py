from flask import request, render_template

from dymm_cms import app
from dymm_cms.errors import bad_req, forbidden, ok, unauthorized
from dymm_cms.helpers.string_helpers import str_to_bool
from . import avatar_api, _m, _r
from .avatar_helpers import AvatarHelper
from .avatar_forms import AvatarForm


# GET services
# -----------------------------------------------------------------------------
@avatar_api.route('/export/<option>/page/<int:page_num>', methods=['GET'])
@avatar_api.route('/export/<option>/<keyword>/<target>', methods=['GET'])
@avatar_api.route('/export/<option>/<target>', methods=['GET'])
def export_tags_file(option=None, keyword=None, page_num=None, target=None):
    if option == 'search' and keyword is not None:
        avatars = AvatarHelper.get_avatars_by_keyword(keyword, target)
        file_name = 'avatar_keyword_' + keyword
        file = AvatarHelper.get_avatars_file(avatars, file_name)
        if not file:
            return bad_req(_m.BAD_PARAM)
        return file
    elif option == 'select':
        avatars = AvatarHelper.get_avatars_by_selected_option(target)
        file_name = 'avatar_select_' + target
        file = AvatarHelper.get_avatars_file(avatars, file_name)
        if not file:
            return bad_req(_m.BAD_PARAM)
        return file
    elif option == 'all':
        avatars = AvatarHelper.get_all_avatars()
        file_name = 'avatar_all'
    elif option == 'limit':
        avatars = AvatarHelper.get_avatars(sort_type='date', page=page_num)
        file_name = 'avatars_p{0}'.format(page_num)
    else:
        return bad_req(_m.BAD_PARAM.format('option'))
    file = AvatarHelper.get_avatars_file(avatars.items, file_name)
    if not file:
        return bad_req(_m.BAD_PARAM)
    return file


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


@avatar_api.route('/search/<string:keyword>')
@avatar_api.route('/search/<string:keyword>/<option>')
@avatar_api.route('/select/<option>')
def search_avatars_by_keyword(keyword=None, option=None):
    if keyword is None:
        avatars = AvatarHelper.get_avatars_by_selected_option(option)
    else:
        avatars = AvatarHelper.get_avatars_by_keyword(keyword, option)
    return render_template('avatar/cp_avatar_tb.html', searched_avatars=avatars)


# POST services
# -----------------------------------------------------------------------------
@avatar_api.route('/import/<option>', methods=['POST'])
@avatar_api.route('/import/<option>/<del_key>', methods=['POST'])
def import_avatar_list_file(option=None, del_key=None):
    if option == 'gen-avatar':
        dicts = request.get_records(field_name='csv', encoding='utf-8-sig')
        cnt = AvatarHelper.create_avatars_w_dicts(dicts)
        return ok(_m.OK_IMPORT.format(cnt, 'avatar'))
    elif option == 'mod-avatar':
        dicts = request.get_records(field_name='csv', encoding='utf-8-sig')
        cnt = AvatarHelper.update_avatars_w_dicts(dicts)
        return ok(_m.OK_IMPORT.format(cnt, 'avatar'))
    elif option == 'del-avatar':
        if del_key != app.config['DELETE_KEY']:
            return unauthorized(_m.UN_AUTH.format('del_key'))
        dicts = request.get_records(field_name='csv', encoding='utf-8-sig')
        cnt = AvatarHelper.delete_avatars_w_dicts(dicts)
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


# DELETE services
# -----------------------------------------------------------------------------
@avatar_api.route('/<int:avatar_id>', methods=['DELETE'])
def delete_a_avatar(avatar_id=None):
    if request.values.get('del_key') != app.config['DELETE_KEY']:
        return unauthorized(_m.UN_AUTH.format('del_key'))
    if avatar_id is None:
        return bad_req(_m.EMPTY_PARAM.format('avatar_id'))
    avatar = AvatarHelper.get_a_avatar(avatar_id)
    if not avatar:
        return forbidden(_m.NONEXISTENT.format(avatar_id))
    AvatarHelper.delete_a_avatar(avatar)
    return ok(_m.OK_DELETE.format(avatar_id))
