import random, re

from sqlalchemy import text, func

from dymm_cms import db, b_crypt, excel
from dymm_cms.models import Avatar, ProfileTag, Tag, TagSet
from dymm_cms.helpers.string_helpers import str_to_bool, str_to_none
from dymm_cms.patterns import TagId
from .avatar_forms import AvatarForm

db_session = db.session


class AvatarHelper(object):

    # Generators
    # -------------------------------------------------------------------------
    @staticmethod
    def gen_random_profile_color() -> int:
        profile_colors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        random.shuffle(profile_colors)
        random.shuffle(profile_colors)
        return profile_colors[5]

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

    @staticmethod
    def get_tag_sets(super_id: int, sort_type, page=None, per_page=40):
        if sort_type == 'eng':
            if page:
                tag_sets = TagSet.query.join(TagSet.sub).filter(
                    TagSet.super_id == super_id,
                    TagSet.is_active == True
                ).order_by(
                    Tag.eng_name
                ).paginate(page, per_page, False).items
                return tag_sets
            tag_sets = db_session.query(TagSet).join(TagSet.sub).filter(
                TagSet.super_id == super_id,
                TagSet.is_active == True
            ).order_by(Tag.eng_name).all()
        elif sort_type == 'kor':
            if page:
                tag_sets = TagSet.query.join(TagSet.sub).filter(
                    TagSet.super_id == super_id,
                    TagSet.is_active == True
                ).order_by(
                    Tag.kor_name
                ).paginate(page, per_page, False).items
                return tag_sets
            tag_sets = db_session.query(TagSet).join(TagSet.sub).filter(
                TagSet.super_id == super_id,
                TagSet.is_active == True
            ).order_by(Tag.kor_name).all()
        elif sort_type == 'jpn':
            if page:
                tag_sets = TagSet.query.join(TagSet.sub).filter(
                    TagSet.super_id == super_id,
                    TagSet.is_active == True
                ).order_by(
                    Tag.jpn_name
                ).paginate(page, per_page, False).items
                return tag_sets
            tag_sets = db_session.query(TagSet).join(TagSet.sub).filter(
                TagSet.super_id == super_id,
                TagSet.is_active == True
            ).order_by(Tag.jpn_name).all()
        elif sort_type == 'priority':
            if page:
                tag_sets = db_session.query(TagSet).filter(
                    TagSet.super_id == super_id,
                    TagSet.is_active == True
                ).order_by(
                    TagSet.priority.desc()
                ).paginate(page, per_page, False).items
                return tag_sets
            tag_sets = db_session.query(TagSet).filter(
                TagSet.super_id == super_id,
                TagSet.is_active == True
            ).order_by(TagSet.priority.desc()).all()
        else:
            return False
        return tag_sets

    @staticmethod
    def get_avatars_file(avatars, file_name, file_extension='xlsx'):
        columns = ['id', 'is_active', 'is_blocked', 'is_confirmed', 'email',
                   'first_name', 'last_name', 'created_timestamp',
                   'modified_timestamp']
        if file_extension == 'xlsx':
            excel_response = excel.make_response_from_query_sets(
                query_sets=avatars, column_names=columns,
                file_type='xlsx', file_name=file_name)
        elif file_extension == 'csv':
            excel_response = excel.make_response_from_query_sets(
                query_sets=avatars, column_names=columns,
                file_type='csv', file_name=file_name)
        else:
            return False
        return excel_response

    @staticmethod
    def get_avatars_by_keyword(keyword: str, option):
        if option == 'first-name':
            avatars = Avatar.query.filter(
                Avatar.first_name.ilike('{0}%'.format(keyword))
            ).order_by(
                Avatar.created_timestamp.desc()
            ).all()
        elif option == 'last-name':
            avatars = Avatar.query.filter(
                Avatar.last_name.ilike('{0}%'.format(keyword))
            ).order_by(
                Avatar.created_timestamp.desc()
            ).all()
        elif option == 'email-addr':
            avatars = Avatar.query.filter(
                Avatar.email.ilike('{0}%'.format(keyword))
            ).order_by(
                Avatar.created_timestamp.desc()
            ).all()
        else:
            return False
        return avatars

    @staticmethod
    def get_avatars_by_selected_option(option):
        if option == 'admin':
            avatars = Avatar.query.filter(
                Avatar.is_admin == True
            ).order_by(
                Avatar.created_timestamp.desc()
            ).all()
        elif option == 'inactive':
            avatars = Avatar.query.filter(
                Avatar.is_active == False
            ).order_by(
                Avatar.created_timestamp.desc()
            ).all()
        elif option == 'block':
            avatars = Avatar.query.filter(
                Avatar.is_blocked == True
            ).order_by(
                Avatar.created_timestamp.desc()
            ).all()
        elif option == 'unconf':
            avatars = Avatar.query.filter(
                Avatar.is_confirmed == False
            ).order_by(
                Avatar.created_timestamp.desc()
            ).all()
        else:
            return False
        return avatars

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
                color_code=AvatarHelper.gen_random_profile_color()
            )
            db_session.add(avatar)
            db_session.commit()
            AvatarHelper.create_def_profile_tags(avatar.id, TagId.eng)
            cnt += 1
        return cnt

    @staticmethod
    def create_profile_tag(avatar_id, super_tag_id, sub_tag_id, is_selected):
        profile_tag = ProfileTag(
            avatar_id=avatar_id,
            super_tag_id=super_tag_id,
            sub_tag_id=sub_tag_id,
            is_active=True,
            is_selected=is_selected
        )
        db_session.add(profile_tag)
        db_session.commit()
        return profile_tag

    @staticmethod
    def create_def_profile_tags(avatar_id, language_id):
        tag_sets = AvatarHelper.get_tag_sets(super_id=TagId.profile,
                                             sort_type='priority')
        for tag_set in tag_sets:
            if tag_set.sub_id == TagId.language:
                AvatarHelper.create_profile_tag(avatar_id=avatar_id,
                                                super_tag_id=tag_set.sub_id,
                                                sub_tag_id=language_id,
                                                is_selected=True)
                continue
            elif tag_set.sub_id == TagId.theme:
                AvatarHelper.create_profile_tag(avatar_id=avatar_id,
                                                super_tag_id=tag_set.sub_id,
                                                sub_tag_id=TagId.light,
                                                is_selected=True)
                continue
            else:
                AvatarHelper.create_profile_tag(avatar_id=avatar_id,
                                                super_tag_id=tag_set.sub_id,
                                                sub_tag_id=tag_set.sub_id,
                                                is_selected=False)
        return True

    # UPDATE methods
    # -------------------------------------------------------------------------
    @staticmethod
    def update_avatars_w_dicts(dicts):
        cnt = 0
        for _dict in dicts:
            avatar = AvatarHelper.get_a_avatar(_dict.get('id', None))
            avatar.is_active = str_to_bool(_dict.get('is_active'))
            avatar.is_blocked = str_to_bool(_dict.get('is_blocked'))
            avatar.is_confirmed = str_to_bool(_dict.get('is_confirmed'))
            avatar.email = _dict.get('email', None)
            avatar.first_name = _dict.get('first_name', None)
            avatar.last_name = _dict.get('last_name', None)
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

    @staticmethod
    def delete_avatars_w_dicts(dicts):
        cnt = 0
        for _dict in dicts:
            avatar = AvatarHelper.get_a_avatar(_dict.get('id', None))
            AvatarHelper.delete_a_avatar(avatar)
            cnt += 1
        return cnt
