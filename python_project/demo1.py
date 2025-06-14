from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import cv2
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation, text):
    print(f"The operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")

    if text:
        cv2.putText(img, text, (100, 100), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 75, 0))

    if operation == "cgray":
        imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        newFilename = f"static/{filename}"
        cv2.imwrite(newFilename, imgProcessed)
        return newFilename

    elif operation == "cwebp":
        newFilename = f"static/{filename.split('.')[0]}.webp"
        cv2.imwrite(newFilename, img)
        return newFilename

    elif operation == "cjpg":
        newFilename = f"static/{filename.split('.')[0]}.jpg"
        cv2.imwrite(newFilename, img)
        return newFilename

    elif operation == "cpng":
        newFilename = f"static/{filename.split('.')[0]}.png"
        cv2.imwrite(newFilename, img)
        return newFilename

    elif operation == "negative":
        imgNegative = 255 - img
        newFilename = f"static/{filename.split('.')[0]}_negative.jpg"
        cv2.imwrite(newFilename, imgNegative)
        return newFilename

    elif operation == "flip":
        imgFlipped = cv2.flip(img, 1)
        newFilename = f"static/{filename.split('.')[0]}_flipped.jpg"
        cv2.imwrite(newFilename, imgFlipped)
        return newFilename

    elif operation == "border":
        imgBordered = cv2.copyMakeBorder(img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        newFilename = f"static/{filename.split('.')[0]}_bordered.jpg"
        cv2.imwrite(newFilename, imgBordered)
        return newFilename

    elif operation == "smooth":
        imgSmooth = cv2.edgePreservingFilter(img, cv2.RECURS_FILTER, 60, 0.6)
        newFilename = f"static/{filename.split('.')[0]}_smooth.jpg"
        cv2.imwrite(newFilename, imgSmooth)
        return newFilename

    elif operation == "blur":
        imgBlurred = cv2.blur(img, (3, 3), 0)
        newFilename = f"static/{filename.split('.')[0]}_blurred.jpg"
        cv2.imwrite(newFilename, imgBlurred)
        return newFilename

    elif operation == "pencil":
        imgPencil, _ = cv2.pencilSketch(img, 200, 0.1, shade_factor=0.1)
        newFilename = f"static/{filename.split('.')[0]}_pencil.jpg"
        cv2.imwrite(newFilename, imgPencil)
        return newFilename

    elif operation == "color_sketch":
        _, imgColored = cv2.pencilSketch(img, 200, 0.1, shade_factor=0.1)
        newFilename = f"static/{filename.split('.')[0]}_color_sketch.jpg"
        cv2.imwrite(newFilename, imgColored)
        return newFilename
    
    elif operation == "resize_250x250":
        resized_img = cv2.resize(img, (250, 250))
        newFilename = f"static/{filename.split('.')[0]}_resized_250x250.jpg"
        cv2.imwrite(newFilename, resized_img)
        return newFilename
    
    elif operation == "resize_500x500":
        resized_img = cv2.resize(img, (500, 500))
        newFilename = f"static/{filename.split('.')[0]}_resized_500x500.jpg"
        cv2.imwrite(newFilename, resized_img)
        return newFilename
    
    elif operation == "resize_1024x1024":
        resized_img = cv2.resize(img, (1024, 1024))
        newFilename = f"static/{filename.split('.')[0]}_resized_1024x1024.jpg"
        cv2.imwrite(newFilename, resized_img)
        return newFilename
    
    elif operation == "rotate_90_clockwise":
        rotated_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        newFilename = f"static/{filename.split('.')[0]}_rotated_90_clockwise.jpg"
        cv2.imwrite(newFilename, rotated_img)
        return newFilename
    
    elif operation == "rotate_90_anticlockwise":
        rotated_img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        newFilename = f"static/{filename.split('.')[0]}_rotated_90_anticlockwise.jpg"
        cv2.imwrite(newFilename, rotated_img)
        return newFilename
    
    elif operation == "rotate_180":
        rotated_img = cv2.rotate(img, cv2.ROTATE_180)
        newFilename = f"static/{filename.split('.')[0]}_rotated_180.jpg"
        cv2.imwrite(newFilename, rotated_img)
        return newFilename
    
    elif operation == "crop":
        r = cv2.selectROI(img)
        cropped_img = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        newFilename = f"static/{filename.split('.')[0]}_cropped.jpg"
        cv2.imwrite(newFilename, cropped_img)
        return newFilename

    else:
        return None

@app.route("/")
def home1():
    return render_template("index1.html")

@app.route("/Subscriptions.html")
def link1():
   return render_template("Subscriptions.html")

@app.route("/contact.html")
def link2():
    return render_template("contact.html")

@app.route("/pay1.html")
def link3():
    return render_template("pay1.html")

@app.route("/index_free.html")
def home22():
    return render_template("index_free.html")

@app.route("/index1.html")
def link5():
    return render_template("index1.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/pay2.html")
def link6():
    return render_template("pay2.html")

@app.route("/index_basic.html")
def home12():
    return render_template("index_basic.html")

@app.route("/login.html")
def link34():
    return render_template("login.html")

@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST": 
        operation = request.form.get("operation")
        text = request.form.get("textToAdd")
        
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation, text)
            if new:
                flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            else:
                flash("Invalid operation selected.")
            return render_template("index.html")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)