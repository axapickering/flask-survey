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
    return render_template("survey_start.html",survey=survey)

@app.post("/begin")
def begin():
    return redirect("/questions/0")

@app.get("/questions/<int:question_number>")
def display_question(question_number):
    return render_template("/question.html",question=survey.questions[question_number],question_number=question_number)

@app.post("/answer/<int:question_number>")
def answer_to_question(question_number):
    responses.append(request.form['answer'])
    next_question = question_number + 1
    return redirect('/question/{question_number+1}')