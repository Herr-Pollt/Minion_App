from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minions.db'
db = SQLAlchemy(app)

class Minion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    eye_color = db.Column(db.String(80))
    size = db.Column(db.Float(80))
    silliness_level = db.Column(db.Integer)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    length = db.Column(db.String(80))
    path = db.Column(db.String(300))

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/minions')
def get_minions():
    minions = Minion.query.all()
    minion_list = [minion.name for minion in minions]
    return jsonify(minion_list)

@app.route('/movies')
def show_movies():
    return render_template("movies.html", data = get_movies())
def get_movies():
    movies = Movie.query.all()
    return movies


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        existing_minion = Minion.query.filter_by(name='Kevin').first()

        if not existing_minion:
            minions_to_add = [
                Minion(name='Kevin', eye_color='brown',size=0.75, silliness_level=0),
                Minion(name='Bob', eye_color='green',size=0.5, silliness_level=6),
                Minion(name='Stuart', eye_color='black',size=0.6, silliness_level=2)
            ]
            db.session.add_all(minions_to_add)
            db.session.commit()
        
        existing_movie = Movie.query.filter_by(name='Despicable Me1').first()

        if not existing_movie:
            movies_to_add = [
                Movie(name='Despicable Me1', length = '1h 35m', path = '/images/Despicableme1.png'),
                Movie(name='Despicable Me2', length = '1h 38m', path = '/images/Despicableme2.jpg'),
                Movie(name='Rise of Gru', length = '1h 28m', path = '/images/RiseOfGru.jpg')
            ]
            db.session.add_all(movies_to_add)
            db.session.commit()
    
    
    app.run(debug=True)