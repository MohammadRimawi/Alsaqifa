# def widgeter(type)
import secrets
from datetime import datetime
from werkzeug.utils import secure_filename
import os


UPLOAD_AUDIO_FOLDER = 'static/audio'
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg'}


UPLOAD_IMAGE_FOLDER = 'static/assets/images/posts'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def parse_in(s):
    new_s=[]
    for i in range(len(s)): 
        if s[i]=='-':new_s.append(' ')
        else: new_s.append(s[i])
    return "".join(new_s)

# def parse_out(s):
#     new_s=[]

#     for i in range(len(s)): 
#         if s[i]==' ':new_s.append('-')
#         else: new_s.append(s[i])

    
#     return "".join(new_s)
def parse_out(s):

    new_s=[]
    # s =  ""
    
    for i in range(len(s)): 
        if s[i]=='/': pass
        else: new_s.append(s[i])
 
    f = "".join(new_s)
    f = " ".join(f.split())

    new_s = []
    for i in range(len(f)): 
        if f[i]==' ':new_s.append('-')
        else: new_s.append(f[i])

    f = "".join(new_s)
    f = " ".join(f.split())
    # print(f,"@@@@@@@@@@@@@@@@@@d")

    # for i in range(len(s)): 
    #     if new_s[i]==' ':new_s.append('-')
    #     elif s[i]=='/': pass
    #     else: new_s.append(s[i])



    return f


def allowed_audio_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS


def allowed_image_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def uploader(file,type):
    response = {}
    try:
        if file.filename != '':
            if file:
                if type.lower() == "image":
                    if allowed_image_file(file.filename):

                        filename = datetime.now().strftime("%Y-%m-%d %H-%M-%S ") + secure_filename(file.filename)
                        path = os.path.join(UPLOAD_IMAGE_FOLDER, filename)
                        file.save(path)
                        response['uploader message'] = "Image uploaded successfully!"
                        response['uploader status'] = 200
                        response['image_url'] = path
                        return response,200
                        pass
                    else:
                        response['uploader message'] = "Uploader Error!<br>file was not uploaded ,not an image!<br>Format must be one of:<br>"+str(ALLOWED_IMAGE_EXTENSIONS)
                        response['uploader status'] = 406
                        return response,406
                elif type.lower() == "audio":
                    if allowed_audio_file(file.filename):

                        filename = datetime.now().strftime("%Y-%m-%d %H-%M-%S ") + secure_filename(file.filename)
                        path = os.path.join(UPLOAD_AUDIO_FOLDER, filename)
                        file.save(path)

                        response['uploader message'] = "Audio uploaded successfully!"
                        response['uploader status'] = 200
                        response['audio_url'] = path
                        return response,200
                        pass
                    else:

                        response['uploader message'] = "Uploader Error!<br>file was not uploaded ,not an audio!<br>Format must be one of:<br>"+str(ALLOWED_AUDIO_EXTENSIONS)
                        response['uploader status'] = 406
                        return response,406
                else:
                    response['uploader message'] = "Uploader Error!<br>file type is unknown!"
                    response['uploader status'] = 500
                    return response,500

            else:
                response['uploader message'] = "Uploader Error!<br>file is corrupted"
                response['uploader status'] = 500
                return response,500
        # else:
        #     return "No file was uploaded!",200

    except Exception as e:
       return str(e),500


def make_token():
    return secrets.token_urlsafe(32)  