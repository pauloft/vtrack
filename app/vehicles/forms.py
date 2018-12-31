# app/vehicles/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import current_user
from app.models import Vehicle, Picture


class VehicleForm(FlaskForm):
    vin = StringField("Vehicle Identification Number", validators=[DataRequired()])
    tag = StringField("Vehicle Tag", validators=[DataRequired()])
    year = StringField(
        "Year",
        validators=[Length(min=4, max=4, message="Use 4-digit year format, e.g. 1998")],
    )
    make = StringField("Make")
    model = StringField("Model")
    picture = FileField(
        "Add a Picture of this vehicle (Optional)",
        validators=[FileAllowed(["jpg", "png"], "Images Only")],
    )
    submit = SubmitField("Save")

