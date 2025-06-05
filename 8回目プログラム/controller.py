from flask import render_template, jsonify
from sqlalchemy import func
from model import db, ユーザ, 所属, 拾得物, 拾得物分類
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
    else:
        j = []
    return jsonify(j)

def j_dept():
    data = db.session.query(所属).all()
    obj = []
    for i in data:
        obj.append({
            "所属ID": i.ID,
            "所属分類": i.所属分類,
        })
    return obj

def j_user():
    data = db.session.query(ユーザ, 所属).filter(ユーザ.所属ID == 所属.ID).all()
    obj = []
    for user, dept in data:
        obj.append({
            "ID": user.ID,
            "氏名": user.氏名,
            "電話番号": user.電話番号,
            "メールアドレス": user.メールアドレス,
            "所属分類": dept.所属分類,
        })
    return obj

def j_item(key=""):
    query = db.session.query(拾得物, 拾得物分類)\
        .filter(拾得物.拾得物分類ID == 拾得物分類.ID)
    if key != "":
        query = query.filter(拾得物分類.物品名.contains(key))
    data = query.all()
    obj = []
    for item, category in data:
        obj.append({
            "拾得物ID": item.ID,
            "拾得場所": item.拾得場所,
            "色": item.色,
            "特徴": item.特徴,
            "画像": item.画像 if item.画像 else "",
            "大分類": category.大分類,
            "物品名": category.物品名,
        })
    return obj

def j_category():
    data = db.session.query(拾得物分類).all()
    obj = []
    for i in data:
        obj.append({
            "ID": i.ID,
            "大分類": i.大分類,
            "物品名": i.物品名,
        })
    return obj

# item_list表示用
def f_item(k):
    j = j_item(k)
    return render_template("item_list.html", j=j, n=len(j))

# item_detail表示用（取得物管理状況無しのためシンプルに）
def d_item(id):
    item, category = db.session.query(拾得物, 拾得物分類)\
        .filter(拾得物.拾得物分類ID == 拾得物分類.ID)\
        .filter(拾得物.ID == id).first()
    if not item:
        return "該当する拾得物がありません", 404

    d = {
        "大分類": category.大分類,
        "物品名": category.物品名,
        "拾得場所": item.拾得場所,
        "色": item.色,
        "特徴": item.特徴,
        "画像": item.画像 if item.画像 else "",
        "id": id
    }
    return render_template("item_detail.html", d=d, u=j_user())


