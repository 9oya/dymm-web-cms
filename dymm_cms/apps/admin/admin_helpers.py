import datetime, pytz

from dymm_cms import b_crypt, db
from dymm_cms.models import Avatar
from .admin_forms import SignUpAdminForm, SignInAdminForm

db_session = db.session


class AdminHelper(object):
    @staticmethod
    def get_empty_admin_sign_up_form():
        form = SignUpAdminForm()
        return form

    @staticmethod
    def get_empty_admin_sign_in_form():
        form = SignInAdminForm()
        return form

    @staticmethod
    def is_admin_mail_duplicated(email) -> bool:
        admin_account = Avatar.query.filter(
            Avatar.email == email,
            Avatar.is_active == True).first()
        if admin_account is not None:
            return True
        return False

    @staticmethod
    def get_admin_avatar(email):
        admin = Avatar.query.filter(
            Avatar.email == email,
            Avatar.is_active == True).first()
        return admin

    @staticmethod
    def get_admin_info_json(admin: Avatar):
        expiration = (datetime.datetime.now(tz=pytz.utc)
                      + datetime.timedelta(minutes=30))
        admin_info = dict(
            email=admin.email,
            first_name=admin.first_name,
            last_name=admin.last_name,
            url_token_expiration=expiration.strftime("%Y-%m-%d %H:%M"))
        return admin_info

    @staticmethod
    def create_admin_avatar(form: SignUpAdminForm):
        password_hash = b_crypt.generate_password_hash(form.password.data).decode(
            'utf-8')
        admin = Avatar(email=form.email.data,
                       is_active=True,
                       is_admin=True,
                       is_blocked=False,
                       is_confirmed=True,
                       first_name=form.first_name.data,
                       last_name=form.last_name.data,
                       password_hash=password_hash,
                       profile_type=1)
        db_session.add(admin)
        db_session.commit()
        return admin
