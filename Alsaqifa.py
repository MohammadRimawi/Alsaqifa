from flask import Flask, render_template, request, session
from flask_assets import Environment, Bundle
import mysql.connector

from utility import *

app = Flask(__name__)


db = mysql.connector.connect(host = "localhost",user="root",passwd="000000",database = "Alsaqifa")


css = Bundle('css/general.css', output = "gen/main.css")

bundles = {
    "slider.js": Bundle("javascript/slider.js", output = "gen/slider.js"),
    "general.css": Bundle('css/general.css', output = "gen/general.css"),
    "general.js": Bundle('javascript/general.js', output = "gen/general.js"),
    "home.css": Bundle('css/home.css', output = "gen/home.css"),
     "home.css": Bundle('modules/ckeditor5/ckeditor.css', output = "gen/ckeditor.css"),
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
        Menu.menu["/podcasts"]=(Menu("البرامج الاذاعية","/podcasts"))
        Menu.menu["#3"]=(Menu("البرامج الاذاعية","#"))

editor_mode = True
editor_mode = False


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
        
    Menu.active="/"
    return render_template("index.html",Menu=Menu,Widget=Widget,editor_mode=editor_mode)

@app.route('/registration')
def registration():
    Menu.active="/registration"
    return render_template("registration.html",Menu=Menu)

@app.route("/posts/<title>")
def posts(title):
    Menu.active="" 
    return render_template("posts.html",title=title,Menu=Menu)

@app.route("/podcasts",defaults={'playlist': None})
@app.route("/podcasts/<playlist>")
def podcast(playlist):
    Menu.active="/podcasts" 
    
    if playlist == None:
        playlist="no playlist"
        
    return render_template("podcast.html",playlist=playlist,Menu=Menu)

@app.route("/tags/<tag>")
def tags(tag):
    return "umm ahhh<br>we didn't finish this page yet!<br><img src='/static//assets/images/whoops.gif'>"

@app.route("/test")
def test():
    return render_template("test.html")
    
@app.route("/playlist/<playlist_name>")
def playlist(playlist_name):

    playlist_name = parse_in(playlist_name)

    try:
        cur = db.cursor(dictionary=True)
        
        playlist_name_sql = "select * from playlists where name = '"+playlist_name+"'"
        cur.execute(playlist_name_sql)
        playlist_name_result = list(cur)
        
        if len(playlist_name_result)>0:
            
            playlists_tracks_sql = "select * from playlists_tracks where playlist_id = "+str(playlist_name_result[0]['playlist_id'])    
            cur.execute(playlists_tracks_sql)

            playlists_tracks_results = list(cur)
            
            tracks_list=[]
            
            for i in playlists_tracks_results:
                
                tracks_list.append(str(i['track_id']))

            
            tracks_sql = "SELECT * FROM tracks WHERE track_id in ("+', '.join(tracks_list)+")"
            cur.execute(tracks_sql)

            tracks_results = list(cur)

            cur.close()

            return render_template("playlist.html",playlist_name=playlist_name,Menu=Menu,tracks_results=tracks_results)
        else: 
            cur.close()
            return "whoops!, we didn't find playlist called "+playlist_name
    except:
        cur.close()
        return "oh no!, something went wrong while getting your playlist called "+playlist_name


if __name__ == '__main__':
    Menu.load_menu()
    app.run(host = '0.0.0.0',debug=True)