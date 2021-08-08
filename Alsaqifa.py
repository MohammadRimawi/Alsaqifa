import json
from flask import Flask,flash, render_template, request, session, jsonify,url_for,redirect
from flask_assets import Environment, Bundle
import requests
from utility import *
import requests, json

from werkzeug.utils import secure_filename

from pprint import pprint

import os

from modules import *
from datetime import datetime,timedelta
from flaskext.markdown import Markdown


app = Flask(__name__)
app.secret_key = os.getenv("SESSION_KEY")

Markdown(app)
# md = Markdown(app, extensions=['fenced_code'])

comments = [
    {   
        "comment_id":"1",
        "user":{
            "name":"فتحي محسن",
        },
        "time":"4/5/2013",
        "text":"مرحبا انا فتحي ارحب بالاعضاء الجدد.",
        "likes":"3",
        "replies":[
            {
                "comment_id":"2",
                "user":{
                "name":"تحسين محسن",
                },
                "time":"4/5/2013",
                "text":"مرحبا بك فتحي.",
                "likes":"1",
                "replies":[]
            },
        ]
    },
]


css = Bundle('css/general.css', output = "gen/main.css")
# static//modules/ckeditor5/build/ckeditor.js
bundles = {
    "ckeditor.js": Bundle("modules/ckeditor5/build/ckeditor.js", output = "gen/ckeditor.js"),
    "slider.js": Bundle("javascript/slider.js", output = "gen/slider.js"),
    "snackbar.js": Bundle("javascript/snackbar.js", output = "gen/snackbar.js"),
    "requests.js": Bundle("javascript/requests.js", output = "gen/requests.js"),
    "general.css": Bundle('css/general.css', output = "gen/general.css"),
    "general.js": Bundle('javascript/general.js', output = "gen/general.js"),
    "home.css": Bundle('css/home.css', output = "gen/home.css"),
    "ckeditor.css": Bundle('modules/ckeditor5/ckeditor.css', output = "gen/ckeditor.css"),
    "flex.css": Bundle('css/flex.css', output = "gen/flex.css"),
    "form.css": Bundle('css/form.css', output = "gen/form.css"),
    "nav.css": Bundle('css/nav.css', output = "gen/nav.css"),
    "media.css": Bundle('css/media.css', output = "gen/media.css"),
    "posts.css": Bundle('css/posts.css', output = "gen/posts.css"),



}

assets = Environment(app)

assets.register(bundles)
api_host="http://rimawidell:5001"




app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


editor_mode = True
editor_mode = False


def get_widgets(data,separated = True):
  
    #TODO Add option to be separated widgets or in one code
    data = json.dumps(data)

    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    tags_posts = requests.post(api_host+"/api/get/posts_by_tag",headers = headers,data=data)
    tags_posts = tags_posts.json()  

    # pprint(tags_posts)

    widgets_list=[]

    for tag in tags_posts['data']['tags']:
        
        cards_list = []
        for post in tag['data']:
            cards_list.append(Card(title=post['title'],description=post['description'],image_url=url_for('static',filename = post['image_url'])))

        widgets_list.append(Widget(
            widget_title=str(tag['name']),
            cards=cards_list,
            descriptive=int(tag['descriptive']),
        ))

    return widgets_list

@app.route('/')
def index():
    menu = Menu.load_menu()

    data = {
            "tags":[
                {
                    "name":"زوجي",
                    "descriptive":"0",
                },
                {
                    "name":"فردي",
                    "descriptive":"1",
                },
            ]
        }

    widgets_list = get_widgets(data)

    try:
        post = requests.get("http://rimawidell:5001/api/post/تيستت-اااااصلي")
        post = post.json()
        post['data']['text']= post['data']['text'].replace("contenteditable='true'","contenteditable='false'")

        # pprint(post["data"]["text"])
    except Exception as e:
        post = {}
        post["data"] = {}
        post["data"]["text"] = "api is off"
        
    menu['active']="/"
    return render_template("index.html",Menu=menu,widgets_list=widgets_list,editor_mode=editor_mode,post= post,session=session,parse_out=parse_out)


@app.route("/test")
def test():
    return render_template("test.html")
    

#--------------------------[ Tags ]---------------------------#

@app.route("/tags/<tag>")
def tags(tag):

    params = {}
    params['cardless'] = 1
    params['page'] = request.args.get('page')
    if params['page'] == None:
        params['page']=1

    data = {
        
        "tags":[
            {
                "name":str(tag),
                "descriptive":"0",
            },
        ]
    }
    data = json.dumps(data)

    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    posts = requests.post(api_host+"/api/get/posts_by_tag",headers = headers,data=data,params=params)
    posts = posts.json()
    
    # pprint(posts)

    menu = Menu.load_menu()
    menu['active'] = "/posts"

    # params = {}
    # params['page'] = request.args.get('page')
    # if params['page'] == None:
    #     params['page']=1

    # headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    # posts = requests.post(api_host+"/api/get/all_posts",headers = headers,params=params)
    # posts = posts.json()  

    return render_template("view/tags.html",Menu=menu,session=session , posts=posts ,parse_out= parse_out)


#--------------------------[ Posts ]--------------------------#

@app.route("/posts")
def all_posts():
    params = {}
    params['page'] = request.args.get('page')
    if params['page'] == None:
        params['page']=1


    menu = Menu.load_menu()

    menu['active'] = "/posts"
    
    response = {}
    response['server message'] = None
    response['status_code'] = 0
    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    posts = requests.post(api_host+"/api/get/all_posts",headers = headers,params=params)
    posts = posts.json()  

    # pprint(posts)


    data = {
        "tags":[
            {
                "name":"زوجي",
                "descriptive":"0",
            },
            {
                "name":"فردي",
                "descriptive":"1",
            },
        ]
    }

    widgets_list = get_widgets(data)

    return render_template("view/posts/all_posts.html",Menu=menu,widgets_list=widgets_list,session=session , posts=posts ,parse_out= parse_out)

@app.route("/posts/<title>")
def posts(title):

    menu = Menu.load_menu()


    data = {
        "tags":[
            {
                "name":"زوجي",
                "descriptive":"0",
            },
            {
                "name":"فردي",
                "descriptive":"1",
            },
        ]
    }

    widgets_list = get_widgets(data)



    menu['active']="" 

    title = parse_in(title)
    try:
        post = requests.get("http://rimawidell:5001/api/post/"+title)
        post = post.json()

        post['data']['text']= post['data']['text'].replace("contenteditable='true'","contenteditable='false'")

 
        url = "http://rimawidell:5001/api/get/comments/"+str(post['data']['post_id'])
        post['data']['comments'] = requests.get(url).json()


        # post['data']['posted_by'] = requests.get("http://rimawidell:5001/api/get/user?user_id="+str(post['data']['posted_by'])).json()['data']
        # post['data']['user_id'] = requests.get("http://rimawidell:5001/api/get/user?user_id="+str(post['data']['user_id'])).json()['data']
        pprint(post["data"]) 



        #TODO Get tags based on user_id and post_id
    except Exception as e:
        post = {}
        post["data"] = {}
        post["data"]["text"] = "api is off"
    return render_template("view/posts/posts.html",title=title,Menu=menu,post=post,widgets_list=widgets_list,session=session,parse_out=parse_out)


#------------------------[ Playlists ]------------------------#

@app.route("/podcasts")
def all_podcasts():

    menu = Menu.load_menu()
    menu['active']="/podcasts" 

    params = {}
    params['page'] = request.args.get('page')
    if params['page'] == None:
        params['page']=1

    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    playlists = requests.post(api_host+"/api/get/all_playlists",headers = headers ,params=params)
    playlists = playlists.json()   

    # pprint(playlists)   

    return render_template("view/podcasts/all_podcasts.html",playlists=playlists,Menu=menu,parse_out=parse_out)

@app.route("/podcasts/<playlist>")
def podcast(playlist):
    # playlists = {}
    menu = Menu.load_menu()
    menu['active']="/podcasts" 


    
    if playlist == None:
        playlist="no playlist"
        
    return render_template("podcast.html",playlist=playlist,Menu=menu)

@app.route("/playlists",methods=['GET','POST'])
def playlists():

    menu = Menu.load_menu()

    response = {}
    response['server message'] = None
    response['status_code'] = 0
    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    playlists = requests.post(api_host+"/api/get/all_playlists",headers = headers)
    playlists = playlists.json()      

    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    tracks = requests.post(api_host+"/api/get/all_tracks",headers = headers)
    tracks = tracks.json()    


    # pprint(playlists)
    # pprint(tracks)  

    if(request.form):
        if request.form['operation'] == "select_playlist":

            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            r = requests.post(url=api_host+"/api/playlist/"+str(request.form["select_playlist_id"]),headers=headers)

            response = r.json()
            
            response['status_code'] = r.status_code
            # pprint(response)
            pass
        
        elif request.form['operation'] == "create_playlist":
            
            data = {
                "name":request.form["name"],
                "visibility":request.form["visibility"]
            }
            data = json.dumps(data)
            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            r = requests.post(url=api_host+"/api/create/playlist",headers=headers,data=data)

            response = r.json()
            response['status_code'] = r.status_code
            # pprint(response)

        elif request.form['operation'] == "update_playlist":
            
            pass

        elif request.form['operation'] == "delete_playlist":

            pass

        elif request.form['operation'] == "upload_track":
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
    
            if file.filename == '':
                flash('No selected file')
            if file and allowed_file(file.filename):
                filename =   secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                                
                # print(filename)
                path = "/audio/"+str(filename)
                # print(path)
                imgpath = "static/"+path

            pass

        elif request.form['operation'] == "update_track":

            pass

        elif request.form['operation'] == "delete_track":

            pass

        elif request.form['operation'] == "add_track_to_playlist":

            pass

        elif request.form['operation'] == "remove_track_from_playlist":

            pass


    # print(response['server message'])
    return render_template(
        "control/playlist_controls.html",
        Menu=menu,
        playlists=playlists,
        tracks=tracks,
        response=response
    )

@app.route("/playlist/<playlist_name>")
def playlist(playlist_name):

    menu = Menu.load_menu()


    try:
        response = requests.get(api_host+'/api/playlist/'+str(playlist_name))
    except:
        return "API NOT AVAILABLE"
        
    if response.status_code == 200:
        data = response.json()
        return render_template("playlist.html",playlist_name=data["playlist_name"],Menu=menu,tracks_results=data["data"])
    elif response.status_code == 404:
        return "whoops!, we didn't find playlist called "+playlist_name
    else:
        return "oh no!, something went wrong while getting your playlist called "+playlist_name


#-------------------- --[ Registration ]----------------------#

@app.route('/registration')
def registration():
    menu = Menu.load_menu()
    # pprint(request.__dict__)
    menu['active']="/registration"
    return render_template("registration.html",Menu=menu,session=session)

@app.route('/registration/login', methods=['GET', 'POST'])
def login():
    
    menu = Menu.load_menu()
    menu['active'] = "/registration/login"


    if request.form :
        if request.form['operation'] == "login":
            # /api/authenticate

            url = "http://rimawidell:5001/api/authenticate"

            data = {
                "username": str(request.form['username']),
                "password": str(request.form['password']), #TODO HASH MEE!!!!!
                "token":"hello"
            }
            data = json.dumps(data)

            # pprint(data)
            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            r = requests.post(url, data=data, headers=headers)

            response = r.json()
            response['status_code'] = r.status_code
            # pprint(response)

            if response['status_code'] == 200:
                session["user_id"] = response['data']['user_id']
                session["name"] =  response['data']['name']
                session["image_url"] =  response['data']['image_url']

                token = make_token()
                session["session_id"] = token

                now = datetime.now()
                creation_date = now.strftime('%Y-%m-%d %H:%M:%S')
                expiration_date = (now + timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')

                data = {
                    "user_id":str(response['data']['user_id']),
                    "creation_date":str(creation_date),
                    "last_touched_date":str(creation_date),
                    "expiration_date":str(expiration_date),
                    "token":str(token)
                }
                data = json.dumps(data)


                headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
                url = "http://rimawidell:5001//api/add_token"

                r = requests.post(url, data=data, headers=headers)

                # pprint(r)
                response['token'] = r.json()
                response['token']['status_code'] = r.status_code

                return redirect("/")
                # TODO Hash this -> remote_addr REMOTE_ADDR
         
    return render_template("view/registration/login.html",Menu=menu,session=session)
    
@app.route('/registration/signup', methods=['GET', 'POST'])
def signup():
    menu = Menu.load_menu()
    menu['active'] = "/registration/signup"
    return render_template("view/registration/signup.html",Menu=menu,session=session)

@app.route('/registration/logout', methods=['GET'])
def logout():
    session.pop("user_id",None)
    session.pop("name",None)
    session.pop("session_id",None)
    session.pop("image_url",None)

    # menu['active']="/"
    return redirect("/")


#-------------------------[ Utility ]-------------------------#

import random
@app.errorhandler(404)
def page_not_found(e):
    s = ['يزم وين رايح؟','بشرفك ارجع!','بتعرف ترجع لحالك ولا اجي ارجعك؟','مش من هون الطريق، ارجع']
    i = random.randint(0, len(s)-1)

    return s[i],404

@app.route("/post_handler" ,methods=['POST'])
def post_handler():

    
    if("HTTP_REFERER" in request.__dict__["environ"].keys()):
        page = request.__dict__["environ"]["HTTP_REFERER"]
        host = request.__dict__["environ"]["HTTP_HOST"]
        # print(host)

    if (request.form or True): #TODO what is this?


        # print(request.form)
        # print("TESSST")
        content = request.form["content"]
        content = content.replace("\"","\'")
        # print(content)
        # content = content.encode("utf-8")
        url = "http://rimawidell:5001/api/add_post"

        data = {
            "description": "هذا تيست مخصص للتستتة،وليس تيست عادي وحسب",
            "image_url": "",
            "posted_by": 1,
            "text": str(content),
            "title": "تيستت اااااصلي",
            "user_id": 1
        }
        data = json.dumps(data)

        # pprint(data)
        headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
        response = requests.post(url, data=data, headers=headers)
        # print(response.text)


        return response.text
        # return data

    # return_to_path = page[page.index(host)+len(host):]
    # return redirect(return_to_path)
    return "hello?"


@app.route("/comment_handler" ,methods=['POST'])
def comment_handler():

    response = {}

    if request and request.form:
        try:
            content = request.form["content"]
            content = content.replace("\"","\'")

            url = "http://rimawidell:5001/api/add_post_comment"

            data = {
                "post_id":str(request.form['post_id']),
                "text": str(content),
                "user_id": session['user_id'],
            }
            data = json.dumps(data)


            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            response = requests.post(url, data=data, headers=headers)



            return response.text
        except Exception as e :
            response["server message"] = 'Server Error!\n"'+str(e)+'"' 
            return response,500
            pass

    return response,404 #FIXME not 404



@app.route("/get/comments/<post_id>")
def get_comments(post_id):
    response = {}
    try:
        if request.args.get('page'):
            page = int(request.args.get('page'))
        else:
            page = 1


        if request.args.get('offset'):
            offset = int(request.args.get('offset'))
        else:
            offset = 5


        params = {}
        params["page"]=page,
        params["offset"]=offset

        url = api_host+"/api/get/comments/"
        data = requests.get(url+str(post_id),params=params).json()
        pprint(data)
        response['data']=render_template("view/posts/comments.html",comments = data)
        response['pages']=data['pages']
        return response,200
    except Exception as e :
        response["server message"] = 'Server Error!\n"'+str(e)+'"' 
        return response,500
        pass

#--------------------- -[ API Redirect ]----------------------#

@app.route("/like_post" ,methods=['POST'])
def like_post_redirect():
    
    try:
        data = request.get_json()
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
        return requests.post(api_host+"/api/like_post",headers = headers,data=data).json()

    except Exception as e :

        response["server message"] = 'Server Error!\n"'+str(e)+'"' 
        return response,500
        pass


@app.route("/add_post_comment" ,methods=['POST'])
def add_post_comment_redirect():
    response = {}
    try:
        data = request.get_json()
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
        response = requests.post(api_host+"/api/add_post_comment",headers = headers,data=data).json()
        response['data']=render_template('view/posts/comments.html',comments = response)
        return response,200
    except Exception as e :
        
        response["server message"] = 'Server Error!\n"'+str(e)+'"' 
        return response,500
        pass



if __name__ == '__main__':
    # menu = Menu.load_menu()
    # post_handler()
    # zeft()
    app.run(host = '0.0.0.0',debug=True)


    