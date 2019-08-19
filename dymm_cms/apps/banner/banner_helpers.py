from sqlalchemy import text

from dymm_cms import excel
from database import db_session
from models import Banner
from patterns import TagType
from helpers.string_helpers import str_to_bool, str_to_none
from .banner_forms import BannerForm


class BannerHelper(object):
    # Validators
    # -------------------------------------------------------------------------

    # GET methods
    # -------------------------------------------------------------------------
    @staticmethod
    def get_a_banner(banner_id):
        banner = Banner.query.filter(
            Banner.id == banner_id
        ).first()
        return banner

    @staticmethod
    def get_banners():
        banners = Banner.query.filter(
            Banner.is_active == True
        ).order_by(Banner.priority.desc()).all()
        return banners

    @staticmethod
    def get_empty_banner_form():
        form = BannerForm()
        form.id.render_kw = {'disabled': True}
        form.is_active.data = 'True'
        form.delete_key.label = ''
        form.delete_key.render_kw = {'hidden': True}
        return form

    @staticmethod
    def get_filled_banner_form(banner: Banner):
        form = BannerForm()
        form.id.data = banner.id
        form.is_active.data = str(banner.is_active)
        form.priority.data = banner.priority
        form.img_name.data = banner.img_name
        form.txt_color.data = banner.txt_color
        form.bg_color.data = banner.bg_color
        form.eng_title.data = banner.eng_title
        form.kor_title.data = banner.kor_title
        form.jpn_title.data = banner.jpn_title
        form.eng_subtitle.data = banner.eng_subtitle
        form.kor_subtitle.data = banner.kor_subtitle
        form.jpn_subtitle.data = banner.jpn_subtitle
        return form

    # CREATE methods
    # -------------------------------------------------------------------------
    @staticmethod
    def create_a_banner(form: BannerForm):
        banner = Banner(is_active=str_to_bool(form.is_active.data),
                        priority=form.priority.data,
                        img_name=form.img_name.data,
                        txt_color=form.txt_color.data,
                        bg_color=form.bg_color.data,
                        eng_title=form.eng_title.data,
                        kor_title=form.kor_title.data,
                        jpn_title=form.jpn_title.data,
                        eng_subtitle=form.eng_subtitle.data,
                        kor_subtitle=form.kor_subtitle.data,
                        jpn_subtitle=form.jpn_subtitle.data)
        db_session.add(banner)
        db_session.commit()
        return True

    # UPDATE methods
    # -------------------------------------------------------------------------
    @staticmethod
    def update_a_banner(banner: Banner, form: BannerForm):
        banner.is_active = str_to_bool(form.is_active.data)
        banner.priority = form.priority.data
        banner.img_name = form.img_name.data
        banner.txt_color = form.txt_color.data
        banner.bg_color = form.bg_color.data
        banner.eng_title = form.eng_title.data
        banner.kor_title = form.kor_title.data
        banner.jpn_title = form.jpn_title.data
        banner.eng_subtitle = form.eng_subtitle.data
        banner.kor_subtitle = form.kor_subtitle.data
        banner.jpn_subtitle = form.jpn_subtitle.data
        banner.modified_timestamp = text("timezone('utc'::text, now())")
        db_session.commit()
        return True
