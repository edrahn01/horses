from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db'
db = SQLAlchemy(app)


@app.route('/verify/<id>')
def verify(id):
    race = db.session.query(Race).filter_by(id=id)
    return render_template('web/verify_main.html', race=race) 
