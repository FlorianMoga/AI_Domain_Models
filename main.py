#performing flask imports
from flask import Flask, request, jsonify
import werkzeug
import backend.extract_text as extrct
from pathlib import Path
import cv2

from backend.extract_table.main import get_table_corners
from backend.extract_text.main import extract_text
from frontend.straighten_image.main import straighten_image

app = Flask(__name__) #intance of our flask application

@app.route('/upload', methods=["POST"])
def upload():
    if(request.method == "POST"):
        # imagefile = request.files['image']
        # filename = werkzeug.utils.secure_filename(imagefile.filename)
        # imagefile.save("./Images/"+filename)
        imagefile = cv2.imread("./Images/photo_2022-06-09_15-03-33.jpg")
        process_image(imagefile)
        return jsonify({
            "message" : "Image Uploaded Successfully"
        })

def main():
    print('da')
    imagefile = cv2.imread("C:/Users/andre/Desktop/gep/AI_Domain_Models/Images/photo_2022-06-09_15-03-33.jpg", cv2.IMREAD_COLOR)
    # cv2.imshow("abc", imagefile)
    # cv2.waitKey(0)
    process_image(imagefile)

def process_image(img):
    out = straighten_image(img)
    corners = get_table_corners(out)
    # extract_text(out, corners)

if __name__ == "__main__":
    main()
    app.run(debug = True, port=8000) #debug will allow changes without shutting down the server