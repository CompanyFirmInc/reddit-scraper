from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    # add sql queries here for extra pizzazz
    return render_template('index.html')