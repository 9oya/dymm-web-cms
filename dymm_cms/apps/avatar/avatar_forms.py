from wtforms import Form, StringField, validators, RadioField, SelectField, \
    IntegerField, HiddenField, PasswordField, TextAreaField


class AvatarForm(Form):
    is_active = RadioField(
        label="Is active?",
        choices=[('True', 'True'), ('False', 'False')],
        validators=[validators.DataRequired()]
    )
    is_admin = RadioField(
        label="Is admin?",
        choices=[('True', 'True'), ('False', 'False')],
        validators=[validators.DataRequired()]
    )
    is_blocked = RadioField(
        label="Is blocked?",
        choices=[('True', 'True'), ('False', 'False')],
        validators=[validators.DataRequired()]
    )
    is_confirmed = RadioField(
        label="Is confirmed?",
        choices=[('True', 'True'), ('False', 'False')],
        validators=[validators.DataRequired()]
    )
    first_name = StringField(
        label="First name",
        validators=[validators.Length(min=2, max=100)]
    )
    last_name = StringField(
        label="Last name",
        validators=[validators.Length(min=2, max=100)]
    )
    email = StringField(
        label="Email address",
        validators=[validators.DataRequired("Please Enter Email address."),
                    validators.Length(min=2, max=100)]
    )
    created_timestamp = StringField(
        label="Created timestamp",
        validators=[validators.Length(min=2, max=200)]
    )
    modified_timestamp = StringField(
        label="Modified timestamp",
        validators=[validators.Optional(),
                    validators.Length(min=0, max=200)]
    )
    delete_key = PasswordField(
        label="Delete key",
        validators=[validators.Optional(),
                    validators.Length(min=0, max=50)]
    )
