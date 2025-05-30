from flask import request, redirect, send_from_directory
import controller

def create_route(app):

    @app.route("/")
    def index():
        return controller.top()
    
    @app.route("/sinsei")
    def index1():
        return controller.sinsei()

    @app.route("/toukou")
    def index2():
        return controller.toukou()
    
    @app.route("/json", methods=["GET","POST"])
    def json():
        if "data" in request.args:
            d = request.args.get("data")
            if d in ["user","item","category","dept"]:
                return controller.json(d)
        return("GETパラメータを指定してください")
    
