import os

from flask import Blueprint, jsonify, render_template, request, send_file

file_store = Blueprint("file_store", __name__)

file_dir = "/home/r2r0m0c0/Projects/Python/Chorus_Stuff/Videos/"


@file_store.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        file.save(file_dir + file.filename)
        return jsonify({"message": "File uploaded successfully!"})
    return jsonify({"message": "Invalid request"})


@file_store.route("/")
def index():
    file_list = os.listdir(file_dir)
    return render_template("index.html", files=file_list)


@file_store.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(file_dir, filename)
    return send_file(file_path, as_attachment=True)
