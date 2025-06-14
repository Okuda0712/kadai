from flask import render_template, jsonify
from sqlalchemy import func
from model import db, ユーザ, 所属, 拾得物, 拾得物分類, 拾得物管理状況
from datetime import datetime
import os
import openpyxl

def top():
    return render_template("top.html")

def json(data):
    if data == "user":
        j = j_user()
    elif data == "item":
        j = j_item()
    elif data == "category":
        j = j_category()
    elif data == "dept":
        j = j_dept()
    return(jsonify(j))

def j_dept():
    data = db.session.query(所属).all()
    obj = []
    for i in data:
        obj.append({
            "所属ID":i.ID,
            "所属分類":i.所属分類,
            })
    return(obj)

def j_user():
    data = db.session.query(ユーザ,所属).filter(ユーザ.所属ID==所属.ID).all()
    obj = []
    for i,j in data:
        obj.append({
            "ID":i.ID,
            "氏名":i.氏名,
            "電話番号":i.電話番号,
            "メールアドレス":i.メールアドレス,
            "所属分類":j.所属分類,
            })
    return(obj)

def j_item(key=""):
    lastdt = db.session.query(拾得物管理状況.拾得物ID.label("oid"),func.max(拾得物管理状況.変更日時).label("last")).group_by(拾得物管理状況.拾得物ID).subquery()
    tmp = db.session.query(拾得物管理状況,拾得物,拾得物分類,ユーザ,所属).filter(拾得物管理状況.拾得物ID==拾得物.ID).filter(拾得物.拾得物分類ID==拾得物分類.ID).filter(拾得物管理状況.ユーザID==ユーザ.ID).filter(ユーザ.所属ID==所属.ID).filter(拾得物管理状況.変更日時==lastdt.c.last).filter(拾得物管理状況.拾得物ID==lastdt.c.oid)
    if key == "":
        data = tmp.all()
    else:
        data = tmp.filter(拾得物分類.分類.contains(key)).all()
    obj = []
    for i,j,k,l,m in data:
        obj.append({
            "分類":k.分類,
            "拾得物ID":j.ID,
            "拾得場所":j.拾得場所,
            "特徴":j.特徴,
            "拾得物管理状況ID":i.ID,
            "変更日時":i.変更日時,
            "変更内容":i.変更内容,
            "氏名":l.氏名,
            "所属分類":m.所属分類, 
            })
    return(obj)

def j_category():
    data = db.session.query(拾得物分類).all()
    obj = []
    for i in data:
        obj.append({
            "ID":i.ID,
            "分類":i.分類,
            })
    return(obj)

#ここまでok

def f_item(k):
    j = j_item(k)
    return render_template("item_list.html", j=j, n=len(j))

def d_item(id):
    data = db.session.query(拾得物管理状況,ユーザ).filter(拾得物管理状況.ユーザID==ユーザ.ID).filter(拾得物管理状況.拾得物ID==id)
    list = []
    for i,j in data:
        list.append({
            "変更日時":i.変更日時,
            "変更内容":i.変更内容,
            "氏名":j.氏名,
        })
    i,j = db.session.query(拾得物,拾得物分類).filter(拾得物.拾得物分類ID==拾得物分類.ID).filter(拾得物.ID==id).first()
    d = {
        "大分類":j.分類,
        "物品名":i.物品名,
        "拾得場所":i.拾得場所,
        "色":i.色,
        "特徴":i.特徴,
        "変更履歴":list, 
        "id":id
        }
    return render_template("item_detail.html", d=d, u=j_user())
