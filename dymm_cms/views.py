from flask import Blueprint, render_template

from .apps.admin.admin_helpers import AdminHelper
from .apps.tag.tag_helpers import TagHelper
from .apps.banner.banner_helpers import BannerHelper
from .apps.asset.asset_helper import AssetHelper

auth_view = Blueprint('auth_view', __name__, url_prefix='')
app_view = Blueprint('app_view', __name__, url_prefix='')


@auth_view.route('/')
@auth_view.route('/admin/sign-in')
def admin_sign_in_view():
    form = AdminHelper.get_empty_admin_sign_in_form()
    return render_template('admin/base_admin.html', pattern="sign-in",
                           form=form)


@auth_view.route('/admin/sign-up')
def admin_sign_up_view():
    form = AdminHelper.get_empty_admin_sign_up_form()
    return render_template('admin/base_admin.html', pattern="sign-up",
                           form=form)


@app_view.route('/asset')
def asset_view():
    dirname = "category"
    dir_names = AssetHelper.get_asset_dir_names()
    png_names = AssetHelper.get_file_names(dirname, 'png', False)
    pdf_names = AssetHelper.get_file_names(dirname, 'pdf', False)
    svg_names = AssetHelper.get_file_names(dirname, 'svg', False)
    pdf_dict = AssetHelper.convert_file_names_into_json(pdf_names)
    svg_dict = AssetHelper.convert_file_names_into_json(svg_names)
    assets = AssetHelper.gen_matching_assets(png_names, pdf_dict, svg_dict)
    dir_form = AssetHelper.get_dir_form()
    choices = AssetHelper.get_dir_select_choices(dir_names)
    dir_form.dir_select.choices = choices
    dir_form.path_select.choices = choices
    dir_form.dir_select.data = dirname
    dir_form.path_select.data = dirname
    return render_template('asset/base_asset.html', dirname=dirname,
                           dirform=dir_form, assets=assets,
                           imgs_cnt=len(assets))


@app_view.route('/home')
def index_view():
    return render_template('home/base_home.html')


@app_view.route('/tag')
def tag_view():
    tags = TagHelper.get_initial_tags()
    form = TagHelper.get_empty_tag_form()
    return render_template('tag/base_tag.html', tags=tags,
                           tags_cnt=len(tags),
                           detail_form=form)


@app_view.route('/banner')
def banner_view():
    banners = BannerHelper.get_banners()
    form = BannerHelper.get_empty_banner_form()
    return render_template('banner/base_banner.html', banners=banners,
                           banners_cnt=len(banners),
                           detail_form=form)
