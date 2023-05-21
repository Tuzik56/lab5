from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db", user="postgres", password="sysiskakolbosa", host="localhost", port="5432")
cursor = conn.cursor()


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login") or request.form.get("signout"):
            login = request.form.get('login')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(login), str(password)))
            records = list(cursor.fetchall())

            if login and password and records:
                return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
            else:
                return redirect('/login')
        elif request.form.get("registration"):
            return redirect("/registration")
    return render_template('login.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        login = request.form.get('login')
        password = request.form.get('password')

        if username and login and password:
            if (not("  " in username or " " in login or " " in password)) and username != " ":
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);', (str(username), str(login), str(password)))
                conn.commit()
                return redirect('/login')
        else:
            redirect('/registration')

    return render_template('registration.html')


app.run()
