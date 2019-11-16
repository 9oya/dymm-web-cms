from wtforms import Form, StringField, validators, RadioField, SelectField, \
    IntegerField, HiddenField, PasswordField


class AssetDirForm(Form):
    dir_select = SelectField(
        validators=[validators.Optional()]
    )
    path_select = SelectField(
        validators=[validators.Optional()]
    )
    delete_key = PasswordField(
        label="Delete key",
        validators=[validators.Optional(),
                    validators.Length(min=0, max=50)]
    )
