from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (name_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    password TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS scammers
                     (name_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                     age_range TEXT NOT NULL,
                     scam_type TEXT NOT NULL,
                     country_code TEXT NOT NULL,
                     scammer_number TEXT NOT NULL,
                     message TEXT NOT NULL,

                     FOREIGN KEY (name_id) REFERENCES users (name_id))''')

    conn.commit()
    conn.close()


# Start page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT name, password
                    FROM users
                    ''')
        datas = cursor.fetchall()
        conn.close()
        try:
          for data in datas:
            if data[0] == username and data[1] == password:
              return render_template('index.html')
        except:
          return render_template('login.html', error='Invalid username or password.')
    
    return render_template('login.html')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
  conn = sqlite3.connect('app.db')
  cursor = conn.cursor()  
  if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = 'Passwords do not match.'
            return render_template('register.html', error=error)

        else:
          with open('info.txt', 'a') as file:
            file.write(username + ' ' + password + ' ' + confirm_password + ' \n')  
          cursor.execute('INSERT INTO users (name, password) VALUES (?, ?)', (username, password))
          conn.commit()
          conn.close()
          notif = 'You have been registered'
          return render_template('register.html', notif=notif)
  else:
    return render_template('register.html')

        
        
# 
@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/fraud", methods=['GET', 'POST'])
def list():
  conn = sqlite3.connect('app.db')
  cursor = conn.cursor()
  cursor.execute('''SELECT name_id
                    FROM users
                    ''')
  id = cursor.fetchall()
  conn.close()
  return render_template("fraud.html", id = id)

@app.route("/result", methods=['GET', 'POST'])
def result():
  return render_template("result.html")

@app.route("/report", methods=['GET','POST'])
def report():
  conn = sqlite3.connect('app.db')
  cursor = conn.cursor()
  if request.method == 'POST':
        name_id = None
        age = None
        type = None
        ccode = None
        number = None
        description = None
        name_id = request.form.get('name_id')
        age = request.form.get('age')
        type = request.form.get('type')
        ccode= request.form.get('ccode')
        number = request.form.get('info')
        description = request.form.get('desc')
        with open('data.txt', 'a') as file:
          file.write(name_id + ' ' + age + ' ' + type + ' '  + ccode + ' ' + number + ' ' + description + ' ' + ' \n')
        cursor.execute('INSERT INTO scammers (name_id, age_range, scam_type, country_code, scammer_number, message) VALUES (?, ?, ?, ?, ?, ?)', (name_id, age, type, ccode, number, description))
        conn.commit()
        conn.close()
        
  return render_template("report.html")
  






@app.route("/call", methods=['GET'])
def call():
  conn = sqlite3.connect('app.db')
  cursor = conn.cursor()
  cursor.execute('''SELECT age_range, country_code, scammer_number, message
                    FROM scammers
                    WHERE scam_type = "Call"''')
  results = cursor.fetchall()
  conn.close()
  return render_template("call.html", results=results)

@app.route("/message", methods=['GET'])
def message():
  conn = sqlite3.connect('app.db')
  cursor = conn.cursor()
  cursor.execute('''SELECT age_range, country_code, scammer_number, message
                    FROM scammers
                    WHERE scam_type = "Messages"''')
  results = cursor.fetchall()
  conn.close()
  return render_template("message.html", results=results)

@app.route("/success", methods=['GET', 'POST'])
def success():
  conn = sqlite3.connect('app.db')
  cursor = conn.cursor()
  if request.method == 'POST':
        name_id = None
        age = None
        type = None
        ccode = None
        number = None
        description = None
        name_id = request.form.get('name_id')
        age = request.form.get('age')
        type = request.form.get('type')
        ccode = request.form.get('ccode')
        number = request.form.get('info')
        description = request.form.get('desc')
        with open('data.txt', 'a') as file:
          file.write(name_id + ' ' + age + ' ' + type + ' '  + ccode + ' ' + number + ' ' + description + ' ' + ' \n')
        cursor.execute('INSERT INTO scammers (name_id, age_range, scam_type, country_code, scammer_number, message) VALUES (?, ?, ?, ?, ?, ?)', (name_id, age, type, ccode, number, description))
        conn.commit()
        conn.close()
  return render_template("success.html")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=81)