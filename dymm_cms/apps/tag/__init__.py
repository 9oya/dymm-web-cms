from flask import Blueprint

from patterns import MessagePattern, RegularExpressionPattern

tag_api = Blueprint('tag_api', __name__, url_prefix='/api/tag')
_m = MessagePattern()
_r = RegularExpressionPattern()
