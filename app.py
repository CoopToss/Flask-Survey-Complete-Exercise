from flask import Flask, render_template, redirect, url_for, request, flash, session
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CoopToss'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['responses'] = []
        return redirect(url_for('question', question_num=0))
    return render_template('index.html', survey_title=satisfaction_survey.title, survey_instructions=satisfaction_survey.instructions)

@app.route('/questions/<int:question_num>', methods=['GET', 'POST'])
def question(question_num):
    responses = session.get('responses', [])
    if question_num < len(satisfaction_survey.questions):
        if len(responses) == question_num:
            if request.method == 'POST':
                selected_choice = request.form['choice']
                responses.append(selected_choice)
                session['responses'] = responses
            question = satisfaction_survey.questions[question_num]
            return render_template('question.html', question=question, question_num=question_num)
        else:
            flash("Please complete the previous question first.")
            return redirect(url_for('question', question_num=len(responses)))
    else:
        return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == "__main__":
    app.run(debug=True)
