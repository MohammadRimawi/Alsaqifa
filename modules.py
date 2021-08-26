import requests, json

class Card:
    def __init__(self,title,description,image_url):
        self.title = title
        self.link = ""
        self.description = description
        self.image_url = image_url
        

class Widget:
    def __init__(self,widget_type,widget_title = None,cards = None,code_block = None,descriptive=False,shuffle=True):
        self.type = widget_type
        self.widget_title=widget_title
        self.cards=cards
        self.descriptive = descriptive
        self.shuffle=shuffle

        self.code_block = code_block
        


# from pydantic import BaseModel
# from typing import List


# class Card(BaseModel):
#     title: str
#     description: str
#     image_url: str
#     link: str = ""


# class Widget(BaseModel):
#     widget_type: str
#     widget_title: str = None
#     cards: List[Card] = None
#     code_block: str = None
#     descriptive: bool = False
#     shuffle: bool = True




class Menu:
    # active="/"
    def __init__(self,name,link):
        self.name=name
        self.link=link
        
    @staticmethod
    def load_menu():
        menu={}
        menu['menu']={}
        menu['menu']['left']={}
        menu['menu']['right']={}

        menu["menu"]['left']["/"]=(Menu("الصفحة الرئيسية","/"))
        menu["menu"]['left']["/posts"]=(Menu("المنشورات","/posts"))
        menu["menu"]['left']["/podcasts"]=(Menu("البرامج الاذاعية","/podcasts"))
        # menu["menu"]['left']["#1"]=(Menu("الجريدة","#"))
        # menu["menu"]['left']["#2"]=(Menu("المعرض","#"))
        menu["menu"]['right']["/registration/signup"]=(Menu("انشاء حساب","/registration/signup"))
        menu["menu"]['right']["/registration/login"]=(Menu("تسجيل دخول","/registration/login"))

        menu["active"] = "/"
        return menu

