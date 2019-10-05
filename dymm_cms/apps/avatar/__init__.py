from flask import Blueprint

from dymm_cms.patterns import MsgPattern, RegExPattern

avatar_api = Blueprint('avatar_api', __name__, url_prefix='/api/avatar')
_m = MsgPattern()
_r = RegExPattern()
