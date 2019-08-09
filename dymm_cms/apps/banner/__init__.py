from flask import Blueprint

from patterns import MessagePattern, RegularExpressionPattern

banner_api = Blueprint('banner_api', __name__, url_prefix='/api/banner')
_m = MessagePattern()
_r = RegularExpressionPattern()
