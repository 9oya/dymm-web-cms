from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import flask_excel as excel

from blueprint import register_blueprint

app = Flask('dymm_cms')
app.config.from_object('dymm_cms.config.ProductionConfig')
# app.config.from_object('dymm_cms.config.DevelopmentConfig')

db = SQLAlchemy(app)
b_crypt = Bcrypt(app)
mail = Mail(app)
register_blueprint(app)
excel.init_excel(app)


# if __name__ == "__main__":
#     context = ('cert.crt', 'key.key')
#     app.run(host='127.0.0.1',
#             port=5000,
#             ssl_context=context,
#             threaded=True,
#             debug=True)
