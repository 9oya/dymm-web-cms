from werkzeug.utils import secure_filename
from flask import request, render_template

from dymm_cms import app
from dymm_cms.errors import bad_req, forbidden, ok, unauthorized
from . import asset_api, _m, _r, _u
from .asset_helpers import AssetHelper
from ..tag.tag_helpers import TagHelper


# GET services
# -----------------------------------------------------------------------------
@asset_api.route('/pop/import/<dirname>/<target>', methods=['GET'])
@asset_api.route('/pop/import/<dirname>/<target>/<tag_id>', methods=['GET'])
def pop_upload_file_form(dirname=None, target=None, tag_id=None):
    return render_template('asset/pop_asset_import.html', dirname=dirname,
                           target=target, tag_id=tag_id)


@asset_api.route('/<dirname>', methods=['GET'])
def fetch_assets(dirname=None):
    dir_names = AssetHelper.get_asset_dir_names()
    dir_form = AssetHelper.get_dir_form()
    choices = AssetHelper.get_dir_select_choices(dir_names)
    dir_form.dir_select.choices = choices
    dir_form.path_select.choices = choices
    dir_form.dir_select.data = dirname
    dir_form.path_select.data = dirname
    if dirname == 'archive':
        zip_names = AssetHelper.get_file_names(dirname, 'zip', True)
        return render_template('asset/bx_asset_list.html', dirname=dirname,
                               dirform=dir_form, zip_names=zip_names,
                               imgs_cnt=len(zip_names))
    pdf_names = AssetHelper.get_file_names(dirname, 'pdf', False)
    png_names = AssetHelper.get_file_names(dirname, 'png', False)
    pdf_dict = AssetHelper.convert_file_names_into_json(pdf_names)
    if dirname == 'photo' or dirname == 'photo@2x':
        org_names = AssetHelper.get_file_names(dirname, 'org', False)
        eps_names = AssetHelper.get_file_names(dirname, 'eps', False)
        org_dict = AssetHelper.convert_file_names_into_json(org_names)
        eps_dict = AssetHelper.convert_file_names_into_json(eps_names)
        assets = AssetHelper.gen_matching_assets(png_names, pdf_dict,
                                                 svg_dict=None,
                                                 org_dict=org_dict,
                                                 eps_dict=eps_dict)
        return render_template('asset/bx_asset_list.html', dirname=dirname,
                               dirform=dir_form, assets=assets,
                               imgs_cnt=len(assets))
    svg_names = AssetHelper.get_file_names(dirname, 'svg', False)
    # pdf_dict = AssetHelper.convert_file_names_into_json(pdf_names)
    svg_dict = AssetHelper.convert_file_names_into_json(svg_names)
    assets = AssetHelper.gen_matching_assets(png_names, pdf_dict, svg_dict)
    return render_template('asset/bx_asset_list.html', dirname=dirname,
                           dirform=dir_form, assets=assets,
                           imgs_cnt=len(assets))


@asset_api.route('/gen-line/<dirname>', methods=['GET'])
def fetch_native_app_code_set(dirname=None):
    png_names = AssetHelper.get_file_names(dirname, 'png', False)
    gen_lines = AssetHelper.convert_file_names_into_app_code(png_names)
    return render_template('asset/pop_asset_gen.html', gen_lines=gen_lines)


# POST services
# -----------------------------------------------------------------------------
@asset_api.route('/import/<dirname>/<target>', methods=['POST'])
@asset_api.route('/import/<dirname>/<target>/file-name/<filename>',
                 methods=['POST'])
@asset_api.route('/import/<dirname>/<target>/id/<int:tag_id>',
                 methods=['POST'])
def import_file(dirname=None, target=None, filename=None, tag_id=None):
    if target == 'files':
        _files = request.files.getlist(target)
        if not _files:
            return bad_req()
        cnt = AssetHelper.upload_multi_files(_files, dirname, 'png')
        return ok(_m.OK_UPLOAD.format(cnt, target))
    file = request.files[target]
    if not file or not AssetHelper.is_allowed_file_type(file.filename, target):
        return bad_req(_m.BAD_PARAM)
    if dirname == 'tag' and tag_id is not None:
        _filename = 'tag-{0}.{1}'.format(tag_id, target)
    elif dirname == 'photo' and tag_id is not None:
        tag = TagHelper.get_a_tag(tag_id)
        if target == 'org':
            _filename = 'photo-{0}-{1}-{2}-{3}-{4}-{5}.{6}'.format(
                tag.class1, tag.division1, tag.division2, tag.division3,
                tag.division4, tag.division5, 'png')
        else:
            _filename = 'photo-{0}-{1}-{2}-{3}-{4}-{5}.{6}'.format(
                tag.class1, tag.division1, tag.division2, tag.division3,
                tag.division4, tag.division5, target)
    elif isinstance(filename, str):
        _filename = '{0}.{1}'.format(filename, target)
    else:
        _filename = secure_filename(file.filename)
    location = _u.ASSET + "/{0}/{1}".format(dirname, target)
    AssetHelper.upload_single_file(file, location, _filename)
    return ok(_m.OK_UPLOAD.format(_filename, target))


@asset_api.route('/zip/<dirname>/<target>', methods=['POST'])
def post_asset_directory_zip(dirname=None, target=None):
    AssetHelper.create_directory_zip(dirname, target)
    return ok(_m.OK_POST.format(dirname))


# PUT services
# -----------------------------------------------------------------------------
@asset_api.route('/<dirname>/<old_name>/rename/<new_name>', methods=['PUT'])
def put_asset_name(dirname=None, old_name=None, new_name=None):
    if new_name is None:
        return bad_req(_m.EMPTY_PARAM.format('asset_name'))
    AssetHelper.rename_asset(dirname, old_name, new_name)
    return ok()


@asset_api.route('/<old_dir>/<filename>/move/<new_dir>', methods=['PUT'])
def put_asset_dir(old_dir=None, filename=None, new_dir=None):
    if not old_dir and not filename and not new_dir:
        return bad_req(_m.EMPTY_PARAM.format('params'))
    AssetHelper.move_asset_dir(old_dir, new_dir, filename)
    return ok(_m.OK_PUT.format('asset dir'))


# DELETE services
# -----------------------------------------------------------------------------
@asset_api.route('/<dirname>/<filename>/del/<target>', methods=['DELETE'])
def delete_asset(dirname=None, filename=None, target=None):
    if not dirname and not filename and not target:
        return bad_req(_m.EMPTY_PARAM.format('params'))
    if target == 'all':
        AssetHelper.delete_asset(dirname, 'png', filename)
        AssetHelper.delete_asset(dirname, 'svg', filename)
        AssetHelper.delete_asset(dirname, 'pdf', filename)
        return ok(_m.OK_DELETE.format(filename + 'all'))
    AssetHelper.delete_asset(dirname, target, filename)
    return ok(_m.OK_DELETE.format(filename + target))


@asset_api.route('/<dirname>/empty', methods=['DELETE'])
def empty_asset_dir(dirname=None):
    if request.values.get('del_key') != app.config['DELETE_KEY']:
        return unauthorized(_m.UN_AUTH.format('del_key'))
    if not dirname:
        return bad_req(_m.EMPTY_PARAM.format('params'))
    AssetHelper.empty_asset_dir(dirname)
    return ok()
