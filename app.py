from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get("/")
def home_page():
    """ Display home page"""

    session["responses"] = []

    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def begin():
    """ Redirect to first survey question"""

    return redirect("/questions/0")


@app.get("/questions/<int:question_number>")
def display_question(question_number):
    """Display current question"""

    response_num = len(session['responses'])

    if response_num == len(survey.questions):
        flash("Once wasn't enough?")
        return redirect("/thanks")
    elif response_num != question_number:
        flash("Hey dummy, stick to the question you're on.")
        return redirect(f'/questions/{response_num}')

    return render_template("/question.html", question=survey.questions[question_number])


@app.post("/answer")
def answer_to_question():
    """Get and store question answer, redirect to next question or completion page"""

    responses = session["responses"]
    responses.append(request.form['answer'])
    session["responses"] = responses

    next_question = len(session["responses"])

    if next_question == (len(survey.questions)):
        return redirect("/thanks")

    return redirect(f'/questions/{next_question}')


@app.get("/thanks")
def thank_you():
    """Display thank you page with all questions/answers"""

    length_list = range(len(session['responses']))

    return render_template("completion.html", questions=survey.questions,length_list=length_list)
