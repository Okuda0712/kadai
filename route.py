from flask import request, session,redirect, send_from_directory, url_for

import controller

def create_route(app):

    @app.route("/")
    def index():
        return controller.top()
    
    @app.route("/login")
    def index1():
        username = url_for("loginA")
        list = [{session.get("user")},{session.get("pass")}]
        if "user" in session:
            html += f"""こんにちは{session.get("user")}さん
        ここは職員ログインページです
         <form method="POST" action="{username}">ユーザ名を入力してください：<input name="user"></br>"""
        return html
    
    @app.route("/loginA", methods=["POST"])
    def login():
        session["user"] = request.form.get("user")
 
        return redirect(url_for("login"))
    
    @app.route("/syuutokubutu")
    def index2():
        html = """ここは落とし物登録ページです"""
        return html
    
    @app.route("/serch")
    def index3():
        html = """ここは落とし物検索ページです"""
        return html
    
    @app.route("/list")
    def index4():
        html = """一覧表示ページです"""
        return html
    
    @app.route("/irai")
    def index5():
        html = """依頼ページです"""
        return html
    
    @app.route("/sinsei")
    def index6():
        return controller.sinsei()

    @app.route("/toukou")
    def index7():
        return controller.toukou()
    

    
    @app.route("/json", methods=["GET","POST"])
    def json():
        if "data" in request.args:
            d = request.args.get("data")
            if d in ["user","item","category","dept"]:
                return controller.json(d)
        return("GETパラメータを指定してください")
    
