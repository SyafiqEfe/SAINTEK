from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class CashFlowForm(FlaskForm):
    date = DateField('Tanggal', format='%Y-%m-%d', validators=[DataRequired()])
    type = SelectField('Tipe', choices=[('income', 'Pemasukan'), ('expense', 'Pengeluaran')], validators=[DataRequired()])
    amount = FloatField('Jumlah', validators=[DataRequired(), NumberRange(min=0)])
    description = StringField('Deskripsi', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Simpan')
