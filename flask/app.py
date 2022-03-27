from flask import*


from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chirag'
 
mysql = MySQL(app)



@app.route("/")
def hello_world():
   return render_template('index.html') 

@app.route("/hii",methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO person VALUES(%s,%s)''',(name,roll))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"

if __name__ == '__main__':  
   app.run(debug = True)  