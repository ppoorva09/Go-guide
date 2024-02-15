from flask import Flask
# from godelv.forms.RegistrationForm import RegistrationForm
# from godelv.forms.LoginForm import LoginForm
from flask_bcrypt import Bcrypt
import pymysql
# from flask_mail import Mail


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = '7981c387e281b6f0bc719f5259a2b2cd'


from datamining import routes
