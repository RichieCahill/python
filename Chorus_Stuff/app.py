import os

from flask import Flask, jsonify, render_template, request, send_file

from .file_store_api import file_store

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/directory")
def directory():
    links = [
        "https://15til.com/njgmc.mp3s",
        "https://15til.com/njgmc.gig.mp3s",
        "https://15til.com/njgmc.pdfs",
        "https://15til.com/njgmc.gig.pdfs",
        "https://15til.com/njgmc.cal.private",
        "https://15til.com/njgmc.cal.absences",
        "https://15til.com/njgmc.rolodex",
    ]
    return render_template("directory.html", links=links)


app.register_blueprint(file_store, url_prefix="/sheet_music")


if __name__ == "__main__":
    app.run(debug=True)
