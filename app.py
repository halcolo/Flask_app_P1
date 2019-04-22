from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash


mysql = MySQL()
app = Flask(__name__)


# MySQL configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')


# Procedure to signUp an user using Jquery/AJAX
@app.route("/signUp", methods=['POST'])
def signUp():

    try:
        # Creating the signUp procedure
        #
        # Read the posted values in Jquery
        _name =  request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']


        if _name and _email and _password:


            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
            return json.dumps({'html':'<span>All the fields are good!</span>'})
        else:
            return json.dumps({'html':'<span>Enter all the fields</span>'})


    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()
        

if __name__ == "__main__":
    app.run()
