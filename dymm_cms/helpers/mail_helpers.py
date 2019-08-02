from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

from dymm_cms import app


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_mail_token(token, expiration=36000):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration)
    except:
        raise ValueError
    return email


def send_mail(mail_address):
    # Generate email-conf-token and send to user.email
    message = Message()
    # TODO: message.add_recipient(mail_address) - Change below line with this.
    # message.add_recipient('eslee004@gmail.com')
    # mail_token = generate_confirmation_token(mail_address)
    # uri = ptrn.URI.HOST + ptrn.URI.USER_MAIL + '/conf/' + mail_token
    # message.html = render_template('mail_conf_msg.html', uri=uri)
    # message.subject = "Confirm your account on Flava"
    # mail.send(message)
