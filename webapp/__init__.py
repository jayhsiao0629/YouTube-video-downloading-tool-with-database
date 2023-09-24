from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#創一個新的SQLAAlchemy物件(objects)
db = SQLAlchemy()
#用一個變量variable去存放資料庫的名字
YOUTUBE_DATABASE = "youtube_database3.db"

def create_web_app():
    #創造一個flask物件 叫做app
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{YOUTUBE_DATABASE}'
    db.init_app(app)
    #註冊藍圖
    from .home import home
    app.register_blueprint(home, url_prefix="/")

    #創建資料庫
    with app.app_context():
        db.create_all()
    return app