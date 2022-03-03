from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    id = IntegerField("ID", validators=[DataRequired()])
    department = SelectField("Department", choices=[(1, "Mechanical"), (2, "Electrical"), (3, "Chemical"), (4, "Civil"),
                                                    (5, "Biomedical")], coerce=int)
    status = SelectField("Vaccination Status", choices=[(0, "Not Vaccinated"), (1, "First Dose"), (2, "Second Dose")],
                         coerce=int)
    enter = SubmitField("Add")


class SearchForm(FlaskForm):
    id = IntegerField("ID", validators=[DataRequired()])
    enter = SubmitField("Search")


class RemoveForm(FlaskForm):
    id = IntegerField("ID", validators=[DataRequired()])
    enter = SubmitField("Remove")
