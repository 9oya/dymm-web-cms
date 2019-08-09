from flask import request, render_template

from dymm_cms import app
from errors import bad_req, forbidden, ok, unauthorized
from helpers.string_helpers import str_to_bool
from . import banner_api, _m, _r
from .banner_helpers import BannerHelper
from .banner_forms import BannerForm


# GET services
# -----------------------------------------------------------------------------
@banner_api.route('/form', methods=['GET'])
@banner_api.route('/<int:banner_id>/form', methods=['GET'])
def fetch_filled_detail_banner_form(banner_id=None):
    if banner_id is None:
        form = BannerHelper.get_empty_banner_form()
        return render_template('banner/bx_banner_detail.html', detail_form=form)
    banner = BannerHelper.get_a_banner(banner_id)
    if not banner:
        return forbidden(_m.NONEXISTENT.format(banner_id))
    form = BannerHelper.get_filled_banner_form(banner)
    return render_template('banner/bx_banner_detail.html', banner=banner,
                           detail_form=form)


# POST services
# -----------------------------------------------------------------------------
@banner_api.route('/form', methods=['POST'])
def post_a_banner_with_detail_form():
    form = BannerForm(request.form)
    if not form.validate():
        return bad_req(form.errors)
    BannerHelper.create_a_banner(form)
    return ok(_m.OK_POST.format('Banner'))


# PUT services
# -----------------------------------------------------------------------------
@banner_api.route('/<int:banner_id>/form', methods=['PUT'])
def put_a_banner_with_detail_form(banner_id=None):
    if banner_id is None:
        return bad_req(_m.EMPTY_PARAM.format('banner_id'))
    form = BannerForm(request.form)
    if not form.validate():
        return bad_req(form.errors)
    banner = BannerHelper.get_a_banner(banner_id)
    if not banner:
        return forbidden(_m.NONEXISTENT.format(banner_id))
    BannerHelper.update_a_banner(banner, form)
    return ok(_m.OK_PUT.format('Banner'))


# DELETE services
# -----------------------------------------------------------------------------
