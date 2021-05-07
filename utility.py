# def widgeter(type)

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
