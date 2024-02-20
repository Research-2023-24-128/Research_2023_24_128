from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb+srv://dmp:d1234@cluster0.2euzljg.mongodb.net/')
db = client['memory_game']
user_collection = db['user']

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phoneNo = request.form['phoneNo']
        username = request.form['newUsername']
        password = request.form['newPassword']
        confirm_password = request.form['confirmPassword']

        # Check if passwords match
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match")

        hashed_password = generate_password_hash(password, method='sha256')

        # Use user_collection for registration
        user_collection.insert_one({
            'name': name,
            'email': email,
            'phoneNo': phoneNo,
            'username': username,
            'password': hashed_password
        })

        return redirect(url_for('login'))

    return render_template('register.html')

# Login page
@app.route('/login')
def login():
    return render_template('login.html')

# Main page (after login)
@app.route('/main')
def main():
    if 'username' in session:
        return render_template('main.html', username=session['username'])
    return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
