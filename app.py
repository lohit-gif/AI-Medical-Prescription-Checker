from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import PyPDF2
import os
import time
from google import genai
from flask_mail import Mail, Message
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


app = Flask(__name__)


# Gmail Configuration

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

app.config["MAIL_USERNAME"] = "mr.truelover12@gmail.com"
app.config["MAIL_PASSWORD"] = "eqdj qbor kvmh yojb"


mail = Mail(app)



# Gemini API Keys

API_KEYS = [

    "AQ.Ab8RN6IfSHps_FWWUnzTBP_6zDPOPp6gW5MrePR9frvByVTmkA",

    "AQ.Ab8RN6K_b0jmTZoONR3VgXwq0nC8XRw6HMuNeCgzc9JcD7V2Mw"

]



app.secret_key = "medical-ai-secret-key"


otp_storage = {}



# Upload Folder

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)




# Database

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)




# User Table

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    username = db.Column(
        db.String(100),
        unique=True
    )


    email = db.Column(
        db.String(150),
        unique=True
    )


    password = db.Column(
        db.String(100)
    )


    verified = db.Column(
        db.Boolean,
        default=False
    )





with app.app_context():

    db.create_all()





@app.route("/")
def home():

    return redirect(
        url_for("login")
    )





# Register

@app.route("/register", methods=["GET","POST"])
def register():


    if request.method == "POST":


        username = request.form["username"]

        email = request.form["email"]


        password = generate_password_hash(

            request.form["password"]

        )


        otp = random.randint(
            100000,
            999999
        )



        otp_storage[email] = {


            "username": username,

            "password": password,

            "otp": otp

        }



        msg = Message(

            "Medical AI Verification OTP",

            sender=app.config["MAIL_USERNAME"],

            recipients=[email]

        )


        msg.body = f"Your verification OTP is {otp}"


        print("OTP:", otp)

# mail.send(msg)



        session["verify_email"] = email



        return redirect(
            url_for("verify_otp")
        )



    return render_template(
        "register.html"
    )





# Verify OTP

@app.route("/verify_otp", methods=["GET","POST"])
def verify_otp():


    email = session.get(
        "verify_email"
    )



    if request.method == "POST":


        entered_otp = request.form["otp"]



        if email in otp_storage:


            saved_otp = otp_storage[email]["otp"]



            if str(saved_otp) == entered_otp:


                user = User(

                    username=otp_storage[email]["username"],

                    email=email,

                    password=otp_storage[email]["password"],

                    verified=True

                )


                db.session.add(user)

                db.session.commit()



                otp_storage.pop(email)



                return redirect(
                    url_for("login")
                )



            else:

                return "Wrong OTP"



    return render_template(
        "verify_otp.html"
    )
# Login

@app.route("/login", methods=["GET","POST"])
def login():


    if request.method == "POST":


        username = request.form["username"]

        password = request.form["password"]



        user = User.query.filter_by(
            username=username
        ).first()



        if user and check_password_hash(
            user.password,
            password
        ):


            session["user"] = username


            return redirect(
                url_for("dashboard")
            )


        else:

            return "Invalid username or password"



    return render_template(
        "login.html"
    )







# Gemini Request Function

def gemini_request(input_data):


    last_error = ""



    for key in API_KEYS:



        try:


            client = genai.Client(

                api_key=key

            )



            for attempt in range(3):



                try:



                    response = client.models.generate_content(


                        model="gemini-2.5-flash",



                        contents=[


                            input_data,



                            """
You are an AI Medical Prescription Checker.

Read this prescription image/text.

Return:

PRESCRIPTION RESULT:

PATIENT DETAILS
Name:
Age:
Gender:
Date:


DOCTOR DETAILS
Doctor Name:
Hospital / Clinic:


MEDICINES PRESCRIBED


DOSAGE / INSTRUCTIONS



AI ANALYSIS:

Include:

- Purpose of medicines
- Important warnings
- Possible side effects
- Patient advice


Rules:

- Correct spelling mistakes.
- Remove unwanted symbols.
- Do not use markdown symbols.
"""

                        ]

                    )



                    return response.text




                except Exception as e:


                    last_error = str(e)



                    if "503" in last_error:


                        time.sleep(10)

                        continue



                    break




        except Exception as e:


            last_error = str(e)

            continue




    return "Gemini Error: " + last_error











# Dashboard

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():


    if "user" not in session:


        return redirect(
            url_for("login")
        )



    clean_prescription = ""

    ai_analysis = ""




    if request.method == "POST":


        file = request.files.get(
            "prescription"
        )



        if file and file.filename:




            filepath = os.path.join(


                app.config["UPLOAD_FOLDER"],


                file.filename


            )



            file.save(filepath)





            try:



                if file.filename.lower().endswith(".pdf"):



                    text = ""



                    with open(filepath,"rb") as pdf:



                        reader = PyPDF2.PdfReader(pdf)



                        for page in reader.pages:


                            text += page.extract_text() or ""



                    input_data = text




                else:



                    input_data = Image.open(filepath)





                output = gemini_request(
                    input_data
                )




                if "AI ANALYSIS:" in output:



                    clean_prescription = output.split(

                        "AI ANALYSIS:"

                    )[0]



                    ai_analysis = output.split(

                        "AI ANALYSIS:"

                    )[1]




                else:



                    clean_prescription = output

                    ai_analysis = output





                session["prescription_result"] = clean_prescription

                session["ai_analysis"] = ai_analysis





            except Exception as e:


                ai_analysis = "Error: " + str(e)






    return render_template(

        "dashboard.html",

        result=clean_prescription,

        ai_analysis=ai_analysis

    )

# Download PDF Report

@app.route("/download_pdf")
def download_pdf():


    if "user" not in session:


        return redirect(
            url_for("login")
        )



    prescription = session.get(

        "prescription_result",

        "No prescription available"

    )



    analysis = session.get(

        "ai_analysis",

        "No AI analysis available"

    )



    pdf_path = "medical_report.pdf"




    pdf = canvas.Canvas(

        pdf_path,

        pagesize=letter

    )



    pdf.setFont(

        "Helvetica",

        12

    )



    pdf.drawString(

        50,

        750,

        "Medical AI Prescription Report"

    )



    y = 720




    content = (


        "PRESCRIPTION RESULT\n\n"

        + prescription

        + "\n\nAI ANALYSIS\n\n"

        + analysis

    )




    for line in content.split("\n"):



        pdf.drawString(

            50,

            y,

            line[:100]

        )


        y -= 18




        if y < 50:


            pdf.showPage()


            y = 750





    pdf.save()




    return send_file(

        pdf_path,

        as_attachment=True

    )








# Logout

@app.route("/logout")
def logout():


    session.clear()


    return redirect(

        url_for("login")

    )








if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )