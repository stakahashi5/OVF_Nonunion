from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, SubmitField
from wtforms.validators import InputRequired, AnyOf, NumberRange, Optional

class OVFForm(FlaskForm):
    Age = IntegerField("Age (years)", validators=[Optional(), NumberRange(min=0)])
    sex = RadioField(
        "Sex",
        coerce=int,
        choices=[(2, "Female"), (1, "Male")],
        default=1,
        validators=[InputRequired(), AnyOf([2, 1])],
    )
    Level3 = RadioField(
        "Level",
        coerce=int,
        choices=[(3, "Lumbar"), (2, "Thoracolumbar"), (1, "Thoracic")],
        default=1,
        validators=[InputRequired(), AnyOf([3, 2, 1])],
    )
    MRIday = IntegerField("MRIday (0-100)", validators=[Optional(), NumberRange(min=0, max=100)])
    VAS0 = IntegerField("VAS (0-10)", validators=[Optional(), NumberRange(min=0, max=10)])
    Poste02 = RadioField(
        "Posterior wall injury",
        coerce=int,
        choices=[(1, "Yes"), (0, "No")],
        default=1,
        validators=[InputRequired(), AnyOf([1, 0])],
    )
    KypFle0 = IntegerField(
        "Kyphotic Angle (degrees)", validators=[Optional(), NumberRange(min=-30)]
    )
    T203 = RadioField(
        "MRI T2",
        coerce=int,
        choices=[(3, "high"), (2, "diffuse low"), (1, "others")],
        default=1,
        validators=[InputRequired(), AnyOf([3, 2, 1])],
    )
    submit = SubmitField('Predict')