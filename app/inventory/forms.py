from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save Category')

class SupplierForm(FlaskForm):
    name = StringField('Supplier Name', validators=[DataRequired()])
    contact = StringField('Contact Information')
    address = TextAreaField('Address')
    submit = SubmitField('Save Supplier')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    barcode = StringField('Barcode (leave empty to auto-generate)', validators=[Optional()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    supplier_id = SelectField('Supplier', coerce=int, validators=[DataRequired()])
    purchase_price = FloatField('Purchase Price', validators=[DataRequired()])
    selling_price = FloatField('Selling Price', validators=[DataRequired()])
    stock_quantity = IntegerField('Initial Stock', validators=[DataRequired()])
    min_stock_alert = IntegerField('Min Stock Alert Level', default=10)
    submit = SubmitField('Save Product')
