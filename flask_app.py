from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, DecimalField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'happypuppy73'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/lkelly00/sites/etsydemo/tmp/database.db'
db = SQLAlchemy(app)

class Listing(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(200))
    price = db.Column(db.Float(2))

class ListingForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])

@app.route('/')
def index():
    results = Listing.query.filter(1==1).all()
    return render_template ('index.html', listings=results)

@app.route('/listing/new', methods=['GET','POST'])
def newlisting():
    form = ListingForm(request.form)
    if request.method == 'POST':
        if form.validate() == False:
          flash('All fields are required.')
          return render_template('newlisting.html', form=form)
        else:
          lst = Listing(name=form.name.data, description= form.description.data, price=form.price.data )
          db.session.add(lst)
          db.session.commit()
          results = Listing.query.filter(1==1).all()
          return render_template('index.html', listings=results)
    else:
        return render_template ('newlisting.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')