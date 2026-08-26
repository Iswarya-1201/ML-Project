from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# =====================================================
# Load Models
# =====================================================

model10 = pickle.load(open("model10.pkl", "rb"))
encoder10 = pickle.load(open("encoder10.pkl", "rb"))

model12 = pickle.load(open("model12.pkl", "rb"))
encoder12 = pickle.load(open("encoder12.pkl", "rb"))

model3 = pickle.load(open("model3.pkl", "rb"))
encoder3 = pickle.load(open("encoder3.pkl", "rb"))

# =====================================================
# Login Credentials
# =====================================================

USERNAME = "student"
PASSWORD = "1234"

# =====================================================
# 10TH STANDARD HELPER FUNCTIONS
# =====================================================

def generate_reasons(result, maths, science, english, aptitude, communication):

    reasons = []

    if maths >= 90:
        reasons.append("Excellent Mathematics score. You have strong logical and analytical skills.")
    elif maths >= 80:
        reasons.append("Good Mathematics score.")

    if science >= 90:
        reasons.append("Excellent Science performance.")
    elif science >= 80:
        reasons.append("Good Science knowledge.")

    if english >= 80:
        reasons.append("Good English communication skills.")

    if aptitude >= 80:
        reasons.append("Excellent aptitude and problem-solving ability.")

    if communication >= 70:
        reasons.append("Good communication skills.")

    reasons.append(
        f"Based on your marks and the Machine Learning model, '{result}' is the most suitable group for you."
    )

    return reasons
def student_strengths(maths, science, english, aptitude, communication):

    strengths = []

    if maths >= 80:
        strengths.append("Strong Mathematics")

    if science >= 80:
        strengths.append("Strong Science Knowledge")

    if english >= 80:
        strengths.append("Good English Communication")

    if aptitude >= 80:
        strengths.append("Excellent Logical Thinking")

    if communication >= 70:
        strengths.append("Good Communication Skills")

    if len(strengths) == 0:
        strengths.append("You have the potential to improve with regular practice.")

    return strengths
def improvements(maths, science, english, aptitude, communication):

    improve = []

    if maths < 80:
        improve.append("Improve Mathematics through regular practice.")

    if science < 80:
        improve.append("Improve Science concepts by revising daily.")

    if english < 80:
        improve.append("Improve English reading, writing and speaking skills.")

    if aptitude < 80:
        improve.append("Practice Aptitude questions every day.")

    if communication < 70:
        improve.append("Improve communication and presentation skills.")

    if len(improve) == 0:
        improve.append("Excellent performance! Keep up the good work.")

    return improve
def other_groups(result):

    groups = {

        "Computer Science": [
            "Biology is less suitable because your profile shows stronger logical and mathematical ability.",
            "Commerce is less suitable because your aptitude and academic performance indicate better technical skills.",
            "Arts is less suitable because your strengths are more technical than language-oriented."
        ],

        "Biology": [
            "Computer Science is less suitable because your Science profile is stronger than your Mathematics profile.",
            "Commerce is less suitable because you have better scientific aptitude.",
            "Arts is less suitable because your interests are more science-oriented."
        ],

        "Commerce": [
            "Computer Science is less suitable because it requires stronger technical aptitude.",
            "Biology is less suitable because your Science performance is comparatively lower.",
            "Arts is less suitable because your profile is more business-oriented."
        ],

        "Arts": [
            "Computer Science requires stronger technical and logical skills.",
            "Biology requires stronger Science performance.",
            "Commerce is more suitable for students interested in business studies."
        ]

    }

    return groups.get(
        result,
        ["Every group has good career opportunities. Choose according to your interests and goals."]
    )
def career_opportunities(result):

    careers = {

        "Computer Science": [
            "Software Engineer",
            "Web Developer",
            "Mobile App Developer",
            "Artificial Intelligence Engineer",
            "Data Scientist",
            "Cyber Security Engineer",
            "Cloud Engineer"
        ],

        "Biology": [
            "Doctor",
            "Dentist",
            "Nurse",
            "Pharmacist",
            "Biotechnologist",
            "Microbiologist"
        ],

        "Commerce": [
            "Chartered Accountant (CA)",
            "Bank Officer",
            "Financial Analyst",
            "Auditor",
            "Business Analyst",
            "Company Secretary"
        ],

        "Arts": [
            "Teacher",
            "Journalist",
            "Lawyer",
            "Psychologist",
            "Civil Service Officer",
            "Graphic Designer"
        ]

    }

    return careers.get(
        result,
        ["Many career opportunities are available based on your interests and higher education."]
    )

@app.route("/")
def home():
    return render_template("login.html")
# =====================================================
# 10TH STANDARD
# =====================================================
# =====================================================
# Login Check
# =====================================================

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    if username == USERNAME and password == PASSWORD:
        return render_template("home.html")
    else:
        return "Invalid Username or Password"
@app.route("/aptitude_test")
def aptitude_test():
    return render_template("aptitude_test.html")


@app.route("/communication_test")
def communication_test():
    return render_template("communication_test.html")

@app.route("/tenth")
def tenth():
    return render_template("tenth.html")





@app.route("/predict10", methods=["POST"])
def predict10():

    # Get values from form
    tenth_marks = float(request.form["tenth_marks"])
    maths = float(request.form["maths"])
    science = float(request.form["science"])
    english = float(request.form["english"])
    aptitude = float(request.form["aptitude"])
    communication = float(request.form["communication"])

    # Create DataFrame
    student = pd.DataFrame([{

        "tenth_marks": tenth_marks,
        "maths": maths,
        "science": science,
        "english": english,
        "aptitude": aptitude,
        "communication": communication

    }])

    # Predict Group
    prediction = model10.predict(student)

    result = encoder10.inverse_transform(prediction)[0]

    # Prediction Confidence
    probability = model10.predict_proba(student)
    confidence = round(probability.max() * 100, 2)

    # Generate Report
    reasons = generate_reasons(
        result,
        maths,
        science,
        english,
        aptitude,
        communication
    )

    strengths = student_strengths(
        maths,
        science,
        english,
        aptitude,
        communication
    )

    improvement_list = improvements(
        maths,
        science,
        english,
        aptitude,
        communication
    )

    other_group_list = other_groups(result)

    career_list = career_opportunities(result)

    return render_template(

        "result10.html",

        result=result,

        confidence=confidence,

        reasons=reasons,

        strengths=strengths,

        improvements=improvement_list,

        others=other_group_list,

        careers=career_list

    )










# =====================================================
# 12TH STANDARD
# =====================================================

@app.route("/twelfth")
def twelfth():
    return render_template("twelfth.html")


# -------------------------------
# Aptitude Test
# -------------------------------
@app.route("/aptitude_test12", methods=["GET", "POST"])
def aptitude_test12():

    if request.method == "POST":

        score = 0

        answers = {
            "q1": "120",
            "q2": "12",
            "q3": "32",
            "q4": "50",
            "q5": "7",
            "q6": "45",
            "q7": "180",
            "q8": "81",
            "q9": "95",
            "q10": "20"
        }

        for q, ans in answers.items():
            if request.form.get(q) == ans:
                score += 10

        return f"""
        <h1>12th Aptitude Test Result</h1>
        <h2>Your Score: {score}/100</h2>

        <br>

        <a href="/twelfth">
            <button>Back to 12th Prediction</button>
        </a>
        """

    return render_template("aptitude_test12.html")


# -------------------------------
# Communication Test
# -------------------------------
@app.route("/communication_test12", methods=["GET", "POST"])
def communication_test12():

    if request.method == "POST":

        score = 0

        answers = {
            "q1": "a",
            "q2": "b",
            "q3": "c",
            "q4": "a",
            "q5": "b",
            "q6": "c",
            "q7": "a",
            "q8": "b",
            "q9": "c",
            "q10": "a"
        }

        for q, ans in answers.items():
            if request.form.get(q) == ans:
                score += 10

        return f"""
        <h1>12th Communication Test Result</h1>

        <h2>Your Score: {score}/100</h2>

        <br>

        <a href="/twelfth">
            <button>Back to 12th Prediction</button>
        </a>
        """

    return render_template("communication_test12.html")

# -------------------------------
# Career Interest Test
# -------------------------------
@app.route("/career_interest12", methods=["GET", "POST"])
def career_interest12():

    if request.method == "POST":

        choices = []

        for i in range(1, 11):
            choices.append(request.form.get(f"q{i}"))

        count = {
            "Engineering": choices.count("Engineering"),
            "Medical": choices.count("Medical"),
            "Commerce": choices.count("Commerce"),
            "Arts": choices.count("Arts"),
            "IT": choices.count("IT")
        }

        result = max(count, key=count.get)

        return f"""
        <h1>🎯 Career Interest Result</h1>

        <h2>Your Interest Area: {result}</h2>

        <p>This result is based on your responses to the Career Interest Test.</p>

        <br>

        <a href="/twelfth">
            <button>Back to 12th Prediction</button>
        </a>
        """

    return render_template("career_interest_test12.html")
# -------------------------------
# Predict Degree
# -------------------------------
@app.route("/predict12", methods=["POST"])
def predict12():

    # Get form values
    tenth = float(request.form["tenth_marks"])
    twelfth = float(request.form["twelfth_marks"])
    stream = request.form["stream"]
    aptitude = float(request.form["aptitude"])
    communication = float(request.form["communication"])

    # Create DataFrame
    student = pd.DataFrame([{
        "level": "12th",
        "tenth_marks": tenth,
        "twelfth_marks": twelfth,
        "stream": stream,
        "aptitude": aptitude,
        "communication": communication
    }])

    # Convert categorical column
    student = pd.get_dummies(student)

    # Match training columns
    df12 = pd.read_csv("12th.csv")

    X12 = df12.drop("target", axis=1)
    X12 = pd.get_dummies(X12)

    student = student.reindex(columns=X12.columns, fill_value=0)

    # Prediction
    prediction = model12.predict(student)

    degree = encoder12.inverse_transform(prediction)[0]

    # Confidence
    probability = model12.predict_proba(student)
    confidence = round(probability.max() * 100, 2)

    # ==========================
    # Reasons
    # ==========================

    reasons = []

    if tenth >= 450:
        reasons.append("Excellent 10th Standard performance.")
    elif tenth >= 400:
        reasons.append("Good 10th Standard performance.")

    if twelfth >= 550:
        reasons.append("Excellent 12th Standard marks.")
    elif twelfth >= 500:
        reasons.append("Good 12th Standard marks.")

    reasons.append(f"You studied in the {stream} stream.")

    if aptitude >= 80:
        reasons.append("Excellent aptitude skills.")

    if communication >= 70:
        reasons.append("Good communication skills.")

    reasons.append(
        f"Based on your academic performance and Machine Learning prediction, '{degree}' is the most suitable degree."
    )

    # ==========================
    # Strengths
    # ==========================

    strengths = []

    if tenth >= 400:
        strengths.append("Strong SSLC Performance")

    if twelfth >= 500:
        strengths.append("Strong HSC Performance")

    if aptitude >= 80:
        strengths.append("Excellent Aptitude Skills")

    if communication >= 70:
        strengths.append("Good Communication Skills")

    if len(strengths) == 0:
        strengths.append("You have good potential to improve.")

    # ==========================
    # Improvements
    # ==========================

    improvements = []

    if tenth < 400:
        improvements.append("Improve your academic foundation.")

    if twelfth < 500:
        improvements.append("Improve subject knowledge.")

    if aptitude < 80:
        improvements.append("Practice aptitude questions regularly.")

    if communication < 70:
        improvements.append("Improve communication skills.")

    if len(improvements) == 0:
        improvements.append("Excellent performance. Keep it up!")

    # ==========================
    # Other Degree Suggestions
    # ==========================

    others = [
        "Consider other degrees based on your interests.",
        "Choose a course that matches your passion.",
        "Explore multiple career opportunities before making a decision."
    ]

    # ==========================
    # Career Opportunities
    # ==========================

    if degree == "B.E Computer Science":

        careers = [
            "Software Engineer",
            "AI Engineer",
            "Web Developer",
            "Data Scientist",
            "Cyber Security Engineer",
            "Cloud Engineer"
        ]

    elif degree == "MBBS":

        careers = [
            "Doctor",
            "Surgeon",
            "Medical Officer",
            "Dentist",
            "Research Scientist"
        ]

    elif degree == "B.Com":

        careers = [
            "Chartered Accountant",
            "Financial Analyst",
            "Bank Officer",
            "Auditor",
            "Tax Consultant"
        ]

    elif degree == "B.A English":

        careers = [
            "Teacher",
            "Journalist",
            "Content Writer",
            "Civil Service",
            "Public Relations Officer"
        ]

    else:

        careers = [
            "Many career opportunities are available.",
            "Choose the degree based on your interests."
        ]

    return render_template(
        "result12.html",
        result=degree,
        confidence=confidence,
        reasons=reasons,
        strengths=strengths,
        improvements=improvements,
        others=others,
        careers=careers
    )
# =====================================================
# COLLEGE
# =====================================================

@app.route("/college")
def college():
    return render_template("college.html")


@app.route("/predict3", methods=["POST"])
def predict3():

    cgpa = float(request.form["cgpa"])
    technical = float(request.form["technical_skill"])
    aptitude = float(request.form["aptitude"])
    certifications = int(request.form["certifications"])
    projects = int(request.form["projects"])
    communication = float(request.form["communication"])

    student = pd.DataFrame([{
        "level": "College",
        "cgpa": cgpa,
        "technical_skill": technical,
        "aptitude": aptitude,
        "certifications": certifications,
        "projects": projects,
        "communication": communication
    }])

    # Convert categorical values
    student = pd.get_dummies(student)

    # Read training dataset
    df3 = pd.read_csv("college.csv")

    X3 = df3.drop("target", axis=1)
    X3 = pd.get_dummies(X3)

    # Match training columns
    student = student.reindex(columns=X3.columns, fill_value=0)

    # Prediction
    prediction = model3.predict(student)

    career = encoder3.inverse_transform(prediction)[0]

    # Prediction Confidence
    probability = model3.predict_proba(student)
    confidence = round(probability.max() * 100, 2)

    # =====================================
    # WHY ML RECOMMENDED THIS CAREER
    # =====================================

    reasons = []

    if cgpa >= 8.5:
        reasons.append("Excellent CGPA indicates strong academic performance.")
    elif cgpa >= 7.5:
        reasons.append("Good academic performance.")

    if technical >= 80:
        reasons.append("Excellent technical skills.")

    if aptitude >= 80:
        reasons.append("Excellent logical and analytical ability.")

    if certifications >= 2:
        reasons.append("Completed multiple certifications.")

    if projects >= 3:
        reasons.append("Good practical project experience.")

    if communication >= 70:
        reasons.append("Good communication skills.")

    reasons.append(
        f"Based on these features, the Machine Learning model predicts '{career}' as your most suitable career."
    )

    # =====================================
    # STRENGTHS
    # =====================================

    strengths = []

    if cgpa >= 8:
        strengths.append("Strong Academic Performance")

    if technical >= 80:
        strengths.append("Excellent Technical Skills")

    if aptitude >= 80:
        strengths.append("Excellent Problem Solving")

    if certifications >= 2:
        strengths.append("Industry Certifications")

    if projects >= 3:
        strengths.append("Real-world Project Experience")

    if communication >= 70:
        strengths.append("Good Communication Skills")

    if len(strengths) == 0:
        strengths.append("You have the potential to improve with practice.")

    # =====================================
    # IMPROVEMENTS
    # =====================================

    improvements = []

    if cgpa < 8:
        improvements.append("Improve your CGPA.")

    if technical < 80:
        improvements.append("Practice coding to improve technical skills.")

    if aptitude < 80:
        improvements.append("Practice aptitude questions regularly.")

    if certifications < 2:
        improvements.append("Complete more certifications.")

    if projects < 3:
        improvements.append("Build more real-time projects.")

    if communication < 70:
        improvements.append("Improve communication skills.")

    if len(improvements) == 0:
        improvements.append("Excellent profile. Continue learning new technologies.")

    # =====================================
    # WHY OTHER CAREERS ARE NOT RECOMMENDED
    # =====================================

    others = []

    if career == "Java Developer":

        others = [
            "Data Analyst requires stronger data analysis skills.",
            "AI Engineer requires advanced Machine Learning knowledge.",
            "Cloud Engineer requires cloud platform experience."
        ]

    elif career == "Data Analyst":

        others = [
            "Java Developer requires stronger software development skills.",
            "AI Engineer requires Machine Learning knowledge.",
            "Cloud Engineer requires cloud deployment skills."
        ]

    elif career == "AI Engineer":

        others = [
            "Java Developer focuses mainly on software development.",
            "Cloud Engineer requires DevOps and Cloud knowledge.",
            "Data Analyst focuses more on business analytics."
        ]

    else:

        others = [
            "Other careers require different technical skills.",
            "The AI model found your profile more suitable for the recommended career.",
            "You can still choose another career with additional learning."
        ]

    # =====================================
    # CAREER OPPORTUNITIES
    # =====================================

    if career == "Java Developer":

        careers = [
            "Software Engineer",
            "Backend Developer",
            "Spring Boot Developer",
            "Full Stack Developer",
            "Android Developer",
            "Microservices Developer"
        ]

    elif career == "Data Analyst":

        careers = [
            "Business Analyst",
            "Data Scientist",
            "BI Developer",
            "SQL Developer",
            "Analytics Consultant"
        ]

    elif career == "AI Engineer":

        careers = [
            "Machine Learning Engineer",
            "AI Engineer",
            "Deep Learning Engineer",
            "NLP Engineer",
            "Computer Vision Engineer"
        ]

    elif career == "Cloud Engineer":

        careers = [
            "AWS Engineer",
            "Azure Engineer",
            "DevOps Engineer",
            "Cloud Architect",
            "Site Reliability Engineer"
        ]

    else:

        careers = [
            "Many excellent career opportunities are available in this field."
        ]

    # =====================================
    # SKILL GAP ANALYSIS
    # =====================================

    skill_gap = []

    if technical < 80:
        skill_gap.append("Improve Technical Skills")

    if communication < 70:
        skill_gap.append("Improve Communication Skills")

    if certifications < 2:
        skill_gap.append("Complete More Certifications")

    if projects < 3:
        skill_gap.append("Build More Real-Time Projects")

    if aptitude < 80:
        skill_gap.append("Practice Aptitude")

    if len(skill_gap) == 0:
        skill_gap.append("No major skill gaps found.")

    return render_template(
        "result3.html",
        result=career,
        confidence=confidence,
        reasons=reasons,
        strengths=strengths,
        improvements=improvements,
        others=others,
        careers=careers,
        skill_gap=skill_gap
    )
# =====================================================
# Run Flask
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)