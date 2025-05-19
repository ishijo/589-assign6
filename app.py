from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

# Replace these values with your actual credentials
server = 'assignment6-sqlserver-ishijo.database.windows.net'
database = 'assignment6-sqldb'
username = 'ishijo'
password = '456012ij@'
driver = '{ODBC Driver 17 for SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

def get_conn():
    return pyodbc.connect(conn_str)

@app.route('/')
def index():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employees")
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    email = request.form['email']
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Employees (Name, Email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Employees WHERE ID = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_conn()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cursor.execute("UPDATE Employees SET Name=?, Email=? WHERE ID=?", (name, email, id))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        cursor.execute("SELECT * FROM Employees WHERE ID = ?", (id,))
        employee = cursor.fetchone()
        conn.close()
        return render_template('edit.html', employee=employee)
    

if __name__ == '__main__':
    app.run(debug=True)
