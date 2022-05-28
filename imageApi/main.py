#performing flask imports
from flask import Flask, request, jsonify
import werkzeug

app = Flask(__name__) #intance of our flask application

@app.route('/upload', methods=["POST"])
def upload():
    if(request.method == "POST"):
        imagefile = request.files['image']
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        imagefile.save("./uploadedImages/"+filename)
        return jsonify({
            "message":"Image Uploaded Successfully"
        })


if __name__ == "__main__":
    app.run(debug = True, port=8000) #debug will allow changes without shutting down the server