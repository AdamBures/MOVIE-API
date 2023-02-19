# Movie API

A simple RESTful API for managing a collection of movies.

## Getting Started

To get started with the API, you'll need to have Python 3 installed on your system.

1. Clone this repository:
git clone https://github.com/AdamBures/movie-api.git

2. Install the dependencies:
pip install -r requirements.txt

3. Run the server:
python app.py

The server will be running at `http://localhost:5000`.

## Endpoints

The API exposes the following endpoints:

### GET /movies

Returns a list of all movies in the database.

### GET /movies/:id

Returns the movie with the specified ID.

### POST /movies

Adds a new movie to the database.

### PUT /movies/:id

Updates the movie with the specified ID.

## Data Model

Each movie in the database has the following fields:

- id (integer)
- title (string)
- description (string)
- release_year (integer)

## Examples
Here are some example requests and their corresponding responses:
`GET /movies`
Request:
```
GET /movies
```

Response:
```
HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "id": 1,
        "title": "The Godfather",
        "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        "release_year": 1972
    },
    {
        "id": 2,
        "title": "The Godfather Part II",
        "description": "The early life and career of Vito Corleone in 1920s New York City is portrayed, while his son, Michael, expands and tightens his grip on the family crime syndicate.",
        "release_year": 1974
    }
]
```


``POST /movies``
Request:
```
POST /movies
Content-Type: application/json

{
    "title": "The Shawshank Redemption",
    "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
    "release_year": 1994
}
Response:

css
Copy code
HTTP/1.1 201 Created
Content-Type: application/json

{
    "id": 3,
    "title": "The Shawshank Redemption",
    "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
    "release_year": 1994
}
```

## Error Handling
If an error occurs while processing a request, the API will return an error response with a JSON body containing an error message.

The API uses the following HTTP status codes to indicate the result of a request:

- 200 OK: The request was successful.
- 201 Created: The request was successful and a new resource was created.
- 400 Bad Request: The request was malformed or invalid.
- 404 Not Found: The requested resource was not found.
- 500 Internal Server Error: An error occurred on the server.
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.





