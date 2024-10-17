from flask import Flask, request, jsonify

app = Flask(__name__)

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@app.route('/')
def home():
    return "Distant Reading Archive: A prototype API for distant reading of science fiction novels."

@app.route('/api/v1/resources/books/all')
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    book_id = request.args.get('id')

    if book_id:
        book_id = int(book_id)

        result = [book for book in books if book['id'] == book_id]

        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "No book found with the given ID"}), 404
    else:
        return jsonify({"error": "ID parameter is required"}), 400

if __name__ == '__main__':
    app.run(debug=True)