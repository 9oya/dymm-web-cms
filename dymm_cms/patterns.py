class URIPattern:
    HOST = 'http://127.0.0.1:5000'
    # HOST = 'https://flava-api-test4.herokuapp.com'
    ASSET = 'dymm_cms/static/asset'


class ErrorPattern:
    EXPR_TOKEN = 'expired-token'


class MsgPattern:
    BAD_PARAM = 'Bad request, Wrong pattern parameters has been passed.'
    EMPTY_PARAM = "Bad request, Parameter {} is Empty."
    EXPIRED = 'Forbidden, Expired token has been passed.'
    DUPLICATED = 'Forbidden, Duplicated {} has been passed.'
    NONEXISTENT = 'Forbidden, Can\' find matching id{}.'
    INCORRECT = 'Forbidden, That {} is incorrect.'
    INVALID = 'Forbidden, Invalid {} has been passed.'
    OK_POST = 'Ok, The {} has been posted.'
    OK_PUT = 'Ok, The {} has been updated.'
    OK_DELETE = 'Ok, The {} has been deleted.'
    OK_IMPORT = 'Ok, The {} {} data has been inserted.'
    OK_UPLOAD = 'Ok, The {} {} data has been uploaded.'
    OK_MODIFY = 'Ok, The {} {} data has been modified.'
    UN_AUTH = 'Unauthorized, Wrong {} has been passed.'


class RegExPattern:
    NUMERIC_ID = '^[0-9]+$'


class TagType:
    activity = 7
    condition = 8
    drug = 9
    food = 10
    character = 11
    category = 12
    bookmark = 13
    diary = 14
    history = 15


class TagId:
    act = 2
    cond = 3
    drug = 4
    food = 5
    profile = 19
    language = 20
    supp = 1040
    date_of_birth = 23
    password = 14641
    theme = 14645
    light = 14646
    eng = 30
    kor = 35
    male = 36
    female = 37
    gender = 22


class AvatarType:
    email = 1
    facebook = 2
    google = 3
