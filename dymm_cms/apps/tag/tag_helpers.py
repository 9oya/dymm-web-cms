from sqlalchemy import text

from dymm_cms import excel
from database import db_session
from models import Tag, TagSet
from patterns import TagType
from helpers.string_helpers import str_to_bool, str_to_none
from .tag_forms import TagForm


class TagHelper(object):
    # Generators
    # -------------------------------------------------------------------------
    @staticmethod
    def gen_tag_set_next_priority(super_id) -> int:
        tag_set = TagSet.query.filter(
            TagSet.super_id == super_id,
            TagSet.is_active == True,
            TagSet.priority != 0
        ).order_by(TagSet.priority).first()
        try:
            priority = tag_set.priority
        except AttributeError:
            return 1000
        return priority - 1

    # Validators
    # -------------------------------------------------------------------------
    @staticmethod
    def is_tag_duplicate(form):
        duplicated_tag = Tag.query.filter(
            Tag.class1 == form.class1.data,
            Tag.division1 == form.division1.data,
            Tag.division2 == form.division2.data,
            Tag.division3 == form.division3.data,
            Tag.division4 == form.division4.data,
            Tag.division5 == form.division4.data
        ).first()
        if duplicated_tag:
            return True
        return False

    # Getters
    # -------------------------------------------------------------------------
    @staticmethod
    def get_tags_file(tags, file_name, file_extension='xlsx'):
        columns = ['id', 'tag_type', 'is_active', 'has_set', 'eng_name',
                   'kor_name', 'jpn_name', 'class1', 'division1', 'division2',
                   'division3', 'division4', 'division5', 'has_low_div', 'has_icon']
        if file_extension == 'xlsx':
            excel_response = excel.make_response_from_query_sets(
                query_sets=tags, column_names=columns,
                file_type='xlsx', file_name=file_name)
        elif file_extension == 'csv':
            excel_response = excel.make_response_from_query_sets(
                query_sets=tags, column_names=columns,
                file_type='csv', file_name=file_name)
        else:
            return False
        return excel_response

    @staticmethod
    def get_tag_sets_file(tag_sets, file_name, file_extension='xlsx'):
        columns = ['id', 'super_id', 'sub_id', 'is_active', 'priority']
        if file_extension == 'xlsx':
            excel_response = excel.make_response_from_query_sets(
                query_sets=tag_sets, column_names=columns,
                file_type='xlsx', file_name=file_name)
        elif file_extension == 'csv':
            excel_response = excel.make_response_from_query_sets(
                query_sets=tag_sets, column_names=columns,
                file_type='csv', file_name=file_name)
        else:
            return False
        return excel_response

    @staticmethod
    def get_tag_type_choices():
        choices = list()
        choices.append(('0', '----'))
        tag_list = Tag.query.filter(
            Tag.class1 == 1,
            Tag.division1 != 0,
            Tag.division2 == 0,
            Tag.division3 == 0,
            Tag.division4 == 0,
            Tag.division5 == 0
        ).order_by(Tag.division1).all()
        for _tag in tag_list:
            value = str(_tag.id)
            name = value + ' ' + _tag.eng_name
            choice = (value, name)
            choices.append(choice)
        return choices

    @staticmethod
    def get_tag_class_choices():
        choices = list()
        choices.append(('0', '----'))
        tag_list = Tag.query.filter(
            Tag.class1 != 0,
            Tag.division1 == 0,
            Tag.division2 == 0,
            Tag.division3 == 0,
            Tag.division4 == 0,
            Tag.division5 == 0
        ).order_by(Tag.class1).all()
        for _tag in tag_list:
            value = str(_tag.class1)
            name = value + ' ' + _tag.eng_name
            choice = (value, name)
            choices.append(choice)
        return choices

    @staticmethod
    def get_tag_division_choices(tag, number):
        choices = list()
        choices.append(('0', '----'))
        if number == 1:
            tags = Tag.query.filter(
                Tag.class1 == tag.class1,
                Tag.division1 != 0,
                Tag.division2 == 0,
                Tag.division3 == 0,
                Tag.division4 == 0,
                Tag.division5 == 0,
            ).order_by(Tag.division1).all()
            for _tag in tags:
                value = str(_tag.division1)
                name = value + ' ' + _tag.eng_name
                choice = (value, name)
                choices.append(choice)
        elif number == 2:
            tags = Tag.query.filter(
                Tag.class1 == tag.class1,
                Tag.division1 == tag.division1,
                Tag.division2 != 0,
                Tag.division3 == 0,
                Tag.division4 == 0,
                Tag.division5 == 0,
            ).order_by(Tag.division2).all()
            for _tag in tags:
                value = str(_tag.division2)
                name = value + ' ' + _tag.eng_name
                choice = (value, name)
                choices.append(choice)
        elif number == 3:
            tags = Tag.query.filter(
                Tag.class1 == tag.class1,
                Tag.division1 == tag.division1,
                Tag.division2 == tag.division2,
                Tag.division3 != 0,
                Tag.division4 == 0,
                Tag.division5 == 0,
            ).order_by(Tag.division3).all()
            for _tag in tags:
                value = str(_tag.division3)
                name = value + ' ' + _tag.eng_name
                choice = (value, name)
                choices.append(choice)
        elif number == 4:
            tags = Tag.query.filter(
                Tag.class1 == tag.class1,
                Tag.division1 == tag.division1,
                Tag.division2 == tag.division2,
                Tag.division3 == tag.division3,
                Tag.division4 != 0,
                Tag.division5 == 0,
            ).order_by(Tag.division4).all()
            for _tag in tags:
                value = str(_tag.division4)
                name = value + ' ' + _tag.eng_name
                choice = (value, name)
                choices.append(choice)
        else:
            return False
        return choices

    @staticmethod
    def get_a_tag(tag_id):
        tag = Tag.query.filter(Tag.id == tag_id).first()
        return tag

    @staticmethod
    def get_initial_tags():
        tags = Tag.query.filter(
            Tag.division1 == 0
        ).order_by(Tag.class1).all()
        return tags

    @staticmethod
    def get_all_tags():
        tags = Tag.query.filter().order_by(
            Tag.class1,
            Tag.division1,
            Tag.division2,
            Tag.division3,
            Tag.division4,
            Tag.division5
        ).all()
        return tags

    @staticmethod
    def get_low_div_tags(tag_id=None, class1=None, division1=None,
                         division2=None, division3=None, division4=None):
        if tag_id:
            tag = TagHelper.get_a_tag(tag_id)
            if tag.division1 == 0:
                tags = Tag.query.filter(
                    Tag.class1 == tag.class1,
                    Tag.division1 != 0,
                    Tag.division2 == 0
                ).order_by(Tag.division1).all()
            elif tag.division2 == 0:
                tags = Tag.query.filter(
                    Tag.class1 == tag.class1,
                    Tag.division1 == tag.division1,
                    Tag.division2 != 0,
                    Tag.division3 == 0
                ).order_by(Tag.division2).all()
            elif tag.division3 == 0:
                tags = Tag.query.filter(
                    Tag.class1 == tag.class1,
                    Tag.division1 == tag.division1,
                    Tag.division2 == tag.division2,
                    Tag.division3 != 0,
                    Tag.division4 == 0
                ).order_by(Tag.division3).all()
            elif tag.division4 == 0:
                tags = Tag.query.filter(
                    Tag.class1 == tag.class1,
                    Tag.division1 == tag.division1,
                    Tag.division2 == tag.division2,
                    Tag.division3 == tag.division3,
                    Tag.division4 != 0,
                    Tag.division5 == 0
                ).order_by(Tag.division4).all()
            elif tag.division5 == 0:
                tags = Tag.query.filter(
                    Tag.class1 == tag.class1,
                    Tag.division1 == tag.division1,
                    Tag.division2 == tag.division2,
                    Tag.division3 == tag.division3,
                    Tag.division4 == tag.division4,
                    Tag.division5 != 0
                ).order_by(Tag.division5).all()
            else:
                return False
            return tags
        elif class1 is None:
            return False
        elif division1 is None:
            tags = Tag.query.filter(
                Tag.class1 == class1,
                Tag.division1 != 0,
                Tag.division2 == 0
            ).order_by(Tag.division1).all()
        elif division2 is None:
            tags = Tag.query.filter(
                Tag.class1 == class1,
                Tag.division1 == division1,
                Tag.division2 != 0,
                Tag.division3 == 0
            ).order_by(Tag.division2).all()
        elif division3 is None:
            tags = Tag.query.filter(
                Tag.class1 == class1,
                Tag.division1 == division1,
                Tag.division2 == division2,
                Tag.division3 != 0,
                Tag.division4 == 0
            ).order_by(Tag.division3).all()
        elif division4 is None:
            tags = Tag.query.filter(
                Tag.class1 == class1,
                Tag.division1 == division1,
                Tag.division2 == division2,
                Tag.division3 == division3,
                Tag.division4 != 0,
                Tag.division5 == 0
            ).order_by(Tag.division4).all()
        else:
            return False
        return tags

    @staticmethod
    def get_all_low_div_tags(tag_id):
        tag = TagHelper.get_a_tag(tag_id)
        if tag.division1 == 0:
            tags = Tag.query.filter(
                Tag.class1 == tag.class1,
                Tag.division1 != 0
            ).order_by(Tag.division1,
                       Tag.division2,
                       Tag.division3,
                       Tag.division4,
                       Tag.division5).all()
        elif tag.division2 == 0:
            tags = Tag.query.filter(
                Tag.class1 == tag.class1,
                Tag.division1 == tag.division1,
                Tag.division2 != 0
            ).order_by(Tag.division2,
                       Tag.division3,
                       Tag.division4,
                       Tag.division5).all()
        elif tag.division3 == 0:
            tags = Tag.query.filter(
                Tag.class1 == tag.class1,
                Tag.division1 == tag.division1,
                Tag.division2 == tag.division2,
                Tag.division3 != 0
            ).order_by(Tag.division3,
                       Tag.division4,
                       Tag.division5).all()
        elif tag.division4 == 0:
            tags = Tag.query.filter(
                Tag.class1 == tag.class1,
                Tag.division1 == tag.division1,
                Tag.division2 == tag.division2,
                Tag.division3 == tag.division3,
                Tag.division4 != 0
            ).order_by(Tag.division4,
                       Tag.division5).all()
        elif tag.division5 == 0:
            tags = Tag.query.filter(
                Tag.class1 == tag.class1,
                Tag.division1 == tag.division1,
                Tag.division2 == tag.division2,
                Tag.division3 == tag.division3,
                Tag.division4 == tag.division4,
                Tag.division5 != 0
            ).order_by(Tag.division5).all()
        else:
            return False
        return tags

    @staticmethod
    def get_specific_div_tags(tag: Tag, div_num):
        if div_num == 'div2':
            tags = Tag.query.filter(
                Tag.class1 == tag.class1,
                Tag.division2 != 0,
                Tag.division3 == 0,
                Tag.division4 == 0
            ).order_by(
                Tag.division1,
                Tag.division2
            ).all()
            return tags
        elif div_num == 'div3':
            tags = Tag.query.filter(
                Tag.class1 == tag.class1,
                Tag.division2 != 0,
                Tag.division3 != 0,
                Tag.division4 == 0
            ).order_by(
                Tag.division1,
                Tag.division2,
                Tag.division3
            ).all()
            return tags
        elif div_num == 'div4':
            tags = Tag.query.filter(
                Tag.class1 == tag.class1,
                Tag.division2 != 0,
                Tag.division3 != 0,
                Tag.division4 != 0,
                Tag.division5 == 0
            ).order_by(
                Tag.division1,
                Tag.division2,
                Tag.division3,
                Tag.division4
            ).all()
            return tags
        else:
            return False

    @staticmethod
    def get_tag_form_for_validate(request):
        form = TagForm(request.form)
        form.type_select.choices = TagHelper.get_tag_type_choices()
        form.class1_select.choices = TagHelper.get_tag_class_choices()
        form.division1_select.choices = [(str(form.division1_select.data), '')]
        form.division2_select.choices = [(str(form.division2_select.data), '')]
        form.division3_select.choices = [(str(form.division3_select.data), '')]
        form.division4_select.choices = [(str(form.division4_select.data), '')]
        return form

    @staticmethod
    def get_empty_tag_form():
        form = TagForm()
        form.id.render_kw = {'disabled': True}
        form.type_select.choices = TagHelper.get_tag_type_choices()
        form.class1_select.choices = TagHelper.get_tag_class_choices()
        form.division1_select.choices = [('0', '----')]
        form.division2_select.choices = [('0', '----')]
        form.division3_select.choices = [('0', '----')]
        form.division4_select.choices = [('0', '----')]
        form.division1.data = 0
        form.division2.data = 0
        form.division3.data = 0
        form.division4.data = 0
        form.division5.data = 0
        form.is_division_modified.data = 'False'
        form.is_division_modified.label = ''
        form.is_division_modified.render_kw = {'hidden': True}
        form.is_active.data = 'True'
        form.has_set.data = 'False'
        form.has_low_div.data = 'False'
        form.has_icon.data = 'False'
        form.delete_key.label = ''
        form.delete_key.render_kw = {'hidden': True}
        return form

    @staticmethod
    def get_filled_tag_form(tag):
        form = TagForm()
        form.id.data = tag.id
        form.id.render_kw = {'disabled': True}
        form.type_select.choices = TagHelper.get_tag_type_choices()
        form.type_select.data = str(tag.tag_type)

        form.class1_select.choices = TagHelper.get_tag_class_choices()
        form.class1_select.data = str(tag.class1)
        form.class1.data = tag.class1
        form.division1_select.choices = (
            TagHelper.get_tag_division_choices(tag, 1)
        )
        form.division1_select.data = str(tag.division1)
        form.division1.data = tag.division1
        form.division2_select.choices = (
            TagHelper.get_tag_division_choices(tag, 2)
        )
        form.division2_select.data = str(tag.division2)
        form.division2.data = tag.division2
        form.division3_select.choices = (
            TagHelper.get_tag_division_choices(tag, 3)
        )
        form.division3_select.data = str(tag.division3)
        form.division3.data = tag.division3
        form.division4_select.choices = (
            TagHelper.get_tag_division_choices(tag, 4)
        )
        form.division4_select.data = str(tag.division4)
        form.division4.data = tag.division4
        form.division5.data = tag.division5
        form.is_division_modified.data = 'False'

        form.is_active.data = str(tag.is_active)
        form.has_set.data = str(tag.has_set)
        form.has_low_div.data = str(tag.has_low_div)
        form.has_icon.data = str(tag.has_icon)
        form.eng_name.data = tag.eng_name
        form.kor_name.data = tag.kor_name
        form.jpn_name.data = tag.jpn_name
        return form

    @staticmethod
    def get_a_tag_set(tag_set_id=None, super_id=None, sub_id=None):
        if super_id is None:
            tag_set = TagSet.query.filter(
                TagSet.id == tag_set_id
            ).first()
        else:
            tag_set = TagSet.query.filter(
                TagSet.super_id == super_id,
                TagSet.sub_id == sub_id
            ).first()
        return tag_set

    @staticmethod
    def get_tag_sets(super_id, sort_type='eng'):
        if sort_type == 'eng':
            tag_set_list = db_session.query(TagSet). \
                join(TagSet.sub). \
                filter(TagSet.super_id == super_id). \
                order_by(Tag.eng_name).all()
        elif sort_type == 'kor':
            tag_set_list = db_session.query(TagSet). \
                join(TagSet.sub). \
                filter(TagSet.super_id == super_id). \
                order_by(Tag.kor_name).all()
        elif sort_type == 'jpn':
            tag_set_list = db_session.query(TagSet). \
                join(TagSet.sub). \
                filter(TagSet.super_id == super_id). \
                order_by(Tag.jpn_name).all()
        elif sort_type == 'priority':
            tag_set_list = db_session.query(TagSet). \
                filter(TagSet.super_id == super_id). \
                order_by(TagSet.priority.desc()).all()
        else:
            return False
        return tag_set_list

    @staticmethod
    def get_top_priority_from_tag_set(super_id):
        tag_set = TagSet.query.filter(
            TagSet.super_id == super_id,
            TagSet.priority != None
        ).order_by(TagSet.priority.desc()).first()
        try:
            return tag_set.priority
        except AttributeError:
            return None

    @staticmethod
    def get_next_priority_from_tag_set(super_id):
        tag_set = TagSet.query.filter(
            TagSet.super_id == super_id,
            TagSet.priority != 0
        ).order_by(TagSet.priority).first()
        try:
            return tag_set.priority
        except AttributeError:
            return None

    # Create methods
    # -------------------------------------------------------------------------
    @staticmethod
    def create_tags_w_dicts(dicts):
        cnt = 0
        for _dict in dicts:
            tag = Tag(
                id=str_to_none(_dict.get('id', None)),
                tag_type=str_to_none(_dict.get('tag_type', None)),
                is_active=str_to_bool(_dict.get('is_active', True)),
                has_set=str_to_bool(_dict.get('has_set', False)),
                eng_name=str_to_none(_dict.get('eng_name', None)),
                kor_name=str_to_none(_dict.get('kor_name', None)),
                jpn_name=str_to_none(_dict.get('jpn_name', None)),
                class1=_dict.get('class1'),
                division1=_dict.get('division1'),
                division2=_dict.get('division2'),
                division3=_dict.get('division3'),
                division4=_dict.get('division4'),
                division5=_dict.get('division5'),
                has_low_div=str_to_bool(_dict.get('has_low_div')),
                has_icon=str_to_bool(_dict.get('has_icon', False))
            )
            db_session.add(tag)
            db_session.commit()
            cnt += 1
        return cnt

    @staticmethod
    def create_tag_sets_w_dicts(dicts, option):
        cnt = 0
        if option == 'gen-set-low':
            for _dict in dicts:
                tag = TagHelper.get_a_tag(_dict.get('id', None))
                low_tags = TagHelper.get_low_div_tags(tag_id=tag.id)
                if len(low_tags) <= 0:
                    tag.has_set = False
                    tag.has_low_div = False
                    db_session.commit()
                    continue
                for low_tag in low_tags:
                    priority = TagHelper.gen_tag_set_next_priority(super_id=tag.id)
                    TagHelper.create_a_tag_set(super_id=tag.id,
                                               sub_id=low_tag.id,
                                               priority=priority)
                cnt += 1
            return cnt
        elif option == 'gen-set-eng':
            for _dict in dicts:
                sub_tag = Tag.query.filter(
                    Tag.eng_name == _dict.get('eng_name')
                ).first()
                try:
                    tag = TagSet(
                        super_id=str_to_none(_dict.get('super_id')),
                        sub_id=sub_tag.id,
                        is_active=str_to_bool(_dict.get('is_active', True))
                    )
                    db_session.add(tag)
                    db_session.commit()
                    cnt += 1
                except AttributeError:
                    print(_dict.get('eng_name'))
            return cnt
        else:
            return False

    @staticmethod
    def create_a_tag(form: TagForm):
        tag = Tag(tag_type=form.type_select.data,
                  class1=form.class1.data,
                  division1=form.division1.data,
                  division2=form.division2.data,
                  division3=form.division3.data,
                  division4=form.division4.data,
                  division5=form.division5.data,
                  is_active=str_to_bool(form.is_active.data),
                  has_set=str_to_bool(form.has_set.data),
                  has_low_div=str_to_bool(form.has_low_div.data),
                  has_icon=str_to_bool(form.has_icon),
                  eng_name=form.eng_name.data,
                  kor_name=form.kor_name.data,
                  jpn_name=form.jpn_name.data)
        db_session.add(tag)
        db_session.commit()
        return tag.eng_name

    @staticmethod
    def create_a_tag_set(super_id, sub_id, priority):
        tag_set = TagSet(super_id=super_id,
                         sub_id=sub_id,
                         is_active=True,
                         priority=priority)
        db_session.add(tag_set)
        db_session.commit()
        return True

    # Update methods
    # -------------------------------------------------------------------------
    @staticmethod
    def update_tag_sets_w_dicts(dicts):
        cnt = 0
        for _dict in dicts:
            tag_set = db_session.query(
                TagSet
            ).join(
                TagSet.sub
            ).filter(
                Tag.eng_name == _dict.get('eng_name', None)
            ).first()
            tag_set.super_id = _dict.get('super_id')
            tag_set.priority = _dict.get('priority', None)
            db_session.commit()
            cnt += 1
        return cnt

    @staticmethod
    def update_tags_w_dicts(dicts):
        cnt = 0
        for _dict in dicts:
            tag = TagHelper.get_a_tag(_dict.get('id', None))
            tag.tag_type = str_to_none(_dict.get('tag_type', None))
            tag.is_active = str_to_bool(_dict.get('is_active'))
            tag.has_set = str_to_bool(_dict.get('has_set'))
            tag.eng_name = _dict.get('eng_name', None)
            tag.kor_name = _dict.get('kor_name', None)
            tag.jpn_name = _dict.get('jpn_name', None)
            tag.class1 = _dict.get('class1')
            tag.division1 = _dict.get('division1')
            tag.division2 = _dict.get('division2')
            tag.division3 = _dict.get('division3')
            tag.division4 = _dict.get('division4')
            tag.division5 = _dict.get('division5')
            tag.has_low_div = str_to_bool(_dict.get('has_low_div'))
            tag.has_icon = str_to_bool(_dict.get('has_icon', None))
            db_session.commit()
            cnt += 1
        return cnt

    @staticmethod
    def update_a_tag(tag: Tag, form: TagForm):
        tag.tag_type = form.type_select.data
        tag.is_active = str_to_bool(form.is_active.data)
        tag.has_set = str_to_bool(form.has_set.data)
        tag.class1 = form.class1.data
        tag.division1 = form.division1.data
        tag.division2 = form.division2.data
        tag.division3 = form.division3.data
        tag.division4 = form.division4.data
        tag.division5 = form.division5.data
        tag.has_low_div = str_to_bool(form.has_low_div.data)
        tag.has_icon = str_to_bool(form.has_icon.data)
        tag.eng_name = form.eng_name.data
        tag.kor_name = form.kor_name.data
        tag.jpn_name = form.jpn_name.data
        db_session.commit()
        return tag.eng_name

    @staticmethod
    def update_tag_divisions(tag, form):
        if form.division1.data == 0:
            db_session.query(Tag).filter(
                Tag.class1 == tag.class1
            ).update({"class1": form.class1.data})
            db_session.commit()
        elif form.division2.data == 0:
            db_session.query(Tag).filter(
                Tag.class1 == tag.class1,
                Tag.division1 == tag.division1
            ).update({"class1": form.class1.data,
                      "division1": form.division1.data})
            db_session.commit()
        elif form.division3.data == 0:
            db_session.query(Tag).filter(
                Tag.class1 == tag.class1,
                Tag.division1 == tag.division1,
                Tag.division2 == tag.division2
            ).update({"class1": form.class1.data,
                      "division1": form.division1.data,
                      "division2": form.division2.data})
            db_session.commit()
        elif form.division4.data == 0:
            db_session.query(Tag).filter(
                Tag.class1 == tag.class1,
                Tag.division1 == tag.division1,
                Tag.division2 == tag.division2,
                Tag.division3 == tag.division3
            ).update({"class1": form.class1.data,
                      "division1": form.division1.data,
                      "division2": form.division2.data,
                      "division3": form.division3.data})
            db_session.commit()
        elif form.division5.data == 0:
            db_session.query(Tag).filter(
                Tag.class1 == tag.class1,
                Tag.division1 == tag.division1,
                Tag.division2 == tag.division2,
                Tag.division3 == tag.division3,
                Tag.division4 == tag.division4
            ).update({"class1": form.class1.data,
                      "division1": form.division1.data,
                      "division2": form.division2.data,
                      "division3": form.division3.data,
                      "division4": form.division4.data})
            db_session.commit()
        return True

    @staticmethod
    def update_a_tag_set(tag_set, form):
        tag_set.is_active = str_to_bool(form.is_active.data)
        tag_set.priority = form.priority.data
        db_session.commit()
        return tag_set.tag.eng_name

    @staticmethod
    def update_a_tag_set_priority(tag_set, priority):
        tag_set.priority = priority
        db_session.commit()
        return True

    @staticmethod
    def update_tag_has_icon(tag: Tag):
        if tag.has_icon:
            tag.has_icon = False
        else:
            tag.has_icon = True
        db_session.commit()
        return True

    @staticmethod
    def update_a_tag_set_w_target(tag_set: TagSet, target, value):
        if target == "is-active":
            if tag_set.is_active:
                tag_set.is_active = False
            else:
                tag_set.is_active = True
        else:
            return False
        tag_set.modified_timestamp = text("timezone('utc'::text, now())")
        db_session.commit()
        return True

    # Delete methods
    # -------------------------------------------------------------------------
    @staticmethod
    def delete_a_tag(tag):
        db_session.delete(tag)
        db_session.commit()
        return True

    @staticmethod
    def delete_a_tag_set(tag_set):
        db_session.delete(tag_set)
        db_session.commit()
        return True

    @staticmethod
    def delete_tag_sets(tag_sets):
        cnt = 0
        for tag_set in tag_sets:
            TagHelper.delete_a_tag_set(tag_set)
            cnt += 1
        return cnt

