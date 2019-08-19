from flask import request, render_template

from dymm_cms import app
from errors import bad_req, forbidden, ok, unauthorized
from helpers.string_helpers import str_to_bool
from . import tag_api, _m, _r
from .tag_helpers import TagHelper
from .tag_forms import TagSortForm


# GET services
# -----------------------------------------------------------------------------
@tag_api.route('/<int:tag_id>/export/<option>', methods=['GET'])
@tag_api.route('/export/<option>', methods=['GET'])
def export_tags_file(tag_id=None, option=None):
    if tag_id is None:
        if option == 'all':
            tags = TagHelper.get_all_tags()
            file_name = 'tag_all'
        elif option == 'limit':
            tags = TagHelper.get_initial_tags()
            file_name = 'tag_super'
        else:
            return bad_req(_m.BAD_PARAM.format('option'))
    else:
        tag = TagHelper.get_a_tag(tag_id)
        if option == 'all':
            tags = TagHelper.get_all_low_div_tags(tag_id)
            file_name = 'tag_{}_all'.format(tag.eng_name.lower())
        elif option == 'limit':
            tags = TagHelper.get_low_div_tags(tag_id)
            file_name = 'tag_' + tag.eng_name.lower()
        else:
            tag = TagHelper.get_a_tag(tag_id)
            tags = TagHelper.get_specific_div_tags(tag, option)
            file_name = 'tag_{}_{}'.format(tag.eng_name, option)
    file = TagHelper.get_tags_file(tags, file_name)
    if not file:
        return bad_req(_m.BAD_PARAM)
    return file


@tag_api.route('/set/<int:tag_id>/export', methods=['GET'])
def export_tag_sets_file(tag_id=None):
    tag_sets = TagHelper.get_tag_sets(tag_id)
    file_name = 'tag{}_set'.format(tag_id)
    file = TagHelper.get_tag_sets_file(tag_sets, file_name)
    return file


@tag_api.route('/<class1_id>/<target>', methods=['GET'])
@tag_api.route('/<class1_id>/<division1_id>/<target>', methods=['GET'])
@tag_api.route('/<class1_id>/<division1_id>/<division2_id>/<target>',
               methods=['GET'])
@tag_api.route('/<class1_id>/<division1_id>/<division2_id>/<division3_id>/'
               '<target>', methods=['GET'])
def fetch_tag_division_list(class1_id=None, division1_id=None,
                            division2_id=None, division3_id=None,
                            target=None):
    if class1_id is None:
        return bad_req(_m.EMPTY_PARAM.format('class1_id'))
    tags = TagHelper.get_low_div_tags(class1=class1_id,
                                      division1=division1_id,
                                      division2=division2_id,
                                      division3=division3_id)
    return render_template('tag/cp_tag_division.html', tags=tags,
                           target=target)


@tag_api.route('', methods=['GET'])
@tag_api.route('/<target>', methods=['GET'])
def fetch_initial_tags(target=None):
    tags = TagHelper.get_initial_tags()
    if target == 'add':
        return render_template('tag/cp_tag_tb.html', tags_w_add=tags)
    return render_template('tag/cp_tag_tb.html', tags=tags)


@tag_api.route('/<int:tag_id>/sub', methods=['GET'])
@tag_api.route('/<int:tag_id>/sub/<target>', methods=['GET'])
def fetch_sub_tags(tag_id=None, target=None):
    if tag_id is None:
        return bad_req(_m.EMPTY_PARAM.format('tag_id'))
    tags = TagHelper.get_low_div_tags(tag_id)
    if target == 'add':
        return render_template('tag/cp_tag_tb.html', tags_w_add=tags)
    return render_template('tag/cp_tag_tb.html', tags=tags)


@tag_api.route('/pick/<int:tag_id>', methods=['GET'])
def fetch_a_fact_and_pick_template(tag_id=None):
    if tag_id is None:
        return bad_req(_m.EMPTY_PARAM.format('tag_id'))
    tag = TagHelper.get_a_tag(tag_id)
    if not tag:
        return forbidden(_m.NONEXISTENT.format(tag_id))
    sub_facts = TagHelper.get_low_div_tags(tag_id)
    return render_template('tag/cp_tag_pick.html', tag=tag,
                           tags_cnt=len(sub_facts))


@tag_api.route('/form', methods=['GET'])
@tag_api.route('/<int:tag_id>/form', methods=['GET'])
def fetch_filled_detail_tag_form(tag_id=None):
    if tag_id is None:
        form = TagHelper.get_empty_tag_form()
        return render_template('tag/bx_tag_detail.html', detail_form=form)
    tag = TagHelper.get_a_tag(tag_id)
    if not tag:
        return forbidden(_m.NONEXISTENT.format(tag_id))
    form = TagHelper.get_filled_tag_form(tag)
    return render_template('tag/bx_tag_detail.html', tag=tag,
                           detail_form=form)


@tag_api.route('/<int:super_id>/set/<sort_type>', methods=['GET'])
def fetch_tag_sets(super_id=None, sort_type=None):
    if super_id is None:
        return bad_req(_m.EMPTY_PARAM.format('tag_id'))
    tag_sets = TagHelper.get_tag_sets(super_id, sort_type)
    form = TagSortForm()
    form.sort_select.data = sort_type
    if not tag_sets:
        super_tag = TagHelper.get_a_tag(super_id)
        return render_template('tag/bx_tag_set.html', super_tag=super_tag,
                               form=form)
    return render_template('tag/bx_tag_set.html',
                           super_tag=tag_sets[0].super,
                           form=form, tag_sets=tag_sets,
                           tag_set_cnt=len(tag_sets))


@tag_api.route('/step/<int:tag_id>', methods=['GET'])
def fetch_tag_step(tag_id=None):
    if tag_id is None:
        return bad_req(_m.EMPTY_PARAM.format('tag_id'))
    tag = TagHelper.get_a_tag(tag_id)
    return render_template('tag/cp_tag_item.html', tag=tag)


# POST services
# -----------------------------------------------------------------------------
@tag_api.route('/import/<option>', methods=['POST'])
def import_tag_list_file(option=None):
    if option == 'gen-tag':
        dicts = request.get_records(field_name='csv', encoding='utf-8-sig')
        cnt = TagHelper.create_tags_w_dicts(dicts)
        return ok(_m.OK_IMPORT.format(cnt, 'tag'))
    elif option == 'mod-tag':
        dicts = request.get_records(field_name='csv', encoding='utf-8-sig')
        cnt = TagHelper.update_tags_w_dicts(dicts)
        return ok(_m.OK_IMPORT.format(cnt, 'tag'))
    elif option == 'gen-set-low':
        dicts = request.get_records(field_name='csv', encoding='utf-8-sig')
        cnt = TagHelper.create_tag_sets_w_dicts(dicts, option)
        return ok(_m.OK_IMPORT.format(cnt, 'tag'))
    elif option == 'mod-set-id':
        dicts = request.get_records(field_name='csv', encoding='utf-8-sig')
        cnt = TagHelper.update_tag_sets_w_dicts(dicts, option)
        return ok(_m.OK_IMPORT.format(cnt, 'tag'))
    elif option == 'gen-set-eng':
        dicts = request.get_records(field_name='csv', encoding='utf-8-sig')
        cnt = TagHelper.create_tag_sets_w_dicts(dicts, option)
        return ok(_m.OK_IMPORT.format(cnt, 'tag'))
    elif option == 'mod-set-eng':
        dicts = request.get_records(field_name='csv', encoding='utf-8-sig')
        cnt = TagHelper.update_tag_sets_w_dicts(dicts, option)
        return ok(_m.OK_IMPORT.format(cnt, 'tag'))
    else:
        return bad_req(_m.BAD_PARAM.format('option'))


@tag_api.route('/form', methods=['POST'])
def post_a_tag_with_detail_form():
    form = TagHelper.get_tag_form_for_validate(request)
    if not form.validate():
        return bad_req(form.errors)
    if TagHelper.is_tag_duplicate(form):
        return forbidden(_m.DUPLICATED.format('division'))
    result = TagHelper.create_a_tag(form)
    return ok(_m.OK_POST.format(result))


@tag_api.route('/set/<int:super_id>/<int:sub_id>', methods=['POST'])
def post_a_tag_set(super_id=None, sub_id=None):
    if super_id is None:
        return bad_req(_m.EMPTY_PARAM.format('super_id'))
    if sub_id is None:
        return bad_req(_m.EMPTY_PARAM.format('tag_id'))
    tag_set = TagHelper.get_a_tag_set(super_id=super_id, sub_id=sub_id)
    if tag_set:
        return forbidden(_m.DUPLICATED.format(sub_id))
    priority = TagHelper.gen_tag_set_next_priority(super_id)
    TagHelper.create_a_tag_set(super_id, sub_id, priority)
    return ok(_m.OK_POST.format(str(super_id) + "+" + str(sub_id)))


# PUT services
# -----------------------------------------------------------------------------
@tag_api.route('/<int:tag_id>/form', methods=['PUT'])
def put_a_tag_with_detail_form(tag_id=None):
    if tag_id is None:
        return bad_req(_m.EMPTY_PARAM.format('tag_id'))
    form = TagHelper.get_tag_form_for_validate(request)
    if not form.validate():
        return bad_req(form.errors)
    tag = TagHelper.get_a_tag(tag_id)
    if not tag:
        return forbidden(_m.NONEXISTENT.format(tag_id))
    if str_to_bool(form.is_division_modified.data) and \
            form.division5.data == 0:
        TagHelper.update_tag_divisions(tag, form)
        return ok(_m.OK_PUT.format('Divisions'))
    result = TagHelper.update_a_tag(tag, form)
    return ok(_m.OK_PUT.format(result))


@tag_api.route('/set/<int:upper_id>/<int:lower_id>/priority/swap',
               methods=['PUT'])
def swap_tag_set_prioritys(upper_id=None, lower_id=None):
    upper_tag_set = TagHelper.get_a_tag_set(upper_id)
    upper_priority = upper_tag_set.priority
    lower_tag_set = TagHelper.get_a_tag_set(lower_id)
    lower_priority = lower_tag_set.priority
    super_id = upper_tag_set.super_id
    if upper_priority is None or upper_priority == 0 or \
            lower_priority is None or lower_priority == 0:
        top_priority = TagHelper.get_top_priority_from_tag_set(super_id)
        if top_priority is None or top_priority == 0:
            TagHelper.update_a_tag_set_priority(lower_tag_set, 1000)
            TagHelper.update_a_tag_set_priority(upper_tag_set, 999)
        else:
            next_prior = TagHelper.get_next_priority_from_tag_set(super_id)
            TagHelper.update_a_tag_set_priority(lower_tag_set, next_prior - 1)
            TagHelper.update_a_tag_set_priority(upper_tag_set, next_prior - 2)
        return ok(_m.OK_PUT.format('fact_set priority'))
    TagHelper.update_a_tag_set_priority(lower_tag_set, upper_priority)
    TagHelper.update_a_tag_set_priority(upper_tag_set, lower_priority)
    return ok(_m.OK_PUT.format('fact_set priority'))


@tag_api.route('/set/<int:tag_set_id>/priority', methods=['PUT'])
@tag_api.route('/set/<int:tag_set_id>/priority/<priority>', methods=['PUT'])
def set_initial_priority_into_tag_set(tag_set_id=None, priority=None):
    tag_set = TagHelper.get_a_tag_set(tag_set_id)
    super_id = tag_set.super_id
    if priority is not None:
        TagHelper.update_a_tag_set_priority(tag_set, priority)
        return ok(_m.OK_PUT.format('tag_set priority'))
    top_priority = TagHelper.get_top_priority_from_tag_set(super_id)
    if top_priority is None or top_priority == 0:
        TagHelper.update_a_tag_set_priority(tag_set, 1000)
        return ok(_m.OK_PUT.format('tag_set priority'))
    if tag_set.priority == top_priority:
        return ok()
    next_priority = TagHelper.get_next_priority_from_tag_set(super_id)
    TagHelper.update_a_tag_set_priority(tag_set, next_priority - 1)
    return ok(_m.OK_PUT.format('tag_set priority'))


@tag_api.route('/set/<int:tag_set_id>/<target>', methods=['PUT'])
@tag_api.route('/set/<int:tag_set_id>/<target>/<value>', methods=['PUT'])
@tag_api.route('/set/<int:tag_set_id>/<target>/<value>', methods=['PUT'])
def put_tag_set(tag_set_id=None, target=None, value=None):
    if tag_set_id is None:
        return bad_req(_m.EMPTY_PARAM.format('tag_set_id'))
    tag_set = TagHelper.get_a_tag_set(tag_set_id)
    if not tag_set:
        return forbidden(_m.NONEXISTENT.format('tag_set_id'))
    TagHelper.update_a_tag_set_w_target(tag_set, target, value)
    return ok(_m.OK_PUT.format(tag_set_id))


# DELETE services
# -----------------------------------------------------------------------------
@tag_api.route('/<int:tag_id>', methods=['DELETE'])
def delete_a_tag(tag_id=None):
    if request.values.get('del_key') != app.config['DELETE_KEY']:
        return unauthorized(_m.UN_AUTH.format('del_key'))
    if tag_id is None:
        return bad_req(_m.EMPTY_PARAM.format('tag_id'))
    tag = TagHelper.get_a_tag(tag_id)
    if not tag:
        return forbidden(_m.NONEXISTENT.format(tag_id))
    TagHelper.delete_a_tag(tag)
    return ok(_m.OK_DELETE.format(tag_id))


@tag_api.route('/set/<int:tag_set_id>', methods=['DELETE'])
def delete_a_tag_set(tag_set_id=None):
    if request.values.get('del_key') != app.config['DELETE_KEY']:
        return unauthorized(_m.UN_AUTH.format('del_key'))
    if tag_set_id is None:
        return bad_req(_m.EMPTY_PARAM.format('tag_set_id'))
    tag_set = TagHelper.get_a_tag_set(tag_set_id=tag_set_id)
    if not tag_set:
        return forbidden(_m.NONEXISTENT.format(str(tag_set_id)))
    deleted_name = TagHelper.delete_a_tag_set(tag_set)
    return ok(_m.OK_DELETE.format(deleted_name))


@tag_api.route('/<int:tag_id>/set', methods=['DELETE'])
def delete_tag_sets(tag_id=None):
    if request.values.get('del_key') != app.config['DELETE_KEY']:
        return unauthorized(_m.UN_AUTH.format('del_key'))
    if tag_id is None:
        return bad_req(_m.EMPTY_PARAM.format('tag_id'))
    tag_sets = TagHelper.get_tag_sets(tag_id)
    cnt = TagHelper.delete_tag_sets(tag_sets)
    return ok(_m.OK_DELETE.format(cnt))
