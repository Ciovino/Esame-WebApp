from flask import Flask, render_template, redirect, request, url_for

app= Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/registrati')
def registrati():
    return render_template('registrati.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    return redirect(url_for('homepage'))

@app.route('/add_new_user', methods=['POST'])
def add_new_user():
    return redirect(url_for('homepage'))