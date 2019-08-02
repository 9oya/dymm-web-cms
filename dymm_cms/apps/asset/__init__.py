from flask import Blueprint

from patterns import MessagePattern, RegularExpressionPattern, URIPattern

asset_api = Blueprint('asset_api', __name__, url_prefix='/api/asset')
_m = MessagePattern()
_r = RegularExpressionPattern()
_u = URIPattern()
