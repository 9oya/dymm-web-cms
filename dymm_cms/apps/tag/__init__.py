from flask import Blueprint

from dymm_cms.patterns import MsgPattern, RegExPattern

tag_api = Blueprint('tag_api', __name__, url_prefix='/api/tag')
_m = MsgPattern()
_r = RegExPattern()
