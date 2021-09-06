import json
from flask import Flask,flash, render_template, request, session, jsonify,url_for,redirect
from flask_assets import Environment, Bundle
import requests, json
from datetime import datetime,timedelta
from werkzeug.utils import secure_filename
from pprint import pprint
import os
from flaskext.markdown import Markdown
import hashlib


from utility import *
from modules import *


app = Flask(__name__)
app.secret_key = os.getenv("SESSION_KEY")

Markdown(app)



css = Bundle('css/general.css', output = "gen/main.css")

bundles = {
    "ckeditor.js": Bundle("modules/ckeditor5/build/ckeditor.js", output = "gen/ckeditor.js"),
    "slider.js": Bundle("javascript/slider.js", output = "gen/slider.js"),
    "snackbar.js": Bundle("javascript/snackbar.js", output = "gen/snackbar.js"),
    "requests.js": Bundle("javascript/requests.js", output = "gen/requests.js"),
    "general.css": Bundle('css/general.css', output = "gen/general.css"),
    "general.js": Bundle('javascript/general.js', output = "gen/general.js"),
    "control_panel.js": Bundle('javascript/control_panel.js', output = "gen/control_panel.js"),
    "modal.js": Bundle('javascript/modal.js', output = "gen/modal.js"),
    "home.css": Bundle('css/home.css', output = "gen/home.css"),
    "ckeditor.css": Bundle('modules/ckeditor5/ckeditor.css', output = "gen/ckeditor.css"),
    "flex.css": Bundle('css/flex.css', output = "gen/flex.css"),
    "form.css": Bundle('css/form.css', output = "gen/form.css"),
    "nav.css": Bundle('css/nav.css', output = "gen/nav.css"),
    "media.css": Bundle('css/media.css', output = "gen/media.css"),
    "posts.css": Bundle('css/posts.css', output = "gen/posts.css"),
    "table.css": Bundle('css/table.css', output = "gen/table.css"),
}

assets = Environment(app)

assets.register(bundles)
api_host="http://rimawidell:5001"



app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER
app.config['UPLOAD_AUDIO_FOLDER'] = UPLOAD_AUDIO_FOLDER


editor_mode = True
editor_mode = False


def get_sliders(data):

    widgets_list= []

    tags = json.dumps(data)

    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    tags_posts = requests.post(api_host+"/api/get/posts_by_tag",headers = headers,data=tags)
    tags_posts = tags_posts.json()  

    for tag in tags_posts['data']['tags']:

        cards_list = []
        for post in tag['data']:
            cards_list.append(Card(title=post['title'],description=post['description'],image_url= post['image_url']))

        widgets_list.append(Widget(
            widget_type = "slider",
            widget_title=str(tag['name']),
            cards=cards_list,
            descriptive=int(tag['descriptive']),

        ))

    return widgets_list
def get_widgets(data):
  

    widgets_list= []
    
    for item in data[0]['data']:
        if item['type'] == "slider":
            tags = json.dumps({
                'tags':[
                    {
                        "name":str(item['tag_name']),
                        "descriptive":str(item['descriptive']),
                        "number_of_cards":str(item['number_of_cards'])
                    }
                ]
            })

            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            tags_posts = requests.post(api_host+"/api/get/posts_by_tag",headers = headers,data=tags)
            tags_posts = tags_posts.json()  

            for tag in tags_posts['data']['tags']:
        
                cards_list = []
                for post in tag['data']:
                    cards_list.append(Card(title=post['title'],description=post['description'],image_url= post['image_url']))

                widgets_list.append(Widget(
                    widget_type = "slider",
                    widget_title=str(tag['name']),
                    cards=cards_list,
                    descriptive=int(tag['descriptive']),

                ))

        elif item['type'] == "post":
            user_id = -1
            if "user_id" in session:
                user_id = session['user_id']

            user_data = {
                "user_id":str(user_id)
            }
            # print(user_data)
            user_data = json.dumps(user_data)
            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}

            post = requests.post(api_host+"/api/get/post/"+str(item['title']),headers = headers)
            post = post.json()
            post['data']['text']= post['data']['text'].replace('contenteditable="true"',"contenteditable='false'")
        
            widgets_list.append(Widget(
                    widget_type = "post",
                    widget_title=str(item['name']),
                    code_block=post['data']['text']
                ))

        elif item['type'] == "embeded":

            widgets_list.append(Widget(
                    widget_type = "embeded",
                    widget_title=str(item['name']),
                    code_block=item['code_block']
                ))
            

    return widgets_list

@app.route('/')
def index():
    menu = Menu.load_menu()

    try:
        data = page_widgets()

        widgets_list = get_widgets(data)
      
    except Exception as e:
        post = {}
        post["data"] = {}
        post["data"]["text"] = "api is off"
        
    menu['active']="/"
    return render_template("index.html",Menu=menu,widgets_list=widgets_list,editor_mode=editor_mode,session=session,parse_out=parse_out)


@app.route("/test")
def test():
    return render_template("test.html")
    
#----------------------[ Control Panel ]-----------------------#
@app.route('/control_panel')
def control_panel():
    menu = Menu.load_menu()

    return render_template("control/control_panel.html",Menu=menu,session=session )

@app.route('/control_panel/tags',methods=['GET','POST'])
def tag_controls():
    menu = Menu.load_menu()


    if request.form and request.form['action']:
        if request.form['action'] == "delete":
            url = api_host+"/api/delete/tag"
            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            data = {
                "tag_id":str(request.form['tag_id'])
            }
            data = json.dumps(data)
            response = requests.delete(url,headers=headers,data=data).json()
            pprint(response)
        

        elif request.form['action'] == "update":

            url = api_host+"/api/update/tag"
            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            data = {
                "tag_id":str(request.form['tag_id']),
                "tag_name":str(request.form['tag_name'])

            }
            data = json.dumps(data)
            response = requests.put(url,headers=headers,data=data).json()
            pprint(response)


        elif request.form['action'] == "insert":
            url = api_host+"/api/create/tag"
            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            data = {
                "tag_name":str(request.form['tag_name'])
            }
            data = json.dumps(data)
            response = requests.post(url,headers=headers,data=data).json()
            pprint(response)

    

    url = api_host+"/api/get/all_tags"

    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    tags = requests.post(url, headers=headers).json()



    return render_template("control/tag_controls.html",Menu=menu,session=session,tags=tags)
  

@app.route('/control_panel/users')
def user_controls():
    menu = Menu.load_menu()


    return render_template("control/user_controls.html",Menu=menu,session=session )


@app.route('/control_panel/pages', methods=['POST','GET'])
def page_controls():

    if request.form and request.form['action']:
        if request.form['action'] == "delete":

            url = api_host+"/api/delete/page_widget"
            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            data = {
                "widget_id":str(request.form['widget_id'])
            }
            data = json.dumps(data)
            print(data)
            response = requests.delete(url,headers=headers,data=data).json()
            pprint(response)

        elif request.form['action'] == "update":

            url = api_host+"/api/update/page_widget"
            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            data = {
                "widget_id":str(request.form['widget_id']),
                "page":str(request.form['page']),
                "order_by":str(request.form['order_by'])
            }
            data = json.dumps(data)
            print(data)
            response = requests.put(url,headers=headers,data=data).json()
            pprint(response)


        elif request.form['action'] == "insert":

            url = api_host+"/api/create/page_widget"
            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            data = {
                "widget_id":str(request.form['widget_id']),
                "page":str(request.form['page']),
                "order_by":str(request.form['order_by'])
            }
            data = json.dumps(data)
            print(data)
            response = requests.post(url,headers=headers,data=data).json()
            pprint(response)

    menu = Menu.load_menu()

    url = api_host+"/api/get/all_page_widgets"
    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    page_widgets = requests.post(url,headers=headers).json()

    url = api_host+"/api/get/all_widgets"
    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    widgets = requests.post(url, headers=headers).json()

  
    return render_template("control/page_controls.html",Menu=menu,session=session,page_widgets=page_widgets,widgets=widgets)

@app.route('/control_panel/playlists')
def playlist_controls():
    menu = Menu.load_menu()

  
    return render_template("control/playlist_controls.html",Menu=menu,session=session )



@app.route('/control_panel/widgets',methods=['GET','POST'])
def widget_controls():

    if request.form:
        if 'action' in request.form:
            if request.form['action'] == "insert":
                url = api_host+"/api/create/widget"
                headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
                
                if request.form['type'] == "slider":

                    if 'shuffle' in request.form: shuffle = 1
                    else: shuffle = 0

                    if 'descriptive' in request.form: descriptive = 1
                    else: descriptive = 0

                    data = {
                        "name":str(request.form['widget_name']),
                        "type":str(request.form['type']),
                        "descriptive":str(descriptive),
                        "tag_id":str(request.form['tag_id']),
                        "shuffle":str(shuffle),
                        "number_of_cards":str(request.form['number_of_cards']),
                        "order_by":str(request.form['order_by']),
                    }

                    data = json.dumps(data)
                    response = requests.post(url,headers=headers,data=data).json()
                    pprint(response)

                elif request.form['type'] == "post":
                    url = api_host+"/api/create/widget"
                    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
                    data = {
                        "name":str(request.form['widget_name']),
                        "type":str(request.form['type']),   
                        "post_id":str(request.form['post_id']),
                    }
                    data = json.dumps(data)
                    response = requests.post(url,headers=headers,data=data).json()
                    pprint(response)

                elif request.form['type'] == "embeded":
                    url = api_host+"/api/create/widget"
                    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}

                    code_block = str(request.form['code_block']).strip()
                    data = {
                        "name":str(request.form['widget_name']),
                        "type":str(request.form['type']),   
                        "code_block":str(request.form['code_block']),
                        }
                    data = json.dumps(data)
                    response = requests.post(url,headers=headers,data=data).json()
                    pprint(response)

        if 'slider_action' in request.form:
            if request.form['slider_action'] == "delete":

                url = api_host+"/api/delete/widget"
                headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
                data = {
                    "widget_id":str(request.form['widget_id'])
                }
                data = json.dumps(data)
                print(data)
                response = requests.delete(url,headers=headers,data=data).json()
                pprint(response)
                pass
            
            if request.form['slider_action'] == "update":
                
                if 'shuffle' in request.form: shuffle = 1
                else: shuffle = 0

                if 'descriptive' in request.form: descriptive = 1
                else: descriptive = 0

                url = api_host+"/api/update/widget"
                headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
                data = {
                    "widget_id":str(request.form['widget_id']),
                    "name":str(request.form['name']),
                    "type":"slider",
                    "descriptive":str(descriptive),
                    "tag_id":str(request.form['tag_id']),
                    "shuffle":str(shuffle),
                    "number_of_cards":str(request.form['number_of_cards']),
                    "order_by":str(request.form['order_by']),
                }
                data = json.dumps(data)
                print(data)
                response = requests.put(url,headers=headers,data=data).json()
                pprint(response)

                pass


        if 'post_action' in request.form:
            if request.form['post_action'] == "delete":

                url = api_host+"/api/delete/widget"
                headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
                data = {
                    "widget_id":str(request.form['widget_id'])
                }
                data = json.dumps(data)
                print(data)
                response = requests.delete(url,headers=headers,data=data).json()
                pprint(response)
                pass
            if request.form['post_action'] == "update":
                
                url = api_host+"/api/update/widget"
                headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
                data = {
                    "widget_id":str(request.form['widget_id']),
                    "name":str(request.form['name']),
                    "type":"post",
                    "post_id":str(request.form['post_id'])
                }
                data = json.dumps(data)
                print(data)
                response = requests.put(url,headers=headers,data=data).json()
                pprint(response)

                pass


        if 'embeded_action' in request.form:
            if request.form['embeded_action'] == "delete":
                url = api_host+"/api/delete/widget"
                headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
                data = {
                    "widget_id":str(request.form['widget_id'])
                }
                data = json.dumps(data)
                print(data)
                response = requests.delete(url,headers=headers,data=data).json()
                pprint(response)
                pass
            if request.form['embeded_action'] == "update":
                url = api_host+"/api/update/widget"
                headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
                data = {
                    "widget_id":str(request.form['widget_id']),
                    "name":str(request.form['name']),
                    "type":"embeded",
                    "code_block":str(request.form['code_block'])
                }
                data = json.dumps(data)
                print(data)
                response = requests.put(url,headers=headers,data=data).json()
                pprint(response)

                pass


    menu = Menu.load_menu()


    url = api_host+"/api/get/all_tags"
    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    tags = requests.post(url, headers=headers).json()

    url = api_host+"/api/get/all_posts?all=true"
    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    posts = requests.post(url, headers=headers).json()

    url = api_host+"/api/get/all_widgets"
    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    widgets = requests.post(url, headers=headers).json()


    return render_template("control/widget_controls.html",Menu=menu,session=session ,tags = tags, posts = posts ,widgets = widgets)




#--------------------------[ Tags ]---------------------------#

@app.route("/tags/<tag>")
def tags(tag):

    params = {}
    params['slider'] = 1
    params['page'] = request.args.get('page')
    if params['page'] == None:
        params['page']=1

    data = {
        
        "tags":[
            {
                "name":str(tag),
                "descriptive":"0",
                "number_of_cards":"0",
            },
        ]
    }
    data = json.dumps(data)

    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    posts = requests.post(api_host+"/api/get/posts_by_tag",headers = headers,data=data,params=params)
    posts = posts.json()
    pprint(posts)
    
    data = {}
    data['tags'] = []
    pprint(posts['data'])
    for i in range(len(posts['data'])):
        print(posts['data'][i]['tags'])
        if  posts['data'][i]['tags']:
            posts['data'][i]['tags'] = posts['data'][i]['tags'].split(',')
        else:
            posts['data'][i]['tags'] = ""
    

    menu = Menu.load_menu()
    menu['active'] = "/posts"

    return render_template("view/tags.html",Menu=menu,session=session , posts=posts ,parse_out= parse_out)


#--------------------------[ Posts ]--------------------------#

@app.route("/posts")
def all_posts():
    params = {}


    try:
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

        data = {}
        data['tags'] = []
        for i in range(len(posts['data'])):
            print(posts['data'][i]['tags'])
            if  posts['data'][i]['tags']:
                posts['data'][i]['tags'] = posts['data'][i]['tags'].split(',')
            else:
                posts['data'][i]['tags'] = ""

        data = {
            "tags":[
                {
                    "name":"زوجي",
                    "descriptive":"0",
                    "number_of_cards":"0"
                },
                {
                    "name":"فردي",
                    "descriptive":"1",
                    "number_of_cards":"0"
                },
            ]
        }

        widgets_list = get_sliders(data)

        return render_template("view/posts/all_posts.html",Menu=menu,widgets_list=widgets_list,session=session , posts=posts ,parse_out= parse_out)

    except Exception as e :
        response["server message"] = 'Server Error!\n"'+str(e)+'"' 
        print(e)
        return response,500
        pass

@app.route("/posts/<title>")
def posts(title):
    pprint(session)
    menu = Menu.load_menu()
    menu['active']=""

    widgets_list = []
    data = {}
    data['tags'] = []

    title = parse_in(title)
    try:
        user_id = -1
        if "user_id" in session:
            user_id = session['user_id']

        user_data = {
            "user_id":str(user_id)
        }

        user_data = json.dumps(user_data)

        headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
        post = requests.post(api_host+"/api/get/post/"+title,headers = headers ,data=user_data)
        post = post.json()

        post['data']['text'] = post['data']['text'].replace('contenteditable="true"',"contenteditable='false'")
      
        user_id = -1
        if "user_id" in session:
            user_id = session['user_id']

        user_data = {
            "user_id":str(user_id),
            "post_id":str(post['data']['post_id'])
        }
        user_data = json.dumps(user_data)
        pprint(user_data)
        url = api_host+"/api/get/comments"
        headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}

        post['data']['comments'] = requests.post(url,headers=headers,data=user_data).json()

        
        pprint(post["data"]['comments']) 
        if post['data']['tags']:
            post['data']['tags'] = post['data']['tags'].split(',')
            for i in post['data']['tags']:
                data['tags'].append({
                    "name":str(i),
                    "descriptive":"0",
                    "number_of_cards":"0"
                })

            widgets_list = get_sliders(data)
        else:
            post['data']['tags'] = ""

       
        #TODO Get tags based on user_id and post_id
    except Exception as e:
        post = {}
        print(e)
        post["data"] = {}
        post["data"]["text"] = "api is off"
    return render_template("view/posts/posts.html",title=title,Menu=menu,post=post,widgets_list=widgets_list,session=session,parse_out=parse_out)

@app.route("/new_post")
def new_posts():
  

    menu = Menu.load_menu()

    menu['active'] = "/posts"

    editor_data = {}
    url = api_host+"/api/get/all_users"

    data = {
        "role":"author"
    }

    data = json.dumps(data)

    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    authors = requests.post(url, data=data, headers=headers).json()
    editor_data['authors'] = authors

    url = api_host+"/api/get/all_tags"

    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    tags = requests.post(url, headers=headers).json()
    editor_data['tags'] = tags

    return render_template("view/posts/add_new_post.html",Menu=menu,session=session,parse_out= parse_out, editor_data = editor_data)

@app.route("/get/edit_post",methods=['POST','GET'])
def edit_post():

    data = request.get_json()
 
    editor_data = {}
    url = api_host+"/api/get/all_users"

    author_data = {
        "condition":"author"
    }

    author_data = json.dumps(author_data)

    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    authors = requests.post(url, data=author_data, headers=headers).json()
    editor_data['authors'] = authors

    url = api_host+"/api/get/all_tags"
    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    tags = requests.post(url, headers=headers).json()
    editor_data['tags'] = tags


    post_data = {
        "post_id":str(data['post_id'])
    }

    post_data = json.dumps(post_data)

    url = api_host+"/api/get/post_update_data"
    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    post = requests.post(url,data=post_data, headers=headers).json()
    if  post['data']['tags']:
        post['data']['tags'] = post['data']['tags'].split(',')
    else:
        post['data']['tags'] = ""
    editor_data['post'] = post
    # print(post)
    # pprint(post)
    editor_data['type'] = "post"

    return render_template('utility/modal.html',editor_data=editor_data)
    

@app.route("/get/edit_comment",methods=['POST','GET'])
def edit_comment():

    data = request.get_json()
 
    editor_data = {}
    url = api_host+"/api/get/all_users"

   

    comment_data = {
        "comment_id":str(data['comment_id'])
    }

    comment_data = json.dumps(comment_data)

    url = api_host+"/api/get/comment"
    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    comment = requests.post(url,data=comment_data, headers=headers).json()

    print(comment)
    editor_data['comment'] = comment
    editor_data['type'] = "comment"

    return render_template('utility/modal.html',editor_data=editor_data)
    
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


    return render_template("view/podcasts/all_podcasts.html",playlists=playlists,Menu=menu,parse_out=parse_out)

@app.route("/podcasts/<playlist>")
def podcast(playlist):
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
    playlists = requests.post(api_host+"/api/get/all_playlists?all=true",headers = headers)
    playlists = playlists.json()      

    headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
    tracks = requests.post(api_host+"/api/get/all_tracks",headers = headers)
    tracks = tracks.json()    

    if(request.form):
        if request.form['operation'] == "select_playlist":

            data = {
                "playlist_id" : str(request.form["select_playlist_id"])
            }
            data = json.dumps(data)
            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            r = requests.post(url=api_host+"/api/get/playlist",data=data,headers=headers)
            response = r.json()
            
            response['status_code'] = r.status_code
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
                file.save(os.path.join(app.config['UPLOAD_AUDIO_FOLDER'], filename))
                                
                path = "/audio/"+str(filename)
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
        data = {
            "name" : parse_in(str(playlist_name))
        }

        data = json.dumps(data)
        headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}

        response = requests.post(api_host+'/api/get/playlist',headers = headers, data=data)
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
    menu['active']="/registration"
    return render_template("registration.html",Menu=menu,session=session)

@app.route('/registration/login', methods=['GET', 'POST'])
def login():
    
    menu = Menu.load_menu()
    menu['active'] = "/registration/login"

    if request.form :
        if request.form['operation'] == "login":

            url = api_host+"/api/authenticate"
            
            salt = str.encode(os.getenv("HASH_SALT"))
            password = hashlib.pbkdf2_hmac('sha256',request.form['password'].encode('utf-8'),salt,100000,dklen=64)

            data = {
                "username": str(request.form['username']),
                "password": str(password), 
                "token":"hello"
            }
            data = json.dumps(data)

            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            r = requests.post(url, data=data, headers=headers)

            response = r.json()
            response['status_code'] = r.status_code

            if response['status_code'] == 200:
                session["user_id"] = response['data']['user_id']
                session["name"] =  response['data']['name']
                session["role"] =  response['data']['role']

                
                if response['data']['image_url'] != None:
                    session["image_url"] = response['data']['image_url']
                else:
                    response['data']['image_url'] = ""
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
                url = api_host+"/api/add/token"

                r = requests.post(url, data=data, headers=headers)

                response['token'] = r.json()
                response['token']['status_code'] = r.status_code

                return redirect("/")
                # TODO Hash this -> remote_addr REMOTE_ADDR
         
    return render_template("view/registration/login.html",Menu=menu,session=session)
    
@app.route('/registration/signup', methods=['GET', 'POST'])
def signup():

    menu = Menu.load_menu()
    menu['active'] = "/registration/login"
    response = {}

    if request.form :

        url = api_host+"/api/create/user"

        data = {
            "name": str(request.form['firstname'])+" "+str(request.form['lastname']),
        }

        data = json.dumps(data)

        headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
        user = requests.post(url,headers=headers,data=data).json()
        pprint(user)
        url = api_host+"/api/create/authentication"
        salt = str.encode(os.getenv("HASH_SALT"))
        password = hashlib.pbkdf2_hmac('sha256',request.form['password'].encode('utf-8'),salt,100000,dklen=64)

        data = {
            "user_id":str(user['data']['user_id']),
            "username": str(request.form['username']),
            "password": str(password),  
            "email": str(request.form['email']),           
        }

        data = json.dumps(data)

        headers = {'Content-Type': 'application/json','charset':'UTF-8'}
        auth_res = requests.post(url,headers=headers,data=data)

        if auth_res.status_code == 200:
            session["user_id"] = str(user['data']['user_id'])
            session["name"] =  str(request.form['firstname'])+" "+str(request.form['lastname'])
            session["image_url"] = ""

            token = make_token()
            session["session_id"] = token

            now = datetime.now()
            creation_date = now.strftime('%Y-%m-%d %H:%M:%S')
            expiration_date = (now + timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')

            data = {
                "user_id":str(user['data']['user_id']),
                "creation_date":str(creation_date),
                "last_touched_date":str(creation_date),
                "expiration_date":str(expiration_date),
                "token":str(token)
            }
            data = json.dumps(data)


            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            url = api_host+"/api/add/token"

            r = requests.post(url, data=data, headers=headers)

            response['token'] = r.json()
            response['token']['status_code'] = r.status_code

            return redirect("/")
            # TODO remote_addr REMOTE_ADDR
         
    return render_template("view/registration/signup.html",Menu=menu,session=session)


@app.route('/registration/logout', methods=['GET'])
def logout():
    session.pop("user_id",None)
    session.pop("name",None)
    session.pop("session_id",None)
    session.pop("image_url",None)

    return redirect("/")


#-------------------------[ Utility ]-------------------------#

import random
@app.errorhandler(404)
def page_not_found(e):
    s = ['يزم وين رايح؟','بشرفك ارجع!','بتعرف ترجع لحالك ولا اجي ارجعك؟','مش من هون الطريق، ارجع']
    i = random.randint(0, len(s)-1)

    return s[i],404



@app.route('/get/page_widgets')
def page_widgets():
    response = {}

    try:
        url = api_host+"/api/get/page_widgets"

        data = {
            "page":"home"
        }

        data = json.dumps(data)

        headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
        widgets = requests.post(url, data=data, headers=headers).json()

        response['data'] = widgets['data']
        return response,200

    except Exception as e :
        response["server message"] = 'Server Error!\n"'+str(e)+'"' 
        return response,500
        pass

@app.route("/get/comments",methods=['POST'])
def get_comments():
    response = {}
    try:
        data = request.get_json()
        data = json.dumps(data)
            
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
        pprint(data)
        
        url = api_host+"/api/get/comments"
        headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
        data = requests.post(url,data=data,headers = headers,params=params).json()
        response['data']=render_template("view/posts/comments.html",comments = data,session = session)
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
        return requests.post(api_host+"/api/toggle/like_post",headers = headers,data=data).json()

    except Exception as e :

        response["server message"] = 'Server Error!\n"'+str(e)+'"' 
        return response,500
        pass

@app.route("/like_comment" ,methods=['POST'])
def like_comment_redirect():
    
    try:
        data = request.get_json()
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
        return requests.post(api_host+"/api/toggle/like_comment",headers = headers,data=data).json()

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
        response = requests.post(api_host+"/api/create/comment",headers = headers,data=data).json()
        response['data']=render_template('view/posts/comments.html',comments = response)
        pprint(response)
        return response,200
    except Exception as e :
        
        response["server message"] = 'Server Error!\n"'+str(e)+'"' 
        return response,500
        pass

@app.route("/update_comment" ,methods=['PUT'])
def update_comment_redirect():
    response = {}
    try:
        data = request.get_json()
        pprint(data)
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
        response = requests.put(api_host+"/api/update/comment",headers = headers,data=data).json()
        pprint(response)
        return response,200
    except Exception as e :
        
        response["server message"] = 'Server Error!\n"'+str(e)+'"' 
        return response,500
        pass


@app.route("/add_new_post", methods=['POST','OPTIONS'])
def add_new_post():
    response = {}
    image_url = ""
    up = {}
    tags=[]
    try:
        if request.form:
            if request.files['image_file']:
                up = uploader(request.files['image_file'],'image')[0]
                if up['uploader status'] != 200:
                    return up['uploader message'] ,up['uploader status']
                image_url = up['image_url']
            
            if request.form['tags_count']:
                for i in range(int(request.form['tags_count'])):
                    try:
                        if request.form['tag_'+str(i)]:
                            tags.append(int(request.form['tag_'+str(i)]))
                    except :
                        pass
                        

            print(tags)
            now = datetime.now()
            creation_date = now.strftime('%Y-%m-%d %H:%M:%S')

            url = api_host+"/api/create/post"


            data = {
                "title":str(request.form['title']),
                "user_id":str(request.form['author']),
                "image_url":str(image_url),
                "text":str(request.form['text']),
                "posted_by":str(request.form['user_id']),
                "token":str(request.form['token']),
                "date":str(creation_date),
                "tags":tags
            }

            # #TODO add desctiption 
            data = json.dumps(data)
            pprint(data)

            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            response = requests.post(url, data=data, headers=headers)
            pprint(response.status_code)

            if response.status_code >=400:

                return response.json(),response.status_code

            response = response.json()
            print("hello?")

            response['uploader message'] = up['uploader message'] 
            response['uploader status'] =  up['uploader status']

        response["server message"] = 'received!<br>at '+image_url 

        return response,200
    except Exception as e :
        response["server message"] = 'Server Error!\n"'+str(e)+'"' 
        print(e)
        return response,500
        pass


@app.route("/update_post", methods=['PUT'])
def update_post():
    response = {}
    image_url = ""
    up = {}
    tags=[]
    try:
        if request.form:
            if request.files['image_file']:
                up = uploader(request.files['image_file'],'image')[0]
                if up['uploader status'] != 200:
                    return up['uploader message'] ,up['uploader status']
                image_url = up['image_url']
   
            if request.form['tags_count']:
                for i in range(int(request.form['tags_count'])):
                    try:
                        if request.form['tag_'+str(i)]:
                            tags.append(int(request.form['tag_'+str(i)]))
                    except :
                        pass
                        # pass

            print(tags)
            now = datetime.now()
            creation_date = now.strftime('%Y-%m-%d %H:%M:%S')

            url = api_host+"/api/update/post"
            data = {
                "title":str(request.form['title']),
                "post_id":str(request.form['post_id']),
                "user_id":str(request.form['author']),
                "image_url":str(image_url),
                "text":str(request.form['text']),
                "token":str(request.form['token']),
                "date":str(creation_date),
                "tags":tags
            }

            # #TODO add desctiption 
            data = json.dumps(data)
            pprint(data)

            headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
            response = requests.put(url, data=data, headers=headers)
            pprint(response.status_code)

            if response.status_code >=400:
                # response = 

                return response.json(),response.status_code

            response = response.json()
            print("hello?")

  
        response["server message"] = 'received!<br>at '+image_url 
        pprint(response)
        return response,200
    except Exception as e :
        response["server message"] = 'Server Error!\n"'+str(e)+'"' 
        print(e)
        return response,500
        pass


@app.route('/delete/delete_post',methods=['DELETE'])
def delete_post():
    response = {}
    try:
        data = request.get_json()
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
        return requests.delete(api_host+"/api/delete/post",headers = headers,data=data).json()
        pass
    except Exception as e :
        response["server message"] = 'Server Error!\n"'+str(e)+'"' 
        print(e)
        return response,500
        pass


@app.route('/delete/delete_comment',methods=['DELETE'])
def delete_comment():
    response = {}
    try:
        data = request.get_json()
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json', 'charset':'UTF-8'}
        return requests.delete(api_host+"/api/delete/comment",headers = headers,data=data).json()
        pass
    except Exception as e :
        response["server message"] = 'Server Error!\n"'+str(e)+'"' 
        print(e)
        return response,500
        pass
######################################################################
#-------------------------[ Control Panel ]--------------------------#
######################################################################

###################################
#[ Get ]--------------------------#
###################################

###################################
#[ Utility ]----------------------#
###################################

###################################
#[ Redirect ]---------------------#
###################################

 
######################################################################
#----------------------------[ Template ]----------------------------#
######################################################################

###################################
#[ Create ]-----------------------#
###################################

###################################
#[ Get ]--------------------------#
###################################

###################################
#[ Update ]-----------------------#
###################################

###################################
#[ Delete ]-----------------------#
###################################


if __name__ == '__main__':
    # menu = Menu.load_menu()
    # post_handler()
    # zeft()
    app.run(host = '0.0.0.0',debug=True)


    