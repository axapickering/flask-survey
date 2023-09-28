from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get("/")
def home_page():
    """ Display home page"""

    responses.clear()

    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def begin():
    """ Redirect to first survey question"""

    return redirect("/questions/0")


@app.get("/questions/<int:question_number>")
def display_question(question_number):
    """Display current question"""

    return render_template("/question.html", question=survey.questions[question_number], responses=responses)
    #TODO: only need to pass in list, can use this to determine next q


@app.post("/answer")
def answer_to_question():
    """Get and store question answer, redirect to next question or completion page"""

    next_question = len(responses)
    responses.append(request.form['answer'])
    if next_question == (len(survey.questions)):
        return redirect("/thanks")


    return redirect(f'/questions/{next_question}')


@app.get("/thanks")
def thank_you():
    """Display thank you page with all questions/answers"""

    length = range(len(responses)-1)

    return render_template("completion.html", questions=survey.questions, responses=responses, length=length)
