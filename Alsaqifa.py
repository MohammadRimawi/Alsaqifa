from flask import Flask, render_template, request, session
from flask_assets import Environment, Bundle
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(host = "localhost",user="root",passwd="000000",database = "Alsaqifa")


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
        self.link = ""
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
        Menu.menu["/podcast"]=(Menu("البرامج الاذاعية","/podcast"))
        Menu.menu["#3"]=(Menu("البرامج الاذاعية","#"))



@app.route('/')
def index():
    filler= "لوريم ايبسوم دولار سيت أميت ,كونسيكتيتور أدايبا يسكينج أليايت,سيت دو لار سيت أميت ,كونسيكتيتور أدايبا يسكينج أليايت,سيت دو أيوسمود تيمبور..."
    Widget.widgets=[]
    Widget.widgets.append(Widget(
        widget_title="w1",
        cards=[
            Card(title="test1",description=filler,image_url="noimage"),
            Card(title="test2",description=filler,image_url="noimage"),
            Card(title="test3",description=filler,image_url="noimage"),
            Card(title="test1",description=filler,image_url="noimage"),
            Card(title="test1",description=filler,image_url="noimage"),
            Card(title="test1",description=filler,image_url="noimage"),
        ],
        descriptive=False
    ))

    Widget.widgets.append(Widget(
        widget_title="w2",
        cards=[
            Card(title="<strong>test1</strong>",description=filler,image_url="noimage"),
            Card(title="test2",description=filler,image_url="noimage"),
            Card(title="test3",description=filler,image_url="noimage"),
            Card(title="test4",description=filler,image_url="noimage"),
            Card(title="test5",description=filler,image_url="noimage"),
            Card(title="test6",description=filler,image_url="noimage"),
            Card(title="test7",description=filler,image_url="noimage"),
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

@app.route("/podcast/<playlist>")
def podcast(playlist):
    Menu.active="/podcast" 
    return render_template("podcast.html",playlist=playlist,Menu=Menu)




if __name__ == '__main__':
    Menu.load_menu()
 
    app.run(host = '0.0.0.0', debug = True)