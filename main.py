from flask import Flask,render_template,redirect,request
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import cv2

app = Flask(__name__)
app.secret_key = 'super secret key'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wepg', 'png', 'jpg', 'jpeg', 'gif','svg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def processImage(filename,operation):
    # print(f"{filename }is doing the {operation}")
    img=cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgrey":
            imgP = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgP)
            return newFilename
        case "cpng":
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg":
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename 
        case "cjpeg":
            newFilename = f"static/{filename.split('.')[0]}.jpeg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cwebp":
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename 
              

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/")


def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit",methods={'GET','POST'})
def edit():
    if request.method=="POST":
        operation=request.form.get('operation')
        if 'file' not in request.files:
                flash('No file part')
                return 'no '
        file = request.files['file']
        if file.filename == '':
                flash('No selected file')
                return 'no file'
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new= processImage(filename,operation)
                flash(f"Your Image is processed and can be found in <a href='/{new}' target='_blank'>here </a>")
                return render_template('index.html')
    return  render_template('index.html')


app.run(debug=False,port=0.0.0.0)
