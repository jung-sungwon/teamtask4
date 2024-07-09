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
    return render_template('index.html')
