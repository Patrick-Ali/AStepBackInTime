from flask_wtf import Form
from wtforms import SubmitField, SelectField, RadioField, BooleanField, TextField, HiddenField, SelectMultipleField, widgets

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RomeQuiz(Form):
	#b1String = ['']
	q1 = RadioField("Who was the first king of Rome", choices = [("Romulus","Romulus"),("Remus","Remus")])
	q2 = RadioField("When was Rome founded", choices = [("720","720"),("850","850"),("600","600")])
	q3 = MultiCheckboxField("Which two groups sacked Rome", choices = [("Gauls","Gauls"),("Visigoths","Visigoths"),("Carthaginians", "Carthaginians"),("Greeks","Greeks")])
	q4 = TextField("What famous mountains did Hannable cross")
	q5 = RadioField("Who was the first king of Rome", choices = [("Augustus Ceaser","Augustus Ceaser"),("Julius Ceaser","Julius Ceaser"),("Nero","Nero"),("Trajan","Trajan")])
	q6 = RadioField("When was Rome founded", choices = [("45","45"),("30","30"),("100","100")])
	q7 = TextField("Ceaser's rival during the civil war was Pompey the")
	q8 = MultiCheckboxField("Select all correct provinces of the Roman empire", choices=[("Aegyptus","Aegyptus"),("Germania","Germania"),("Britania", "Britania"),("Grecce","Grecce")])
	q9 = TextField("Who was Mark Anthony's most famous lover")
	q10 = TextField("Which member of Julius Ceasers family infamously helped assassinate him")

	submit = SubmitField("Grade")
