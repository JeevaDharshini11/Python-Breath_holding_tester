from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('start_test', username=username))
    return render_template('index.html')

@app.route('/start_test/<username>')
def start_test(username):
    return render_template('start_test.html', username=username)

@app.route('/result/<username>', methods=['POST'])
def result(username):
    timeElapsed = float(request.form['timeElapsed'])
    if timeElapsed < 20:
        result = "Easy"
        note = "You can improve your lung capacity by practicing deep breathing exercises."
    elif timeElapsed < 40:
        result = "Medium"
        note = "Good job! You have a decent lung capacity. Keep practicing to improve."
    else:
        result = "Hard"
        note = "Excellent! You have a great lung capacity. Keep up the good work!"
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, lung_capacity) VALUES (?, ?)", (username, timeElapsed))
    conn.commit()
    conn.close()
    return render_template('result.html', breath_holding_time=timeElapsed, result=result, note=note, username=username)
@app.route('/leaderboard')
def leaderboard():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT username, lung_capacity FROM users ORDER BY lung_capacity DESC LIMIT 1")
    best_record = c.fetchone()
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]
    conn.close()
    return render_template('leaderboard.html', best_record=best_record, total_users=total_users)

if __name__ == "__main__":
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users
                 (username text, lung_capacity real)""")
    conn.commit()
    conn.close()
    app.run(debug=True)
