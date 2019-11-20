from wtforms import Form, StringField, validators, RadioField, SelectField, \
    IntegerField, HiddenField, PasswordField


class TagForm(Form):
    id = IntegerField(
        label="ID",
        validators=[validators.Optional(),
                    validators.NumberRange(min=0, max=None)],
        description="Autoincrement"
    )
    type_select = SelectField(
        label="Tag Type",
        validators=[validators.Optional()]
    )
    class1_select = SelectField(
        label="Class1 Select",
        validators=[validators.Optional()]
    )
    class1 = IntegerField(
        label="Class1",
        validators=[
            validators.DataRequired(),
            validators.NumberRange(min=0, max=None)
        ]
    )
    division1_select = SelectField(
        label="Division1 Select",
        validators=[validators.Optional()]
    )
    division1 = IntegerField(
        label="Division1",
        validators=[validators.Optional(),
                    validators.NumberRange(min=0, max=None)]
    )
    division2_select = SelectField(
        label="Division2 Select",
        validators=[validators.Optional()]
    )
    division2 = IntegerField(
        label="Division2",
        validators=[validators.Optional(),
                    validators.NumberRange(min=0, max=None)]
    )
    division3_select = SelectField(
        label="Division3 Select",
        validators=[validators.Optional()]
    )
    division3 = IntegerField(
        label="Division3",
        validators=[validators.Optional(),
                    validators.NumberRange(min=0, max=None)]
    )
    division4_select = SelectField(
        label="Division4 Select",
        validators=[validators.Optional()]
    )
    division4 = IntegerField(
        label="Division4",
        validators=[validators.Optional(),
                    validators.NumberRange(min=0, max=None)]
    )
    division5 = IntegerField(
        label="Division5",
        validators=[validators.Optional(),
                    validators.NumberRange(min=0, max=None)]
    )
    is_division_modified = RadioField(
        label="Is division modified?",
        choices=[('True', 'True'), ('False', 'False')],
        validators=[validators.DataRequired()]
    )
    is_active = RadioField(
        label="Is active?",
        choices=[('True', 'True'), ('False', 'False')],
        validators=[validators.DataRequired()]
    )
    eng_name = StringField(
        label="English name",
        validators=[validators.DataRequired("Please Enter English Name."),
                    validators.Length(min=2, max=100)]
    )
    kor_name = StringField(
        label="Korean name",
        validators=[validators.Optional(),
                    validators.Length(min=0, max=100)]
    )
    jpn_name = StringField(
        label="Japanese name",
        validators=[validators.Optional(),
                    validators.Length(min=0, max=100)]
    )
    delete_key = PasswordField(
        label="Delete key",
        validators=[validators.Optional(),
                    validators.Length(min=0, max=50)]
    )


class TagSortForm(Form):
    sort_select = SelectField(
        label="Sort type select",
        choices=[
            ('eng', 'Eng'), ('kor', 'Kor'), ('jpn', 'Jpn'), ('priority', 'Priority')
        ],
        validators=[validators.Optional()]
    )
    delete_key2 = PasswordField(
        label="Delete key",
        validators=[validators.Optional(),
                    validators.Length(min=0, max=50)],
        description="Delete key"
    )
