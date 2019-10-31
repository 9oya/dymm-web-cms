from sqlalchemy import text

from dymm_cms import db, b_crypt
from dymm_cms.models import Avatar
from dymm_cms.helpers.string_helpers import str_to_bool, str_to_none
from .avatar_forms import AvatarForm

db_session = db.session


class AvatarHelper(object):

    # GET methods
    # -------------------------------------------------------------------------
    @staticmethod
    def get_a_avatar(avatar_id):
        avatar = Avatar.query.filter(
            Avatar.id == avatar_id
        ).first()
        return avatar

    @staticmethod
    def get_avatars(sort_type, page=None, per_page=40):
        if sort_type == 'date':
            avatars = Avatar.query.filter().order_by(
                Avatar.created_timestamp.desc()
            ).paginate(page, per_page, False)
            return avatars
        elif sort_type == 'email':
            avatars = Avatar.query.filter().order_by(
                Avatar.email
            ).paginate(page, per_page, False).items
            return avatars
        else:
            return False

    @staticmethod
    def get_filled_avatar_form(avatar: Avatar):
        form = AvatarForm()
        form.is_active.data = str(avatar.is_active)
        form.is_admin.data = str(avatar.is_admin)
        form.is_blocked.data = str(avatar.is_blocked)
        form.is_confirmed.data = str(avatar.is_confirmed)
        form.first_name.data = avatar.first_name
        form.last_name.data = avatar.last_name
        form.email.data = avatar.email
        form.created_timestamp.data = avatar.created_timestamp
        form.created_timestamp.render_kw = {'disabled': True}
        form.modified_timestamp.data = avatar.modified_timestamp
        form.modified_timestamp.render_kw = {'disabled': True}
        return form

    # Create methods
    # -------------------------------------------------------------------------
    @staticmethod
    def create_avatars_w_dicts(dicts):
        cnt = 0
        for _dict in dicts:
            password_hash = b_crypt.generate_password_hash(
                _dict['password']).decode('utf-8')
            avatar = Avatar(
                is_active=str_to_bool(_dict.get('is_active', True)),
                is_admin=str_to_bool(_dict.get('is_admin', True)),
                is_blocked=str_to_bool(_dict.get('is_blocked', True)),
                is_confirmed=str_to_bool(_dict.get('is_confirmed', True)),
                email=str_to_none(_dict.get('email', None)),
                password_hash=password_hash,
                first_name=str_to_none(_dict.get('first_name', None)),
                last_name=str_to_none(_dict.get('last_name', None)),
                color_code=str_to_none(_dict.get('color_code', None))
            )
            db_session.add(avatar)
            db_session.commit()
            cnt += 1
        return cnt

    # UPDATE methods
    # -------------------------------------------------------------------------
    @staticmethod
    def update_avatars_w_dicts(dicts):
        cnt = 0
        for _dict in dicts:
            avatar = AvatarHelper.get_a_avatar(_dict.get('id', None))
            avatar.is_active = str_to_bool(_dict.get('is_active'))
            avatar.is_admin = str_to_bool(_dict.get('is_admin'))
            avatar.is_blocked = str_to_bool(_dict.get('is_blocked'))
            avatar.is_confirmed = str_to_bool(_dict.get('is_confirmed'))
            avatar.email = _dict.get('email', None)
            avatar.first_name = _dict.get('first_name', None)
            avatar.last_name = _dict.get('last_name', None)
            avatar.color_code = _dict.get('color_code')
            avatar.modified_timestamp = text("timezone('utc'::text, now())")
            db_session.commit()
            cnt += 1
        return cnt
    
    @staticmethod
    def update_a_avatar(avatar: Avatar, form: AvatarForm):
        avatar.is_active = str_to_bool(form.is_active.data)
        avatar.is_admin = str_to_bool(form.is_admin.data)
        avatar.is_blocked = str_to_bool(form.is_blocked.data)
        avatar.is_confirmed = str_to_bool(form.is_confirmed.data)
        avatar.first_name = form.first_name.data
        avatar.last_name = form.last_name.data
        avatar.email = form.email.data
        avatar.modified_timestamp = text("timezone('utc'::text, now())")
        db_session.commit()
        return True

    # Delete methods
    # -------------------------------------------------------------------------
    @staticmethod
    def delete_a_avatar(avatar):
        db_session.delete(avatar)
        db_session.commit()
        return True
