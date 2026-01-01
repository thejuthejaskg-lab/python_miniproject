from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__)
CSV_FILE = "book.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["BookID", "Title", "Author"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_book():
    data = request.json
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([data["id"], data["title"], data["author"]])
    return jsonify({"status": "Book added"})

@app.route("/get/<book_id>")
def get_book(book_id):
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] == book_id:
                return jsonify({"id": row[0], "title": row[1], "author": row[2]})
    return jsonify({"status": "not found"})

@app.route("/delete", methods=["POST"])
def delete_book():
    book_id = request.json["id"]
    rows = []

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in rows:
            if row and row[0] != book_id:
                writer.writerow(row)

    return jsonify({"status": "Book deleted"})

@app.route("/list")
def list_books():
    books = []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            books.append({
                "id": row[0],
                "title": row[1],
                "author": row[2]
            })
    return jsonify(books)

if __name__ == "__main__":
    app.run(debug=True)