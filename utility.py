# def widgeter(type)
import secrets

def parse_in(s):
    new_s=[]
    for i in range(len(s)): 
        if s[i]=='-':new_s.append(' ')
        else: new_s.append(s[i])
    return "".join(new_s)

def parse_out(s):
    new_s=[]
    for i in range(len(s)): 
        if s[i]==' ':new_s.append('-')
        else: new_s.append(s[i])
    return "".join(new_s)


UPLOAD_FOLDER = 'static/audio'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def make_token():
    return secrets.token_urlsafe(32)  