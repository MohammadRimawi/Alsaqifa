from flask import Flask, render_template, request, session
from flask_assets import Environment, Bundle
import mysql.connector

from utility import *


app = Flask(__name__)


db = mysql.connector.connect(host = "192.168.1.70",user="python-connector",passwd="000000",database = "Alsaqifa")

@app.route('/api')
def index():
    return "test"


@app.route('/api/widget/tag_posts/<tag_name>')
def tag_posts(tag_name):
    tag_name = parse_in(tag_name)
    response = {}
   
    try:
        cur = db.cursor(dictionary=True)
        if request.args.get('type').lower() == "brief":
            
            command = "SELECT * FROM posts WHERE post_id in (SELECT post_id FROM posts_tags WHERE tag_id in(SELECT tag_id FROM tags WHERE tag_name = \""+tag_name+"\"))"

        else:
             command = "SELECT * FROM tags WHERE tag_name = \""+tag_name+"\""

        cur.execute(str(command))
        result = cur.fetchall()
        cur.close()

        if len(result) == 0:
            return response,404    
        else:
            response["data"] = {}
            response["data"]["type"] = request.args.get('type').lower()
            response["data"]["tag_name"] = tag_name
            response["data"]["cards"]=result
            return response,200

        pass

    except:
        cur.close()
        return response,500
        pass

    pass


@app.route('/api/post_info/<post_name>')
def post_info(post_name):

    post_name = parse_in(post_name)
    response = {}
    
    try:
        cur = db.cursor(dictionary=True)
        if request.args.get('type').lower() == "brief":
            
            command = "SELECT * FROM posts WHERE title = \""+post_name+"\""

        else:

             command = "SELECT * FROM posts WHERE title = \""+post_name+"\""

        cur.execute(str(command))
        result = cur.fetchall()
        cur.close()

        if len(result) == 0:
            return response,404    
        else:
            response["post_name"] = post_name
            response["data"] = result
            return response,200

        pass

    except:
        cur.close()
        return response,500
        pass

   



@app.route('/api/playlist/<playlist_name>')
def playlist(playlist_name):
  
    playlist_name = parse_in(playlist_name)
    response = {}

    try:
        cur = db.cursor(dictionary=True)
        
        command = "SELECT * FROM tracks where track_id in (SELECT track_id FROM playlists_tracks WHERE playlist_id in (SELECT playlist_id from playlists WHERE name = \""+playlist_name+"\"))"
        cur.execute(str(command))
        result = cur.fetchall()
        cur.close()

        if len(result) == 0:
            return response,404    
        else:
            response["playlist_name"] = playlist_name
            response["data"] = result
            return response,200
            
    except:
        cur.close()
        return response,500


if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5001,debug=True)