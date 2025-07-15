from flask import Flask, render_template, request, url_for, flash, jsonify
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'some_random_data'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "inventory"

mysql = MySQL(app)

@app.route('/')
def Index():
    cursor = mysql.connection.cursor() 
    cursor.execute("SELECT * FROM soft_drinks_tbl")
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('index.html', drinks=data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name_of_drink']
        price = request.form['price']
        quantity = request.form['quantity']
        expiry_date = request.form['expiry_date']
        batch_number = request.form['batch_number']
        drink_subtype = request.form['drink_subtype']
        
        cursor = mysql.connection.cursor()  
        cursor.execute("INSERT INTO soft_drinks_tbl (name_of_drink, price, quantity, expiry_date, batch_number, drink_subtype) VALUES (%s, %s, %s, %s, %s, %s)", (name, price, quantity, expiry_date, batch_number, drink_subtype))
        mysql.connection.commit()
        cursor.close()
        flash("Record Inserted Successfully")
        return redirect(url_for('Index'))

@app.route('/details', methods=['GET'])
def details():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM soft_drinks_tbl")
    data = cursor.fetchall()
    cursor.close()
    return jsonify({ "data": data })
    

@app.route('/delete/<int:id>', methods=["POST", "DELETE"])
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM soft_drinks_tbl WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash("Record Deleted Successfully")
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(debug=True)