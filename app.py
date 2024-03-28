from flask import Flask, render_template, request, redirect, flash, session, jsonify
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define the path to the JSON file
JSON_FILE_PATH = 'todos.json'

# Load to-do list from JSON file
def load_todos():
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save to-do list to JSON file
def save_todos(todos):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(todos, file, indent=4)

# Route to render the login page
@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            if username == 'admin' and password == '12345':
                session['logged_in'] = True  # Set session only after successful login
                return redirect('/table')
            else:
                flash('Invalid username or password. Please try again.', 'error')
                return redirect('/')
        else:
            flash('Please provide both username and password.', 'error')
            return redirect('/')

# Route to render the table page
@app.route("/table", methods=['GET', 'POST'])
def table():
    if not session.get('logged_in'):
        return redirect('/')

    if request.method == 'POST':
        data = request.form  # Get form data from the request
        name = data.get('name')
        category = data.get('category')
        price = data.get('price')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Generate timestamp dynamically
        todos = load_todos()
        todos.append({'name': name, 'category': category, 'price': price, 'timestamp': timestamp})
        save_todos(todos)
        return redirect('/table')

    todos = load_todos()
    print("Loaded todos:", todos)  # Add this debug statement
    return render_template('table.html', todos=todos)

# Route to delete a budget item
@app.route("/delete", methods=['POST'])
def delete_todo():
    try:
        todo_id = int(request.form.get('id'))
        todos = load_todos()
        if 0 <= todo_id < len(todos):
            del todos[todo_id]
            save_todos(todos)
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="Invalid todo ID")
    except Exception as e:
        return jsonify(success=False, error=str(e))

# Run the application
if __name__ == "__main__":
    app.run(debug=True)