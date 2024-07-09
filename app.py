import random
from flask import Flask, render_template, request
import os

rsp = ['가위', '바위', '보']
app = Flask(__name__)

# 초기 무승부, 승리, 패배 초기화 (기본)
draw = 0
win = 0
lose = 0


@app.route('/')
def home():
    # 초기화한 무승부/승/패 기록을 HTML에 렌더링하여 전달(우선)
    return render_template('index.html')


while True:
    player = input('가위,바위,보 중 하나를 선택하세요. ')
    computer = random.choice(rsp)
    print(computer)

    if player not in rsp:
        print("다시 내세요.")
        continue

    if player == computer:
        draw += 1
        print('무')
    elif (computer == '가위' and player == '바위') or (computer == '바위' and player == '보') or (
            computer == '보' and player == '가위'):
        win += 1
        print('승')
    else:
        lose += 1
        print('패')
print()
