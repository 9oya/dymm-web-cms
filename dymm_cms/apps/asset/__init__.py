from flask import Blueprint

from dymm_cms.patterns import MsgPattern, RegExPattern, URIPattern

asset_api = Blueprint('asset_api', __name__, url_prefix='/api/asset')
_m = MsgPattern()
_r = RegExPattern()
_u = URIPattern()
