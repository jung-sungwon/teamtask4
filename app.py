import random
from flask import Flask, render_template, request, session
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션을 사용하기 위한 비밀 키
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class RPS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.String, nullable=False)
    user_choice = db.Column(db.String, nullable=False)
    # 'win', 'lose', or 'draw'
    computer_choice = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'RPS(id={self.id}, result={self.result}, computer_choice={self.computer_choice}, user_choice={self.user_choice})'


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    # 초기화한 무승부/승/패 기록을 세션에 저장
    session['win'] = 0
    session['lose'] = 0
    session['draw'] = 0
    return render_template('index.html', win=session['win'], lose=session['lose'], draw=session['draw'])


def play(user_choice):
    choices = ['가위 ✌️', '바위 ✊', '보 ✋']
    computer_choice = random.choice(choices)

    result = ""
    if user_choice not in choices:
        result = "유효 값이 아닙니다."
    elif user_choice == computer_choice:
        session['draw'] += 1
        result = "비겼습니다"
    elif (user_choice == "바위 ✊" and computer_choice == "가위 ✌️") or (user_choice == "보 ✋" and computer_choice == "바위 ✊") or (user_choice == "가위 ✌️" and computer_choice == "보 ✋"):
        session['win'] += 1
        result = "유저 승리!"
    else:
        session['lose'] += 1
        result = "컴퓨터 승리!"

    new_result = RPS(result=result, user_choice=user_choice,
                     computer_choice=computer_choice)
    db.session.add(new_result)
    db.session.commit()
    return result, user_choice, computer_choice


@app.route('/play', methods=['POST'])
def play_game():
    user_choice = request.form.get('choice')
    result, user_choice, computer_choice = play(user_choice)
    return render_template('index.html', user_choice=user_choice, computer_choice=computer_choice, result=result, win=session['win'], draw=session['draw'], lose=session['lose'])


if __name__ == '__main__':
    app.run(debug=True)
