from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Criar banco de dados e tabela
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        registration_date TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        registration_date = request.form['registration_date']
        
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, registration_date) VALUES (?, ?, ?)",
                       (name, age, registration_date))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
