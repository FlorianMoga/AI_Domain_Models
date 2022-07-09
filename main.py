#performing flask imports
from flask import Flask, request, jsonify
import werkzeug
import backend.extract_text as extrct
from pathlib import Path
import cv2
import fitz

from backend.extract_table.main import get_table_corners
from backend.extract_text.main import extract_text
from frontend.straighten_image.main import straighten_image

app = Flask(__name__) #intance of our flask application

@app.route('/upload', methods=["POST"])
def upload():
    if(request.method == "POST"):
        file = request.files['file']
        filename = werkzeug.utils.secure_filename(file.filename)
        print(filename)
        file.save("C:/Users/andre/Desktop/gep/AI_Domain_Models/Images/"+filename)
        if(filename[-3:]=='pdf'):
            processPdf(filename[:-4])
        else:
            process_image(filename)
        # img = cv2.imread("C:/Users/andre/Desktop/gep/AI_Domain_Models/Images/"+filename)
        return jsonify({
            "message": "File Uploaded Successfully"
        })


@app.route('/token', methods=["POST"])
def token():
    if (request.method == "POST"):
        global token
        request_data = request.get_json()
        token = request_data['token']
        print("token: ", token)
        return jsonify({
            "message": "Token received"
        })

def process_image(file):
    print('processing...')
    img = cv2.imread("C:/Users/andre/Desktop/gep/AI_Domain_Models/Images/"+file)
    out = straighten_image(img)
    corners = get_table_corners(out)
    #[79, 549, 920, 1001]
    # de_aratat = out.copy()
    # cv2.rectangle(out, (corners[0] - 1, corners[1] - 1), (corners[0] + 1, corners[1] + 1), (0, 0, 255), 2)
    # cv2.rectangle(out, (corners[2] - 1, corners[3] - 1), (corners[2] + 1, corners[3] + 1), (0, 0, 255), 2)
    # cv2.imshow("segments", de_aratat)
    # cv2.waitKey(0)
    filepath = "C:/Users/andre/Desktop/gep/AI_Domain_Models/Images/resized_"+file
    # cv2.imwrite(filepath, out)
    extract_text(filepath, corners, token)

def processPdf(filename):
    pdffile = "C:/Users/andre/Desktop/gep/AI_Domain_Models/Images/"+filename+".pdf"
    doc = fitz.open(pdffile)
    page = doc.load_page(0)  # number of page
    pix = page.get_pixmap()
    output = "C:/Users/andre/Desktop/gep/AI_Domain_Models/Images/"+filename+".png"
    pix.save(output)
    img = cv2.imread("C:/Users/andre/Desktop/gep/AI_Domain_Models/Images/"+filename+".png")
    corners = get_table_corners(img)
    extract_text("C:/Users/andre/Desktop/gep/AI_Domain_Models/Images/"+filename+".png", corners, token)


if __name__ == "__main__":
    app.run(debug = True, port=8000) #debug will allow changes without shutting down the server