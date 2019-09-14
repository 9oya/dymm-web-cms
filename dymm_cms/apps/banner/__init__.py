from flask import Blueprint

from dymm_cms.patterns import MsgPattern, RegExPattern

banner_api = Blueprint('banner_api', __name__, url_prefix='/api/banner')
_m = MsgPattern()
_r = RegExPattern()
