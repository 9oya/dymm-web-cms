from wtforms import Form, StringField, validators, RadioField, SelectField, \
    IntegerField, HiddenField, PasswordField, TextAreaField


class BannerForm(Form):
    id = IntegerField(
        label="ID",
        validators=[validators.Optional(),
                    validators.NumberRange(min=0, max=None)],
        description="Autoincrement"
    )
    score = IntegerField(
        label="Score",
        validators=[validators.Optional(),
                    validators.NumberRange(min=0, max=None)]
    )
    is_active = RadioField(
        label="Is active?",
        choices=[('True', 'True'), ('False', 'False')],
        validators=[validators.DataRequired()]
    )
    img_name = StringField(
        label="Image name",
        validators=[validators.Optional(),
                    validators.Length(min=2, max=100)]
    )
    txt_color = StringField(
        label="Text color",
        validators=[validators.Optional(),
                    validators.Length(min=2, max=100)]
    )
    bg_color = StringField(
        label="Background color",
        validators=[validators.Optional(),
                    validators.Length(min=2, max=100)]
    )
    eng_title = StringField(
        label="English title",
        validators=[validators.DataRequired("Please enter english title."),
                    validators.Length(min=2, max=200)]
    )
    kor_title = StringField(
        label="Korean title",
        validators=[validators.Optional(),
                    validators.Length(min=0, max=200)]
    )
    jpn_title = StringField(
        label="Japanese title",
        validators=[validators.Optional(),
                    validators.Length(min=0, max=200)]
    )
    eng_subtitle = TextAreaField(
        label="English subtitle",
        validators=[validators.Optional(),
                    validators.Length(min=2, max=300)]
    )
    kor_subtitle = TextAreaField(
        label="Korean subtitle",
        validators=[validators.Optional(),
                    validators.Length(min=0, max=300)]
    )
    jpn_subtitle = TextAreaField(
        label="Japanese subtitle",
        validators=[validators.Optional(),
                    validators.Length(min=0, max=300)]
    )
    delete_key = PasswordField(
        label="Delete key",
        validators=[validators.Optional(),
                    validators.Length(min=0, max=50)]
    )
