import sqlite3
from flask import Flask, jsonify, request, abort
from contextlib import contextmanager
from jsonschema import validate, ValidationError

app = Flask(__name__)
DATABASE = 'movies.db'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

# Create the movies table if it doesn't already exist
with sqlite3.connect(DATABASE) as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS movies
    (id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    release_year INTEGER NOT NULL)''')


@contextmanager
def connect_db():
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()


def validate_movie_data(data):
    schema = {
        'type': 'object',
        'properties': {
            'title': {'type': 'string'},
            'description': {'type': 'string'},
            'release_year': {'type': 'integer'}
        },
        'required': ['title', 'release_year']
    }
    try:
        validate(data, schema)
    except ValidationError as e:
        abort(400, str(e))


@app.route('/movies')
def get_movies():
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, title, description, release_year FROM movies')
        rows = cur.fetchall()
        movies = [{'id': row[0], 'title': row[1], 'description': row[2], 'release_year': row[3]} for row in rows]
        return jsonify(movies)


@app.route('/movies/<int:id>')
def get_movie(id):
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM movies WHERE id = ?', (id,))
        row = cur.fetchone()
        if row:
            movie = {'id': row[0], 'title': row[1], 'description': row[2], 'release_year': row[3]}
            return jsonify(movie)
        else:
            abort(404)


@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    validate_movie_data(data)

    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO movies (title, description, release_year) VALUES (?, ?, ?)',
                    (data['title'], data.get('description', ''), data['release_year']))
        movie_id = cur.lastrowid
        conn.commit()

    movie = {'id': movie_id, 'title': data['title'], 'description': data.get('description', ''), 'release_year': data['release_year']}
    return jsonify(movie), 201


@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    data = request.get_json()
    validate_movie_data(data)

    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute('UPDATE movies SET title = ?, description = ?, release_year = ? WHERE id = ?',
                    (data['title'], data.get('description', ''), data['release_year'], id))
        conn.commit()

    return jsonify(data), 201


if __name__ == '__main__':
    app.run(debug=True)
