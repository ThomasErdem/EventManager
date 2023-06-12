from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SelectField, TextAreaField, DateField, SubmitField, TimeField
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()], render_kw={"placeholder": "id"})
    name = StringField('Naam', validators=[DataRequired()], render_kw={"placeholder": "Event name"})
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"placeholder": "Event description"})
    location = StringField('Location', validators=[DataRequired()], render_kw={"placeholder": "Event location"})
    budget = IntegerField('Budget', validators=[DataRequired()], render_kw={"placeholder": "Event budget"})
    date = DateField('Date', validators=[DataRequired()], format='%d-%m-%Y', render_kw={"placeholder": "DD-MM-YYYY"})
    program = StringField('Program', validators=[DataRequired()], render_kw={"placeholder": "program"})
    category = SelectField('Category', validators=[DataRequired()], choices=[('conference', 'Conference'), ('seminar', 'Seminar'), ('workshop', 'Workshop')], render_kw={"placeholder": "Event type"})
    submit = SubmitField('Save')


class MeetingForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()], render_kw={"placeholder": "id"})
    subject = StringField('Subject', validators=[DataRequired()], render_kw={"placeholder": "Event name"})
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"placeholder": "Event description"})
    date = DateField('Date', validators=[DataRequired()], format='%d-%m-%Y', render_kw={"placeholder": "DD-MM-YYYY"})
    time = TimeField('Time', validators=[DataRequired()], format='%H:%M', render_kw={"placeholder": "HH:MM"})
    location = StringField('Location', validators=[DataRequired()], render_kw={"placeholder": "Event location"})

    

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()], render_kw={"placeholder": "Search events"})
    submit = SubmitField('Search')



class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    data = TextAreaField('Content', validators=[DataRequired()])
    status = SelectField('Status', choices=[('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], validators=[DataRequired()])



class StakeholderForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()], render_kw={"placeholder": "id"})
    name = StringField('Subject', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    email = TextAreaField('Description', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    phone_number = IntegerField('Phone number', validators=[DataRequired()], render_kw={"placeholder": "Phone number"})
    function = StringField('Location', validators=[DataRequired()], render_kw={"placeholder": "Function"})


class UserDataForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                                choices=[('income', 'income'),
                                        ('expense', 'expense')])
    category = SelectField("Category", validators=[DataRequired()],
                                            choices =[('rent', 'rent'),
                                            ('salary', 'salary'),
                                            ('investment', 'investment'),
                                            ('side_hustle', 'side_hustle')
                                            ]
                            )
    amount = IntegerField('Amount', validators = [DataRequired()])                                   
    submit = SubmitField('Generate Report')                            