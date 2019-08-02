def register_blueprint(app):
    from views import auth_view, app_view
    from apps.admin.admin_api import admin_api
    from apps.tag.tag_api import tag_api
    from apps.asset.asset_api import asset_api
    from helpers.token_helpers import (validate_token_and_redirect,
                                       validate_token_before_request)

    app_view.before_request(validate_token_and_redirect)
    tag_api.before_request(validate_token_before_request)
    asset_api.before_request(validate_token_before_request)

    app.register_blueprint(auth_view)
    app.register_blueprint(app_view)
    app.register_blueprint(admin_api)
    app.register_blueprint(tag_api)
    app.register_blueprint(asset_api)
