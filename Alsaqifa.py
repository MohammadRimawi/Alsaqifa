from flask import Flask, render_template, request, session
from flask_assets import Environment, Bundle
# from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import mysql.connector



app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:00000000@localhost/Alsaqifa'
# db = SQLAlchemy(app)

 
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '00000000'
# app.config['MYSQL_DB'] = 'Alsaqifa'

# mysql = MySQL(app)

db = mysql.connector.connect(host = "localhost",user="root",passwd="",database = "Alsaqifa")
# class User(db.Model):
#     __tablename__="users"
#     user_id = db.Column("user_id",db.Integer,primary_key=True)
#     full_name = db.Column("full_name",db.String(100))
#     image_url = db.Column("image_url",db.String(100))
#     title = db.Column("title",db.String(100))

css = Bundle('css/general.css', output = "gen/main.css")

bundles = {
    "slider.js": Bundle("javascript/slider.js", output = "gen/slider.js"),
    "general.css": Bundle('css/general.css', output = "gen/general.css"),
    "general.js": Bundle('javascript/general.js', output = "gen/general.js"),
    "home.css": Bundle('css/home.css', output = "gen/home.css"),
}

assets = Environment(app)

assets.register(bundles)


class Menu:
    menu={}
    active="/"
    def __init__(self,name,link):
        self.name=name
        self.link=link
    
    
    @staticmethod
    def load_menu():
        Menu.menu["/registration"]=(Menu("تسجيل دخول","/registration"))
        Menu.menu["#1"]=(Menu("البرامج الاذاعية","#"))
        Menu.menu["/"]=(Menu("الصفحة الرئيسية","/"))
        Menu.menu["#2"]=(Menu("البرامج الاذاعية","#"))
        Menu.menu["#3"]=(Menu("البرامج الاذاعية","#"))



@app.route('/')
def index():
    cur = db.cursor()
    cur.execute("select * from users where user_id = 1")
    for i in cur:
        print(i)
    cur.close()
        
    # # # User.query.filter_by(id=1)
    # # mysql.connection.commit()
    # cur.execute('''SELECT * FROM users''')
    # rv = cur.fetchall()
    # print(str(rv))
    # cur.close()
    Menu.active="/"
    return render_template("index.html",Menu=Menu)

@app.route('/registration')
def registration():
    Menu.active="/registration"
    return render_template("registration.html",Menu=Menu)

@app.route("/posts/<title>")
def posts(title):
    Menu.active="" 
    return render_template("posts.html",title=title,Menu=Menu)



if __name__ == '__main__':
    Menu.load_menu()
 
    app.run(host = '0.0.0.0', debug = True)