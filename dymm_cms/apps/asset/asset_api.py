from werkzeug.utils import secure_filename
from flask import request, render_template

from dymm_cms.errors import bad_req, forbidden, ok
from . import asset_api, _m, _r, _u
from .asset_helper import AssetHelper
from ..tag.tag_helpers import TagHelper


@asset_api.route('/import/<dirname>/<target>', methods=['POST'])
@asset_api.route('/import/<dirname>/<target>/<id_or_name>', methods=['POST'])
def import_file(dirname=None, target=None, id_or_name=None):
    if target == 'files':
        _files = request.files.getlist(target)
        if not _files:
            return bad_req()
        cnt = AssetHelper.upload_multi_files(_files, dirname, 'png')
        return ok(_m.OK_UPLOAD.format(cnt, target))
    file = request.files[target]
    if not file or not AssetHelper.is_allowed_file_type(file.filename, target):
        return bad_req(_m.BAD_PARAM)
    if dirname == 'tag':
        tag_id = int(id_or_name)
        filename = 'tag-{0}.{1}'.format(tag_id, target)
        if target == 'png':
            tag = TagHelper.get_a_tag(tag_id)
            TagHelper.update_tag_has_icon(tag)
    elif target != 'png' and isinstance(id_or_name, str):
        filename = '{0}.{1}'.format(id_or_name, target)
    else:
        filename = secure_filename(file.filename)
        # str_list = file.filename.split('.')
        # filename = "{0}.{1}".format(str_list[0], str_list[1])
    location = _u.ASSET + "/{0}/{1}".format(dirname, target)
    AssetHelper.upload_single_file(file, location, filename)
    return ok(_m.OK_UPLOAD.format(filename, target))


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
    png_names = AssetHelper.get_file_names(dirname, 'png', False)
    pdf_names = AssetHelper.get_file_names(dirname, 'pdf', False)
    svg_names = AssetHelper.get_file_names(dirname, 'svg', False)
    pdf_dict = AssetHelper.convert_file_names_into_json(pdf_names)
    svg_dict = AssetHelper.convert_file_names_into_json(svg_names)
    assets = AssetHelper.gen_matching_assets(png_names, pdf_dict, svg_dict)
    return render_template('asset/bx_asset_list.html', dirname=dirname,
                           dirform=dir_form, assets=assets,
                           imgs_cnt=len(assets))


@asset_api.route('/gen-line/<dirname>', methods=['GET'])
def fetch_native_app_code_set(dirname=None):
    png_names = AssetHelper.get_file_names(dirname, 'png', False)
    gen_lines = AssetHelper.convert_file_names_into_app_code(png_names)
    return render_template('asset/pop_asset_line.html', gen_lines=gen_lines)


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


@asset_api.route('/zip/<dirname>/<target>', methods=['POST'])
def post_asset_directory_zip(dirname=None, target=None):
    AssetHelper.create_directory_zip(dirname, target)
    return ok(_m.OK_POST.format(dirname))
