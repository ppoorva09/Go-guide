from datamining.forms.RegistrationForm import RegistrationForm
from datamining.forms.LoginForm import LoginForm
from flask import Flask, render_template, url_for, flash, redirect, session, abort, request, make_response, jsonify
from datamining import app, bcrypt
import pymysql


'''
API File
'''


def dbconnect():
    return pymysql.connect(host="localhost", port=3306, user="root", passwd="12345678", db="datamining",
                                 cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def main():
    return render_template('home.html')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/hotels')
def hotels():
    return render_template('hotels.html')


# @app.route('/restaurants', methods=['GET'])
# def restaurants():
#     connection = dbconnect()
#     cursor = connection.cursor()
#
#     # Extracting filters from request args
#     budget = request.args.get('budget')
#     city = request.args.get('city')
#     cuisine = request.args.get('cuisine')
#
#     # Building SQL query with optional filters
#     query = "SELECT * FROM Restaurants"
#     conditions = []
#     if budget:
#         conditions.append(f"rest_budget <= {budget}")
#     if city:
#         conditions.append(f"rest_city = '{city}'")
#     if cuisine:
#         conditions.append(f"rest_cuisine = '{cuisine}'")
#
#     if conditions:
#         query += " WHERE " + " AND ".join(conditions)
#
#     # Executing SQL query
#     cursor.execute(query)
#     rows = cursor.fetchall()
#     tablerows = []
#
#     if not rows:
#         # No restaurants found
#         return render_template('restaurants.html', no_results=True)
#
#     for row in rows:
#         tablerows.append({
#             "rest_name": row['rest_name'],
#             "rest_city": row['rest_city'],
#             "rest_cuisine": row['rest_cuisine'],
#             "rest_budget": row['rest_budget']
#         })
#
#     cursor.close()
#     return render_template('restaurants.html', tablerows=tablerows)


@app.route('/restaurants', methods=['GET'])
def restaurants():
    connection = dbconnect()
    cursor = connection.cursor()

    # Extracting filters from request args
    budget = request.args.get('budget')
    city = request.args.get('city')
    cuisine = request.args.get('cuisine')

    # Building SQL query with optional filters
    query = "SELECT * FROM Restaurants"
    conditions = []
    if budget:
        conditions.append(f"rest_budget <= {budget}")
    if city:
        conditions.append(f"rest_city = '{city}'")
    if cuisine:
        conditions.append(f"rest_cuisine = '{cuisine}'")

    if len(conditions) > 0:
        query += " WHERE " + " AND ".join(conditions)

    # Executing SQL query
    cursor.execute(query)
    rows = cursor.fetchall()
    tablerows = []

    if len(rows) > 0:
        for row in rows:
            tablerows.append({
                "rest_name": row['rest_name'],
                "rest_city": row['rest_city'],
                "rest_cuisine": row['rest_cuisine'],
                "rest_budget": row['rest_budget']
            })
    else:
        return render_template('restaurants.html', no_results=True)


    cursor.close()
    return render_template('restaurants.html', tablerows=tablerows)


@app.route('/register', methods=['GET', 'POST'])
def register():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    form = RegistrationForm()

    if form.submitRegistration.data and form.validate():
        # check if user exists
        '''
            for my reference
            cursor.execute() returns list of dictionary(records of table)
        '''
        cursor.execute("SELECT email_id FROM User WHERE email_id = % s", (form.email.data))
        query_op = cursor.fetchall()
        if (len(query_op) > 0):
            # user exists with same emailid
            flash(f'Account already existed with emailid: {form.email.data}', 'danger')
            return redirect(url_for('register'))
        else:
            # enter user details in User table

            session['userEmail'] = form.email.data
            session['userType'] = form.userType.data


            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            if form.userType.data == 'CUSTOMER':
                cursor.execute('INSERT INTO User VALUES(% s, % s, % s)',
                               (form.email.data, hashed_password, 'CUSTOMER'))

            elif form.userType.data == 'ADMINISTRATOR':
                cursor.execute('INSERT INTO User VALUES(% s, % s, % s',
                               (form.email.data, hashed_password, form.name.data, 'ADMINISTRATOR'))
            connection.commit()

            flash(f'Account created successfully!, {form.email.data}', 'success')

            if form.userType.data == 'CUSTOMER':
                return redirect(url_for('home'))

            elif form.userType.data == 'ADMINISTRATOR':
                return redirect(url_for('adminhome'))

    cursor.close()
    return render_template('register.html', page_title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    form = LoginForm()
    if form.validate_on_submit():
        cursor.execute('SELECT * FROM User WHERE email_id = % s', (form.id.data))
        userDBData = cursor.fetchone()

        if userDBData and bcrypt.check_password_hash(userDBData['password'], form.password.data):
            flash('You have been logged in!', 'success')
            session['userEmail'] = userDBData['email_id']
            session['userType'] = userDBData['usertype']


            if session['userType'] == 'CUSTOMER':
                return redirect(url_for('home'))

        else:
            flash('Login Unsuccessful. Please check emailid or password!', 'danger')
            return redirect(url_for('login'))
    cursor.close()

    return render_template('login.html', page_title='Login', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))















