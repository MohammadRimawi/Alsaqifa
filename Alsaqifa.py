from flask import Flask, render_template, request, session
from flask_assets import Environment, Bundle
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(host = "localhost",user="root",passwd="",database = "Alsaqifa")


css = Bundle('css/general.css', output = "gen/main.css")

bundles = {
    "slider.js": Bundle("javascript/slider.js", output = "gen/slider.js"),
    "general.css": Bundle('css/general.css', output = "gen/general.css"),
    "general.js": Bundle('javascript/general.js', output = "gen/general.js"),
    "home.css": Bundle('css/home.css', output = "gen/home.css"),
}

assets = Environment(app)

assets.register(bundles)

class Card:
    def __init__(self,title,description,image_url):
        self.title = title
        self.description = description
        self.image_url = image_url
        

class Widget:
    widgets = []
    def __init__(self,widget_title,cards,descriptive=False,shuffle=True):
        self.widget_title=widget_title
        self.cards=cards
        self.descriptive = descriptive
        self.shuffle=shuffle


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

    Widget.widgets=[]
    Widget.widgets.append(Widget(
        widget_title="w1",
        cards=[
            Card(title="test1",description="Hello this is test",image_url="noimage"),
            Card(title="test1",description="Hello this is test",image_url="noimage"),
            Card(title="test1",description="Hello this is test",image_url="noimage"),
            # Card(title="test1",description="Hello this is test",image_url="noimage"),
            # Card(title="test1",description="Hello this is test",image_url="noimage"),
        ],
        descriptive=False
    ))

    Widget.widgets.append(Widget(
        widget_title="w2",
        cards=[
            Card(title="test1",description="Hello this is test",image_url="noimage"),
            Card(title="test1",description="Hello this is test",image_url="noimage"),
            Card(title="test1",description="Hello this is test",image_url="noimage"),
            Card(title="test1",description="Hello this is test",image_url="noimage"),
            Card(title="test1",description="Hello this is test",image_url="noimage"),
            Card(title="test1",description="Hello this is test",image_url="noimage"),
            Card(title="test1",description="Hello this is test",image_url="noimage"),
        ],
        descriptive=True
    ))

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
    return render_template("index.html",Menu=Menu,Widget=Widget)

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