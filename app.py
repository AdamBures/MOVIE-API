import sqlite3
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
DATABASE = 'movies.db'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

with sqlite3.connect(DATABASE) as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS movies
    (id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    release_year INTEGER NOT NULL)''')


@app.route('/movies')
def get_movies():
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, title, description, release_year FROM movies')
        rows = cur.fetchall()
        movies = [{'id': row[0], 'title': row[1], 'description': row[2], 'release_year': row[3]} for row in rows]
        return jsonify(movies)


@app.route('/movies/<int:id>')
def get_movie(id):
    with sqlite3.connect(DATABASE) as conn:
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
    if not request.json or not 'title' in request.json or not 'release_year' in request.json:
        abort(400)
    movie = {
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'release_year': request.json['release_year'],
    }
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO movies (title, description, release_year) VALUES (?, ?, ?)', (movie['title'], movie['description'], movie['release_year']))
        movie['id'] = cur.lastrowid
        conn.commit()
    return jsonify(movie), 201


@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    data = request.get_json()
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute('UPDATE movies SET title = ?, description = ?, release_year = ? WHERE id = ?', (
        data.get('title', None),
        data.get('description', None),
        data.get('release_year', None),
        id
    ))

    conn.commit()
    conn.close()

    return jsonify(data), 201


if __name__ == '__main__':
    app.run(debug=True)
