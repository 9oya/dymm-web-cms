from wtforms import Form, StringField, validators, RadioField, SelectField, \
    IntegerField, HiddenField, PasswordField


class AssetDirForm(Form):
    dir_select = SelectField(
        validators=[validators.Optional()]
    )
    path_select = SelectField(
        validators=[validators.Optional()]
    )
