from flask import Flask
import os

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    
    with app.app_context():
        print(f"Current working directory: {os.getcwd()}")
        print(f"Templates folder: {app.template_folder}")
        
        from . import routes
        routes.init_app(app)
    
    return app
