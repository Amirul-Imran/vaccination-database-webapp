from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    id = IntegerField("ID", validators=[DataRequired()])
    department = SelectField("Department", choices=["Biomedical", "Chemical", "Civil", "Electrical", "Mechanical"],
                             validators=[DataRequired()])
    status = SelectField("Vaccination Status", choices=[(0, "Not Vaccinated"), (1, "First Dose"), (2, "Second Dose")],
                         validators=[DataRequired()], coerce=int)
    enter = SubmitField("Add")


class SearchForm(FlaskForm):
    id = IntegerField("ID", validators=[DataRequired()])
    enter = SubmitField("Search")


class RemoveForm(FlaskForm):
    id = IntegerField("ID", validators=[DataRequired()])
    department = SelectField("Department",
                             choices=[(1, "Biomedical"), (2, "Chemical"), (3, "Civil"), (4, "Electrical"),
                                      (5, "Mechanical")])
    enter = SubmitField("Remove")
