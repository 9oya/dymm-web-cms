from wtforms import validators, Form, StringField, PasswordField


class SignInAdminForm(Form):
    email = StringField(label="Email", validators=[
        validators.DataRequired('Please Enter Mail Address'),
        validators.Length(min=5)
    ])
    password = PasswordField(label="Password", validators=[
        validators.DataRequired('Please Enter Password'),
        validators.Length(min=8, max=50)
    ])


class SignUpAdminForm(Form):
    first_name = StringField(label="First Name", validators=[
        validators.DataRequired('Please Enter First Name'),
        validators.Length(min=2)
    ])
    last_name = StringField(label="Last Name", validators=[
        validators.DataRequired('Please Enter Last Name'),
        validators.Length(min=2)
    ])
    email = StringField(label="Mail Address", validators=[
        validators.DataRequired('Please Enter Mail Address'),
        validators.Length(min=5)
    ])
    password = PasswordField(label="Password", validators=[
        validators.DataRequired('Please Enter Password'),
        validators.Length(min=8, max=50)
    ])
    password_confirm = PasswordField(label="Confirm Password", validators=[
        validators.DataRequired('Please Enter Confirmation Password'),
        validators.Length(min=8, max=50)
    ])
    master_key = PasswordField(label="==MASTER KEY==", validators=[
        validators.DataRequired('Please Enter Master Key'),
        validators.Length(min=8, max=50)
    ])
