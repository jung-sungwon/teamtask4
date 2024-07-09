import random
from flask import Flask, render_template, request
import os

app = Flask(__name__)

# 초기 무승부, 승리, 패배 초기화 (기본)
draw = 0
win = 0
lose = 0


@app.route('/')
def home():
    # 초기화한 무승부/승/패 기록을 HTML에 렌더링하여 전달(우선)
    return render_template('index.html', win=win, lose=lose, draw=draw)


# 최종 목적은 html 에서 사용자가 가위,바위,보 중 선택하는 것
# 터미널의 input X / 함수 사용
def play(user_choice):
    global draw, win, lose  # draw , win ,lose 은 글로벌 함수
    choices = ['가위', '바위', '보']
    computer_choice = random.choice(choices)

    # result 안에 값을 담을 담기
    result = ""
    if user_choice not in choices:
        result = "유효 값이 아닙니다."
    elif user_choice == computer_choice:
        draw += 1
        result = "비겼습니다"
    elif (user_choice == "바위 ✊" and computer_choice == "가위 ✌️") or (user_choice == "보 ✋" and computer_choice == "바위 ✊") or (user_choice == "가위 ✌️" and computer_choice == "보 ✋"):
        win += 1
        result = "유저 승리!"
    else:
        lose += 1
        reulst = "컴퓨터 승리!"

    return result, user_choice, computer_choice


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/play', methods=['POST'])
def play_game():
    # 사용자가 선택한 값 가져오기
    user_choice = request.form.get('choice')
    result, user_choice, computer_choice = play(user_choice)
    # index.html 템플릿에 렌더링하여 사용자 선택, 컴퓨터 선택, 게임 결과 전달
    return render_template('index.html', user_choice=user_choice, computer_choice=computer_choice, result=result, win=win, draw=draw, lose=lose)


if __name__ == '__main__':
    app.run(debug=True)