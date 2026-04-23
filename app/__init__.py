from flask import Flask
import os

def create_app():
    # 建立 Flask 應用程式實例
    app = Flask(__name__, instance_relative_config=True)
    
    # 基本設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # 確保 instance 目錄存在以存放資料庫
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊路由 Blueprints
    from app.routes import index, transaction
    app.register_blueprint(index.bp)
    app.register_blueprint(transaction.bp)

    return app
